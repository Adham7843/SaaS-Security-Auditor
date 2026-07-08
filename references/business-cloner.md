# Business Cloner

**Type:** 1-stage intelligence pipeline
**Location:** `F:\Notes\Second_Brain\00_System\00_Command_Center\Tools&Agents\Opencode_Agents\mothra-harnesses\output\business-intel-harness\`

## What It Does

Clones and analyzes any SaaS business website. Uses Playwright for screenshots, stackmd for tech stack detection, and AI for business model extraction.

## Pipeline

1. Accepts a SaaS URL (optionally a Capterra URL)
2. Fetches the site + Capterra page
3. Runs stackmd for technology profiling
4. Takes Playwright screenshots
5. Produces structured business intelligence report

## Data Extracted

| Category | Details |
|----------|---------|
| Identity | Name, tagline, founded, HQ, social links |
| Product | Products, pricing tiers, free trial, freemium |
| Tech Stack | Frontend, backend, hosting, CDN, analytics |
| Design | Screenshots, colors, typography, UX patterns |
| Marketing | Brand voice, SEO score, CTAs |
| Business | B2B/B2C, revenue model, PLG, enterprise readiness |

## How This Project Uses It

The `agents/business-cloner/` agent delegates to this harness.
Output is saved to `brands/<name>/intel/` for each brand.
Used by the Security Auditor to understand the target before scanning.

## Invocation

```bash
cd F:\Notes\Second_Brain\00_System\00_Command_Center\Tools&Agents\Opencode_Agents\mothra-harnesses\output\business-intel-harness
python pipeline.py <url> --capterra <capterra_url> --output <output_dir>
```

## Dependencies

- Python 3.11+
- Node.js + stackmd (`npm install -g stackmd`)
- Playwright (`pip install playwright && playwright install chromium`)
- pywebcopy (`pip install pywebcopy`)
