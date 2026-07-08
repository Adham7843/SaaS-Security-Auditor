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
| `opencode.json` | Master agent registry (see format rules below) |
| `.zed/tasks.json` | Zed editor tasks — one-click agent launch |
| `config/default.yaml` | Global defaults |
| `.env.example` | Environment variables template |

### `opencode.json` — FORMAT RULES (NON-NEGOTIABLE)

**These are hard rules. Violating any of them causes "Configuration is invalid" errors.**

#### Top-level keys

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": { ... }
}
```

- ✅ `"agent"` — SINGULAR. NEVER `"agents"`.
- ✅ `"$schema"` — optional but recommended.
- ❌ NO `"schema_version"` — this key is unrecognized.
- ❌ NO `"mcps"` or `"mcp"` at root level. MCPs go inside each agent.

#### Agent entry structure

```json
"agent-name": {
  "model": "opencode/deepseek-v4-flash-free",
  "variant": "high",
  "prompt": "{file:./path/to/AGENT.md}",
  "description": "What this agent does",
  "permission": { ... },
  "mcp": ["filesystem", "websearch"]
}
```

- ✅ `"prompt"` — NEVER `"system_prompt"`.
- ✅ `"permission"` — SINGULAR. NEVER `"permissions"`.
- ✅ `"mcp"` — SINGULAR array. NEVER `"mcps"`.
- ✅ `"hidden": true` — for sub-agents that shouldn't appear in the @ menu.
- ✅ `"mode": "primary"` — for main agents (optional).
- ✅ `"variant"` — `"low"`, `"medium"`, `"high"`, `"max"` for reasoning effort.

#### Permission rules — CRITICAL

**Only these 3 permissions support granular object rules (`{"pattern": "allow"}`):**
- `bash`
- `read`
- `edit`

**ALL other permissions MUST be simple strings (`"allow"` or `"deny"`):**
- `webfetch`, `websearch`, `grep`, `glob`, `question`, `task`, `skill`, `todowrite`, `lsp`, `doom_loop`, `external_directory`

```json
// CORRECT
"permission": {
  "read": { "*.py": "allow", "*": "deny" },
  "bash": { "python *": "allow", "*": "deny" },
  "webfetch": "allow",
  "websearch": "allow",
  "grep": "allow",
  "glob": "allow"
}

// WRONG — will fail validation
"permission": {
  "webfetch": { "*": "allow" },    // ❌ must be "allow"
  "websearch": { "*": "allow" },   // ❌ must be "allow"
  "question": { "*": "allow" }     // ❌ must be "allow"
}
```

### `.zed/tasks.json` Template

Every project gets a `tasks.json` in `.zed/` with one task per registered agent. Format:

```json
[
  {
    "label": "Agent Name — Description",
    "command": "pwsh -NoExit -Command \"cd '<PROJECT_DIR>'; opencode --agent <agent-name>\"",
    "spawn": "local",
    "use_new_terminal": true
  }
]
```

**Rules:**
- Array format (NOT `{"tasks": [...]}`  — that's VS Code, not Zed)
- `spawn: "local"` and `use_new_terminal: true` REQUIRED
- `pwsh -NoExit -Command` so the terminal stays open after agent exits
- Paths use escaped backslashes: `F:\\Notes\\Projects\\...`
- NO `--model` flag — agent's opencode.json already specifies it
- NO `--dangerously-skip-permissions` — agent's opencode.json handles permissions
- One task entry per agent in the registry

## Agent Registry (opencode.json)

Every new project's `opencode.json` registers:

1. `saas-security-auditor` — Main orchestrator
2. `saas-scanner` — Scan-only sub-agent (hidden)
3. `saas-fixer` — Fix-only sub-agent (hidden)
4. `distribution-classifier` — Classify + route findings
5. `spec-designer` — Security spec design (OPSX)
6. `design-factory` — Full design system (brand, UX, animation, 3D)
7. `business-cloner` — Clone + extract full business intel from any SaaS URL
8. `brand-spec-designer` — Per-brand scoped spec designer (hidden)

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
├── .zed/
│   └── tasks.json              ← Zed tasks: one-click agent launch
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
