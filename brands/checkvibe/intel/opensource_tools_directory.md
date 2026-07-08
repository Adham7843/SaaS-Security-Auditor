# OPEN-SOURCE TOOLS DIRECTORY — Replicate CheckVibe

**Purpose:** Complete directory of every open-source tool you need to build a CheckVibe clone. Organized by feature pillar.

**Date:** July 8, 2026

---

## TABLE OF CONTENTS

1. AI-Powered Pentesting (Strix & alternatives)
2. Secret / API Key Detection
3. SQL Injection & XSS Scanners
4. HTTP Security Headers & SSL/TLS
5. CORS & Security Misconfigurations
6. Full-Suite Security Scanners (DAST)
7. SEO Scanners
8. AEO (Answer Engine Optimization) Scanners
9. Performance Monitoring (Core Web Vitals)
10. Accessibility (WCAG) Scanners
11. Email Security (SPF/DKIM/DMARC)
12. Domain & DNS Monitoring
13. Uptime Monitoring & Status Pages
14. MCP Servers (Model Context Protocol)
15. Vulnerability Databases (CVE/NVD)
16. Build Your Stack: Recommended Combinations

---

## 1. AI-POWERED PENTESTING

The heavy hitters. These tools use AI agents to find and validate vulnerabilities.

### ⭐ Strix (THE BEST — 38k+ stars)
The one you mentioned. This is your core scanner engine.

| Detail | Value |
|--------|-------|
| **GitHub** | https://github.com/usestrix/strix |
| **Stars** | 38,349 |
| **Language** | Python |
| **License** | Apache 2.0 |
| **Last Release** | v1.0.4 (June 2026) |
| **What It Does** | Autonomous AI penetration testing agents. Runs your code dynamically, finds vulnerabilities, validates with proof-of-concepts. Full OWASP Top 10 coverage. |
| **Key Features** | Multi-agent orchestration, real exploit validation, auto-fix & reporting, CI/CD integration, browser automation, HTTP proxy, terminal + Python runtime |
| **Install** | `curl -sSL https://strix.ai/install | bash` |
| **Use For** | THE core scanner — SQLi, XSS, SSRF, IDOR, auth bypass, command injection, everything |

### Other AI Pentesting Tools

| Tool | GitHub | Stars | Language | Notes |
|------|--------|-------|----------|-------|
| **Magnus** | https://github.com/carolinacherry/magnus | 5 | TypeScript | Self-hosted, 5-phase autonomous scan, LLM-powered, PDF reports, MCP-friendly |
| **Xalgorix** | https://github.com/xalgorix3-dotcom/xalgorix | 0 | Go | 70+ tools auto-installed, Web UI, PDF reports, any LLM |
| **Sentinel** | https://github.com/EKasuti/sentinel | 0 | Python/TS | 10 specialized AI agents, Gemini-powered, Supabase backend |
| **CyberShield** | https://github.com/minidu-lab/cybershield-oss | 0 | Python | Claude-powered, XSS/SQLi/CSRF/Auth/API keys, security tutor |
| **Vibe-Audit** | https://github.com/vipulawl/vibe-audit | 0 | Python | Specifically for AI-built apps. Scored HTML report, fix prompts for Cursor/Claude |

---

## 2. SECRET / API KEY DETECTION

Find exposed keys in JS bundles, source maps, and responses.

| Tool | GitHub | Stars | Language | What It Detects | Best For |
|------|--------|-------|----------|----------------|----------|
| **KeyLeak** | https://github.com/Amal-David/keyleak-detector | 0 | Python | API keys, BaaS misconfigs (Supabase/Firebase RLS), JWT analysis, Chrome extension | Runtime key detection with active validation. Probes Supabase RLS in real-time. |
| **SecretSifter** | https://github.com/secretsifter/secretsifter-desktop | 0 | C# | 160+ detection rules, MITM proxy, Playwright crawler, HAR import, MCP server | Desktop app. Burp-free secret scanning. MCP + REST API server built-in. |
| **Termite Recon** | https://github.com/muh-syaipullah/termite-recon | 0 | JS | Chrome extension, 70+ patterns, AI analysis, JSON deep scan | Browser extension for real-time scanning while browsing |
| **KeyFinder** | https://github.com/momenbasel/keyFinder | 0 | JS | Browser extension, 80+ patterns, zero config, 10 attack surfaces | Passive scanning while browsing |
| **Secret Detector** | https://github.com/haxshadow/secret_detector | 0 | Python | 100+ regex patterns, git history scanning, subdomain discovery, multi-threaded | Large-scale web reconnaissance |
| **Onam Security Scanner** | https://github.com/onamfc/security-scanner | 0 | Python | 50+ secret patterns + 30 SAST patterns, SARIF output | CLI + CI/CD integration |
| **CyberMat Shield** | https://github.com/Martysunshine/cybermat-shield | 0 | JS/TS | 66 detectors, OWASP Top 10:2025, VS Code extension, local-first | Local-first, privacy-focused. Runs entirely on your machine. |

---

## 3. SQL INJECTION & XSS SCANNERS

Dedicated injection testing tools.

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **sqlmap** | https://github.com/sqlmapproject/sqlmap | 32k+ | Python | Automatic SQL injection and database takeover tool |
| **Dalfox** | https://github.com/hahwul/dalfox | 3.6k+ | Go | Parameter analysis and XSS scanner, fast, open-source |
| **Nuclei** | https://github.com/projectdiscovery/nuclei | 22k+ | Go | Template-based vulnerability scanning. 8000+ templates for CVEs, misconfigs, exposures |

---

## 4. HTTP SECURITY HEADERS & SSL/TLS

| Tool | GitHub | Stars | Language | What It Checks |
|------|--------|-------|----------|---------------|
| **SSLyze** | https://github.com/nabla-c0d3/sslyze | 3.4k+ | Python | SSL/TLS configuration scanner — protocols, ciphers, certificates |
| **testssl.sh** | https://github.com/drwetter/testssl.sh | 8k+ | Shell | Comprehensive TLS testing — everything |
| **Recon-Web** | https://github.com/BrunoAFK/recon-web | 0 | TypeScript | 39 checks across security, DNS, performance, tech stack. SSL grade A-F, HSTS, headers, WAF detection, blocklists, VirusTotal. Self-hosted. |
| **HARIS** | https://github.com/calghar/HARIS | 0 | Python | 7 security headers, cookie flags, TLS, CORS, sensitive paths, info disclosure. Orchestrates Wapiti, SSLyze, Nmap, Nikto, Nuclei. |

---

## 5. CORS & SECURITY MISCONFIGURATIONS

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **Corsy** | https://github.com/s0md3v/Corsy | 1k+ | Python | CORS misconfiguration scanner |
| **Nuclei (templates)** | https://github.com/projectdiscovery/nuclei | 22k+ | Go | Has templates for CORS misconfigs, exposed panels, default credentials |

---

## 6. FULL-SUITE SECURITY SCANNERS (DAST)

Complete web app scanners that do it all.

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **DAST Scanner** | https://github.com/Krishcalin/Dynamic-Application-Security-Testing | 0 | Python | OWASP Top 10 scanner. SQLi (error/time/boolean), XSS, SSRF, LFI, XXE, headers, CORS, JWT, WAF detection. Auth support. |
| **VulnHawk** | https://github.com/SakshamSrivastava92110/VulnHawk | 0 | Python | Full OWASP Top 10 scanner. ML severity, CVE enrichment via NVD, WebSocket dashboard, PDF reports, MITRE ATT&CK. |
| **VulnScope** | https://github.com/Suman99pro/vulnscope | 0 | HTML/JS | Single-file HTML app. CVE lookup (269K+), HTTP headers, TLS/SSL, tech fingerprint, DNS security, cookies, CORS. Zero-dependency. |
| **ShakerScan** | https://github.com/andriyze/shakerscan | 0 | Python | DAST + AI red teaming. Drives via AI agent. DNS, TLS, headers, content discovery, Playwright crawl, subdomain enum. Integrates 10+ tools. |
| **Web Security Scanner** | https://github.com/UnlimitedEdition/security-scanner | 4 | Python | 240+ checks. TLS, headers, DNS, cookies, JS, APIs, CMS, GDPR, SEO, performance, accessibility. FastAPI, Docker, Hugging Face Spaces. |

---

## 7. SEO SCANNERS

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **Unlighthouse** | https://github.com/harlan-zw/unlighthouse | 4,554 | JS/TS | Lighthouse for every page. Auto-discovers URLs, parallel crawl, unified report. SEO insights, titles, meta, share images. |
| **Site Audit SEO** | https://github.com/viasite/site-audit-seo | 290 | JavaScript | Crawl entire site, Lighthouse every page, output to console/json/csv/xlsx. Public reports. |
| **SEO Analyzer** | https://github.com/ihuzaifashoukat/seo-analyzer | 0 | Python | Full site audit. On-page, technical, content analysis. LLM/AI directives (llms.txt/ai.txt). PSI/CrUX. Duplicate detection. Link graph. CLI + Flask API. |
| **Lighthouse** | https://github.com/GoogleChrome/lighthouse | 28k+ | JS | Google's own. Performance, SEO, accessibility, best practices. The industry standard. |
| **SEO Audits Toolkit** | https://github.com/StanGirard/seo-audits-toolkit | 0 | Python | Lighthouse scores, SERP rank, keywords, headers/links/images, sitemap, summarizer, security audit. Flask + auth + RBAC. |
| **Universal SEO Audit** | https://github.com/pbpyrojust/universal-seo-audit | 0 | JS | Technical SEO for staging/auth sites. Agentic Lighthouse scoring, WebMCP protocol, llms.txt, accessibility-tree, layout stability. Branded PDF reports. |

---

## 8. AEO (ANSWER ENGINE OPTIMIZATION) SCANNERS

Brand new category — CheckVibe's biggest differentiator. Multiple open-source options now exist.

### ⭐ AEOrank (THE BEST FOR CHECKVIBE CLONE)
Closest to what CheckVibe's AEO scanner does. 36 deterministic checks.

| Detail | Value |
|--------|-------|
| **GitHub** | https://github.com/vinpatel/aeorank |
| **Stars** | 11 |
| **Language** | TypeScript |
| **License** | MIT |
| **What It Does** | Scores AI visibility 0-100 across 36 criteria. Generates 9 AI-readable files (llms.txt, ai.txt, CLAUDE.md, schema.json, etc.). CLI + GitHub App + 13 framework plugins. |
| **Why Use It** | Only open-source CLI for AEO. Generates the actual files AI engines need. Works in CI. |
| **Install** | `npx aeorank-cli scan https://yoursite.com` |

### All AEO Tools

| Tool | GitHub | Stars | Lang | What It Does |
|------|--------|-------|------|-------------|
| **AEOrank** | https://github.com/vinpatel/aeorank | 11 | TS | 36 checks, generates 9 files, CLI + GitHub App + 13 plugins |
| **AEO Audit** | https://github.com/Canonry/aeo-audit | 9 | TS | 16 ranking factors, CLI, Claude Code skill (/aeo), Lighthouse optional |
| **AEO Platform** | https://github.com/webappski/aeo-platform | 10 | JS | Measures 4 engines (ChatGPT/Claude/Gemini/Perplexity), 30-mission plan generator |
| **AEO Radar** | https://github.com/hellowalt/aeo-radar | 19 | TS | Daily headless crawl of ChatGPT, brand mention tracking, dark dashboard |
| **AEO Toolkit** | https://github.com/Advance-Labs/aeo-toolkit | 0 | TS | 9-package monorepo. Crawler, HTML parser, schema validator, scoring, MCP, UI components |
| **Mentha** | https://github.com/beenruuu/Mentha | 0 | TS | Full AEO platform. Real browser automation, LLM-as-Judge, knowledge graph, MCP server |
| **AI SEO Platform** | https://github.com/dipakkr/ai-seo-platform | 0 | Python | Tracks ChatGPT/Perplexity/Gemini/Claude/Grok visibility. 50+ queries, 0-100 score. |
| **GetCito** | https://github.com/ai-search-guru/getcito | 128 | TS | World's first open-source AIO/AEO/GEO tool. Multi-engine monitoring, analytics. |
| **AEO Mentions Crawler** | https://github.com/federicodeponte/aeo-mentions-crawler | 12 | TS/Python | Brand mention tracking across LLMs. Keyword research, blog generation with AEO optimization. |

---

## 9. PERFORMANCE MONITORING (CORE WEB VITALS)

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **Lighthouse** | https://github.com/GoogleChrome/lighthouse | 28k+ | JS | The standard. LCP, FID/INP, CLS, and more. |
| **Unlighthouse** | https://github.com/harlan-zw/unlighthouse | 4,554 | JS/TS | Scans every page with Lighthouse. Best for site-wide performance. |
| **Lighthouse Crawler** | https://github.com/anvil-solutions/lighthouse-crawler | 0 | JS | Crawl + Lighthouse each page. Consolidated report. |
| **PageSpeed Insights API** | https://developers.google.com/speed/docs/insights/v5 | — | API | Google's free API for CrUX data and Lighthouse scores |

---

## 10. ACCESSIBILITY (WCAG) SCANNERS

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **axe-core** | https://github.com/dequelabs/axe-core | 6,997 | JS | Industry standard. WCAG 2.0/2.1/2.2 A/AA/AAA. Zero false positives. 57% of WCAG issues automated. 230+ contributors. |
| **Accessio Scan** | https://github.com/The-Pixel-Boys/accessio-scan | 0 | JS | axe-core + Playwright. Single page scan, WCAG violations. MIT. |
| **WCAG Scanner** | https://github.com/cpt-cheezbrgr/wcag-scanner | 0 | JS | Multi-page scanner. axe-core + Playwright, BFS crawl, HTML/JSON reports, CLI + web UI. |
| **WCAG GitHub Action** | https://github.com/sret-farhan2021/WCAG2.1-Scanner-github-action | 0 | JS | GitHub Action. Smart scanning (PR vs full). HTML + JSON reports. |

---

## 11. EMAIL SECURITY (SPF/DKIM/DMARC)

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **dmarcheck** | https://github.com/schmug/dmarcheck | 4 | TS | DMARC/SPF/DKIM/BIMI/MTA-STS. Cloudflare Worker, JSON API, HTML report. Self-hostable. Paid tier $19/mo. |
| **dns-auth-check** | https://github.com/trustyourwebsite/dns-auth-check | 0 | JS | Zero-dependency Node.js tool. SPF/DKIM/DMARC/BIMI/MTA-STS. Grades A+ to F. CI-friendly. |
| **mailauth** | https://github.com/postalsys/mailauth | 0 | JS | Full Node.js library for SPF/DKIM/DMARC/ARC/BIMI/MTA-STS verification and signing |
| **mailvalidator** | https://github.com/NC3-TestingPlatform/mailvalidator | 0 | Python | MX/SPF/DMARC/DKIM/BIMI/TLSRPT/MTA-STS/104 DNSBLs. Letter grades. CLI + library. |

---

## 12. DOMAIN & DNS MONITORING

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **Recon-Web** | https://github.com/BrunoAFK/recon-web | 0 | TS | SSL grade, HSTS, headers, WAF detection, blocklists, VirusTotal, DNS |
| **VulnScope** | https://github.com/Suman99pro/vulnscope | 0 | HTML/JS | CVE lookup (269K+), tech fingerprint, DNS security, subdomain discovery |
| **DonScan** | https://github.com/cysec-don/DonScan | 0 | Python | Full vulnerability platform. Network discovery, fingerprinting, CVE enrichment, TLS, reports. Docker Compose. |

---

## 13. UPTIME MONITORING & STATUS PAGES

| Tool | GitHub | Stars | Language | What It Does |
|------|--------|-------|----------|-------------|
| **Uptime Kuma** | https://github.com/louislam/uptime-kuma | 63k+ | JS | Self-hosted. HTTP(s)/TCP/Ping/DNS/SSL. 90+ notifications. Status page. 2FA. Docker. |
| **Checkmate** | https://github.com/bluewave-labs/checkmate | 10,122 | TS | Uptime + infrastructure monitoring. Status pages, incidents, 4 themes. Docker/Ping/SSL/Port/Game server. 150 contributors. |
| **OpenStatus** | https://github.com/openstatusHQ/openstatus | 0 | TS | Status page + uptime monitoring. Open-source. |
| **Statping-ng** | https://github.com/statping-ng/statping-ng | 1,980 | Go | Status page + monitoring. Multiple DBs. Prometheus exporter. Mobile app. |
| **Uptimepage** | https://github.com/uptimepage/uptimepage | 0 | Rust | HTTP/TCP/DNS/TLS/domain-expiry. Multi-region, incidents, subscribers, MCP server, Terraform provider. |
| **Pong** | https://github.com/FluxNat/pong | 0 | JS | Self-hosted. HTTP(s)/TCP/Ping/DNS/SSL/Websocket/Push. 90+ notifications. Status page. |
| **Status One** | https://github.com/DeForge-Labs/status-one | 0 | JS | Self-hosted. HTTP/keyword/Ping/TCP/DNS/SSL/Push. Status pages, incidents, custom domains. SQLite. |
| **Upptime** | https://github.com/upptime/upptime | 15k+ | JS | GitHub Actions-based. Every 5 min. Issues for incidents. Status page on GitHub Pages. Free. |
| **Uni-Status** | https://github.com/unified-projects/uni-status | 4 | JS | Status monitoring. Uptime checks, status pages, incidents, multi-channel alerting. Docker Compose. |
| **ShadowStatus** | https://github.com/Shadow-Develops/ShadowStatus | 0 | JS | Static status page for GitHub Pages. 10 monitor types. GitHub Issues integration. |

---

## 14. MCP SERVERS (MODEL CONTEXT PROTOCOL)

CheckVibe's secret weapon. Here are open-source MCP tools you can use.

| Tool | GitHub | Description |
|------|--------|-------------|
| **CheckVibe's MCP (study this)** | npm: @checkvibe/mcp-server | 9 tools: run_scan, get_scan_results, list_scans, list_projects, get_project, update_project, dismiss_finding, list_dismissals, restore_finding |
| **MCP SDK** | https://github.com/modelcontextprotocol/typescript-sdk | Official TypeScript SDK for building MCP servers |
| **SecretSifter MCP** | Built into https://github.com/secretsifter/secretsifter-desktop | REST + MCP server built-in. JSON-RPC at /mcp |
| **Mentha MCP** | https://github.com/beenruuu/Mentha | MCP server for AEO. Tools: get_brand_visibility, analyze_sentiment, track_competitors, get_optimization_tips |
| **AEO Toolkit MCP** | https://github.com/Advance-Labs/aeo-toolkit/tree/main/packages/mcp-core | MCP transport helpers for exposing AEO tools to AI agents |

---

## 15. VULNERABILITY DATABASES (CVE/NVD)

| Source | URL | What It Provides |
|--------|-----|-----------------|
| **NIST NVD** | https://nvd.nist.gov/ | 269K+ CVEs. Free API. Package/version lookup. |
| **osv.dev** | https://osv.dev | Open Source Vulnerabilities. Google-backed. |
| **GitHub Advisory DB** | https://github.com/github/advisory-database | CVEs mapped to GitHub repos |
| **Exploit-DB** | https://www.exploit-db.com | Public exploits and PoCs |

---

## 16. BUILD YOUR STACK: RECOMMENDED COMBINATIONS

### Minimum Viable Scanner Stack (Phase 1)

| CheckVibe Feature | Open-Source Tool | Integration Method |
|-------------------|-----------------|-------------------|
| **Security Scanner (core)** | Strix | CLI: `strix --target https://site.com` |
| **Secrets in JS bundles** | KeyLeak | CLI: `keyleak site-scan https://site.com` |
| **HTTP Headers + SSL** | Recon-Web | Docker, API |
| **SEO** | Unlighthouse | npx CLI: `npx unlighthouse --site https://site.com` |
| **AEO** | AEOrank | npx CLI: `npx aeorank-cli scan https://site.com` |
| **Performance** | Lighthouse (via Unlighthouse) | Built into Unlighthouse |
| **Accessibility** | axe-core + Playwright | Programmatic via Node.js |
| **Email Security** | dns-auth-check | npm library: `auditDNSAuth()` |
| **Uptime Monitoring** | Uptime Kuma | Docker, API |
| **Status Page** | OpenStatus or Checkmate | Docker, API |
| **CVE Intelligence** | NIST NVD API | REST API |
| **MCP Server** | MCP SDK + your wrapper | TypeScript SDK |

### Architecture Diagram

```
User submits URL
    |
    v
Your Next.js Frontend (Vercel)
    |
    v
Your Backend API (Node.js/TypeScript)
    |
    ├── Strix CLI ──────────── AI pentesting (SQLi, XSS, SSRF, etc.)
    ├── KeyLeak ────────────── Secret detection in bundles
    ├── Recon-Web API ──────── Headers, SSL, DNS, WAF
    ├── Unlighthouse ───────── SEO + Performance (Lighthouse)
    ├── AEOrank CLI ────────── AI visibility (36 checks)
    ├── axe-core ───────────── WCAG accessibility
    ├── dns-auth-check ─────── SPF/DKIM/DMARC
    ├── Uptime Kuma API ────── Uptime monitoring
    └── NIST NVD API ───────── CVE enrichment
    |
    v
Supabase (Database + Auth + Storage)
    |
    v
AI Fix Prompts (Gemini API / Claude API) ← Generate remediation
    |
    v
MCP Server (your wrapper) ← Expose 9 tools for Cursor/Claude
    |
    v
Stripe ← Payment processing
Resend ← Email notifications
PostHog ← Analytics
Sentry ← Error tracking
```

### Key Insights

1. **Strix is your foundation** — it's the most starred (38k+) and most capable open-source security scanner. Use it as the engine, wrap it in your own API.

2. **AEOrank fills CheckVibe's biggest differentiator** — AI visibility. It's the only open-source AEO scanner with 36 deterministic checks. Use it as-is.

3. **MCP is how you win** — Build your own MCP server wrapping all these tools. Follow CheckVibe's pattern: 9 tools (run_scan, get_results, dismiss, etc.)

4. **The paywall is the business** — Show issue counts, lock details. This is the 3x conversion lever. All open-source tools give you full output — you gate it.

5. **Your total infra cost** — ~$200/mo (same as CheckVibe). All tools above are free/self-hosted.

---

*Directory compiled by Business Cloner Agent • SaaS Security Auditor*
*Date: July 8, 2026*
