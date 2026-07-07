#!/usr/bin/env python3
"""
Initialize a new SaaS brand — deploys spec-designer agent + creates brand config.

Usage:
    python scripts/init_brand.py brands/my-new-brand
    python scripts/init_brand.py brands/my-new-brand --url https://my-new-brand.com
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a new SaaS brand")
    parser.add_argument("brand_dir", type=Path, help="Path to brand directory")
    parser.add_argument("--url", "-u", help="Target URL for the brand")
    parser.add_argument("--name", "-n", help="Brand name (default: folder name)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    brand_dir: Path = args.brand_dir

    if not brand_dir.exists():
        print(f"[!] Brand directory not found: {brand_dir}")
        print("    Run: cp -r brands/_template brands/your-brand-name")
        return 1

    brand_name = args.name or brand_dir.name

    # Check if it already has a brand.yaml
    brand_yaml = brand_dir / "brand.yaml"
    brand_json = brand_dir / "brand.json"
    config_file = brand_yaml if brand_yaml.exists() else (brand_json if brand_json.exists() else None)

    if config_file:
        print(f"  [OK] Found config: {config_file}")
        # Update the name in brand.yaml if needed
        text = config_file.read_text(encoding="utf-8")
        if args.name and f"name: \"{brand_name}\"" not in text:
            import re
            text = re.sub(r'name:\s*".*?"', f'name: "{brand_name}"', text)
            config_file.write_text(text, encoding="utf-8")
            print(f"  [OK] Updated brand name to: {brand_name}")
    else:
        print(f"  [!] No brand config found. Create brands/{brand_name}/brand.yaml first.")
        return 1

    # ===== AUTO-DEPLOY SPEC-DESIGNER AGENT =====
    spec_dir = brand_dir / "agents" / "spec-designer"
    template_spec_dir = PROJECT_ROOT / "brands" / "_template" / "agents" / "spec-designer"

    if template_spec_dir.exists():
        spec_dir.mkdir(parents=True, exist_ok=True)

        # Copy and template the AGENT.md
        agent_src = template_spec_dir / "AGENT.md"
        if agent_src.exists():
            agent_text = agent_src.read_text(encoding="utf-8")
            agent_text = agent_text.replace("{{BRAND_NAME}}", brand_name)
            agent_text = agent_text.replace("{{BRAND_DIR}}", brand_dir.name)
            agent_text = agent_text.replace("{{TARGET_URL}}", args.url or f"https://{brand_name}.example.com")
            (spec_dir / "AGENT.md").write_text(agent_text, encoding="utf-8")
            print(f"  [OK] Spec-designer AGENT.md deployed for {brand_name}")

        # Copy and template opencode.json
        config_src = template_spec_dir / "opencode.json"
        if config_src.exists():
            config_text = config_src.read_text(encoding="utf-8")
            config_text = config_text.replace("{{BRAND_NAME}}", brand_name)
            config_text = config_text.replace("{{BRAND_DIR}}", brand_dir.name)
            (spec_dir / "opencode.json").write_text(config_text, encoding="utf-8")
            print(f"  [OK] Spec-designer opencode.json deployed for {brand_name}")
    else:
        print(f"  [!] Spec-designer template not found at {template_spec_dir}")

    # Create brand docs directory
    docs_dir = brand_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / ".gitkeep").write_text("", encoding="utf-8")

    # Create brand src directory if not exists
    src_dir = brand_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / ".gitkeep").write_text("", encoding="utf-8")

    print(f"\n  [DONE] Brand '{brand_name}' initialized successfully!")
    print(f"  Path: {brand_dir.resolve()}")
    print(f"  Agents deployed: spec-designer")
    print()
    print(f"  Next steps:")
    print(f"    1. Edit {brand_yaml} to configure the brand")
    print(f"    2. Place source code in {src_dir}/ (optional)")
    print(f"    3. Run scan: python scripts/run_scan.py {brand_name} --url {args.url or 'https://...'}")
    print(f"    4. Use spec-designer: opencode run --agent brand-spec-designer")

    return 0


if __name__ == "__main__":
    exit(main())
