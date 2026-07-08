# External References

This directory documents every external tool, pipeline, and agent that the SaaS-Security-Auditor depends on or references. 

Each file describes:
- **What** the tool does
- **Where** it lives on disk
- **How** this project uses it
- **How** to invoke it

## Index

| Reference | Type | Location |
|-----------|------|----------|
| `website-cloner.md` | Pipeline | `Automations_Dev/output/saas-auto-builder/` |
| `business-cloner.md` | Harness | `mothra-harnesses/output/business-intel-harness/` |
| `repo-scanner.md` | Harness | `mothra-harnesses/output/repo-scanner/` |
| `mothra-harnesses.md` | Agent Kit | `mothra-harnesses/` |
| `distribution-classifier-factory.md` | System | `My_Systems/Distribution_Classifier_Factory/` |
| `design-factory.md` | System | `My_Systems/Design_Factory/` |
| `marketing-video-harness.md` | Harness | `mothra-harnesses/output/marketing-video-harness/` |
| `meme-video-harness.md` | Harness | `mothra-harnesses/output/meme-video-harness/` |
| `business-intel-harness.md` | Harness | `mothra-harnesses/output/business-intel-harness/` |
| `transcript-to-study-pipeline.md` | Pipeline | `mothra-harnesses/output/transcript-to-study-pipeline/` |

## Path Quick Reference

```
F:\Notes\
├── Projects\
│   ├── Automations_Dev\output\saas-auto-builder\         ← Website + Business Cloner
│   └── SAAS_Businesses\SaaS-Security-Auditor\             ← THIS REPO
├── Second_Brain\00_System\00_Command_Center\Tools&Agents\
│   └── Opencode_Agents\mothra-harnesses\                   ← All harnesses
│       └── output\                                          ← Forged harnesses
├── Notes\Tools\                                             ← External CLI tools
│   ├── opensource-clipping\
│   └── ...
└── Notes\My_Systems\                                        ← Factory systems
    ├── Distribution_Classifier_Factory\
    └── Design_Factory\
```
