# Mothra Harnesses

**Type:** Agent Kit + Harness Forge
**Location:** `F:\Notes\Second_Brain\00_System\00_Command_Center\Tools&Agents\Opencode_Agents\mothra-harnesses\`
**Output:** `mothra-harnesses/output/`

## What It Is

Mothra is the meta-wrapper that builds deterministic Python wrappers (harnesses) for AI tools, CLIs, and pipelines. Every harness in `output/` is a complete, self-contained, async-native Python wrapper.

## All Forged Harnesses

| Harness | Type | Used By This Project |
|---------|------|---------------------|
| `marketing-video-harness/` | 5-stage video pipeline | Content-Creation |
| `meme-video-harness/` | 5-stage meme pipeline | Content-Creation |
| `business-intel-harness/` | Business intelligence | SaaS-Security-Auditor |
| `repo-scanner/` | Repo analysis pipeline | SaaS-Security-Auditor |
| `book-to-study-pipeline/` | Book → study materials | — |
| `transcript-to-study-pipeline/` | Transcript → study | Content-Creation |
| `engineering-team-harness/` | Team management | — |
| `local-business-ai-playbook/` | Local business AI | — |
| `mothra-self-pipeline/` | Self-referential | — |
| `project-configurator-harness/` | Project setup | — |
| `project-initializer-harness/` | Project init | — |
| `startup-forge-harness/` | Startup builder | — |
| `test-agent-harness/` | Testing | — |

## How This Project Uses It

This project references harnesses from mothra-harnesses/output/ as external tools:
- `business-intel-harness/` → through `agents/business-cloner/`
- `repo-scanner/` → through `agents/repo-scanner/`
- `marketing-video-harness/` + `meme-video-harness/` → through Content-Creation

## Invocation

Mothra itself is invoked as an Opencode agent:
```bash
opencode --agent mothra-harnesses
```
