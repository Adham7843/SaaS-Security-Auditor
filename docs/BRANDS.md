# Brands System

## Overview

Each brand (client, SaaS product) gets a directory under `brands/` with its own configuration, intel, and scan history.

```
brands/
├── _template/              ← Copy to create new brands
│   ├── brand.yaml          ← Brand identity + scan config
│   └── agents/             ← Brand-specific agent configs
├── checkvibe/              ← Example brand
│   └── intel/              ← Business intelligence data
│       ├── screenshots/
│       ├── checkvibe_clone_playbook.md
│       └── checkvibe_intel.md
└── your-brand/
    ├── brand.yaml
    ├── intel/
    ├── config/
    └── output/
```

## brand.yaml Fields

| Field | Description | Required |
|-------|-------------|----------|
| `name` | Brand name | Yes |
| `target_url` | URL to scan | Yes |
| `target_dir` | Path to source code (optional) | No |
| `severity_threshold` | Minimum severity to report | No |
| `timeout_seconds` | Scan timeout | No |
| `enabled_categories` | Scanner categories to run | No |
| `env_vars` | Environment variables needed | No |
| `custom_checks` | Brand-specific custom checks | No |

## Creating a Brand

```bash
# Copy template
Copy-Item -Path brands/_template -Destination brands/new-client -Recurse

# Initialize (deploys agents)
python scripts/init_brand.py brands/new-client

# Edit brand.yaml
# Set target_url, name, etc.

# Gather intel (optional)
python ../mothra-harnesses/output/business-intel-harness/pipeline.py \
  https://newclient.com \
  --output brands/new-client/intel/

# Run security scan
python scripts/run_scan.py new-client --url https://app.newclient.com
```

## Brand Lifecycle

1. **Discovery** — Business cloner gathers intel → `brands/<name>/intel/`
2. **Scanning** — Security scanners analyze → `output/reports/`
3. **Classification** — Results classified by severity → `output/reports/classified/`
4. **Fixing** — Auto-fixes applied → `output/fixes/`
5. **Reporting** — Reports generated → `output/reports/`
6. **Monitoring** — Continuous scanning via pipeline
