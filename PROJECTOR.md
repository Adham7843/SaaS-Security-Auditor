# PROJECTOR — Project Deployment Manifest

**What deploys to EVERY new project.**

This manifest defines the standard deployment kit: agents, tools, MCPs, skills, and configs that are deployed to every new project created under Mothra Harnesses. The `scripts/deploy_project.py` script reads `project-manifest.json` and executes the deployment.

---

## Always Deployed (Core)

| Component | Type | Source | Purpose |
|-----------|------|--------|---------|
| **Spec Designer** | Agent | `agents/spec-designer/` | OPSX workflow for specs |
| **Distribution Classifier** | Agent | `agents/distribution-classifier/` | Classify + route findings |
| **Website Cloner** | Tool | `Automations_Dev/output/saas-auto-builder/website-cloner/` | Clone competitor websites |
| **Business Cloner** | Pipeline | `Automations_Dev/output/saas-auto-builder/` | Full SAAS auto-builder pipeline |
| **Design Factory** | Agent + Skills | `agents/design-factory/` | 60+ design skills, 21 animation templates, 20 page layouts |

## MCPs

| MCP | Type | When |
|-----|------|------|
| `filesystem` | Builtin | Always |
| `websearch` | Builtin | Always |
| `gh_grep` | Builtin | When GitHub is the platform |
| `playwright` | Node | When website cloning is needed |
| `stripe` | API | When payments are involved |
| `postgres` | API | When database is needed |

## Skills Loaded

| Skill Source | Contents |
|-------------|----------|
| `agents/design-factory/skills/` | Brand (01), UX (02), 3D/WebGL (05), GSAP (06), Framer Motion (07) |
| `agents/spec-designer/` | OPSX workflow (explore, propose, apply, archive, sync) |

## Configs

| Config | Purpose |
|--------|---------|
| `opencode.json` | Master agent registry |
| `config/default.yaml` | Global defaults |
| `.env.example` | Environment variables template |

## Agent Registry (opencode.json)

Every new project's `opencode.json` registers:

1. `saas-security-auditor` — Main orchestrator
2. `saas-scanner` — Scan-only sub-agent (hidden)
3. `saas-fixer` — Fix-only sub-agent (hidden)
4. `distribution-classifier` — Classify + route findings
5. `spec-designer` — Security spec design (OPSX)
6. `design-factory` — Full design system (brand, UX, animation, 3D)
7. `brand-spec-designer` — Per-brand scoped spec designer (hidden)

---

## Per-Project Directory Structure

```
project-root/
├── agents/
│   ├── spec-designer/          ← Deployed
│   ├── distribution-classifier/ ← Deployed
│   └── design-factory/         ← Deployed (with skills/)
├── brands/                      ← SaaS brands go here
│   └── _template/              ← Brand template
├── scripts/                     ← All CLI scripts
├── src/                         ← Core engine
│   ├── core/                   ← Models, engine, fixer, reporter
│   ├── scanners/               ← 7 vulnerability scanners
│   └── fixers/                 ← Auto-fix modules
├── pipelines/                   ← Pipeline orchestrator
├── config/                      ← Config files
├── output/                      ← Reports & artifacts
├── opencode.json                ← Agent registry
├── PROJECTOR.md                 ← This manifest
└── project-manifest.json        ← Machine-readable version
```

---

## Deployment Command

```bash
# Deploy the full kit to a new project
python scripts/deploy_project.py /path/to/target-project

# Deploy specific components
python scripts/deploy_project.py /path/to/target-project --components agents,skills

# List available components
python scripts/deploy_project.py --list
```

---

*Version 1.0.0 — Standard deployment manifest for all Mothra-deployed projects*
