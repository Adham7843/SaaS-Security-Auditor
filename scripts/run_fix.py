#!/usr/bin/env python3
"""
SaaS-Security-Auditor — Fix CLI

Apply automated fixes to vulnerabilities found by a scan.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.fixer import FixEngine
from src.core.fixers.config_fixer import ConfigFixer
from src.core.models import ScanResult


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SaaS-Security-Auditor — Apply automated fixes",
    )
    parser.add_argument("scan_result", type=Path, help="Path to scan JSON result file")
    parser.add_argument("--dir", "-d", type=Path, required=True, help="Target source code directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without applying")
    return parser.parse_args()


async def main() -> int:
    args = parse_args()

    if not args.scan_result.exists():
        print(f"[!] Scan result not found: {args.scan_result}")
        return 1

    data = json.loads(args.scan_result.read_text(encoding="utf-8"))
    result = ScanResult(
        brand=data["brand"],
        scan_id=data["scan_id"],
        started_at=data["started_at"],
        completed_at=data["completed_at"],
        duration_seconds=data.get("duration_seconds"),
    )

    # Reconstruct vulnerability objects (simplified)
    from src.core.models import Vulnerability, Severity, ScanCategory, FixStatus
    for vd in data.get("vulnerabilities", []):
        v = Vulnerability(
            id=vd["id"],
            category=ScanCategory(vd["category"]),
            severity=Severity(vd["severity"]),
            title=vd["title"],
            description=vd["description"],
            location=vd["location"],
            remediation=vd["remediation"],
            evidence=vd.get("evidence"),
            fixable=vd.get("fixable", False),
            fix_status=FixStatus(vd.get("fix_status", "pending")),
            cvss_score=vd.get("cvss_score"),
            cve_id=vd.get("cve_id"),
        )
        result.vulnerabilities.append(v)

    fixers = [ConfigFixer()]
    engine = FixEngine(fixers)

    fixable = [v for v in result.vulnerabilities if v.fixable]
    print(f"[SaaS-Security-Auditor] Fix engine ready")
    print(f"  Total vulns: {len(result.vulnerabilities)}")
    print(f"  Fixable: {len(fixable)}")
    print(f"  Target: {args.dir}")

    if args.dry_run:
        print("\n  [DRY RUN] Would attempt to fix:")
        for v in fixable:
            print(f"    - [{v.severity.value.upper()}] {v.title}")
            print(f"      Location: {v.location}")
        return 0

    fixes = await engine.fix_all(result, args.dir)

    auto_fixed = [f for f in fixes if f.fix_status.value == "auto_fixed"]
    manual = [f for f in fixes if f.fix_status.value == "manual_required"]
    not_fixable = [f for f in fixes if f.fix_status.value == "not_fixable"]

    print(f"\n  Results:")
    print(f"    Auto-fixed: {len(auto_fixed)}")
    print(f"    Manual required: {len(manual)}")
    print(f"    Not fixable: {len(not_fixable)}")

    for f in fixes:
        status = {
            "auto_fixed": "[OK]",
            "manual_required": "[!]",
            "not_fixable": "[--]",
        }.get(f.fix_status.value, "[?]")
        print(f"    {status} {f.vulnerability_id[:8]}: {f.description}")

    # Save fix manifest
    output_dir = Path("output/fixes")
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / f"fix-manifest-{result.scan_id}.json"
    manifest_path.write_text(
        json.dumps([f.to_dict() for f in fixes], indent=2),
        encoding="utf-8",
    )
    print(f"\n  [OK] Fix manifest saved: {manifest_path}")

    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
