"""
SaaS-Security-Auditor — Data Models

All shared types used across scanners, fixers, and reporters.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanCategory(Enum):
    DEPENDENCIES = "dependencies"
    CONFIGURATION = "configuration"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    CORS_HEADERS = "cors_headers"
    SECRETS = "secrets"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    SSL_TLS = "ssl_tls"
    RATE_LIMITING = "rate_limiting"
    LOGGING = "logging"
    GENERAL = "general"


class FixStatus(Enum):
    PENDING = "pending"
    AUTO_FIXED = "auto_fixed"
    MANUAL_REQUIRED = "manual_required"
    IGNORED = "ignored"
    NOT_FIXABLE = "not_fixable"


@dataclass
class Vulnerability:
    id: str
    category: ScanCategory
    severity: Severity
    title: str
    description: str
    location: str
    remediation: str
    cvss_score: Optional[float] = None
    cve_id: Optional[str] = None
    evidence: Optional[str] = None
    fixable: bool = False
    fix_status: FixStatus = FixStatus.PENDING
    discovered_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="microseconds")
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "remediation": self.remediation,
            "cvss_score": self.cvss_score,
            "cve_id": self.cve_id,
            "evidence": self.evidence,
            "fixable": self.fixable,
            "fix_status": self.fix_status.value,
            "discovered_at": self.discovered_at,
        }


@dataclass
class ScanResult:
    brand: str
    scan_id: str
    started_at: str
    completed_at: Optional[str] = None
    vulnerabilities: list[Vulnerability] = field(default_factory=list)
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    duration_seconds: Optional[float] = None

    @property
    def summary(self) -> str:
        total = len(self.vulnerabilities)
        by_sev: dict[str, int] = {}
        for v in self.vulnerabilities:
            by_sev[v.severity.value] = by_sev.get(v.severity.value, 0) + 1
        sev_str = ", ".join(f"{k}={v}" for k, v in sorted(by_sev.items()))
        return (
            f"[{self.brand}] {total} vulns ({sev_str}) "
            f"| Checks: {self.passed_checks}/{self.total_checks} passed"
        )

    def to_dict(self) -> dict:
        return {
            "brand": self.brand,
            "scan_id": self.scan_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "vulnerabilities": [v.to_dict() for v in self.vulnerabilities],
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "duration_seconds": self.duration_seconds,
        }

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path


@dataclass
class FixResult:
    vulnerability_id: str
    fix_status: FixStatus
    description: str
    diff: Optional[str] = None
    error: Optional[str] = None
    fixed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="microseconds")
    )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["fix_status"] = self.fix_status.value
        return d
