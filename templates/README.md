# Templates

Reusable templates for reports, configs, and notifications.

## Structure

```
templates/
├── reports/               ← Report output templates
│   ├── vulnerability-report.md   → Full vulnerability report (Markdown)
│   ├── executive-summary.md      → Executive summary for stakeholders
│   └── json-output.json          → Machine-readable JSON report
├── config/                ← Configuration templates
│   └── scan-config.yaml          → Brand scan configuration
└── notifications/         ← Notification channel templates
    ├── github-issue.md           → GitHub issue format
    └── slack-message.json        → Slack message blocks
```

## Usage

These templates are filled in by the Report Engine (`src/reporters/`) and Distribution Classifier (`agents/distribution-classifier/`).

To create a new brand's config:
```bash
cp templates/config/scan-config.yaml brands/my-brand/scan-config.yaml
# Edit brands/my-brand/scan-config.yaml with brand-specific settings
```
