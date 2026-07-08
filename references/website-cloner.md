# Website Cloner

**Type:** 6-stage SaaS pipeline
**Location:** `F:\Notes\Projects\Automations_Dev\output\saas-auto-builder\`
**Source:** `saas_auto_builder.py` + `pipeline/` submodules

## What It Does

Full SaaS cloning system: research → validation → competitor analysis → generate → distribute.
Takes a business idea/vertical and produces a complete SaaS app with:
- Researched market validation
- Competitor clones with full business intel
- Generated SaaS code
- Distribution plan

## Pipeline Stages

| Stage | File | Output |
|-------|------|--------|
| 0. Research | `research_stage.py` | Market research brief |
| 1. Validation | `validator_stage.py` | Market validation report |
| 2. Competitors | `competitor_stage.py` | Competitor analysis |
| 3. Clones | `generator_stage.py` | Generated SaaS clones |
| 4. Distribution | `distribution_stage.py` | Distribution strategy |

## How This Project Uses It

- Referenced in `project-manifest.json` as an external tool
- Used when a new SaaS brand is being created in `brands/`
- Business intelligence from cloned sites feeds into security scanning

## Invocation

```bash
python F:\Notes\Projects\Automations_Dev\output\saas-auto-builder\saas_auto_builder.py \
  --vertical "real-estate" \
  --output ./output/saas-clones/
```

## Dependencies

- Python 3.11+
- No external pip packages (stdlib only)
