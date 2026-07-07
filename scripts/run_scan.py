#!/usr/bin/env python3
"""
SaaS-Security-Auditor — CLI Entry Point

Run a security scan against a single SaaS brand.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.engine import ScanEngine, ScannerConfig
from src.core.models import ScanCategory
from src.core.reporter import ReportEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SaaS-Security-Auditor — Scan a SaaS brand for vulnerabilities",
    )
    parser.add_argument("brand", help="Brand name (used for report labeling)")
    parser.add_argument("--url", "-u", required=True, help="Target SaaS URL (e.g., https://app.example.com)")
    parser.add_argument("--dir", "-d", type=Path, help="Target source code directory")
    parser.add_argument("--categories", "-c", nargs="+",
                        choices=[c.value for c in ScanCategory],
                        help="Specific categories to scan (default: all)")
    parser.add_argument("--output", "-o", type=Path, default=Path("output/reports"),
                        help="Output directory for reports")
    parser.add_argument("--timeout", type=int, default=300, help="Scanner timeout in seconds")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "html", "all"],
                        default="markdown", help="Report format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    return parser.parse_args()


async def main() -> int:
    args = parse_args()

    categories = [ScanCategory(c) for c in args.categories] if args.categories else list(ScanCategory)

    config = ScannerConfig(
        brand=args.brand,
        target_url=args.url,
        target_dir=args.dir,
        categories=categories,
        timeout_seconds=args.timeout,
        output_dir=args.output,
    )

    engine = ScanEngine()
    print(f"[SaaS-Security-Auditor] Scanning {args.brand}...")
    print(f"  Target: {args.url}")
    print(f"  Categories: {len(categories)}")
    print(f"  Scanners: {len(engine.scanners)}")

    result = await engine.run(config)

    print(f"\n  [DONE] {result.summary}")

    # Generate reports
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    reporter = ReportEngine()
    formats = ["markdown", "json", "html"] if args.format == "all" else [args.format]

    for fmt in formats:
        ext = {"markdown": "md", "json": "json", "html": "html"}[fmt]
        out_path = output_dir / f"{args.brand}-scan.{ext}"
        getattr(reporter, f"generate_{fmt}")(result, out_path)
        print(f"  [OK] Report: {out_path}")

    print(f"\n  Found {len(result.vulnerabilities)} vulnerabilities:")
    for v in sorted(result.vulnerabilities, key=lambda x: x.severity.value):
        print(f"    [{v.severity.value.upper():8}] {v.title}")
        print(f"           -> {v.remediation}")

    return 0 if len(result.vulnerabilities) == 0 else 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
