# SaaS-Security-Auditor — Architecture

## Overview

```
SAAS_Businesses/
└── SaaS-Security-Auditor/         ← YOU ARE HERE
    ├── src/
    │   ├── core/
    │   │   ├── engine.py          ← ScanEngine — orchestrates scanners
    │   │   ├── fixer.py           ← FixEngine — applies automated fixes
    │   │   ├── reporter.py        ← ReportEngine — generates MD/JSON/HTML
    │   │   └── models.py          ← Vulnerability, ScanResult, FixResult, enums
    │   ├── scanners/
    │   │   ├── dependency.py      ← Dep scanner (requires.txt, package.json, Cargo.toml)
    │   │   ├── config.py          ← Config scanner (DEBUG, SECRET_KEY, CORS, etc.)
    │   │   ├── auth.py            ← Auth scanner (JWT, sessions, SSL redirect)
    │   │   ├── cors.py            ← Live HTTP header scanner (CORS, HSTS, CSP)
    │   │   ├── secrets.py         ← Hardcoded secrets scanner (API keys, tokens, passwords)
    │   │   ├── headers.py         ← Security middleware scanner (rate limiting, CSP)
    │   │   └── ssl.py             ← SSL/TLS certificate scanner (expiry, ciphers)
    │   └── fixers/
    │       └── config_fixer.py    ← Auto-fix for DEBUG, secret key, CORS config
    ├── brands/
    │   ├── _template/             ← Brand config template
    │   └── {brand-name}/          ← One folder per SaaS brand
    │       ├── brand.yaml          ← Brand-specific config
    │       └── src/               ← (Optional) Source code for static analysis
    ├── scripts/
    │   ├── run_scan.py            ← Single-brand scan CLI
    │   ├── run_fix.py             ← Fix application CLI
    │   └── scan_all_brands.py     ← Multi-brand batch scan
    ├── config/
    │   └── default.yaml           ← Global defaults
    ├── pipelines/
    │   └── scan_pipeline.py       ← (Coming soon) Full CI/CD pipeline
    ├── agents/
    │   ├── distribution-classifier/ ← Classifies & routes security findings
    │   │   ├── AGENT.md
    │   │   ├── opencode.json
    │   │   ├── classifiers/         ← Severity/category/brand classifiers
    │   │   └── distributors/        ← GitHub/Slack/report distributors
    │   └── spec-designer/          ← Security specification engine (OPSX)
    │       ├── AGENT.md
    │       └── opencode.json
    └── opencode.json              ← Opencode agent config with 5 sub-agents
```

## Data Flow

```
User / Agent
    │
    ▼
scripts/run_scan.py
    │
    ▼
ScanEngine.run(config)
    │
    ├── DependencyScanner.scan()   → checks requirements.txt, package.json, Cargo.toml
    ├── ConfigScanner.scan()       → checks .env, settings.py for misconfigs
    ├── AuthScanner.scan()         → checks auth config files
    ├── CorsScanner.scan()         → fetches live HTTP headers from target_url
    ├── SecretsScanner.scan()      → regex scans all source files for secrets
    ├── SecurityHeadersScanner.scan() → checks middleware config
    └── SslScanner.scan()          → connects to target_url, inspects cert
    │
    ▼
ScanResult (vulnerabilities list)
    │
    ├── ReportEngine.generate_markdown()  → output/reports/{brand}-scan.md
    ├── ReportEngine.generate_json()      → output/reports/{brand}-scan.json
    └── ReportEngine.generate_html()      → output/reports/{brand}-scan.html
    │
    ▼ (optional)
scripts/classify_results.py       ← Distribution Classifier
    │
    ├── Severity classification → priority + SLA
    ├── Category classification → fixer assignment
    └── Brand classification    → brand queue
    │
    ▼ (optional)
scripts/distribute_findings.py   ← Distribution Router
    │
    ├── GitHub Issue Distributor → creates issues per vuln
    ├── Slack Alert Distributor  → sends urgent alerts
    └── Report Distributor       → distribution manifest
    │
    ▼ (optional)
agents/spec-designer/            ← Spec Designer (OPSX workflow)
    │
    ├── /sec:explore  → Investigate security concerns
    ├── /sec:propose  → Create remediation specs
    ├── /sec:apply    → Implement fixes
    ├── /sec:archive  → Close completed changes
    └── /sec:sync     → Update security playbook
    │
    ▼ (optional)
FixEngine.fix_all()
    │
    ├── ConfigFixer.apply_fix()    → auto-fix DEBUG, SECRET_KEY, CORS
    └── FixResult → output/fixes/fix-manifest-{scan_id}.json
```

## Scanner Architecture

Each scanner extends `BaseScanner` and implements `async scan(config) -> list[Vulnerability]`:

```python
class MyScanner(BaseScanner):
    category = ScanCategory.SOME_CATEGORY

    async def scan(self, config: ScannerConfig) -> list[Vulnerability]:
        vulns = []
        # ... scan logic ...
        return vulns
```

**Two scan modes:**
1. **Static analysis** — scans source code files (secrets, config, deps, headers)
2. **Live analysis** — connects to target URL (CORS headers, SSL cert)

## Brand System

Each brand is a subfolder under `brands/`. The brand system allows:
- Per-brand configuration (URL, threshold, timeouts)
- Per-brand source code for static analysis
- Per-brand custom checks
- Batch scanning across the entire portfolio

## Extension Points

| Extension | How |
|-----------|-----|
| New scanner | Create `src/scanners/your_scanner.py` → register in `engine.py:_register_default_scanners()` |
| New fixer | Create `src/fixers/your_fixer.py` → register in `fixers` list |
| New report format | Add method to `ReportEngine` → call from CLI |
| New brand | Copy `brands/_template/` → fill `brand.yaml` → run scan |
