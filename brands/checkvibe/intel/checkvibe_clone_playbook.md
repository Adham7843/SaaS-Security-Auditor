# HOW TO CLONE CHECKVIBE — Complete Business Playbook

**Cloned:** July 8, 2026
**Source:** https://checkvibe.dev
**Original Founder Story:** r/StartupSoloFounder — $7k MRR after 3 months, 2-person team
**Author:** Business Cloner Agent

---

## TABLE OF CONTENTS

1. Executive Summary
2. The Opportunity: Why This Works
3. Product Architecture: What to Build
4. Tech Stack Blueprint: Exact Infrastructure
5. The Scanner Engine: How It Works
6. Pricing & Monetization Strategy
7. The Paywall Secret (3x Conversion)
8. Go-to-Market: Exact Marketing Playbook
9. Content Engine: Blog & SEO Strategy
10. MCP Server: The Distribution Moonshot
11. Competitive Positioning
12. Operational Runway & Team
13. Growth Roadmap (Months 1-12)
14. Risks & Mitigations

---

## 1. EXECUTIVE SUMMARY

CheckVibe is a 2-person Swiss SaaS that built a security + SEO + AEO scanner targeted specifically at the "vibe coding" market — developers who build apps with AI tools (Cursor, Copilot, Lovable, Bolt, v0, Replit) and ship fast without security expertise.

**Key metrics from the founder (3 months in):**
- $7k MRR
- 2-person team
- ~5,000 registered developers
- TikTok slideshows generating millions of views
- Cold outreach (scan-first, DM-second) converting consistently
- Free tier → paid conversion tripled by showing issue count instead of blurring everything

**Why clone this?**
- New market category ("vibe coding security") with no dominant player
- 2-person team proves it's buildable alone or as a duo
- Clear product-led growth (PLG) motion
- MCP server creates distribution moat inside AI IDEs
- Founder publicly shared the exact playbook

---

## 2. THE OPPORTUNITY: WHY THIS WORKS

### The Market Shift

AI coding tools (Cursor, GitHub Copilot, Lovable, Bolt, v0, Replit, Windsurf, Claude Code, Codex) are exploding. Developers now ship production apps in hours, not weeks. But these tools routinely produce:

- Exposed API keys in client bundles (Stripe, OpenAI, Supabase)
- Open Firebase/Supabase database rules (RLS misconfigs)
- Missing HTTP security headers (CSP, HSTS, X-Frame-Options)
- SQL injection and XSS vulnerabilities
- Poor SEO and zero AEO (Answer Engine Optimization — invisible to ChatGPT/Claude)
- Expired domains, broken SSL, missing DMARC

### Total Addressable Market

- **Direct:** All "vibe coders" using AI tools — estimated 5-15M developers globally using AI coding assistants
- **Adjacent:** Indie hackers, agency developers, startup CTOs who need quick security audits
- **Future:** Any website owner who wants a "check engine light" for their web presence

### Why Now

1. "Vibe coding" is the hottest trend in developer tools (2025-2026)
2. AEO (Answer Engine Optimization) is a brand-new category CheckVibe essentially invented
3. MCP (Model Context Protocol) is growing fast — first-mover advantage for security scanning inside AI IDEs
4. No incumbent has claimed this specific niche

---

## 3. PRODUCT ARCHITECTURE: WHAT TO BUILD

### Core Product — Security Scanner

The flagship product. Users paste a URL, you scan it, you show them what's wrong.

**Minimum Viable Scanner (Phase 1):**

| Check Category | Specific Checks | Priority |
|---------------|----------------|----------|
| **Exposed Secrets** | Stripe keys, OpenAI API keys, Supabase anon/service-role keys, Firebase configs, AWS keys, JWT tokens in client bundles | P0 |
| **SQL Injection** | Reflected SQLi probes on form inputs, URL params, API endpoints | P0 |
| **XSS** | Reflected, stored, DOM-based XSS vectors | P0 |
| **HTTP Headers** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy | P0 |
| **SSL/TLS** | Certificate validity, protocol versions (TLS 1.2/1.3), cipher strength, HSTS preload | P0 |
| **BaaS Misconfigs** | Supabase RLS policy check, Firebase rules check, Clerk config check | P0 |
| **Cookies** | Secure flag, HttpOnly flag, SameSite, expiry | P1 |
| **CORS** | Permissive CORS policies, wildcard origins | P1 |

**Phase 2 — Expanded Checks:**

| Check Category | Specific Checks | Priority |
|---------------|----------------|----------|
| **SEO (68 checks)** | Indexability, robots.txt, canonicals, sitemaps, metadata, structured data, Core Web Vitals, internal linking | P1 |
| **AEO (46 checks)** | AI crawler access (GPTBot, ClaudeBot, PerplexityBot), JS-free extractability, llms.txt, schema.org depth, trust signals | P1 |
| **Performance** | Lab + field Core Web Vitals (CrUX), LCP, FID/INP, CLS | P1 |
| **Accessibility** | WCAG 2.2 — contrast, alt text, landmarks, keyboard traps, ARIA | P2 |
| **Email** | SPF, DKIM, DMARC, blocklist presence | P2 |
| **Domain** | Expiry, DNS hygiene, nameserver health, TLS cert rotation | P2 |
| **Compliance** | Cookie consent presence, privacy policy, GDPR signals, CCPA | P2 |
| **Uptime Monitoring** | 60-second pings, public status page, incident timeline, 90-day history | P1 |

### The AI Fix Prompt System

This is a KEY differentiator. Every finding ships with a ready-to-use remediation prompt.

Example structure:
```
Fix: [Vulnerability Name] on [endpoint/path]

The [problem description] means [impact]. 

To fix: [exact code/config change needed]
Handler: [file path if GitHub connected]

→ Paste into Claude, Cursor, or Windsurf
```

Format: Copy-paste ready. Engineered specifically for Claude Code, Cursor, and Windsurf.

### The Paywall (Critical Design Choice)

**Do NOT blur all results.** This was the founder's biggest lesson:

- ❌ **Old approach:** Blur all findings → barely any conversions
- ✅ **New approach:** Show the COUNT of critical/high/medium/low issues, lock the DETAILS → 3x conversion

The UI should show:
- "4 Critical | 7 High | 12 Medium | 3 Low" clearly
- Each category expandable to a teaser
- Clicking any finding → "Upgrade to Starter (£24/mo) to see full details and AI fix prompts"

### The Live Threat Detection

A secondary feature that differentiates from free tools:
- Real-time attack feed showing credential stuffing, scraping, prompt-injection probes
- Attacker IP intelligence
- Email alerts on new threats

### The Public Uptime Status Page

Surprisingly powerful for a security scanner:
- "status.yourcompany.com" — free for every paid project
- Checks every 60 seconds
- Shareable public page (great for customer trust)
- Incident timeline & 90-day history
- Uptime percentages per endpoint

---

## 4. TECH STACK BLUEPRINT: EXACT INFRASTRUCTURE

### Confirmed Stack (from Terms of Service, Subprocessors page, npm registry, and site analysis)

| Layer | Technology | Purpose | Estimated Monthly Cost |
|-------|-----------|---------|----------------------|
| **Frontend** | Next.js (React) | Marketing site + dashboard | — |
| **Hosting** | Vercel | Web serving, edge functions, CDN | $20-200/mo |
| **CDN/Edge** | Cloudflare | DNS, DDoS protection, caching | $0-200/mo |
| **Database** | Supabase (PostgreSQL) | Auth, primary DB, file storage | $0-25/mo (start) |
| **Auth** | Supabase Auth | User authentication | Included above |
| **Payments** | Stripe | Subscription billing, invoicing | 2.9% + $0.30/transaction |
| **Email** | Resend | Transactional emails, notifications | $0-100/mo |
| **Analytics** | PostHog | Product analytics (self-hosted or cloud) | $0-50/mo |
| **Error Monitoring** | Sentry | Error tracking & alerting | $0-50/mo |
| **AI Analysis** | Google Gemini API | AI fix prompt generation, finding analysis | $5-50/mo |
| **Reputation Lookup** | Google Safe Browsing | Malicious URL detection | Free |
| **CVE Database** | NIST NVD | CVE lookups for dependency scanning | Free |
| **Source Control** | GitHub API | Repo scanning (opt-in) | Free |
| **Build System** | TypeScript + tsc | MCP server build | Free |
| **MCP Package** | npm (@checkvibe/mcp-server) | MCP server distribution | Free |

### MCP Server Architecture

```
npm package: @checkvibe/mcp-server
Dependencies:
  - @modelcontextprotocol/sdk ^1.29.0
  - zod ^4.4.3
  
Dev Dependencies:
  - @types/node ^25.9.1
  - typescript ^6.0.3

Node requirement: >=18
```

The MCP server exposes 9 tools:
1. run_scan — Trigger a scan
2. get_scan_results — Retrieve findings
3. list_scans — List scan history
4. list_projects — List user projects
5. get_project — Get project details
6. update_project — Update project settings
7. dismiss_finding — Mark false positive
8. list_dismissals — View dismissed findings
9. restore_finding — Restore dismissed finding

### Scanner Engine Design (Inferred)

The scanner must:
1. **Crawl the target URL** — Discover pages, subdomains, SPA routes, API endpoints
2. **Run 42+ parallel scanners** against each discovered endpoint
3. **Be browser-aware** — Render JavaScript (not just curl), follow redirects
4. **Be source-map-aware** — Parse source maps to find leaked keys in bundles
5. **Understand frameworks** — Detect Next.js, Vite, Remix, SvelteKit routes
6. **Be BaaS-aware** — Know the difference between Supabase anon key (low risk) and service-role key (critical)
7. **Score findings** — Rank on exploitability, not just presence
8. **Generate fix prompts** — AI-generated remediation with exact file paths if GitHub connected

---

## 5. THE SCANNER ENGINE: HOW IT WORKS

### Step-by-Step Scan Flow

1. **User submits URL** → POST to /api/scan with { url: "https://example.com" }
2. **Crawl phase** (5-10 seconds):
   - Fetch homepage
   - Parse sitemap.xml, robots.txt
   - Discover subdomains via DNS/CRT.sh
   - Crawl internal links and SPA routes
   - Identify tech stack (Next.js, Vite, etc.)
3. **Scan phase** (15-25 seconds):
   - Run all 42+ scanners in parallel against all discovered endpoints
   - Each scanner is an independent module
   - Results stream back progressively (UI shows live progress)
4. **Analysis phase** (2-5 seconds):
   - Deduplicate findings
   - Score by severity (Critical/High/Medium/Low)
   - Generate AI fix prompts using Gemini API
   - Log results to Supabase
5. **Report phase**:
   - Show severity overview (Critical: N, High: N, etc.)
   - Paid users see full details + fix prompts
   - Option to export PDF or generate shareable dashboard link

### Scanner Modules to Build

Here are the scanner modules in priority order. Build these first:

| Module | What It Checks | How It Works |
|--------|---------------|--------------|
| **secret-scanner** | Exposed API keys in JS bundles | Parse HTML for script tags, fetch JS files, regex for known key patterns (sk-..., pk_..., rk_..., etc.) |
| **sourcemap-scanner** | Keys in source maps | Check for .map files, parse them, scan for secrets |
| **sqli-scanner** | SQL injection points | Try SQLi payloads on params, forms, API endpoints |
| **xss-scanner** | XSS vectors | Try XSS payloads on inputs, URL params |
| **header-scanner** | HTTP security headers | Analyze response headers against OWASP checklist |
| **ssl-scanner** | TLS cert and config | Check cert issuer, expiry, protocol versions, cipher strength |
| **baas-scanner** | Supabase/Firebase rules | Check if Supabase anon key is actually anon vs service-role; test Firebase rules endpoints |
| **cookie-scanner** | Cookie security | Check Secure, HttpOnly, SameSite flags |
| **cors-scanner** | CORS policies | Test for wildcard origins, reflected origins |
| **dns-scanner** | DNS hygiene | Check A/AAAA records, nameservers, CAA, SPF |
| **seo-scanner** | 68 SEO checks | Check indexability, metadata, structured data, Core Web Vitals |
| **aeo-scanner** | 46 AI visibility checks | Check robots.txt for GPTBot/ClaudeBot, test JS-free rendering, check llms.txt |
| **uptime-monitor** | Site availability | HTTP GET every 60s, track response times |

---

## 6. PRICING & MONETIZATION STRATEGY

### Exact Pricing to Replicate

| Tier | Monthly | Annual (Save 30%) | Scans | Projects | Key Features |
|------|---------|-------------------|-------|----------|-------------|
| **Free** | $0 | $0 | 4/mo | 1 | Severity overview only, no fix prompts |
| **Starter** | $24 (£24) | $199/yr (£199) | 30/mo | 1 | Full findings, fix prompts, PDF, API, MCP |
| **Pro** | $39 (£39) | $329/yr (£329) | 155/mo | 5 | Daily monitoring, live threats, priority support |
| **Max** | $59 (£59) | $496/yr (£496) | Unlimited | 50 | Custom monitoring, dedicated support |

### Pricing Psychology

Key insights from CheckVibe:
- **Free is FOREVER**, not a trial — builds trust, drives word-of-mouth
- Paywall shows **issue counts**, not blur — curiosity drives conversion
- **GBP pricing** is interesting: positions as European/premium
- Annual billing at 30% discount is standard but effective
- **"Only pay if you have issues"** — brilliant positioning (reduces friction)

### Expansion Revenue Opportunities

Planned features that justify upgrades:
- More scans/month (scarcity drives upgrades)
- More projects (teams need this)
- Live threat detection (compelling security feature)
- AI fix prompts (the core value unlock)
- MCP server access (AI-native developers NEED this)
- PDF exports (agencies need this for client delivery)

---

## 7. THE PAYWALL SECRET (3x Conversion)

This is the single most important product lesson from the founder.

### The Wrong Way (What CheckVibe Initially Did)

```
┌─────────────────────────────────────┐
│  Scan Results for example.com       │
│                                     │
│  🔒 [All results blurred]           │
│  🔒 [All results blurred]           │
│  🔒 [All results blurred]           │
│                                     │
│  Upgrade to see results → $24/mo    │
└─────────────────────────────────────┘
```

**Problem:** User has NO idea what they're paying for. Curiosity isn't triggered. Conversion barely registers.

### The Right Way (What They Switched To)

```
┌─────────────────────────────────────┐
│  Scan Results for example.com       │
│                                     │
│  🔴 4 Critical    🟠 7 High         │
│  🟡 12 Medium     🔵 3 Low          │
│                                     │
│  [Critical] ▼                       │
│  ├─ 🔴 Exposed Supabase service-    │
│  │   role key in client bundle      │
│  │   📍 /_next/static/chunks/...js  │
│  │   [ Upgrade to see fix → ]       │
│  │                                  │
│  ├─ 🔴 SQL Injection on /api/users  │
│  │   📍 Parameter: id               │
│  │   [ Upgrade to see fix → ]       │
│  │                                  │
│  ├─ 🔴 Missing CSP header           │
│  │   📍 All pages                   │
│  │   [ Upgrade to see fix → ]       │
│  │                                  │
│  └─ 🔴 Open Firebase database      │
│      📍 /firebase-config.json      │
│      [ Upgrade to see fix → ]      │
│                                     │
│  🔓 Unlock full details & AI fixes  │
│  → Just £17/mo (annual)             │
└─────────────────────────────────────┘
```

**Why it works:**
1. Shows the user EXACTLY what's broken (creates urgency)
2. Shows the COUNT (4 criticals! That's alarming!)
3. Shows the LOCATION (they can verify it's real)
4. BLOCKS the fix (they can't fix it without paying)
5. NOW they know what they're paying for — peace of mind

### Mobile Activation Lesson

- ❌ Too many onboarding steps on mobile → massive drop-off
- ✅ Cut 2 steps → gap closed overnight
- Rule: Minimize friction on mobile. Desktop users tolerate more steps. Mobile users bounce.

---

## 8. GO-TO-MARKET: EXACT MARKETING PLAYBOOK

This is pulled directly from the founder's playbook + analysis of their site.

### Channel 1: TikTok Slideshows (THEIR BIGGEST WIN)

**Format:**
- 5 slides
- Aesthetic Pinterest-style backgrounds (vintage, muted tones, or tech-noir)
- Tool names overlaid in clean typography
- NO branding on the account (makes it feel like organic discovery)
- 15 minutes to produce

**Example sequence:**
1. Slide 1: "Your Cursor app probably has 4 critical security issues"
2. Slide 2: "Cursor writes code fast — but it also writes bad security"
3. Slide 3: "Hardcoded API keys in client bundles? Super common"
4. Slide 4: "Open database rules? That's what we see every day"
5. Slide 5: "Paste your URL → get a free report in 30 seconds"

**Results:** One video hit 1M views. Still sending signups weeks later.

**Why it works:**
- No promotion of the brand (just the problem)
- Relatable to the target audience
- Aesthetic visuals stop the scroll
- 15 minutes to make = compounding content machine

### Channel 2: Cold Outreach (Scan-First, DM-Second)

**The method:**
1. Find indie hackers / agency developers on X/Twitter, LinkedIn, or Reddit
2. Scan their website/app with your tool
3. DM them THE FINDINGS (not a pitch)
4. Generic pitch = ignored. Useful findings = replies every time.

**Example DM:**
"Hey — I was looking at your site and noticed your Supabase service-role key is exposed in your JS bundle. Just a heads up. If you want to check for other issues, I use [your tool] — happy to run a full scan."

**Why it works:**
- You're providing value before asking for anything
- The finding is real and actionable
- It demonstrates your tool works

### Channel 3: Content Marketing (Blog + SEO)

CheckVibe runs an aggressive blog with 20+ detailed technical posts. This drives organic traffic from developers searching for:

- "How to check if my website is secure"
- "Supabase security checklist"
- "Cursor security audit"
- "What is AEO"
- "How to rank in ChatGPT"
- "Firebase security rules guide"
- "JWT security best practices"
- "SaaS security checklist before launch"

**Topic strategy:** Create the definitive guide for every security topic relevant to AI-built apps. These rank well because they're genuinely useful and technically deep.

### Channel 4: Product Comparisons

CheckVibe has dedicated comparison pages:
- /compare — compares with other scanners
- /alternatives — "CheckVibe alternatives"
- Comparison blog posts (vs ZeriFlow, Snyk, OWASP ZAP, Comply Code)

**Strategy:** Own the comparison SEO traffic. Be the page developers find when they search "[competitor] vs checkvibe".

### Channel 5: Affiliate Program

Referral/affiliate program listed in the footer. Typical SaaS model.

### Channel 6: MCP Ecosystem Distribution

This is the MOONSHOT channel. By building an MCP server that works with Cursor, Claude Desktop, Windsurf, and Codex CLI:
- Every user who configures MCP gets CheckVibe baked into their workflow
- Users discover CheckVibe from within their AI coding tool
- It's a distribution moat — once configured, it stays

---

## 9. CONTENT ENGINE: BLOG & SEO STRATEGY

### Content Pillars

| Pillar | Topics | Search Volume Potential |
|--------|--------|----------------------|
| **Vibe Coding Security** | Cursor security, AI-generated code vulnerabilities, vibe-coding risks | Medium (growing fast) |
| **AEO (Answer Engine Optimization)** | What is AEO, ChatGPT citation, AI visibility, llms.txt, GPTBot | Low (new category — first-mover) |
| **Framework Security** | Next.js security, Supabase RLS, Firebase rules, JWT, CSRF | High (stable) |
| **SEO for Developers** | Core Web Vitals, structured data, SPAs and SEO | High (stable) |
| **Security Fundamentals** | SSL/TLS guide, DMARC guide, uptime monitoring, headers | High (stable) |

### Content Format

Every post follows a pattern:
1. **Problem statement** — what goes wrong
2. **Why it matters** — real-world impact
3. **Step-by-step fix** — exact code changes
4. **Automation** — how CheckVibe catches it
5. **CTA** — "Scan your site free →"

### Publishing Cadence

- CheckVibe publishes 2-3 posts per week
- Posts are 5-15 min read (deep technical)
- Mix of long-form guides and shorter focused pieces

### SEO Quick Wins

| Query | Landing Page Strategy |
|-------|----------------------|
| "exposed API key scanner" | Free dedicated tool page |
| "Supabase RLS checker" | Free dedicated tool page |
| "Lovable security scanner" | Free dedicated tool page |
| "website security scanner" | Homepage + product page |
| "check if website is secure" | Blog guide + free scan CTA |
| "what is AEO" | Blog post (category-creator) |
| "Cursor security audit" | Blog post + product page |

---

## 10. MCP SERVER: THE DISTRIBUTION MOONSHOT

### What It Is

The MCP (Model Context Protocol) server lets users run CheckVibe scans directly from within their AI coding environment:

```json
{
  "mcpServers": {
    "checkvibe": {
      "command": "npx",
      "args": ["-y", "@checkvibe/mcp"],
      "env": { "CHECKVIBE_API_KEY": "cv_live_..." }
    }
  }
}
```

### Why It's a Moat

1. **Integration depth** — Once a developer sets this up, scanning is a natural part of their workflow
2. **Distribution inside AI tools** — Cursor, Claude Desktop, Windsurf, Codex CLI all support MCP
3. **Ecosystem effects** — MCP is growing; CheckVibe is the first security scanner on the protocol
4. **Switching cost** — Moving to a competitor means re-configuring MCP

### Compatible Clients

- Claude Desktop
- Cursor
- Continue
- Windsurf
- Codex CLI
- Any MCP-compatible client

### The 9 MCP Tools to Build

1. `run_scan` — Trigger a scan from the AI chat
2. `get_scan_results` — Pull structured results
3. `list_scans` — View recent scans
4. `list_projects` — See all projects
5. `get_project` — Get project details
6. `update_project` — Modify project settings
7. `dismiss_finding` — Mark false positives
8. `list_dismissals` — Review dismissed findings
9. `restore_finding` — Undo a dismissal

---

## 11. COMPETITIVE POSITIONING

### Competitive Landscape

| Competitor | Price | Strengths | Weaknesses vs CheckVibe |
|-----------|-------|-----------|------------------------|
| **ZeriFlow** | $9.99/mo | Cheaper, 80+ checks, CI/CD integration | No MCP server, no AEO, no BaaS-specific checks |
| **Snyk** | $25/mo+ | Code-level scanning, dependency CVEs, enterprise trust | Expensive, not vibe-coder focused, heavy setup |
| **OWASP ZAP** | Free | Comprehensive, open source, active exploitation | Steep learning curve, no AI features, no managed service |
| **Comply Code** | $29/mo | Legal/IP compliance, ADA scanning | Different category (legal vs security) |
| **CheckYourVibe** | Unknown | Similar positioning, same niche | Smaller, less established, no MCP |

### CheckVibe's Differentiators

1. **BaaS-aware scanning** — Understands Supabase, Firebase, Clerk specifics (not just generic scanner)
2. **MCP server** — Scan from inside Cursor, Claude, Windsurf
3. **AI-native fix prompts** — Copy-paste remediation that works with AI coding tools
4. **Combined Security + SEO + AEO** — One scan for all three
5. **AEO category creation** — First-mover in AI visibility scanning

### Your Positioning If You Clone

Focus on ONE angle:
- **If you can beat on price:** Undercut at $9.99/mo like ZeriFlow
- **If you can beat on MCP:** Make the MCP integration even deeper
- **If you can beat on features:** Focus on a specific framework (e.g., ONLY Supabase scanning)
- **If you can beat on content:** Out-blog them (they're small, you can win on SEO)

---

## 12. OPERATIONAL RUNWAY & TEAM

### Current CheckVibe Team

- **Size:** 2 people (per founder's Reddit post)
- **Roles inferred:**
  - Person A: Product + Engineering (building the scanner, MCP server, infrastructure)
  - Person B: Marketing + Design (TikTok slideshows, content, cold outreach, UI)

### Estimated Monthly Costs to Operate

| Item | Estimated Cost |
|------|---------------|
| Vercel (hosting) | $50-200/mo |
| Supabase (DB + auth) | $0-25/mo |
| Stripe (processing) | ~2.9% + $0.30/txn (~$200/mo at $7k) |
| Resend (email) | $0-50/mo |
| PostHog (analytics) | $0-50/mo |
| Sentry (errors) | $0-50/mo |
| Google Gemini API | $5-50/mo |
| Cloudflare | $0-200/mo |
| Domain + misc | $20/mo |
| **Total** | **~$75-625/mo (likely ~$200/mo at their stage)** |

At $7k MRR and ~$200/mo costs, they're running at ~97% margin for the founders. Insanely efficient.

### What You Need to Build This

**Person A (Technical — you):**
- TypeScript/Node.js expertise
- Next.js (React) for frontend
- Experience with web security (OWASP Top 10, common vulns)
- Understanding of AI coding tools (Cursor, Claude)
- Familiarity with Supabase

**Person B (Go-to-Market — optional at first, needed for scale):**
- Can be outsourced to freelancers
- TikTok content creation
- Technical writing / content marketing
- Cold outreach / sales

---

## 13. GROWTH ROADMAP (Months 1-12)

### Month 1: MVP Scanner

- [ ] Build the core scanner engine (secret-scanner, header-scanner, ssl-scanner, sqli-scanner)
- [ ] Simple Next.js landing page with hero + scan input
- [ ] Free tier: severity overview only
- [ ] Stripe integration for paid plans
- [ ] Launch on Product Hunt, Hacker News

**Goal:** 100 scans, 10 paid users

### Month 2: MCP Server + BaaS Checks

- [ ] Build @checkvibe/mcp-server (or your equivalent)
- [ ] Add Supabase RLS checks
- [ ] Add Firebase rules checks
- [ ] Add AI fix prompt generation
- [ ] Publish npm package

**Goal:** 500 scans, 30 paid users, $500 MRR

### Month 3: Content Engine

- [ ] Blog: 3 posts/week on security + AI topics
- [ ] SEO: Target 10 high-volume keywords
- [ ] TikTok: 15-min slideshows, 5/week
- [ ] Cold outreach: 20 personalized DMs/day

**Goal:** $2k MRR

### Month 4: SEO + AEO Scanner

- [ ] Add 68 SEO checks
- [ ] Add 46 AEO checks
- [ ] Create dedicated landing pages for each scanner type
- [ ] Launch comparison pages (vs ZeriFlow, vs Snyk)

**Goal:** $3.5k MRR

### Month 5: Enter the Competition

- [ ] Add uptime monitoring (60s pings + public status page)
- [ ] Add performance monitoring (Core Web Vitals)
- [ ] Add PDF report exports
- [ ] Launch affiliate program

**Goal:** $5k MRR

### Month 6: Mobile + Conversion Optimization

- [ ] Audit mobile onboarding (cut steps)
- [ ] A/B test paywall designs (issue count vs blur)
- [ ] Improve scan speed (target: <20s)
- [ ] Add live threat detection feed

**Goal:** $7k MRR (CheckVibe's current milestone)

### Months 7-9: Scale

- [ ] Add accessibility scanning (WCAG 2.2)
- [ ] Add email deliverability scanning (SPF, DKIM, DMARC)
- [ ] Add domain monitoring (expiry, DNS, TLS)
- [ ] Expand to USD/EUR/CHF pricing tiers
- [ ] Build team (hire VA for content)

**Goal:** $15k MRR

### Months 10-12: Moat

- [ ] Build integrations: GitHub Actions, Vercel, Linear, Slack
- [ ] Create "scanned by CheckVibe" badge (viral loop)
- [ ] Enterprise features: SSO, SOC-2 reports, team accounts
- [ ] Raise prices or introduce usage-based billing

**Goal:** $25k+ MRR

---

## 14. RISKS & MITIGATIONS

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **ZeriFlow undercuts on price** | Medium | Differentiate on MCP + AEO + BaaS checks; compete on value, not price |
| **Big players copy features** | Medium | Build moat via MCP ecosystem + content authority + community |
| **Vibe coding hype cools** | Low-Medium | Expand positioning to "web security scanner" (still a big market) |
| **Scanner accuracy issues** | High | Invest in QA; show evidence for every finding; accept false positives but never false negatives |
| **Legal liability (false negatives)** | High | Clear disclaimers (CheckVibe has them); position as "automated check, not a pentest" |
| **MCP protocol changes** | Low | Follow @modelcontextprotocol closely; contribute to spec |
| **Google/OpenAI block scanning** | Low | Scanning is legal (same as any security scanner); stay above board |
| **Churn** | Medium | Annual discounts (30%), sticky features (monitoring, status page), ongoing value delivery |

---

## APPENDIX A: Key Founder Quotes (r/StartupSoloFounder)

> "Three months ago I was refreshing Stripe hoping for one sale. Now there's a small but growing group of people paying every month to keep their apps from leaking."

> "TikTok slideshows have carried us. Aesthetic Pinterest-style backgrounds with tool names overlaid, five slides, no branding on the account. One hit a million views and is still quietly sending signups weeks later."

> "Cold outreach worked, but only the version where I scanned the prospect's app first and DMed them what I found. Generic pitches got ignored. Useful findings got replies almost every time."

> "Paywall design was a 3x lever. The first version blurred all results, which felt clever and barely converted. Switched to one that just shows the count of critical issues with the actual findings locked. Conversion tripled."

> "What nearly killed me was mobile activation tanking compared to desktop and not catching it for weeks. Onboarding had too many steps on small screens. Cut two and the gap basically closed overnight."

> "If you've shipped something with AI tools and haven't really checked what's exposed, checkvibe.dev runs in 30 seconds. Scan for free, only pay if you have issues. Almost every app I've scanned came back with something."

## APPENDIX B: Links to Study

| Resource | URL |
|----------|-----|
| CheckVibe Homepage | https://checkvibe.dev |
| Pricing Page | https://checkvibe.dev/pricing |
| About Page | https://checkvibe.dev/about |
| Security Scanner | https://checkvibe.dev/products/scanner |
| SEO & AEO Scanner | https://checkvibe.dev/products/seo-aeo |
| MCP Server | https://checkvibe.dev/products/mcp-server |
| All Security Checks | https://checkvibe.dev/security-checks |
| Blog | https://checkvibe.dev/blog |
| Terms of Service | https://checkvibe.dev/terms |
| Subprocessors | https://checkvibe.dev/subprocessors |
| NPM Package | https://www.npmjs.com/package/@checkvibe/mcp-server |
| Reddit Founder Post | r/StartupSoloFounder (search "CheckVibe" or "After 3 Months of GRINDING") |
| Competitor Comparison | https://zeriflow.com/blog/zeriflow-vs-checkvibe-vs-snyk-vs-owasp-zap |
| Competitor Comparison 2 | https://complycode.app/vs/checkvibe |

## APPENDIX C: Infrastructure Confirmed via Subprocessors

From CheckVibe's own subprocessors page, their exact stack:

| Service | Role | Data Handled |
|---------|------|-------------|
| Vercel | Web hosting, edge functions, CDN | Account identifiers, request logs, IPs |
| Supabase | Auth, primary DB, file storage | Account data, scan data, encrypted tokens |
| Stripe | Payment processing, billing | Billing email, payment metadata, transaction history |
| Resend | Transactional + outreach email | Email address, content, delivery metadata |
| Google Safe Browsing | Malicious URL lookup | Hashed URLs |
| Google Gemini API | AI analysis of scan findings | Scan-finding text (no training use) |
| GitHub API | Repository scanning (opt-in) | Repo metadata (authorized only) |
| NIST NVD | CVE lookup | Package names and versions |
| Sentry | Error monitoring | Error stacks, request metadata |
| PostHog | Product analytics | Event metadata, account identifier |
| Cloudflare | DNS, DDoS, edge caching | IP addresses, request metadata |

---

*This cloning playbook was generated by Business Cloner Agent • SaaS Security Auditor*
*Data sources: checkvibe.dev, npm registry, subprocessors page, Terms of Service, r/StartupSoloFounder*
*Date: July 8, 2026*