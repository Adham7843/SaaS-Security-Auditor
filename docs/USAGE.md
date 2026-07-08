# SaaS-Security-Auditor Usage Guide

## Quick Start

```bash
# Scan a single URL
python scripts/run_scan.py test --url https://example.com

# Scan all brands
python scripts/scan_all_brands.py

# Apply fixes to a brand
python scripts/run_fix.py --brand my-brand

# Classify results
python scripts/classify_results.py --input output/reports/scan-123.json

# Distribute findings
python scripts/distribute_findings.py --input output/reports/classified.json
```

## Scanning

### Single URL Scan
```bash
python scripts/run_scan.py test --url https://example.com
```
Scans the URL across all enabled categories. Output saved to `output/reports/`.

### Full Brand Scan
```bash
python scripts/scan_all_brands.py
```
Scans every brand in `brands/` that has a `brand.yaml` with a `target_url`.

### Custom Scan Config
Edit `config/default.yaml` or per-brand config:
```bash
python scripts/run_scan.py test --url https://example.com --config brands/my-brand/scan-config.yaml
```

## Fix Engine

### Auto-Fix Vulnerabilities
```bash
python scripts/run_fix.py --brand my-brand
```
Applies automated fixes (DEBUG mode, weak secrets, CORS, SSL, cookies).

### Preview Fixes Without Applying
```bash
python scripts/run_fix.py --brand my-brand --dry-run
```

## Classification & Distribution

```bash
# Classify scan results by severity and category
python scripts/classify_results.py --input output/reports/latest.json

# Route findings to channels (GitHub issues, Slack, reports)
python scripts/distribute_findings.py --input output/reports/classified.json
```

## Pipeline

```bash
# Run the full pipeline: scan → classify → distribute → fix → report
python pipelines/scan_pipeline.py --brand my-brand
```

## Brands

### Create a Brand
```bash
# Copy template
Copy-Item -Path brands/_template -Destination brands/my-brand -Recurse

# Initialize
python scripts/init_brand.py brands/my-brand

# Edit brand.yaml with URL and settings
```

### Scan a Specific Brand
```bash
python scripts/run_scan.py my-brand --url https://app.mybrand.com
```

## CI/CD Integration

```bash
# Scan, fix, report, and generate manifest
python pipelines/scan_pipeline.py --brand my-brand --ci-mode
```

Outputs:
- `output/reports/` — Scan results (JSON + Markdown)
- `output/fixes/` — Applied fixes
- `output/reports/manifest.json` — Pipeline manifest

## External Tools

See `references/` for documentation on all external tools this project depends on.
