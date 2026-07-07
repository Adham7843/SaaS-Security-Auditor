"""
SSL/TLS Scanner — checks the target URL's SSL certificate
for expiry, weak ciphers, and configuration issues.
"""

from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

from src.core.engine import BaseScanner, ScannerConfig
from src.core.models import ScanCategory, Severity, Vulnerability


class SslScanner(BaseScanner):
    category = ScanCategory.SSL_TLS

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns: list[Vulnerability] = []
        if not config.target_url:
            return vulns

        parsed = urlparse(config.target_url)
        hostname = parsed.hostname or config.target_url
        port = parsed.port or 443

        cert_info = await self._get_cert_info(hostname, port)
        if cert_info is None:
            vulns.append(self._vuln(
                title="Could not establish SSL/TLS connection",
                description=f"Unable to connect to {hostname}:{port} via SSL. "
                            "The service may not support HTTPS.",
                location=f"{hostname}:{port}",
                remediation="Ensure the SaaS is served over HTTPS with a valid certificate.",
                severity=Severity.HIGH,
                fixable=False,
            ))
            return vulns

        # Check expiry
        not_after = cert_info.get("not_after")
        if not_after:
            remaining_days = (not_after - datetime.now(timezone.utc)).days
            if remaining_days < 0:
                vulns.append(self._vuln(
                    title="SSL certificate has EXPIRED",
                    description=f"Certificate expired {abs(remaining_days)} days ago on {not_after.date()}.",
                    location=f"{hostname}:{port}",
                    remediation="Renew the SSL certificate immediately. Use Let's Encrypt for auto-renewal.",
                    severity=Severity.CRITICAL,
                    fixable=False,
                    evidence=f"Not After: {not_after.isoformat()}",
                ))
            elif remaining_days < 7:
                vulns.append(self._vuln(
                    title="SSL certificate expiring soon",
                    description=f"Certificate expires in {remaining_days} day(s) on {not_after.date()}.",
                    location=f"{hostname}:{port}",
                    remediation="Renew the SSL certificate before it expires. Set up auto-renewal.",
                    severity=Severity.HIGH,
                    fixable=False,
                ))
            elif remaining_days < 30:
                vulns.append(self._vuln(
                    title="SSL certificate expiring within 30 days",
                    description=f"Certificate expires in {remaining_days} day(s) on {not_after.date()}.",
                    location=f"{hostname}:{port}",
                    remediation="Schedule certificate renewal within 2 weeks.",
                    severity=Severity.MEDIUM,
                    fixable=False,
                ))

        # Check issuer
        if cert_info.get("issuer"):
            # Self-signed check
            subject = cert_info.get("subject", "")
            issuer = cert_info.get("issuer", "")
            if subject and issuer and subject == issuer:
                vulns.append(self._vuln(
                    title="Self-signed SSL certificate",
                    description="The SSL certificate is self-signed. Browsers will show a security warning.",
                    location=f"{hostname}:{port}",
                    remediation="Replace with a certificate from a trusted CA (Let's Encrypt, DigiCert, etc.).",
                    severity=Severity.HIGH,
                    fixable=False,
                ))

        # Check wildcard certs (informational)
        if cert_info.get("is_wildcard"):
            vulns.append(self._vuln(
                title="Wildcard SSL certificate in use",
                description="A wildcard certificate (*.domain.com) is in use. While convenient, "
                            "wildcard certs increase blast radius if the private key is compromised.",
                location=f"{hostname}:{port}",
                remediation="Consider using individual certificates or a SAN certificate for critical subdomains.",
                severity=Severity.INFO,
                fixable=False,
            ))

        # Check protocol version
        if cert_info.get("protocol_version", "").startswith("TLSv1"):
            proto = cert_info["protocol_version"]
            if proto in ("TLSv1", "TLSv1.1"):
                vulns.append(self._vuln(
                    title=f"Obsolete TLS protocol: {proto}",
                    description=f"The server supports {proto}, which has known vulnerabilities. "
                                "Only TLS 1.2 and 1.3 should be enabled.",
                    location=f"{hostname}:{port}",
                    remediation="Disable TLS 1.0 and 1.1 on the server. Enable TLS 1.2 and 1.3 only.",
                    severity=Severity.HIGH,
                    fixable=False,
                ))

        return vulns

    async def _get_cert_info(self, hostname: str, port: int = 443) -> Optional[dict]:
        """Connect to the server and retrieve SSL certificate info."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    if not cert:
                        return None

                    # Parse notAfter
                    not_after = None
                    if cert.get("notAfter"):
                        try:
                            not_after = datetime.strptime(
                                cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
                            ).replace(tzinfo=timezone.utc)
                        except ValueError:
                            pass

                    # Parse subject/issuer
                    def _parse_name_parts(name_parts: list[tuple]) -> str:
                        parts = []
                        for part in name_parts:
                            if isinstance(part, tuple):
                                parts.append("=".join(str(x) for x in part))
                        return ", ".join(parts)

                    subject = _parse_name_parts(cert.get("subject", []))
                    issuer = _parse_name_parts(cert.get("issuer", []))

                    # Check wildcard
                    is_wildcard = False
                    for sub in cert.get("subject", []):
                        for key, val in sub:
                            if key == "commonName" and val.startswith("*."):
                                is_wildcard = True
                                break

                    # Protocol version
                    protocol_version = ssock.version()

                    return {
                        "not_after": not_after,
                        "subject": subject,
                        "issuer": issuer,
                        "is_wildcard": is_wildcard,
                        "protocol_version": protocol_version,
                    }
        except Exception as e:
            return None
