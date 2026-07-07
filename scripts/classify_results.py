#!/usr/bin/env python3
"""
Distribution Classifier — Classify scan results by severity, category, brand.

Assigns priority, SLA, and recommended action to each vulnerability.
Outputs a classified report that can be fed to distribute_findings.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

SEVERITY_CONFIG = {
    "critical": {"priority": 1, "sla_hours": 1, "auto_block": True,  "channels": ["slack", "github", "email"]},
    "high":     {"priority": 2, "sla_hours": 24, "auto_block": False, "channels": ["github", "slack"]},
    "medium":   {"priority": 3, "sla_hours": 168, "auto_block": False, "channels": ["github"]},
    "low":      {"priority": 4, "sla_hours": 720, "auto_block": False, "channels": ["report"]},
    "info":     {"priority": 5, "sla_hours": 0, "auto_block": False,   "channels": ["report"]},
}

CATEGORY_FIXER_MAP = {
    "dependencies":    "dependabot / pip audit",
    "configuration":   "src/fixers/config_fixer.py (auto-fix available)",
    "authentication":  "manual review required",
    "secrets":         "manual rotation required — CRITICAL",
    "cors_headers":    "src/fixers/config_fixer.py (auto-fix available)",
    "ssl_tls":         "devops / cert manager",
    "general":         "manual review",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify scan results by severity/category/brand")
    parser.add_argument("scan_result", type=Path, help="Path to scan JSON result file")
    parser.add_argument("--output", "-o", type=Path, default=Path("output/reports"),
                        help="Output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.scan_result.exists():
        print(f"[!] Scan result not found: {args.scan_result}")
        return 1

    data = json.loads(args.scan_result.read_text(encoding="utf-8"))
    vulnerabilities = data.get("vulnerabilities", [])
    brand = data.get("brand", "unknown")

    print(f"[Distribution Classifier] Classifying {len(vulnerabilities)} vulns for {brand}")
    print()

    classified = []
    for v in vulnerabilities:
        sev = v.get("severity", "low").lower()
        cat = v.get("category", "general")
        sev_config = SEVERITY_CONFIG.get(sev, SEVERITY_CONFIG["low"])

        entry = {
            "id": v.get("id"),
            "title": v.get("title"),
            "severity": sev,
            "category": cat,
            "brand": brand,
            "priority": sev_config["priority"],
            "sla_hours": sev_config["sla_hours"],
            "auto_block": sev_config["auto_block"],
            "channels": list(sev_config["channels"]),
            "recommended_fixer": CATEGORY_FIXER_MAP.get(cat, "manual review"),
            "location": v.get("location", "N/A"),
            "fixable": v.get("fixable", False),
            "fix_status": v.get("fix_status", "pending"),
            "classified_at": datetime.now(timezone.utc).isoformat(),
        }
        classified.append(entry)

    # Summary by severity
    by_sev: dict[str, int] = {}
    for c in classified:
        by_sev[c["severity"]] = by_sev.get(c["severity"], 0) + 1

    print("  Classification Summary:")
    for sev in ["critical", "high", "medium", "low", "info"]:
        count = by_sev.get(sev, 0)
        if count:
            sla = SEVERITY_CONFIG[sev]["sla_hours"]
            sla_str = f" (SLA: {sla}h)" if sla else ""
            print(f"    [{sev.upper():8}] {count} findings{sla_str}")

    print()
    for c in classified:
        if c["severity"] in ("critical", "high"):
            print(f"    [!] [{c['severity'].upper()}] {c['title']}")
            print(f"        -> Fixer: {c['recommended_fixer']}")
            print(f"        -> Channels: {', '.join(c['channels'])}")

    # Save classified report
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{brand}-classified.json"
    out_path.write_text(json.dumps(classified, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  [OK] Classified report: {out_path}")

    return 0


if __name__ == "__main__":
    exit(main())
