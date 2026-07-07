"""
Secrets Scanner — scans codebase for hardcoded API keys,
passwords, tokens, and private keys.
"""

from __future__ import annotations

import re
from pathlib import Path

from src.core.engine import BaseScanner, ScannerConfig
from src.core.models import ScanCategory, Severity, Vulnerability


class SecretsScanner(BaseScanner):
    category = ScanCategory.SECRETS

    # Inspired by truffleHog/gitleaks regex patterns
    PATTERNS: list[dict] = [
        {
            "name": "AWS Access Key",
            "regex": re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
            "severity": Severity.CRITICAL,
            "remediation": "Revoke the key in AWS IAM immediately. Rotate to a new key. Check CloudTrail for usage.",
            "fixable": False,
        },
        {
            "name": "AWS Secret Key",
            "regex": re.compile(r"(?i)aws(.{0,20})?(?:key|secret|access)(.{0,20})?['\"\s][0-9a-zA-Z\/+]{40}['\"\s]"),
            "severity": Severity.CRITICAL,
            "remediation": "Revoke the secret key. Use IAM roles or AWS Secrets Manager instead.",
            "fixable": False,
        },
        {
            "name": "GitHub Token",
            "regex": re.compile(r"(?i)(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}"),
            "severity": Severity.CRITICAL,
            "remediation": "Revoke the token on GitHub. Use fine-grained tokens with minimal scopes.",
            "fixable": False,
        },
        {
            "name": "Slack Bot Token",
            "regex": re.compile(r"xox[bprsa]-[0-9A-Za-z-]{10,}"),
            "severity": Severity.HIGH,
            "remediation": "Revoke and regenerate the token in Slack API dashboard.",
            "fixable": False,
        },
        {
            "name": "Google API Key",
            "regex": re.compile(r"(?i)AIza[0-9A-Za-z\-_]{35}"),
            "severity": Severity.HIGH,
            "remediation": "Regenerate the key in Google Cloud Console. Restrict by IP/HTTP referrer.",
            "fixable": False,
        },
        {
            "name": "Private SSH Key",
            "regex": re.compile(r"-----BEGIN\s*(?:RSA|DSA|EC|OPENSSH)\s*PRIVATE\s*KEY-----"),
            "severity": Severity.CRITICAL,
            "remediation": "Remove from codebase. Use SSH agent or secrets manager. Rotate the key.",
            "fixable": False,
        },
        {
            "name": "Generic API Key",
            "regex": re.compile(r"(?i)(?:api[_-]?key|apikey|api_secret|apiSecret)[\s:=]+['\"]?([A-Za-z0-9_\-]{16,64})['\"]?"),
            "severity": Severity.HIGH,
            "remediation": "Move the key to environment variables or a secrets vault.",
            "fixable": False,
        },
        {
            "name": "Database Connection String",
            "regex": re.compile(r"(?i)(?:postgres(?:ql)?|mysql|mongodb(?:\\+srv)?|redis|rediss)://[^\s]{10,}"),
            "severity": Severity.CRITICAL,
            "remediation": "Use environment variables or a secrets manager. Never hardcode connection strings.",
            "fixable": False,
        },
        {
            "name": "JWT Token",
            "regex": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
            "severity": Severity.HIGH,
            "remediation": "Revoke the JWT. Use short expiration times and refresh tokens.",
            "fixable": False,
        },
    ]

    EXCLUDE_DIRS: set[str] = {
        ".git", "__pycache__", "node_modules", ".venv", "venv",
        ".eggs", "*.egg-info", ".mypy_cache", ".pytest_cache",
        ".ruff_cache", ".tox", "dist", "build", ".github",
    }

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns: list[Vulnerability] = []
        if not config.target_dir:
            return vulns

        for file_path in config.target_dir.rglob("*"):
            # Skip dirs and excluded patterns
            if file_path.is_dir():
                continue
            if any(part.startswith(".") and part not in {".env", ".env.example"}
                   for part in file_path.parts):
                continue
            if file_path.suffix in {".pyc", ".pyo", ".so", ".dll", ".exe", ".jpg", ".png", ".svg", ".ico"}:
                continue
            if file_path.stat().st_size > 1_000_000:  # skip files > 1MB
                continue

            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            for pattern in self.PATTERNS:
                for match in pattern["regex"].finditer(text):
                    matched_text = match.group(0)
                    # Get context: line number
                    line_num = text[:match.start()].count("\n") + 1

                    vulns.append(self._vuln(
                        title=f"Hardcoded {pattern['name']}",
                        description=f"A {pattern['name']} was found in source code. "
                                    f"This can lead to unauthorized access if the repo is exposed.",
                        location=f"{file_path.relative_to(config.target_dir)}:{line_num}",
                        remediation=pattern["remediation"],
                        severity=pattern["severity"],
                        fixable=pattern.get("fixable", False),
                        evidence=f"Matched: {matched_text[:80]}",
                    ))
                    # Only report first match per pattern per file
                    break

        return vulns
