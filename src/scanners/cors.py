"""
CORS & Security Headers Scanner — checks HTTP response headers for
security best practices.
"""

from __future__ import annotations

import asyncio
from typing import Optional
from urllib.parse import urlparse

from src.core.engine import BaseScanner, ScannerConfig
from src.core.models import ScanCategory, Severity, Vulnerability


class CorsScanner(BaseScanner):
    category = ScanCategory.CORS_HEADERS

    RECOMMENDED_HEADERS: dict[str, dict] = {
        "Strict-Transport-Security": {
            "description": "Enforces HTTPS connections. Prevents SSL stripping attacks.",
            "expected": "max-age=31536000; includeSubDomains",
            "severity": Severity.HIGH,
            "remediation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains",
        },
        "X-Content-Type-Options": {
            "description": "Prevents MIME type sniffing by browsers.",
            "expected": "nosniff",
            "severity": Severity.MEDIUM,
            "remediation": "Add: X-Content-Type-Options: nosniff",
        },
        "X-Frame-Options": {
            "description": "Prevents clickjacking by blocking iframe embedding.",
            "expected": "DENY",
            "severity": Severity.MEDIUM,
            "remediation": "Add: X-Frame-Options: DENY",
        },
        "Content-Security-Policy": {
            "description": "Controls which resources can be loaded. Prevents XSS.",
            "expected": "default-src 'self'",
            "severity": Severity.HIGH,
            "remediation": "Add a Content-Security-Policy header. Start with: default-src 'self'",
        },
        "Referrer-Policy": {
            "description": "Controls how much referrer info is sent with requests.",
            "expected": "strict-origin-when-cross-origin",
            "severity": Severity.LOW,
            "remediation": "Add: Referrer-Policy: strict-origin-when-cross-origin",
        },
        "Permissions-Policy": {
            "description": "Restricts browser API access (camera, mic, geolocation).",
            "expected": "geolocation=(), camera=(), microphone=()",
            "severity": Severity.LOW,
            "remediation": "Add a Permissions-Policy header restricting unnecessary APIs.",
        },
    }

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns: list[Vulnerability] = []
        if not config.target_url:
            return vulns

        # Parse base URL
        parsed = urlparse(config.target_url)
        if not parsed.scheme:
            config.target_url = f"https://{config.target_url}"
            parsed = urlparse(config.target_url)

        # Try to fetch headers
        headers = await self._fetch_headers(config.target_url)
        if headers is None:
            vulns.append(self._vuln(
                title="Could not reach target URL",
                description=f"Unable to fetch headers from {config.target_url}. Check network/URL.",
                location=config.target_url,
                remediation="Verify the SaaS is running and reachable.",
                severity=Severity.INFO,
                fixable=False,
            ))
            return vulns

        # Check each recommended header
        for header, info in self.RECOMMENDED_HEADERS.items():
            lower_header = header.lower()
            found = False
            for resp_header, value in headers:
                if resp_header.lower() == lower_header:
                    found = True
                    break

            if not found:
                vulns.append(self._vuln(
                    title=f"Missing security header: {header}",
                    description=info["description"],
                    location=config.target_url,
                    remediation=info["remediation"],
                    severity=info["severity"],
                    fixable=True,
                ))

        # Check CORS
        cors_origin = None
        for resp_header, value in headers:
            if resp_header.lower() == "access-control-allow-origin":
                cors_origin = value
                break

        if cors_origin == "*":
            vulns.append(self._vuln(
                title="CORS allows all origins (*)",
                description="Access-Control-Allow-Origin: * allows any website to read API responses.",
                location=config.target_url,
                remediation="Restrict Access-Control-Allow-Origin to specific trusted domains.",
                severity=Severity.HIGH,
                fixable=True,
                evidence="Access-Control-Allow-Origin: *",
            ))
        elif cors_origin and cors_origin.startswith("http"):
            vulns.append(self._vuln(
                title="CORS allows specific origin via reflection",
                description=f"Access-Control-Allow-Origin: {cors_origin} reflects the Origin header. "
                            "If not validated, any site can bypass CORS.",
                location=config.target_url,
                remediation="Validate Origin against a whitelist before reflecting it.",
                severity=Severity.MEDIUM,
                fixable=True,
                evidence=f"Access-Control-Allow-Origin: {cors_origin}",
            ))

        return vulns

    async def _fetch_headers(self, url: str) -> Optional[list[tuple[str, str]]]:
        """Fetch HTTP response headers using urllib (stdlib, no external deps)."""
        try:
            import urllib.request
            req = urllib.request.Request(url, method="GET", headers={"User-Agent": "SaaS-Security-Auditor/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return list(resp.headers.items())
        except Exception:
            return None
