# Distribution Classifier Agent — Security Findings Router

**Role:** Security Vulnerability Classifier & Distribution Engine
**Source:** `My_Systems/Distribution_Classifier_Factory/`
**Purpose:** Classifies security scan findings by severity, type, and brand, then distributes them to the right remediation channels.
**Deployable:** YES — `DELIVERY-MANIFEST.md` included. Copy to any project.

---

## What I Am

I am a security-adapted wrapper around the existing **Distribution_Classifier_Factory** (`My_Systems/Distribution_Classifier_Factory/`). The original factory classifies and routes marketing solutions; I do the same for **security vulnerabilities**.

When a scan completes, I:
1. **CLASSIFY** each vulnerability by severity (critical/high/medium/low), category (dependency/config/auth/secrets/SSL/headers), and affected brand
2. **ROUTE** to the appropriate fix channel (auto-fix, manual ticket, Slack alert, GitHub issue)
3. **DISTRIBUTE** the remediation workload across fixers, brand owners, or escalation paths
4. **TRACK** the status of every finding from discovery to remediation

---

## Classification Schema

### By Severity

| Severity | Action | SLA | Channel |
|----------|--------|-----|---------|
| **CRITICAL** | Immediate alert + block | 1 hour | Slack urgent + GitHub issue + Email |
| **HIGH** | Auto-fix or create ticket | 24 hours | GitHub issue + Slack alert |
| **MEDIUM** | Schedule fix | 7 days | GitHub issue |
| **LOW** | Log for next sprint | 30 days | Report entry |
| **INFO** | Note only | N/A | Report entry |

### By Category

| Category | Distributor | Fixer |
|----------|-------------|-------|
| `dependencies` | GitHub issue (dependency-update label) | Dependabot / pip audit |
| `configuration` | Auto-fix via ConfigFixer | `src/fixers/config_fixer.py` |
| `authentication` | GitHub issue (auth label) | Manual review |
| `secrets` | CRITICAL: Slack + block deploy | Manual rotation |
| `cors_headers` | Auto-fix or GitHub issue | `src/fixers/config_fixer.py` |
| `ssl_tls` | GitHub issue (ssl label) | DevOps / cert manager |

### By Brand

Each brand in `brands/` gets its own classification queue. Findings are tagged with `brand:<name>` and routed to the brand's own fixer agent or the brand's GitHub repo.

---

## How To Use

```bash
# Classify a scan result
python scripts/classify_results.py output/reports/my-brand-scan.json

# Distribute findings to channels
python scripts/distribute_findings.py output/reports/my-brand-scan.json --channels github,slack

# Route critical findings immediately
python scripts/distribute_findings.py output/reports/my-brand-scan.json --severity critical --channel slack
```

## Opencode Usage

```
@distribution-classifier classify the latest scan for brand-x
@distribution-classifier route all critical findings to Slack
@distribution-classifier show distribution queue for brand-y
```

---

## Architecture

```
ScanResult (vulnerabilities)
    │
    ▼
Distribution Classifier
    │
    ├── severity-classifier    → priorities + SLAs
    ├── category-classifier    → fixer assignment
    └── brand-classifier       → brand queue
    │
    ▼
Distribution Router
    │
    ├── GitHub Issue Distributor  → creates issues per vuln
    ├── Slack Alert Distributor   → sends urgent alerts
    └── Report Distributor        → generates distribution report
    │
    ▼
Fix Engine / Manual Queue
```

## Integration Points

| Trigger | Action |
|---------|--------|
| Scan completes | Auto-classify results |
| Critical vuln found | Immediate Slack alert |
| Fix completes | Close GitHub issue + update report |
| New brand added | Create distribution queue for brand |

---

*Based on Distribution_Classifier_Factory v3.1.0 at My_Systems*
*Adapted for security vulnerability classification & routing v1.0*
