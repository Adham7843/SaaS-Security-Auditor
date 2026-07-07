#!/usr/bin/env python3
"""
SaaS-Security-Auditor — Scan All Brands

Iterates through all brands/ subdirectories and runs a scan on each.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.engine import ScanEngine, ScannerConfig
from src.core.models import ScanCategory
from src.core.reporter import ReportEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan all SaaS brands configured in brands/",
    )
    parser.add_argument("--brands-dir", type=Path, default=Path("brands"),
                        help="Directory containing brand configs (default: brands/)")
    parser.add_argument("--output", "-o", type=Path, default=Path("output/reports"),
                        help="Output directory for reports")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "html", "all"],
                        default="markdown", help="Report format")
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    brands_dir = (PROJECT_ROOT / args.brands_dir).resolve()
    output_dir = (PROJECT_ROOT / args.output).resolve()

    if not brands_dir.exists():
        print(f"[!] Brands directory not found: {brands_dir}")
        return 1

    # Discover brand configs
    brand_configs = []
    for entry in sorted(brands_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("_"):
            continue
        config_file = entry / "brand.yaml"
        if not config_file.exists():
            # Try a simple JSON file
            config_file = entry / "brand.json"
        if not config_file.exists():
            # Minimal config from folder name
            brand_configs.append({
                "name": entry.name,
                "url": f"https://{entry.name}.example.com",
                "dir": str(entry),
            })
            continue
        # Parse config (simplified YAML-free version using JSON)
        import json
        try:
            config = json.loads(config_file.read_text(encoding="utf-8"))
            config["name"] = config.get("name", entry.name)
            brand_configs.append(config)
        except Exception:
            brand_configs.append({"name": entry.name, "url": "", "dir": str(entry)})

    if not brand_configs:
        print(f"[!] No brand configs found in {brands_dir}")
        return 1

    print(f"[SaaS-Security-Auditor] Found {len(brand_configs)} brand(s) to scan")
    print()

    engine = ScanEngine()
    reporter = ReportEngine()
    all_results = []

    for bc in brand_configs:
        print(f"  Scanning: {bc['name']}")
        config = ScannerConfig(
            brand=bc["name"],
            target_url=bc.get("url", ""),
            target_dir=Path(bc.get("dir", "")) if bc.get("dir") else None,
            categories=list(ScanCategory),
        )
        result = await engine.run(config)
        all_results.append(result)

        # Generate per-brand report
        brand_out = output_dir / bc["name"]
        brand_out.mkdir(parents=True, exist_ok=True)
        for fmt in (["markdown", "json", "html"] if args.format == "all" else [args.format]):
            ext = {"markdown": "md", "json": "json", "html": "html"}[fmt]
            getattr(reporter, f"generate_{fmt}")(result, brand_out / f"scan.{ext}")

        print(f"    {result.summary}")
        print()

    # Generate summary
    total_vulns = sum(len(r.vulnerabilities) for r in all_results)
    print(f"  [DONE] All brands scanned. Total vulnerabilities: {total_vulns}")

    # Summary report
    summary_lines = [
        "# SaaS-Security-Auditor — Multi-Brand Scan Summary",
        "",
        f"**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Brands Scanned:** {len(all_results)}",
        f"**Total Vulnerabilities:** {total_vulns}",
        "",
        "| Brand | Vulnerabilities | Critical | High | Medium | Low | Duration |",
        "|-------|----------------|----------|------|--------|-----|----------|",
    ]
    for r in all_results:
        by_sev: dict[str, int] = {}
        for v in r.vulnerabilities:
            by_sev[v.severity.value] = by_sev.get(v.severity.value, 0) + 1
        d = r.duration_seconds or 0
        summary_lines.append(
            f"| {r.brand} | {len(r.vulnerabilities)} | "
            f"{by_sev.get('critical', 0)} | {by_sev.get('high', 0)} | "
            f"{by_sev.get('medium', 0)} | {by_sev.get('low', 0)} | "
            f"{d:.1f}s |"
        )

    summary_path = output_dir / "_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"  [OK] Summary: {summary_path}")

    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
