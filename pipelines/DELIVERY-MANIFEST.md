# SaaS-Security-Auditor Pipeline — Delivery Manifest

**Version:** v1.0.0
**Date:** 2026-07-08
**Origin:** `SAAS_Businesses/SaaS-Security-Auditor/`

---

## What's Included

| Component | Location | Description |
|-----------|----------|-------------|
| **Scan Pipeline** | `pipelines/scan_pipeline.py` | Full CI/CD orchestration (scan -> fix -> report -> manifest) |
| **Scan Engine** | `src/core/engine.py` | 7 vulnerability scanners |
| **Fix Engine** | `src/core/fixer.py` | Automated fix application |
| **Report Engine** | `src/core/reporter.py` | MD/JSON/HTML report generation |
| **Data Models** | `src/core/models.py` | Vulnerability, ScanResult, FixResult, enums |
| **Distribution Classifier** | `agents/distribution-classifier/` | Classify + route findings (see its DELIVERY-MANIFEST) |
| **Spec Designer** | `agents/spec-designer/` | Security spec OPSX workflow (see its DELIVERY-MANIFEST) |

---

## How to Deploy to Any Project

### Full Pipeline

```bash
# Copy everything
cp -r src/ /path/to/target-project/src/
cp -r pipelines/ /path/to/target-project/pipelines/
cp -r scripts/ /path/to/target-project/scripts/
cp -r config/ /path/to/target-project/config/

# Copy agents (optional)
cp -r agents/distribution-classifier/ /path/to/target-project/agents/distribution-classifier/
cp -r agents/spec-designer/ /path/to/target-project/agents/spec-designer/

# Run a scan
cd /path/to/target-project
python scripts/run_scan.py my-brand --url https://my-brand.com --dir ./src
```

### Minimal (Just the Scan Engine)

If you only want the scanning capability:

```bash
cp -r src/core/ /path/to/target-project/src/core/
cp scripts/run_scan.py /path/to/target-project/scripts/
# Then run:
python scripts/run_scan.py my-brand --url https://example.com
```

---

## Dependencies

| Component | Dependencies |
|-----------|--------------|
| **Scan Engine** | Python 3.11+, stdlib only (`asyncio`, `json`, `re`, `ssl`, `socket`, `urllib`) |
| **Report Engine** | Python 3.11+, stdlib only |
| **Fix Engine** | Python 3.11+, stdlib only |
| **Distribution Classifier** | Python 3.11+, stdlib only; optional: `gh` CLI |
| **Spec Designer** | Python 3.11+ (prompt-only agent) |

**Zero external packages required.** The entire pipeline runs on Python stdlib.

---

## Schema Compatibility

All components communicate via JSON using the `ScanResult` schema:

```json
{
  "brand": "string",
  "scan_id": "string",
  "vulnerabilities": [
    {
      "id": "string",
      "category": "string",
      "severity": "string",
      "title": "string",
      "description": "string",
      "location": "string",
      "remediation": "string",
      "fixable": bool,
      "fix_status": "string"
    }
  ]
}
```

Any tool that produces this schema can feed into the pipeline.

---

*Deployable to any project with Python 3.11+*
*Built for Mothra Harnesses deployment pipeline*
