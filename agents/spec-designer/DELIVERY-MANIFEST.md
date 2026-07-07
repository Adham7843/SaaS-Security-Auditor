# Spec Designer Agent — Delivery Manifest

**Version:** v1.0.0
**Date:** 2026-07-08
**Origin:** `SAAS_Businesses/SaaS-Security-Auditor/agents/spec-designer/`

---

## What's Included

| Component | File | Description |
|-----------|------|-------------|
| **Agent Definition** | `AGENT.md` | Full agent prompt — OPSX workflow for security specs |
| **Agent Config** | `opencode.json` | Permission-scoped agent with OPSX-style operations |
| **Brand Template** | `brands/_template/agents/spec-designer/` | Per-brand scoped spec-designer template |
| **Init Script** | `scripts/init_brand.py` | One-command brand setup + spec-designer auto-deploy |

---

## How to Deploy to Any Project

### Option A: Deploy as Global Agent

```bash
# Copy to target project
cp -r agents/spec-designer/ /path/to/target-project/agents/spec-designer/

# Register in target's opencode.json:
# {
#   "agents": {
#     "spec-designer": {
#       "system_prompt": "{file:./agents/spec-designer/AGENT.md}",
#       ...
#     }
#   }
# }
```

### Option B: Deploy with Brand Auto-Setup

```bash
# Copy the init script
cp scripts/init_brand.py /path/to/target-project/scripts/

# Copy the brand template
cp -r brands/_template /path/to/target-project/brands/_template

# Then for each brand:
cd /path/to/target-project
python scripts/init_brand.py brands/my-brand --url https://my-brand.com
```

---

## Dependencies

- **Runtime:** Python 3.11+
- **Libraries:** stdlib only
- **No external deps** — the spec-designer is a prompt-based agent, not a code tool

---

## Portability Notes

- AGENT.md uses **relative paths** and template placeholders (`{{BRAND_NAME}}`, `{{BRAND_DIR}}`)
- Brand template uses `{{BRAND_NAME}}` and `{{TARGET_URL}}` — filled by `init_brand.py`
- The `init_brand.py` script works in any project structure with `brands/` and `scripts/`
- No hardcoded paths to SaaS-Security-Auditor — fully portable

---

## Customization

When deploying to a non-security project:

1. Edit `AGENT.md` — change `/sec:explore` to `/explore`, update the workflow description
2. Edit `opencode.json` — adjust permissions to match the target project's structure
3. Edit `brands/_template/agents/spec-designer/AGENT.md` — update the template placeholders

---

*Deployable to any project with Python 3.11+*
*Built for Mothra Harnesses deployment pipeline*
