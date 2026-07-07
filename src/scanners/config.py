"""
Configuration Scanner — checks for common security misconfigurations
in .env files, Dockerfiles, nginx configs, and app settings.
"""

from __future__ import annotations

import re
from pathlib import Path

from src.core.engine import BaseScanner, ScannerConfig
from src.core.models import ScanCategory, Severity, Vulnerability


class ConfigScanner(BaseScanner):
    category = ScanCategory.CONFIGURATION

    CHECKS: list[dict] = [
        {
            "pattern": r"DEBUG\s*=\s*True",
            "files": [".env", "settings.py", "config.py", "app/config.py", "settings/local.py"],
            "title": "Debug mode enabled in production",
            "description": "DEBUG=True exposes stack traces, environment variables, and sensitive data to end users.",
            "remediation": "Set DEBUG=False in production. Use environment-specific config files.",
            "severity": Severity.CRITICAL,
            "fixable": True,
        },
        {
            "pattern": r"SECRET_KEY\s*=\s*['\"](?:changeme|secret|password|your-secret)['\"]",
            "files": [".env", "settings.py", "config.py"],
            "title": "Weak/placeholder secret key",
            "description": "Secret key is set to an easily guessable value, compromising session signing and CSRF protection.",
            "remediation": "Generate a cryptographically random secret key (e.g., python -c 'import secrets; print(secrets.token_hex(32))').",
            "severity": Severity.CRITICAL,
            "fixable": True,
        },
        {
            "pattern": r"ALLOWED_HOSTS\s*=\s*\[\s*['\"]*['\"]\s*\]",
            "files": ["settings.py", "config.py"],
            "title": "Empty ALLOWED_HOSTS",
            "description": "An empty ALLOWED_HOSTS list allows HTTP Host header attacks.",
            "remediation": "Set ALLOWED_HOSTS to specific domain names: ALLOWED_HOSTS = ['yourdomain.com', 'api.yourdomain.com']",
            "severity": Severity.HIGH,
            "fixable": True,
        },
        {
            "pattern": r"CORS_ORIGIN_ALLOW_ALL\s*=\s*True",
            "files": ["settings.py", "config.py", "cors.py"],
            "title": "CORS allows all origins",
            "description": "CORS_ORIGIN_ALLOW_ALL=True allows any website to make cross-origin requests.",
            "remediation": "Set CORS_ORIGIN_ALLOW_ALL=False and specify allowed origins in CORS_ORIGIN_WHITELIST.",
            "severity": Severity.HIGH,
            "fixable": True,
        },
        {
            "pattern": r"add_header\s+X-Frame-Options\s+(DENY|SAMEORIGIN)",
            "files": ["nginx.conf", "nginx/*.conf", ".htaccess"],
            "title": "Missing X-Frame-Options header",
            "description": "Without X-Frame-Options or Content-Security-Policy, your site can be embedded in iframes (clickjacking).",
            "remediation": "Add X-Frame-Options: DENY to nginx: add_header X-Frame-Options DENY;",
            "severity": Severity.MEDIUM,
            "fixable": True,
            "inverted": True,  # presence = good, absence = vuln
        },
        {
            "pattern": r"(?:password|passwd|pwd)\s*[=:]\s*['\"]?[^'\"\s]{3,}['\"]?",
            "files": [".env", "config.py", "settings.py", "docker-compose.yml", "docker-compose.yaml"],
            "title": "Hardcoded password in config file",
            "description": "Plaintext passwords in configuration files can leak via version control or server access.",
            "remediation": "Use environment variables or a secrets manager (Vault, AWS Secrets Manager).",
            "severity": Severity.CRITICAL,
            "fixable": True,
        },
    ]

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns: list[Vulnerability] = []
        if not config.target_dir:
            return vulns

        for check in self.CHECKS:
            pattern = re.compile(check["pattern"], re.IGNORECASE)
            inverted = check.get("inverted", False)

            matched = False
            for rel_path in check["files"]:
                target_file = config.target_dir / rel_path
                if not target_file.exists():
                    continue
                text = target_file.read_text(encoding="utf-8", errors="replace")
                if pattern.search(text):
                    matched = True
                    if inverted:
                        # Pattern found means header IS present — skip
                        matched = False
                        continue
                    vulns.append(self._vuln(
                        title=check["title"],
                        description=check["description"],
                        location=f"{rel_path}",
                        remediation=check["remediation"],
                        severity=check["severity"],
                        fixable=check.get("fixable", False),
                        evidence=f"Pattern '{check['pattern']}' matched in {rel_path}",
                    ))
                    break  # one match per check

            if inverted and not matched:
                # Security header NOT found — report as vulnerability
                # Check multiple possible file paths
                found_any_path = False
                for rel_path in check["files"]:
                    target_file = config.target_dir / rel_path
                    if target_file.exists():
                        found_any_path = True
                        vulns.append(self._vuln(
                            title=check["title"],
                            description=check["description"],
                            location=rel_path,
                            remediation=check["remediation"],
                            severity=check["severity"],
                            fixable=check.get("fixable", False),
                        ))
                        break
                if not found_any_path:
                    vulns.append(self._vuln(
                        title=check["title"] + " (config file not found)",
                        description=f"No config file found to check. " + check["description"],
                        location="N/A",
                        remediation=check["remediation"],
                        severity=Severity.INFO,
                        fixable=False,
                    ))

        return vulns
