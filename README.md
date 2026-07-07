# SaaS-Security-Auditor 🛡️

> Automated security vulnerability detection & fix engine for SaaS brands.

Scans your SaaS apps for:
- **Dependencies** — known CVEs in Python, Node.js, Rust packages
- **Configuration** — DEBUG mode, weak secrets, open CORS, missing SSL
- **Authentication** — weak JWT secrets, long-lived tokens, insecure cookies
- **Secrets** — hardcoded API keys, passwords, tokens, private keys (truffleHog-style)
- **HTTP Headers** — missing HSTS, CSP, X-Frame-Options, CORS misconfigs
- **SSL/TLS** — expired certs, weak protocols, self-signed certs

Then **auto-fixes** what it can — and gives you clear remediation steps for the rest.

---

## Quick Start

```bash
# Scan a single brand
python scripts/run_scan.py my-brand --url https://app.mybrand.com

# With source code analysis
python scripts/run_scan.py my-brand --url https://app.mybrand.com --dir ./brands/my-brand/src

# Review report
cat output/reports/my-brand-scan.md

# Apply auto-fixes
python scripts/run_fix.py output/reports/my-brand-scan.json --dir ./brands/my-brand/src

# Scan all brands at once
python scripts/scan_all_brands.py
```

## Adding Brands

```bash
# Create a new brand from template
cp -r brands/_template brands/my-new-brand

# Edit configuration
vim brands/my-new-brand/brand.yaml

# Place source code (optional)
mkdir brands/my-new-brand/src

# Scan it
python scripts/run_scan.py my-new-brand --url https://my-new-brand.com
```

## Project Structure

```
├── src/              ← Scanner & fixer source code
│   ├── core/         ← Engine, models, reporter
│   ├── scanners/     ← 7 vulnerability scanners
│   └── fixers/       ← Automated fix modules
├── brands/           ← One folder per SaaS brand
│   └── _template/    ← Template for new brands
├── scripts/          ← CLI entry points
├── config/           ← Global configuration
├── output/           ← Reports & fix manifests
└── opencode.json     ← Agent config for Opencode
```

## Reports

| Format | File | Use Case |
|--------|------|----------|
| Markdown | `output/reports/{brand}-scan.md` | Readable summary |
| JSON | `output/reports/{brand}-scan.json` | Machine parsing / CI |
| HTML | `output/reports/{brand}-scan.html` | Dashboard view |
| Summary | `output/reports/_summary.md` | Multi-brand overview |

## Opencode Agent

Run via Opencode:

```bash
opencode --agent saas-security-auditor
```

Then use prompts like:
- _"Scan all brands and show me critical findings"_
- _"Check my-brand for hardcoded secrets before we deploy"_
- _"Auto-fix config issues on my-brand and create a summary report"_

---

**Built by Mothra Harnesses 🦋**
