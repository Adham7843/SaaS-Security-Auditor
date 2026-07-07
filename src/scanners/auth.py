"""
Authentication & Authorization Scanner — checks for weak auth patterns,
missing rate limiting, session config issues.
"""

from __future__ import annotations

import re
from pathlib import Path

from src.core.engine import BaseScanner, ScannerConfig
from src.core.models import ScanCategory, Severity, Vulnerability


class AuthScanner(BaseScanner):
    category = ScanCategory.AUTHENTICATION

    CHECKS: list[dict] = [
        {
            "pattern": r"JWT_SECRET\s*=\s*['\"](?:changeme|secret|default|test)['\"]",
            "files": [".env", "config.py", "settings.py", "auth.py", "jwt.py"],
            "title": "Weak JWT signing secret",
            "description": "A weak or default JWT secret allows attackers to forge authentication tokens.",
            "remediation": "Use a cryptographically random secret of at least 256 bits. Rotate periodically.",
            "severity": Severity.CRITICAL,
            "fixable": True,
        },
        {
            "pattern": r"ACCESS_TOKEN_EXPIRE_MINUTES\s*=\s*(\d+)",
            "files": [".env", "config.py", "settings.py", "auth.py"],
            "title": "Long-lived access tokens",
            "description": "Access tokens with excessive expiry increase the window for token theft.",
            "remediation": "Set ACCESS_TOKEN_EXPIRE_MINUTES to 15 or less. Use refresh tokens for longer sessions.",
            "severity": Severity.MEDIUM,
            "fixable": True,
        },
        {
            "pattern": r"SESSION_COOKIE_SECURE\s*=\s*False",
            "files": ["settings.py", "config.py"],
            "title": "Session cookie not marked Secure",
            "description": "Session cookies without the Secure flag can be transmitted over unencrypted HTTP.",
            "remediation": "Set SESSION_COOKIE_SECURE = True and SESSION_COOKIE_HTTPONLY = True.",
            "severity": Severity.HIGH,
            "fixable": True,
        },
        {
            "pattern": r"PASSWORD_HASHERS\s*=\s*\[\s*['\"]django\.contrib\.auth\.hashers\.(?:MD5PasswordHasher|SHA1PasswordHasher|UnsaltedMD5PasswordHasher|UnsaltedSHA1PasswordHasher)",
            "files": ["settings.py", "config.py"],
            "title": "Weak password hashing algorithm",
            "description": "MD5, SHA1, or unsalted hashes are vulnerable to rainbow table and brute force attacks.",
            "remediation": "Use Django's Argon2PasswordHasher or PBKDF2PasswordHasher with a high iteration count.",
            "severity": Severity.CRITICAL,
            "fixable": True,
        },
        {
            "pattern": r"SECURE_SSL_REDIRECT\s*=\s*False",
            "files": ["settings.py", "config.py"],
            "title": "SSL redirect disabled",
            "description": "Without SSL redirect, unencrypted HTTP traffic can be intercepted.",
            "remediation": "Set SECURE_SSL_REDIRECT = True and configure HSTS headers.",
            "severity": Severity.HIGH,
            "fixable": True,
        },
    ]

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns: list[Vulnerability] = []
        if not config.target_dir:
            return vulns

        for check in self.CHECKS:
            pattern = re.compile(check["pattern"], re.IGNORECASE)
            for rel_path in check["files"]:
                target_file = config.target_dir / rel_path
                if not target_file.exists():
                    continue
                text = target_file.read_text(encoding="utf-8", errors="replace")
                for match in pattern.finditer(text):
                    # Special handling: check expire time threshold
                    if "ACCESS_TOKEN_EXPIRE_MINUTES" in check["pattern"]:
                        val = int(match.group(1))
                        if val <= 60:
                            continue  # acceptable
                        extra = f" (expires in {val} minutes)"
                    else:
                        extra = ""

                    vulns.append(self._vuln(
                        title=check["title"] + extra,
                        description=check["description"],
                        location=f"{rel_path}",
                        remediation=check["remediation"],
                        severity=check["severity"],
                        fixable=check.get("fixable", False),
                        evidence=f"Pattern '{check['pattern']}' matched value in {rel_path}",
                    ))
                    break  # one per file

        return vulns
