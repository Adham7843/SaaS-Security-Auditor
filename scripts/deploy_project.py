#!/usr/bin/env python3
"""
PROJECTOR — Deploy the full Mothra project kit to a target directory.

Reads project-manifest.json and deploys all agents, skills, configs,
scripts, and core engine to the target project.

Usage:
    python scripts/deploy_project.py /path/to/target-project
    python scripts/deploy_project.py /path/to/target-project --components agents,skills
    python scripts/deploy_project.py --list
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "project-manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PROJECTOR — Deploy Mothra project kit to target directory",
    )
    parser.add_argument("target", nargs="?", type=Path, help="Target project directory")
    parser.add_argument("--components", "-c", help="Comma-separated: agents,skills,scripts,core,config,all")
    parser.add_argument("--list", action="store_true", help="List available deployable components")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be copied")
    return parser.parse_args()


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        print(f"[!] Manifest not found: {MANIFEST_PATH}")
        print("    Run this script from the project root (where project-manifest.json lives)")
        sys.exit(1)
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def list_components(manifest: dict) -> None:
    print("=== PROJECTOR — Available Deployable Components ===")
    print()
    print("Agents:")
    for name, info in manifest.get("agents", {}).items():
        flag = "[ALWAYS]" if info.get("always_deploy") else "[OPTIONAL]"
        print(f"  {flag} agents/{name}/  — {info['description']}")
    print()
    print("External Tools (reference only — not copied):")
    for name, info in manifest.get("external_tools", {}).items():
        print(f"  {name}  — {info['description']}")
        print(f"    Source: {info['source']}")
    print()
    print("MCPs:")
    for name, info in manifest.get("mcps", {}).items():
        flag = "[ALWAYS]" if info.get("always_deploy") else "[OPTIONAL]"
        print(f"  {flag} {name} ({info['type']})")
    print()
    print("Core Engine Files:")
    for path, desc in manifest.get("core_engine", {}).items():
        print(f"  {path}  — {desc}")
    print()
    print("Per-Project Structure:")
    for d in manifest.get("per_project_structure", []):
        print(f"  {d}/")


def deploy_agents(manifest: dict, target: Path, dry_run: bool = False) -> list[str]:
    deployed = []
    agents_root = PROJECT_ROOT / "agents"
    target_agents = target / "agents"

    for name, info in manifest.get("agents", {}).items():
        src = agents_root / name
        dst = target_agents / name
        if not src.exists():
            print(f"  [!] Agent source not found: {src}")
            continue
        if info.get("type") == "opencode-agent-with-skills":
            # Deploy agent definition + skills
            skills_src = src / ".opencode" / "skills"
            skills_dst = dst / ".opencode" / "skills"
            if dry_run:
                print(f"  [DRY-RUN] Would deploy: {name} (agent + skills)")
            else:
                dst.mkdir(parents=True, exist_ok=True)
                # Copy AGENT.md and opencode.json
                for f in ["AGENT.md", "opencode.json"]:
                    sf = src / f
                    if sf.exists():
                        shutil.copy2(sf, dst / f)
                # Copy skills
                if skills_src.exists():
                    skills_dst.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(skills_src, skills_dst, dirs_exist_ok=True)
                print(f"  [OK] Deployed: {name} (agent + {_count_files(skills_src)} skills)")
        else:
            if dry_run:
                print(f"  [DRY-RUN] Would deploy: {name}")
            else:
                dst.mkdir(parents=True, exist_ok=True)
                _copy_dir(src, dst)
                print(f"  [OK] Deployed: {name}")
        deployed.append(name)

    return deployed


def deploy_core_engine(manifest: dict, target: Path, dry_run: bool = False) -> None:
    engine = manifest.get("core_engine", {})
    for rel_path, desc in engine.items():
        src = PROJECT_ROOT / rel_path
        dst = target / rel_path
        if not src.exists():
            continue
        if dry_run:
            print(f"  [DRY-RUN] Would copy: {rel_path}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"  [OK] {desc}: {rel_path}")


def deploy_structure(manifest: dict, target: Path, dry_run: bool = False) -> None:
    for rel_path in manifest.get("per_project_structure", []):
        d = target / rel_path
        if dry_run:
            print(f"  [DRY-RUN] Would create: {rel_path}/")
        else:
            d.mkdir(parents=True, exist_ok=True)
            # Add .gitkeep
            gitkeep = d / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.write_text("", encoding="utf-8")


def _copy_dir(src: Path, dst: Path) -> None:
    """Copy directory contents, merging with existing."""
    for item in src.iterdir():
        s = item
        d = dst / item.name
        if s.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)


def _count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in path.rglob("*") if _.is_file())


def main() -> int:
    args = parse_args()
    manifest = load_manifest()

    if args.list:
        list_components(manifest)
        return 0

    if not args.target:
        print("[!] Specify a target project directory")
        print("    python scripts/deploy_project.py /path/to/target-project")
        return 1

    target = args.target.resolve()
    if not target.exists():
        if args.dry_run:
            target.mkdir(parents=True, exist_ok=True)
            print(f"[DRY-RUN] Target would be created: {target}")
        else:
            print(f"[!] Target does not exist: {target}")
            return 1

    # Determine which components to deploy
    components = ["agents", "core", "structure"]
    if args.components:
        components = [c.strip() for c in args.components.split(",")]

    print(f"=== PROJECTOR — Deploying to {target} ===")
    print()

    if "structure" in components:
        print("--- Project Structure ---")
        deploy_structure(manifest, target, args.dry_run)
        print()

    if "agents" in components:
        print("--- Agents ---")
        deploy_agents(manifest, target, args.dry_run)
        print()

    if "core" in components:
        print("--- Core Engine ---")
        deploy_core_engine(manifest, target, args.dry_run)
        print()

    print(f"[DONE] Deployment complete. {len(components)} component(s) deployed.")
    print(f"  Target: {target}")
    if not args.dry_run:
        print(f"  Next: Register agents in {target}/opencode.json")
        print(f"  See PROJECTOR.md for full documentation")

    return 0


if __name__ == "__main__":
    exit(main())
