"""
Dependency Scanner — checks for known vulnerable packages
in requirements.txt, package.json, Cargo.toml, etc.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from src.core.engine import BaseScanner, ScannerConfig
from src.core.models import ScanCategory, Severity, Vulnerability


class DependencyScanner(BaseScanner):
    category = ScanCategory.DEPENDENCIES

    # Simulated known-vulnerability database (in production, query OSV.dev API)
    KNOWN_VULNS: dict[str, list[dict]] = {
        "requests": [
            {"max_version": "2.31.0", "cve": "CVE-2024-3651", "severity": Severity.HIGH,
             "description": "Insufficient validation of redirects in requests library",
             "remediation": "Upgrade requests to >= 2.32.0"}
        ],
        "django": [
            {"max_version": "4.2.15", "cve": "CVE-2024-42005", "severity": Severity.CRITICAL,
             "description": "SQL injection via crafted JSON input in Django ORM",
             "remediation": "Upgrade Django to >= 4.2.16 or >= 5.1.1"}
        ],
        "flask": [
            {"max_version": "2.3.3", "cve": "CVE-2024-32879", "severity": Severity.HIGH,
             "description": "Session cookie tampering due to weak signing",
             "remediation": "Upgrade Flask to >= 3.0.0"}
        ],
        "express": [
            {"max_version": "4.19.2", "cve": "CVE-2024-29041", "severity": Severity.MEDIUM,
             "description": "Open redirect via malformed URL in Express.js",
             "remediation": "Upgrade express to >= 4.20.0"}
        ],
        "lodash": [
            {"max_version": "4.17.20", "cve": "CVE-2024-23346", "severity": Severity.HIGH,
             "description": "Prototype pollution in lodash merge functions",
             "remediation": "Upgrade lodash to >= 4.17.21"}
        ],
        "jinja2": [
            {"max_version": "3.1.3", "cve": "CVE-2024-34064", "severity": Severity.MEDIUM,
             "description": "HTML attribute injection in Jinja2 template rendering",
             "remediation": "Upgrade jinja2 to >= 3.1.4"}
        ],
    }

    # Regex patterns for dep files
    DEP_PATTERNS: dict[str, tuple[re.Pattern, int]] = {
        "requirements.txt": (re.compile(r"^([a-zA-Z0-9_.-]+)\s*(?:[=~><]+\s*([\d.]+))?"), 0.5),
        "Pipfile": (re.compile(r'^([a-zA-Z0-9_.-]+)\s*=\s*"?([\d.*]+)"?'), 1),
        "package.json": (re.compile(r'"([^"]+)":\s*"[\^~]?(\d+\.\d+\.\d+)"'), 0),
        "Cargo.toml": (re.compile(r'^([a-zA-Z0-9_-]+)\s*=\s*"([\d.]+)"'), 0),
        "yarn.lock": (re.compile(r'^\s{4}"([@a-zA-Z0-9_/-]+)@'), 0.5),
    }

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns: list[Vulnerability] = []
        if not config.target_dir:
            return vulns

        for filename, (pattern, version_group) in self.DEP_PATTERNS.items():
            dep_file = config.target_dir / filename
            if not dep_file.exists():
                continue

            text = dep_file.read_text(encoding="utf-8", errors="replace")
            for match in pattern.finditer(text):
                pkg_name = match.group(1).lower().strip('"').strip("@")
                installed_ver = match.group(2) if match.lastindex and match.lastindex >= 2 else None

                if pkg_name in self.KNOWN_VULNS:
                    for advisory in self.KNOWN_VULNS[pkg_name]:
                        max_ver = advisory["max_version"]
                        if installed_ver and self._version_compare(installed_ver, max_ver) <= 0:
                            vulns.append(self._vuln(
                                title=f"Vulnerable dependency: {pkg_name} ({installed_ver})",
                                description=advisory["description"],
                                location=f"{filename}: {pkg_name}=={installed_ver}",
                                remediation=advisory["remediation"],
                                severity=advisory["severity"],
                                fixable=True,
                                cvss_score=self._severity_to_cvss(advisory["severity"]),
                                cve_id=advisory["cve"],
                                evidence=f"Found {pkg_name}@{installed_ver} in {filename}",
                            ))
        return vulns

    @staticmethod
    def _version_compare(v1: str, v2: str) -> int:
        """Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2."""
        try:
            parts1 = [int(x) for x in v1.split(".")]
            parts2 = [int(x) for x in v2.split(".")]
            for a, b in zip(parts1, parts2):
                if a < b:
                    return -1
                if a > b:
                    return 1
            return 0
        except (ValueError, IndexError):
            return 0

    @staticmethod
    def _severity_to_cvss(severity: Severity) -> float:
        return {"critical": 9.5, "high": 7.5, "medium": 5.5, "low": 2.5, "info": 0.0}.get(severity, 5.0)
