# Distribution Classifier Factory

**Type:** Classification system
**Location:** `F:\Notes\My_Systems\Distribution_Classifier_Factory\`

## What It Is

The original marketing solution factory that classifies business problems and routes them to solutions. Adapted for this project's security-specific distribution classifier at `agents/distribution-classifier/`.

## How This Project Uses It

The `agents/distribution-classifier/` system was adapted FROM this factory:
- Classification logic for severity/category/brand routing
- Distribution channels (GitHub issues, Slack, reports)
- Delivery manifest pattern

## Key Concepts Adapted

| Original | Security Auditor Adaptation |
|----------|---------------------------|
| Marketing problem classification | Vulnerability severity classification |
| Solution routing | Fix routing + channel distribution |
| Solution factories | Fix engine + report engine |
| Delivery manifest | `DELIVERY-MANIFEST.md` per agent |

## Files Referenced

- `classifiers/` → adapted to `agents/distribution-classifier/classifiers/`
- `distributors/` → adapted to `agents/distribution-classifier/distributors/`
- Solution templates → adapted to security fixer patterns
