"""
Config Fixer — applies automated fixes to configuration files.
"""

from __future__ import annotations

import re
from pathlib import Path

from src.core.fixer import BaseFixer
from src.core.models import FixResult, FixStatus, Vulnerability


class ConfigFixer(BaseFixer):
    """
    Fixes common config issues:
    - DEBUG=True -> DEBUG=False
    - Weak secret keys -> generated random key
    - CORS_ORIGIN_ALLOW_ALL=True -> False + whitelist
    """

    def can_fix(self, vuln: Vulnerability) -> bool:
        return vuln.fixable and vuln.category.value in ("configuration", "authentication")

    async def apply_fix(self, vuln: Vulnerability, target_dir: Path) -> FixResult:
        location = vuln.location
        file_path = target_dir / location if not Path(location).is_absolute() else Path(location)
        if not file_path.exists():
            return FixResult(
                vulnerability_id=vuln.id,
                fix_status=FixStatus.MANUAL_REQUIRED,
                description=f"File not found: {file_path}",
            )

        original = file_path.read_text(encoding="utf-8")
        modified = original

        if "DEBUG" in vuln.title and "True" in vuln.description:
            modified = re.sub(r'(DEBUG\s*=\s*)True', r'\1False', modified, flags=re.IGNORECASE)

        elif "secret key" in vuln.title.lower() or "JWT" in vuln.title:
            import secrets
            new_key = secrets.token_hex(32)
            modified = re.sub(
                r'(SECRET_KEY\s*=\s*)[\'\"][^\'\"]*[\'\"]',
                rf'\1"{new_key}"',
                modified, flags=re.IGNORECASE,
            )
            vuln.evidence = "Secret key rotated to a new 256-bit random value"

        elif "CORS" in vuln.title and "all origins" in vuln.title.lower():
            modified = re.sub(
                r'(CORS_ORIGIN_ALLOW_ALL\s*=\s*)True',
                r'\1False',
                modified, flags=re.IGNORECASE,
            )
            # Add whitelist if not present
            if "CORS_ORIGIN_WHITELIST" not in modified:
                modified += "\nCORS_ORIGIN_WHITELIST = ['https://yourdomain.com']\n"

        elif "SSL redirect" in vuln.title:
            modified = re.sub(
                r'(SECURE_SSL_REDIRECT\s*=\s*)False',
                r'\1True',
                modified, flags=re.IGNORECASE,
            )

        elif "session cookie" in vuln.title.lower():
            if "SESSION_COOKIE_SECURE" in modified:
                modified = re.sub(r'SESSION_COOKIE_SECURE\s*=\s*False', 'SESSION_COOKIE_SECURE = True', modified)
            if "SESSION_COOKIE_HTTPONLY" in modified:
                modified = re.sub(r'SESSION_COOKIE_HTTPONLY\s*=\s*False', 'SESSION_COOKIE_HTTPONLY = True', modified)

        elif "ALLOWED_HOSTS" in vuln.title:
            modified = re.sub(
                r'ALLOWED_HOSTS\s*=\s*\[\s*['\"]*['\"]\s*\]',
                "ALLOWED_HOSTS = ['*']  # TODO: Restrict in production",
                modified,
            )

        if modified == original:
            return FixResult(
                vulnerability_id=vuln.id,
                fix_status=FixStatus.MANUAL_REQUIRED,
                description="Could not auto-fix: pattern not found for automated replacement.",
            )

        import json
        diff = self._generate_diff(original, modified, file_path)
        file_path.write_text(modified, encoding="utf-8")

        return FixResult(
            vulnerability_id=vuln.id,
            fix_status=FixStatus.AUTO_FIXED,
            description=f"Applied fix to {file_path.name}",
            diff=diff,
        )

    @staticmethod
    def _generate_diff(original: str, modified: str, path: Path) -> str:
        """Simple line-based diff."""
        orig_lines = original.splitlines(keepends=True)
        mod_lines = modified.splitlines(keepends=True)

        diff_lines = [f"--- {path}", f"+++ {path}"]
        for i, (o, m) in enumerate(zip(orig_lines, mod_lines), 1):
            if o != m:
                diff_lines.append(f"-{o.rstrip()}")
                diff_lines.append(f"+{m.rstrip()}")
        return "\n".join(diff_lines)
