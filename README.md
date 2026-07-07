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

## Agents

| Agent | Command | Purpose |
|-------|---------|---------|
| **SaaS Security Auditor** | `opencode run --agent saas-security-auditor` | Main agent — scan, fix, report |
| **Distribution Classifier** | `opencode run --agent distribution-classifier` | Classify & route findings to channels |
| **Spec Designer** | `opencode run --agent spec-designer` | Design security specs & remediation plans |

### Distribution Classifier

After a scan, classify and route findings:

```bash
# Classify by severity/category/brand
python scripts/classify_results.py output/reports/my-brand-scan.json

# Route critical findings to Slack + GitHub
python scripts/distribute_findings.py output/reports/my-brand-classified.json --channels slack github
```

### Spec Designer (OPSX for Security)

Turn findings into structured specs:

```bash
/sec:explore "What's the risk of weak JWT secrets in brand-x?"
/sec:propose "JWT secret rotation for brand-x"
/sec:apply "JWT secret rotation for brand-x"
/sec:archive "JWT secret rotation for brand-x"
/sec:sync "JWT secret rotation for brand-x"
```

Every brand automatically gets its own scoped spec-designer agent when initialized:

```bash
python scripts/init_brand.py brands/my-brand --url https://my-brand.com
```

This creates `brands/my-brand/agents/spec-designer/` with a brand-scoped agent.

---

## Deployability

All agents and pipelines in this project are **deployable to any other project**. Each comes with a `DELIVERY-MANIFEST.md`:

| Component | Manifest |
|-----------|----------|
| **Full Pipeline** | `pipelines/DELIVERY-MANIFEST.md` |
| **Distribution Classifier** | `agents/distribution-classifier/DELIVERY-MANIFEST.md` |
| **Spec Designer** | `agents/spec-designer/DELIVERY-MANIFEST.md` |

To deploy any component to another project:
1. Copy the component directory
2. Register in the target project's `opencode.json`
3. Run it — **zero external dependencies** (stdlib only)

---

**Built for Mothra Harnesses deployment pipeline**
