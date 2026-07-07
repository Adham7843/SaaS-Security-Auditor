"""
SaaS-Security-Auditor — Scan Engine

Orchestrates multiple scanners against a target SaaS brand,
collects vulnerabilities, and produces a ScanResult.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.core.models import ScanCategory, ScanResult, Vulnerability, Severity


@dataclass
class ScannerConfig:
    """Configuration for a single scan of one brand."""
    brand: str
    target_url: str
    target_dir: Optional[Path] = None
    categories: list[ScanCategory] = field(default_factory=lambda: list(ScanCategory))
    severity_threshold: Severity = Severity.LOW
    timeout_seconds: int = 300
    skip_fix: bool = False
    output_dir: Optional[Path] = None


class BaseScanner:
    """Abstract scanner — each category subclasses this."""

    category: ScanCategory = ScanCategory.GENERAL

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        """Override with the actual scan logic. Return discovered vulnerabilities."""
        raise NotImplementedError

    @staticmethod
    def _vuln(
        title: str,
        description: str,
        location: str,
        remediation: str,
        severity: Severity = Severity.MEDIUM,
        evidence: Optional[str] = None,
        fixable: bool = False,
        cvss_score: Optional[float] = None,
        cve_id: Optional[str] = None,
    ) -> Vulnerability:
        return Vulnerability(
            id=uuid.uuid4().hex[:12],
            category=BaseScanner.category,  # will be overridden by subclass
            severity=severity,
            title=title,
            description=description,
            location=location,
            remediation=remediation,
            evidence=evidence,
            fixable=fixable,
            cvss_score=cvss_score,
            cve_id=cve_id,
        )


class ScanEngine:
    """
    Core engine. Accepts a list of scanner instances, runs them all,
    aggregates results, and produces a ScanResult.
    """

    def __init__(self, scanners: Optional[list[BaseScanner]] = None):
        self.scanners: list[BaseScanner] = scanners or []
        self._register_default_scanners()

    def _register_default_scanners(self) -> None:
        """Lazy-import and register all known scanners."""
        from src.scanners.dependency import DependencyScanner
        from src.scanners.config import ConfigScanner
        from src.scanners.auth import AuthScanner
        from src.scanners.cors import CorsScanner
        from src.scanners.secrets import SecretsScanner
        from src.scanners.headers import SecurityHeadersScanner
        from src.scanners.ssl import SslScanner

        builtins: list[BaseScanner] = [
            DependencyScanner(),
            ConfigScanner(),
            AuthScanner(),
            CorsScanner(),
            SecretsScanner(),
            SecurityHeadersScanner(),
            SslScanner(),
        ]
        # Avoid duplicates if user also passed scanners
        existing_cats = {s.category for s in self.scanners}
        for s in builtins:
            if s.category not in existing_cats:
                self.scanners.append(s)

    def register_scanner(self, scanner: BaseScanner) -> None:
        self.scanners.append(scanner)

    async def run(self, config: ScannerConfig) -> ScanResult:
        scan_id = f"scan-{uuid.uuid4().hex[:8]}"
        result = ScanResult(
            brand=config.brand,
            scan_id=scan_id,
            started_at=datetime.now(timezone.utc).isoformat(timespec="microseconds"),
        )
        start = datetime.now(timezone.utc)

        # Filter scanners to requested categories
        active = [s for s in self.scanners if s.category in config.categories]
        if not active:
            active = self.scanners  # fallback: run all

        tasks = []
        for scanner in active:
            tasks.append(self._run_scanner(scanner, config))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for r in results:
            if isinstance(r, Exception):
                print(f"  [!] Scanner error: {r}")
                continue
            for vuln in r:
                result.vulnerabilities.append(vuln)

        end = datetime.now(timezone.utc)
        result.completed_at = end.isoformat(timespec="microseconds")
        result.duration_seconds = (end - start).total_seconds()
        result.total_checks = len(active)
        result.passed_checks = len(active) - len(result.vulnerabilities)
        result.failed_checks = len(result.vulnerabilities)

        return result

    async def _run_scanner(self, scanner: BaseScanner, config: ScannerConfig) -> list[Vulnerability]:
        try:
            vulns = await asyncio.wait_for(
                scanner.scan(config), timeout=config.timeout_seconds
            )
            # Fix the category on each vuln (BaseScanner.category is class-level)
            for v in vulns:
                v.category = scanner.category
            return vulns
        except asyncio.TimeoutError:
            return [Vulnerability(
                id=uuid.uuid4().hex[:12],
                category=scanner.category,
                severity=Severity.INFO,
                title=f"Scanner timed out: {scanner.category.value}",
                description=f"The {scanner.category.value} scanner exceeded {config.timeout_seconds}s.",
                location="N/A",
                remediation="Increase timeout_seconds or check network connectivity.",
            )]
