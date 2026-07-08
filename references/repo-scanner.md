# Repo Scanner

**Type:** 3-stage analysis pipeline
**Location:** `F:\Notes\Second_Brain\00_System\00_Command_Center\Tools&Agents\Opencode_Agents\mothra-harnesses\output\repo-scanner\`

## What It Does

Analyzes any public repository (GitHub, npm, PyPI) by:
1. Fetching the source code (via `git clone` or `pip download`)
2. Building a knowledge graph of the codebase
3. Analyzing patterns, architecture, licenses, and dependencies

## Pipeline Stages

| Stage | File | Output |
|-------|------|--------|
| 1. Fetch | `stage1_fetch.py` | Cloned/downloaded source |
| 2. Graphify | `stage2_graphify.py` | Knowledge graph JSON |
| 3. Analyze | `stage3_analyze.py` | AI-powered analysis report |

## How This Project Uses It

The `agents/repo-scanner/` agent delegates to this harness.
Used to:
- Scan open-source dependencies for vulnerabilities
- Analyze competitor SDKs
- Map architecture of SaaS tools
- Audit license compliance

## Invocation

```bash
cd F:\Notes\Second_Brain\00_System\00_Command_Center\Tools&Agents\Opencode_Agents\mothra-harnesses\output\repo-scanner
python pipeline.py <repo_ref> --output-dir ./output/repo-scans/
```

Supported repo refs: `owner/repo`, `npm:pkg-name`, `https://github.com/...`

## Dependencies

- Python 3.11+
- Git (for cloning repos)
- pip (for npm/PyPI package downloads)
