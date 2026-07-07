"""
Security Headers Scanner — checks source code for hardcoded
security header configurations in web frameworks.
"""

from __future__ import annotations

import re
from pathlib import Path

from src.core.engine import BaseScanner, ScannerConfig
from src.core.models import ScanCategory, Severity, Vulnerability


class SecurityHeadersScanner(BaseScanner):
    category = ScanCategory.CORS_HEADERS

    CHECKS: list[dict] = [
        {
            "name": "HSTS via middleware",
            "pattern": re.compile(r"SecurityMiddleware|StrictTransportSecurityMiddleware"),
            "description": "HSTS middleware not found. Users may connect via unencrypted HTTP.",
            "severity": Severity.HIGH,
            "remediation": "Add SecurityMiddleware to WSGI/ASGI middleware stack, or configure nginx to send HSTS header.",
        },
        {
            "name": "CORS middleware",
            "pattern": re.compile(r"django-cors-headers|flask-cors|corsheaders|CORSMiddleware"),
            "description": "CORS middleware not found in dependencies or middleware config.",
            "severity": Severity.MEDIUM,
            "remediation": "Install and configure django-cors-headers or flask-cors to manage CORS explicitly.",
        },
        {
            "name": "Content Security Policy",
            "pattern": re.compile(r"csp|Content-Security-Policy|CSP_MIDDLEWARE|django-csp"),
            "description": "No Content Security Policy found. CSP prevents XSS by controlling resource loading.",
            "severity": Severity.HIGH,
            "remediation": "Add a CSP header. Use django-csp or flask-csp. Start restrictive: default-src 'self'",
        },
        {
            "name": "Rate limiting",
            "pattern": re.compile(r"ratelimit|throttle|django-ratelimit|flask-limiter|slowapi"),
            "description": "No rate limiting middleware found. APIs without rate limits are vulnerable to brute force and DoS.",
            "severity": Severity.MEDIUM,
            "remediation": "Add rate limiting via django-ratelimit, flask-limiter, or nginx rate limit zones.",
        },
    ]

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns: list[Vulnerability] = []
        if not config.target_dir:
            return vulns

        # Scan dependency files + settings files
        scan_files: list[Path] = []
        for pattern in ["requirements.txt", "Pipfile", "package.json", "settings.py",
                         "config.py", "middleware.py", "asgi.py", "wsgi.py"]:
            f = config.target_dir / pattern
            if f.exists():
                scan_files.append(f)

        # Also scan any .py files for middleware patterns
        for py_file in config.target_dir.rglob("*.py"):
            if py_file not in scan_files:
                scan_files.append(py_file)
            if len(scan_files) > 50:
                break  # limit search

        combined_text = ""
        for f in scan_files:
            try:
                combined_text += f.read_text(encoding="utf-8", errors="replace") + "\n"
            except Exception:
                continue

        for check in self.CHECKS:
            if not check["pattern"].search(combined_text):
                vulns.append(self._vuln(
                    title=check["name"],
                    description=check["description"],
                    location="config/settings files",
                    remediation=check["remediation"],
                    severity=check["severity"],
                    fixable=True,
                ))

        return vulns
