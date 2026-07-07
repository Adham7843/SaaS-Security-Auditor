"""
SaaS-Security-Auditor — Pipeline Orchestrator

Multi-stage pipeline for CI/CD integration:
  1. Scan → 2. Fix → 3. Report → 4. Notify
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.engine import ScanEngine, ScannerConfig
from src.core.fixer import FixEngine
from src.core.fixers.config_fixer import ConfigFixer
from src.core.models import ScanCategory
from src.core.reporter import ReportEngine


class ScanPipeline:
    """
    Full CI/CD pipeline:
    1. Scan the brand
    2. Apply auto-fixes
    3. Generate all report formats
    4. Save pipeline manifest
    """

    def __init__(self, brand: str, url: str, brand_dir: Path | None = None):
        self.brand = brand
        self.url = url
        self.brand_dir = brand_dir
        self.pipeline_id = f"pipe-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    async def run(self) -> dict:
        print(f"[Pipeline {self.pipeline_id}] Starting scan for {self.brand}...")

        config = ScannerConfig(
            brand=self.brand,
            target_url=self.url,
            target_dir=self.brand_dir,
            categories=list(ScanCategory),
        )

        # STAGE 1: Scan
        engine = ScanEngine()
        result = await engine.run(config)
        print(f"  [Stage 1] Scan complete: {result.summary}")

        # Save raw result
        scan_path = Path("output/reports") / f"{self.brand}-scan.json"
        result.save(scan_path)
        print(f"  [Stage 1] Raw result saved: {scan_path}")

        # STAGE 2: Fix
        fixers = [ConfigFixer()]
        fix_engine = FixEngine(fixers)
        fix_dir = Path("output/fixes")
        fix_dir.mkdir(parents=True, exist_ok=True)

        fix_results = await fix_engine.fix_all(result, self.brand_dir or PROJECT_ROOT)
        auto_fixed = sum(1 for f in fix_results if f.fix_status.value == "auto_fixed")
        print(f"  [Stage 2] Fixes applied: {auto_fixed}/{len(fix_results)}")

        fix_manifest = fix_dir / f"fix-manifest-{result.scan_id}.json"
        fix_manifest.write_text(
            json.dumps([f.to_dict() for f in fix_results], indent=2),
            encoding="utf-8",
        )

        # STAGE 3: Report
        reporter = ReportEngine()
        reports = {}
        for fmt, ext in [("markdown", "md"), ("json", "json"), ("html", "html")]:
            out = Path("output/reports") / f"{self.brand}-scan.{ext}"
            text = getattr(reporter, f"generate_{fmt}")(result, out)
            reports[fmt] = str(out)
        print(f"  [Stage 3] Reports generated: {len(reports)} formats")

        # STAGE 4: Pipeline manifest
        manifest = {
            "pipeline_id": self.pipeline_id,
            "brand": self.brand,
            "url": self.url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scan_result": result.to_dict(),
            "fix_results": [f.to_dict() for f in fix_results],
            "reports": reports,
        }
        manifest_path = Path("output") / f"pipeline-{self.pipeline_id}.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"  [Stage 4] Pipeline manifest: {manifest_path}")

        return manifest


async def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Run the full scan-fix-report pipeline")
    parser.add_argument("brand", help="Brand name")
    parser.add_argument("--url", "-u", required=True, help="Target URL")
    parser.add_argument("--dir", "-d", type=Path, help="Source code directory")
    args = parser.parse_args()

    pipeline = ScanPipeline(args.brand, args.url, args.dir)
    manifest = await pipeline.run()

    print(f"\n[DONE] Pipeline complete. Found {len(manifest['scan_result']['vulnerabilities'])} vulnerabilities.")
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
