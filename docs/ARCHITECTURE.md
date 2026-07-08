# Architecture Deep Dive

## System Overview

```
                     ┌──────────────┐
                     │   Opencode   │
                     │   Agents     │
                     └──────┬───────┘
                            │ orchestrates
                     ┌──────▼───────┐
                     │  Pipeline    │
                     │  scan_pipeline.py
                     └──────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────▼────┐ ┌─────▼──────┐ ┌────▼──────┐
       │  Scanner  │ │  Fixer    │ │ Reporter  │
       │  Engine   │ │  Engine   │ │  Engine   │
       └──────┬────┘ └─────┬──────┘ └────┬──────┘
              │             │             │
       ┌──────▼────┐       │      ┌──────▼──────┐
       │ 7 Scanner │       │      │ Markdown    │
       │  Modules  │       │      │ JSON        │
       └───────────┘       │      │ HTML        │
                           │      └─────────────┘
                    ┌──────▼──────┐
                    │ 5 Fixer    │
                    │  Modules   │
                    └─────────────┘
```

## Core Components

### `src/core/`
| File | Purpose |
|------|---------|
| `models.py` | Data models: Vulnerability, ScanResult, FixResult, Severity enum |
| `engine.py` | ScanEngine — orchestrates scanner execution |
| `fixer.py` | FixEngine — applies automated fixes |
| `reporter.py` | ReportEngine — generates Markdown/JSON/HTML reports |

### `src/scanners/`
7 scanner modules, one per category (see `SCANNERS.md`).

### `src/fixers/`
5 fixer modules corresponding to the most common vulnerability types.

### `scripts/`
| Script | Purpose |
|--------|---------|
| `run_scan.py` | Single URL or brand scan |
| `run_fix.py` | Apply fixes to scan results |
| `scan_all_brands.py` | Batch scan all brands |
| `classify_results.py` | Classify findings by severity/category |
| `distribute_findings.py` | Route to GitHub/Slack/report |
| `init_brand.py` | Initialize a new brand |
| `deploy_project.py` | Deploy PROJECTOR manifest to target |

### `pipelines/`
| File | Purpose |
|------|---------|
| `scan_pipeline.py` | Full CI/CD: scan → classify → distribute → fix → report → manifest |

## Data Flow

```
1. User triggers scan (script/agent/pipeline)
2. ScanEngine loads brand config
3. Each scanner runs against target
4. Vulnerabilities collected + deduplicated
5. Results saved to output/reports/
6. (Optional) FixEngine applies auto-fixes
7. ReportEngine generates output formats
8. DistributionClassifier routes findings
```

## External Dependencies

All Python dependencies are stdlib-only. External tools:
- `../mothra-harnesses/output/business-intel-harness/` — Business cloning
- `../mothra-harnesses/output/repo-scanner/` — Repo analysis
- `../Automations_Dev/output/saas-auto-builder/` — SaaS cloning pipeline
- `../My_Systems/Distribution_Classifier_Factory/` — Classification reference
- `../My_Systems/Design_Factory/` — Design system reference

See `references/` for full documentation.
