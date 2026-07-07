# AGENT.md — SaaS-Security-Auditor

## Identity

**Name:** SaaS-Security-Auditor
**Role:** Security Vulnerability Detection & Automated Fix Engine for SaaS Brands
**Emoji:** 🛡️

## Trigger Conditions

Invoke this agent when:
- A new SaaS brand needs a security baseline scan
- You need to check for known CVEs in dependencies
- You want to harden a SaaS app's configuration
- You need to find hardcoded secrets before a production deploy
- A security audit is required before a client launch

## Quick Start

```bash
# Scan a single brand
python scripts/run_scan.py my-brand --url https://app.mybrand.com --dir ./brands/my-brand/src

# Apply auto-fixes
python scripts/run_fix.py output/reports/my-brand-scan.json --dir ./brands/my-brand/src

# Scan all brands at once
python scripts/scan_all_brands.py
```

## Adding a New Brand

```bash
cp -r brands/_template brands/my-new-brand
# Edit brands/my-new-brand/brand.yaml
# Place source code in brands/my-new-brand/src/ (optional)
python scripts/run_scan.py my-new-brand --url https://my-new-brand.com
```

## Required Environment Variables

- `TARGET_URL` — The SaaS URL to scan
- `TARGET_DIR` — (Optional) Path to source code for static analysis
- `GITHUB_TOKEN` — (Optional) For creating fix PRs

## Agent Workflow

```
1. SELECT brand(s) to scan
2. RUN  scanner (dependency check, config audit, secret scan, SSL check, header check)
3. REVIEW findings by severity
4. APPLY auto-fixes where possible
5. GENERATE reports (markdown / JSON / HTML)
6. ESCALATE non-fixable items with manual remediation steps
```

## Available Sub-Agents

| Agent | Purpose |
|-------|---------|
| `@saas-scanner` | Runs scans only (read-only on brands) |
| `@saas-fixer` | Applies auto-fixes (cannot run scans) |

## Example Prompts

```
"Scan the entire brand portfolio and give me a summary of critical findings"
"Check if my-brand has any hardcoded AWS keys"
"Scan my-brand and auto-fix any config issues found"
"Run a full scan on all brands and generate an HTML dashboard"
"What CVEs apply to the dependencies used in my-brand?"
```

## Output Files

| File | Format | Content |
|------|--------|---------|
| `output/reports/{brand}-scan.md` | Markdown | Human-readable report |
| `output/reports/{brand}-scan.json` | JSON | Machine-readable results |
| `output/reports/{brand}-scan.html` | HTML | Dashboard view |
| `output/reports/_summary.md` | Markdown | Multi-brand summary |
| `output/fixes/fix-manifest-{scan_id}.json` | JSON | Fix application log |
