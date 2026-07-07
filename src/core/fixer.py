"""
SaaS-Security-Auditor — Fix Engine

Applies automated fixes for fixable vulnerabilities.
Non-fixable vulns get annotated with manual remediation steps.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.core.models import FixResult, FixStatus, ScanResult, Vulnerability


class BaseFixer:
    """Override to implement fix logic for a vulnerability category."""

    def can_fix(self, vuln: Vulnerability) -> bool:
        return vuln.fixable

    async def apply_fix(self, vuln: Vulnerability, target_dir: Path) -> FixResult:
        raise NotImplementedError


class FixEngine:
    """
    Runs fixers on a ScanResult. Writes fix diffs and
    updates vulnerability fix_status fields.
    """

    def __init__(self, fixers: Optional[list[BaseFixer]] = None):
        self.fixers = fixers or []

    def register_fixer(self, fixer: BaseFixer) -> None:
        self.fixers.append(fixer)

    async def fix_all(self, result: ScanResult, target_dir: Path) -> list[FixResult]:
        fixes: list[FixResult] = []
        for vuln in result.vulnerabilities:
            fr = await self._try_fix(vuln, target_dir)
            fixes.append(fr)
            vuln.fix_status = fr.fix_status
        return fixes

    async def _try_fix(self, vuln: Vulnerability, target_dir: Path) -> FixResult:
        # Find a fixer that can handle this vulnerability
        for fixer in self.fixers:
            if fixer.can_fix(vuln):
                try:
                    return await fixer.apply_fix(vuln, target_dir)
                except Exception as e:
                    return FixResult(
                        vulnerability_id=vuln.id,
                        fix_status=FixStatus.MANUAL_REQUIRED,
                        description=f"Auto-fix failed: {e}",
                        error=str(e),
                    )

        return FixResult(
            vulnerability_id=vuln.id,
            fix_status=FixStatus.NOT_FIXABLE,
            description=vuln.remediation,
        )
