# Distribution Classifier Agent — Delivery Manifest

**Version:** v1.0.0
**Date:** 2026-07-08
**Origin:** `SAAS_Businesses/SaaS-Security-Auditor/agents/distribution-classifier/`

---

## What's Included

| Component | File | Description |
|-----------|------|-------------|
| **Agent Definition** | `AGENT.md` | Full agent prompt — classifies vulns by severity/category/brand |
| **Agent Config** | `opencode.json` | Permission-scoped agent for Opencode |
| **Classifiers** | `classifiers/` | (Extensible) severity, category, brand classifiers |
| **Distributors** | `distributors/` | (Extensible) GitHub, Slack, report distributors |
| **Classify Script** | `scripts/classify_results.py` | CLI — classifies a scan JSON result |
| **Distribute Script** | `scripts/distribute_findings.py` | CLI — routes findings to channels |

---

## How to Deploy to Any Project

### Step 1: Copy Files

```bash
# From this repo to target project
cp -r agents/distribution-classifier/ /path/to/target-project/agents/distribution-classifier/
cp scripts/classify_results.py /path/to/target-project/scripts/
cp scripts/distribute_findings.py /path/to/target-project/scripts/
```

### Step 2: Register in Target Project's opencode.json

```json
{
  "agents": {
    "distribution-classifier": {
      "model": "opencode/deepseek-v4-flash-free",
      "variant": "medium",
      "system_prompt": "{file:./agents/distribution-classifier/AGENT.md}",
      "permissions": {
        "read": { "*": "allow" },
        "edit": { "output/reports/*": "allow" },
        "bash": {
          "python scripts/classify_results*": "allow",
          "python scripts/distribute_findings*": "allow",
          "*": "ask"
        },
        "grep": { "*": "allow" },
        "glob": { "*": "allow" }
      },
      "mcps": ["filesystem"],
      "description": "Distribution Classifier — classify and route findings"
    }
  }
}
```

### Step 3: Verify

```bash
python scripts/classify_results.py --help
python scripts/distribute_findings.py --help
```

---

## Dependencies

- **Runtime:** Python 3.11+
- **Libraries:** stdlib only (`json`, `pathlib`, `argparse`, `subprocess`)
- **Optional:** `gh` CLI (for GitHub issue creation), `SLACK_WEBHOOK_URL` env var (for Slack alerts)
- **Input:** Scan JSON result from SaaS-Security-Auditor (or any tool producing compatible JSON)

---

## Portability Notes

- All paths are **relative** — no hardcoded absolute paths
- The classify script works on **any** JSON file matching the `ScanResult` schema
- The distribute script routes to **channels independently** — if one fails, others continue
- Distribution manifests are saved to `output/distributions/` (relative to project root)
- GitHub issue creation falls back to local file save if `gh` CLI is unavailable

---

## Schema: Required Input JSON

The classify script expects a JSON file with this shape (compatible with ScanResult.to_dict()):

```json
{
  "brand": "my-brand",
  "scan_id": "scan-abc123",
  "vulnerabilities": [
    {
      "id": "abc123def456",
      "severity": "critical",
      "category": "secrets",
      "title": "Hardcoded AWS key",
      "description": "...",
      "location": "src/config.py:42",
      "remediation": "Rotate the key",
      "fixable": false,
      "fix_status": "pending"
    }
  ]
}
```

---

*Deployable to any project with Python 3.11+*
*Built for Mothra Harnesses deployment pipeline*
