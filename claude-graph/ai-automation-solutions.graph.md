# ai-automation-solutions — Knowledge Graph
<!-- graphify:v1 | project:ai-automation-solutions | owner:jackjk521 | branch:claude/web-scraping-business-analysis-kU2s7 -->
<!-- LLM-READY: paste this file into any Claude/GPT session to resume full context instantly -->

---

## META

```yaml
project: ai-automation-solutions
repo: https://github.com/jackjk521/ai-automation-solutions
branch: claude/web-scraping-business-analysis-kU2s7
author: Jed Abner Chu (jedchu541@gmail.com)
site: aceinternational.solutions
license: MIT
last_commit: 76886d1
stack: [Next.js 14, Python 3.10+, n8n, Playwright, Tailwind CSS, TypeScript]
hosting: Cloudflare Pages (showcase), self-hosted Docker (n8n templates)
```

---

## GRAPH NODES

### NODE · REPO_ROOT
```
id: REPO_ROOT
type: repository
path: /
children: [SHOWCASE, TEMPLATES, CLAUDE_AUTOMATIONS, PROMPT_FORGE, DOCS, CLAUDE_GRAPH]
key_files: [README.md, CONTRIBUTING.md, LICENSE, .github/workflows/validate.yml]
```

---

### NODE · SHOWCASE
```
id: SHOWCASE
type: next_app
path: showcase/
framework: Next.js 14
deploy: Cloudflare Pages (wrangler.toml)
fonts: [Inter (body), JetBrains Mono (code)]
styling: Tailwind CSS 3.4
description: >
  Public-facing template showcase site. Live search + filter across all 10
  n8n templates with richer cards, dot-grid hero, gradient text, and
  glassmorphism card-shine effects.
```

**SHOWCASE → Components:**
| File | Role |
|------|------|
| `src/app/page.tsx` | Hero + stats cards + TemplateGrid + AI callout |
| `src/app/globals.css` | dot-grid, gradient-text, card-shine CSS utilities |
| `src/app/templates/[slug]/page.tsx` | Individual template detail page |
| `src/app/docs/page.tsx` | Documentation page |
| `src/components/TemplateGrid.tsx` | `'use client'` — live search + trigger filter pills + AI toggle |
| `src/components/TemplateCard.tsx` | Trigger-coloured accent bar, complexity badge, node count |
| `src/components/Navigation.tsx` | `usePathname` active highlight, backdrop-blur |
| `src/components/Footer.tsx` | 4-col: brand, Popular Templates, Resources, Author/license |
| `src/data/templates.ts` | Single source of truth — all 10 template objects |

**SHOWCASE → Data Schema (templates.ts):**
```typescript
interface Template {
  id: string           // "01"–"10"
  slug: string         // URL slug
  name: string
  description: string
  fullDescription: string
  trigger: "webhook" | "schedule" | "manual" | "gmail"
  isAIPowered: boolean
  integrations: string[]
  tags: string[]
  nodes: string[]      // node names for complexity badge
  prerequisites: string[]
  credentials: { node, type, notes }[]
  customization: string[]
  githubPath: string   // path to workflow.json
}
```

**SHOWCASE → Filter Logic (TemplateGrid.tsx):**
```
useMemo over templates array
  → search: name + description + tags + integrations (case-insensitive)
  → trigger filter: All | Webhook | Scheduled | Manual | Gmail
  → AI toggle: isAIPowered === true
Empty state shows "Clear all filters" + result count display
```

---

### NODE · TEMPLATES
```
id: TEMPLATES
type: n8n_workflow_library
path: templates/
count: 10
format: workflow.json (n8n import format) + README.md per template
node_schema: { id: UUIDv4, name, type, typeVersion, position:[x,y], parameters }
```

**TEMPLATES → Index:**
| # | Folder | Trigger | AI? | Nodes | Key Integrations |
|---|--------|---------|-----|-------|-----------------|
| 01 | lead-capture-to-crm | webhook | No | 8 | Airtable, Gmail, Slack |
| 02 | invoice-automation | schedule | No | 6 | Google Sheets, Gmail |
| 03 | slack-project-notifications | webhook | No | 12 | Slack, Google Sheets |
| 04 | ai-email-triage | gmail | Yes | 7 | Gmail, Notion, Slack, Anthropic |
| 05 | real-estate-lead-nurture | webhook | No | 9 | Google Sheets, Gmail |
| 06 | support-ticket-classifier | webhook | Yes | 11 | Slack, Gmail, Anthropic |
| 07 | weekly-report-generator | schedule | Yes | 7 | Google Sheets, Gmail, Anthropic |
| 08 | client-onboarding-sequence | webhook | No | 13 | Gmail, Notion, Slack, Google Sheets |
| 09 | web-scraping-business-analysis | manual | Yes | 15 | SerpAPI, BuiltWith, Anthropic, Google Sheets, Gmail |
| 10 | b2b-lead-gen-pipeline | schedule | Yes | 55 | Apify, BuiltWith, PageSpeed, OpenPageRank, Vercel, Gmail, Google Sheets |

**TEMPLATES → n8n Node Types used:**
```
manualTrigger, scheduleTrigger, formTrigger, gmailTrigger
webhook, splitInBatches, if, switch, set, code, merge
httpRequest, googleSheets, gmail, slack, notion, wait
stickyNote (section labels)
```

**TEMPLATES → Template 10 Architecture (55 nodes, 11 sections):**
```
§1 Trigger & Config     → Schedule + Form → Sheets Config → Split rows
§2 Apify Search         → Start run → Bounded poll (max 15×10s) → Fetch dataset → Normalize
§3 Deduplication        → Read existing URLs → Filter fresh → Check if any
§4 Industry LLM         → Build prompt → LLM Router → HTTP → Parse (1 call/niche)
§5 Per-Lead Enrichment  → Split → Circuit Breaker → PageSpeed → OpenPageRank (per lead)
§6 LLM Scoring          → Build prompt → LLM Router → HTTP → Parse (5 dims, 100pts)
§7 Rank & Select        → Accumulate in $workflow.vars.scoredLeads → Sort top N
§8 Sheets + Gate        → Append to Sheets → Score gate (≥THRESHOLD → §9, else → §10)
§9 MVP HTML → Vercel    → LLM Router → HTTP → Parse → Deploy → Save URL
§10 Email Digest         → Build → Send via Gmail
§11 Error Logger         → ALL node errors wired here → Write to Errors sheet
```

**TEMPLATES → Template 10 Key Patterns:**
```yaml
universal_llm_router:
  provider_env: LLM_PROVIDER  # deepseek | anthropic | openai | groq | moonshot
  switch_vars: [LLM_PROVIDER, LLM_BASE_URL, LLM_MODEL, LLM_API_KEY]
  reused_count: 3  # Industry Overview, Scoring, MVP HTML

circuit_breaker:
  reads: $workflow.vars.errorCount
  threshold_env: MAX_ERRORS_BEFORE_ABORT  # default: 5
  action: skip remaining leads → jump to Email Digest

scoring_dimensions:
  - tech_score: 25     # modern stack vs legacy CMS
  - seo_score: 25      # PageSpeed + PageRank signals
  - brand_score: 25    # site quality + brand clarity
  - sales_readiness: 25  # decision-maker accessibility
  - expansion_score: bonus tiebreaker
  - local_business: flag (filters pure-local from outreach list)

accumulator:
  store: $workflow.vars.scoredLeads
  ranks_by: total score, tiebreak non-local first

env_vars:
  MAX_LEADS_FETCHED: 30
  TOP_LEADS_KEPT: 10
  MAX_APIFY_POLL_ATTEMPTS: 15
  MAX_ERRORS_BEFORE_ABORT: 5
  SCORE_THRESHOLD: 70
```

**TEMPLATES → Template 10 Extra Files:**
```
.env.template        → LLM provider options (DeepSeek recommended)
docker-compose.yml   → n8nio/n8n:latest, Asia/Manila TZ, all env vars
diagram.html         → Mermaid.js browser-viewable flowchart (11 sections, colour-coded)
```

**TEMPLATES → Google Sheets Schema (Template 10):**
```
Tab: Config  → niche, region, active, run schedule
Tab: Leads   → scored leads with Vercel URLs + all 5 scores
Tab: Errors  → timestamped error log per run
```

---

### NODE · CLAUDE_AUTOMATIONS
```
id: CLAUDE_AUTOMATIONS
type: python_library
path: claude-automations/
count: 21
runtime: Python 3.10+
deps: anthropic>=0.40.0, python-dotenv>=1.0.0, requests>=2.31.0
env_base: ANTHROPIC_API_KEY
pattern: single main.py per automation, run(input_data: dict) -> dict
```

**CLAUDE_AUTOMATIONS → Universal Pattern:**
```python
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
SYSTEM_PROMPT = "..."
response = client.messages.create(
    model="claude-sonnet-4-6",         # or claude-haiku-4-5-20251001
    max_tokens=1500,
    system=[{"type":"text","text":SYSTEM_PROMPT,"cache_control":{"type":"ephemeral"}}],
    messages=[{"role":"user","content":build_prompt(input_data)}],
    extra_headers={"anthropic-beta":"prompt-caching-2024-07-31"},
)
raw = response.content[0].text
match = re.search(r'\{[\s\S]+\}', raw)
return json.loads(match.group(0)) if match else {"raw": raw}
```

**CLAUDE_AUTOMATIONS → Index:**
| # | Name | Category | Model | Use Case |
|---|------|----------|-------|----------|
| 01 | email-triage | Email | Haiku | Classify + draft replies |
| 02 | lead-qualifier | Sales | Haiku | BANT score leads |
| 03 | support-ticket-classifier | Support | Haiku | Route by category/priority/sentiment |
| 04 | weekly-report-generator | Analytics | Sonnet | KPI data → narrative report |
| 05 | invoice-generator | Finance | Sonnet | Client + line items → HTML invoice |
| 06 | cold-outreach-generator | Sales | Sonnet | Prospect → personalised email sequence |
| 07 | social-media-generator | Marketing | Haiku | Topic → LinkedIn/Twitter/Instagram posts |
| 08 | seo-content-optimizer | Marketing | Sonnet | Blog → SEO improvements + meta |
| 09 | resume-screener | HR | Sonnet | JD + CV → fit score + questions |
| 10 | meeting-summarizer | Productivity | Sonnet | Transcript → summary + action items |
| 11 | contract-analyzer | Legal | Sonnet | Contract → risks + negotiation points |
| 12 | customer-review-analyzer | CX | Sonnet | Batch reviews → insights + responses |
| 13 | competitor-analyzer | Strategy | Sonnet | Competitor info → battle card |
| 14 | product-description-generator | E-commerce | Sonnet | Specs → SEO product copy |
| 15 | code-reviewer | Dev Tools | Sonnet | Code → issues + fixes |
| 16 | document-qa | Research | Sonnet | Document + questions → cited answers |
| 17 | content-calendar-generator | Marketing | Sonnet | Brand info → 30-day calendar |
| 18 | data-extractor | Data | Sonnet | Unstructured text → structured JSON |
| 19 | faq-builder | Support | Sonnet | Source docs → FAQ pairs |
| 20 | web-presence-analyzer | Lead Gen | Sonnet | Business data → score + outreach email |
| 21 | social-trend-newsletter | Research | Sonnet | Weekly trends → HTML newsletter |

**CLAUDE_AUTOMATIONS → Automation 21 (Social Trend Newsletter):**
```yaml
file: claude-automations/21-social-trend-newsletter/main.py
frequency: weekly (cron 0 7 * * 1)
niches: [F&B, Active Lifestyle, Shopping]
locations: [Philippines, International]
search_matrix: 6 pairs × 3 platforms = 18 queries/week (72/month, fits Google CSE free tier)
platforms: [reddit.com, tiktok.com, instagram.com]
query_template: 'site:{platform} "{niche}" {location} trending'

phases:
  1_parallel:
    scraper: Google Custom Search API (18 calls)
    researcher: Claude research agent (6 calls, one per pair)
    executor: concurrent.futures.ThreadPoolExecutor(max_workers=12)
  2_synthesis: Claude synthesis agent (6 calls, cites search URLs)
  3_newsletter: Claude newsletter generator (1 call, full HTML)
  4_email: Gmail SMTP_SSL port 465

env_vars:
  ANTHROPIC_API_KEY: required
  GOOGLE_CSE_API_KEY: Google Custom Search API key
  GOOGLE_CSE_ID: Programmable Search Engine ID (cx)
  EMAIL_FROM: Gmail address
  EMAIL_APP_PASSWORD: 16-char Gmail app password
  EMAIL_TO: recipient (same as FROM is fine)

cost_per_run: ~$0.07
cost_per_month: ~$0.28 (4 runs)
```

---

### NODE · PROMPT_FORGE
```
id: PROMPT_FORGE
type: browser_tool
path: prompt-forge/
main_file: prompt-generator.html
description: >
  Single-file offline prompt generator. Pick a template, fill fields, get a
  sequenced Claude Code prompt with auto-wired ingestion, taste guardrails,
  SEO/CRO, motion principles, and testing. No build step, no server needed.
fonts: [Fraunces (serif/headings), Hanken Grotesk (sans/body), JetBrains Mono (mono/code)]
palette: warm amber (#e08a3c) + teal (#5ec7b8) on dark charcoal (#16130f)
storage: none (no localStorage, no sessionStorage — all state in memory)
```

**PROMPT_FORGE → 8 Templates:**
| # | Template ID | Phases | Key Tools |
|---|-------------|--------|-----------|
| 1 | client-website-brand-seo | 7 | codefetch, designlang, markitdown, founder:prd, impeccable, ai-seo, seo-audit, schema, founder:cro |
| 2 | mvp-webapp-artifact | 5 | codefetch, designlang, founder:prd, impeccable, web-artifacts-builder, playwright |
| 3 | ingest-inputs | 2 | codefetch, markitdown, designlang, graphify, claude-video |
| 4 | design-from-reference | 4 | designlang, impeccable, design-motion-principles |
| 5 | seo-cro-pass | 2 | ai-seo, seo-audit, schema, founder:cro |
| 6 | project-face-off | 4 | designlang, impeccable (A), taste-skill (B), design-motion-principles, playwright |
| 7 | redesign-audit | 5 | designlang, codefetch, impeccable, redesign-skill, ui-ux-pro-max, founder:cro |
| 8 | knowledge-graph-system | 5 | codefetch, graphify, founder:prd, impeccable, playwright |

**PROMPT_FORGE → Auto-Wiring Rules:**
```
github_refs    → codefetch (+ graphify if "complex repo" checkbox)
documents      → markitdown (+ brand-guidelines if doc is brand guide)
inspiration_urls → designlang
reference_url  → designlang
video_refs     → claude-video
```

**PROMPT_FORGE → Taste Guardrail Logic:**
```
Radio: impeccable | taste-skill | ui-ux-pro-max-skill  (mutually exclusive)
Conflict pairs: [impeccable+taste-skill, impeccable+ui-ux-pro-max, taste-skill+ui-ux-pro-max]
Conflict trigger: red warn-box with "Conflict: X + Y — choose only one primary taste guardrail"
design-motion-principles = secondary skill (does NOT conflict with any primary)
```

**PROMPT_FORGE → Token Budget:**
```
chars > 8,000  → stat.className = "stat warn"   (yellow)
chars > 12,000 → stat.className = "stat danger"  (red)
estimate: Math.round(words * 1.3) tokens
```

**PROMPT_FORGE → Test Suite (tests/generator.spec.ts):**
```
Test 1: client-website + all inputs filled + complex repo checked + ai-seo/seo-audit/schema
        → clipboard contains: codefetch, graphify, markitdown, designlang, impeccable,
          ai-seo, seo-audit, schema, Playwright, "STOP. Do not proceed to Phase 2",
          "If a skill/CLI is missing, log it and continue"
Test 2: taste-skill clicked while impeccable active → #conflictWarn has class "show" + text "Conflict"
Test 3: 3000-word brief → #stat has class "warn" or "danger"
```

---

### NODE · DOCS
```
id: DOCS
type: documentation
path: docs/
files:
  - how-to-import.md    → step-by-step n8n workflow import guide
  - configuring-ai-nodes.md → Anthropic + OpenAI credential setup in n8n
```

---

### NODE · CLAUDE_GRAPH
```
id: CLAUDE_GRAPH
type: knowledge_graph_output
path: claude-graph/
files:
  - ai-automation-solutions.graph.md   ← this file
purpose: project migration, context handoff, LLM resumption
```

---

## GRAPH EDGES

```yaml
edges:
  - from: REPO_ROOT
    to: [SHOWCASE, TEMPLATES, CLAUDE_AUTOMATIONS, PROMPT_FORGE, DOCS, CLAUDE_GRAPH]
    rel: contains

  - from: SHOWCASE
    to: TEMPLATES
    rel: displays_data_from
    via: src/data/templates.ts  →  githubPath field links to templates/*/workflow.json

  - from: CLAUDE_AUTOMATIONS
    to: TEMPLATES
    rel: conceptual_parallel
    note: >
      Automations 04/06/07/09/21 duplicate the intelligence of n8n templates 07/06/09 —
      same use-cases implemented in Python (standalone) vs n8n (visual workflow)

  - from: PROMPT_FORGE
    to: CLAUDE_AUTOMATIONS
    rel: generates_prompts_for
    note: >
      prompt-generator.html produces sequenced Claude Code prompts.
      Automation #21 is itself an example of what a forged prompt would build.

  - from: PROMPT_FORGE
    to: TEMPLATES
    rel: generates_prompts_for
    note: >
      client-website-brand-seo + mvp-webapp-artifact templates output prompts
      that, when run, produce n8n-style deliverables.

  - from: TEMPLATES["10-b2b-lead-gen-pipeline"]
    to: TEMPLATES["09-web-scraping-business-analysis"]
    rel: extends
    note: >
      Template 10 is an enterprise-grade evolution of Template 09:
      adds Apify (vs SerpAPI), 5-dimension LLM scoring (vs simple score),
      Vercel publishing, circuit breaker, universal LLM router, deduplication.

  - from: CLAUDE_AUTOMATIONS["21-social-trend-newsletter"]
    to: TEMPLATES["09-web-scraping-business-analysis"]
    rel: conceptual_parallel
    note: Both scrape → AI analyze → outreach. #21 is Python; Template 09 is n8n.

  - from: SHOWCASE["TemplateGrid"]
    to: SHOWCASE["src/data/templates.ts"]
    rel: reads_data
    via: import { templates } from '@/data/templates'

  - from: SHOWCASE["Footer"]
    to: TEMPLATES
    rel: links_to
    via: TEMPLATE_LINKS array (Popular Templates section)
```

---

## CREDENTIAL MAP

```yaml
# All credentials needed to run the full stack

anthropic:
  key: ANTHROPIC_API_KEY
  used_by: [claude-automations/*, templates/04, 06, 07, 09, 10]

google:
  oauth2: Google OAuth2
  used_by: [templates/* (Sheets + Gmail), showcase (none)]
  custom_search:
    key: GOOGLE_CSE_API_KEY
    cx: GOOGLE_CSE_ID
    used_by: [claude-automations/21-social-trend-newsletter]

apify:
  token: APIFY_TOKEN
  used_by: [templates/10-b2b-lead-gen-pipeline]

builtwith:
  key: BUILTWITH_API_KEY
  used_by: [templates/09, 10]

pagespeed:
  key: PAGESPEED_API_KEY  # free, Google Cloud Console
  used_by: [templates/10]

open_pagerank:
  key: OPEN_PAGERANK_KEY  # free, domcop.com/openpagerank
  used_by: [templates/10]

vercel:
  token: VERCEL_TOKEN
  used_by: [templates/10]

slack:
  bot_token: Slack API (chat:write scope)
  used_by: [templates/01, 03, 04, 06, 08]

gmail:
  oauth2: Gmail OAuth2 (gmail.send scope)
  used_by: [templates/02, 04, 05, 06, 07, 08, 09, 10]
  smtp:
    EMAIL_FROM: Gmail address
    EMAIL_APP_PASSWORD: 16-char app password
    EMAIL_TO: recipient
    used_by: [claude-automations/21]

notion:
  token: Notion API (internal integration)
  used_by: [templates/04, 08]

airtable:
  token: Airtable Personal Access Token
  used_by: [templates/01]

serpapi:
  key: SERPAPI_KEY
  used_by: [templates/09]  # note: template 10 uses Apify instead

llm_router (template 10 only):
  LLM_PROVIDER: deepseek | anthropic | openai | groq | moonshot
  LLM_BASE_URL: provider API endpoint
  LLM_MODEL: model identifier
  LLM_API_KEY: provider API key
```

---

## SETUP QUICK-START

### Clone & run showcase
```bash
git clone https://github.com/jackjk521/ai-automation-solutions
cd ai-automation-solutions/showcase
npm install
npm run dev          # http://localhost:3000
```

### Run any Claude automation
```bash
cd claude-automations
pip install -r requirements.txt
cp .env.example .env    # fill ANTHROPIC_API_KEY (+ extras for #21)
python 21-social-trend-newsletter/main.py
```

### Run Template 10 (n8n B2B pipeline)
```bash
cd templates/10-b2b-lead-gen-pipeline
cp .env.template .env   # fill all keys
docker-compose up -d    # starts n8n at http://localhost:5678
# Import workflow.json via n8n UI → Workflows → Import
# Open diagram.html in browser to verify flow matches expectations
```

### Open Prompt Forge
```bash
# Just open the file in any browser — no server needed
open prompt-forge/prompt-generator.html
# or via Live Server in VS Code (works after JS syntax fix in 76886d1)
```

### Run Prompt Forge tests
```bash
cd prompt-forge
npm install
npm run install-browsers
npm test
```

---

## KNOWN DECISIONS & RATIONALE

```yaml
decisions:
  - id: D1
    decision: Python (claude-automations) chosen over n8n for #21 social newsletter
    reason: 1×/week frequency → ~$0.28/month Python vs $20+/month n8n cloud; parallel
            agents easier with concurrent.futures than n8n Merge nodes

  - id: D2
    decision: Google Custom Search API (not SerpAPI) for #21
    reason: user chose it; free 100 queries/day (72/month needed); one-time setup

  - id: D3
    decision: Universal LLM Router in Template 10 (Code node, not HTTP node)
    reason: Anthropic API schema differs from OpenAI-compatible endpoints; single code
            node handles both; swap provider with 4 env vars, zero workflow edits

  - id: D4
    decision: Bounded Apify poll loop in Code node (not n8n Loop node)
    reason: n8n Loop nodes risk infinite execution hangs; Code node for loop with
            MAX_APIFY_POLL_ATTEMPTS cap prevents runaway workflows

  - id: D5
    decision: $workflow.vars for accumulator + circuit breaker
    reason: n8n SplitInBatches nodes don't share state across iterations; workflow vars
            persist across the entire execution

  - id: D6
    decision: Prompt Forge as single HTML file (no build step)
    reason: spec requirement; works offline; no Node.js runtime needed on client machine

  - id: D7
    decision: Prompt caching on system prompts (all 21 automations)
    reason: ~90% cost reduction on repeated runs; cache_control: ephemeral on system
            prompt + anthropic-beta: prompt-caching-2024-07-31 header

  - id: D8
    decision: Mermaid.js (CDN) for Template 10 diagram
    reason: zero install, browser-viewable, dark-theme customisable, user can verify
            flow before setting up n8n credentials

  - id: D9
    decision: Showcase deployed to Cloudflare Pages
    reason: wrangler.toml present; _headers file adds security headers; free tier;
            Next.js 14 static export compatible
```

---

## BUGS FIXED IN SESSION

```yaml
bug_fixes:
  - id: BF1
    file: prompt-forge/prompt-generator.html
    commit: 76886d1
    issue: >
      Two literal newlines inside JavaScript double-quoted string literals (lines 170-171,
      215-216) caused a SyntaxError. Entire <script> block failed to parse → all panels
      rendered empty. Panels visible but no template cards, no fields, no output.
    fix: Replaced raw newlines with \n escape sequences in both placeholder strings.
    symptom: UI loads but 01·JOB TYPE / 02·BRIEF / 03-04·CHIPS all empty

  - id: BF2
    file: showcase/src/data/templates.ts
    commit: fdb8edc
    issue: Template 10 (B2B Lead Gen Pipeline) was missing from templates array
    fix: Added full entry with 15 nodes, 7 integrations, 5-dimension scoring description

  - id: BF3
    files: [templates/03, 06, 07, 08]
    commit: a8df50e
    issue: Only README.md existed; workflow.json files were missing
    fix: Generated all 4 workflow.json files via Python script (12, 11, 7, 13 nodes)
```

---

## FILE TREE (complete)

```
ai-automation-solutions/
├── .github/workflows/validate.yml
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE (MIT)
├── README.md
│
├── claude-automations/
│   ├── .env.example                    ← ANTHROPIC_API_KEY + Google CSE + Email vars
│   ├── requirements.txt                ← anthropic, python-dotenv, requests
│   ├── README.md                       ← 21-row index table
│   ├── 01-email-triage/main.py+README
│   ├── 02-lead-qualifier/main.py+README
│   ├── 03-support-ticket-classifier/main.py+README
│   ├── 04-weekly-report-generator/main.py+README
│   ├── 05-invoice-generator/main.py+README
│   ├── 06-cold-outreach-generator/main.py+README
│   ├── 07-social-media-generator/main.py+README
│   ├── 08-seo-content-optimizer/main.py+README
│   ├── 09-resume-screener/main.py+README
│   ├── 10-meeting-summarizer/main.py+README
│   ├── 11-contract-analyzer/main.py+README
│   ├── 12-customer-review-analyzer/main.py+README
│   ├── 13-competitor-analyzer/main.py+README
│   ├── 14-product-description-generator/main.py+README
│   ├── 15-code-reviewer/main.py+README
│   ├── 16-document-qa/main.py+README
│   ├── 17-content-calendar-generator/main.py+README
│   ├── 18-data-extractor/main.py+README
│   ├── 19-faq-builder/main.py+README
│   ├── 20-web-presence-analyzer/main.py+README
│   └── 21-social-trend-newsletter/main.py+README   ← NEW: parallel agents, Google CSE
│
├── claude-graph/
│   └── ai-automation-solutions.graph.md            ← THIS FILE
│
├── docs/
│   ├── how-to-import.md
│   └── configuring-ai-nodes.md
│
├── prompt-forge/
│   ├── prompt-generator.html           ← single-file offline tool, no build step
│   ├── toolchain-reference.md          ← ground truth for all tools/skills
│   ├── package.json                    ← Playwright dev dep only
│   ├── playwright.config.ts
│   ├── prompts/
│   │   ├── README.md                   ← placeholder glossary + wiring rules
│   │   ├── client-website-brand-seo.md
│   │   ├── mvp-webapp-artifact.md
│   │   ├── ingest-inputs.md
│   │   ├── design-from-reference.md
│   │   ├── seo-cro-pass.md
│   │   ├── project-face-off.md
│   │   ├── redesign-audit.md
│   │   └── knowledge-graph-system.md
│   └── tests/
│       └── generator.spec.ts           ← 3 Playwright tests
│
├── showcase/                           ← Next.js 14, Cloudflare Pages
│   ├── src/
│   │   ├── app/page.tsx                ← hero + TemplateGrid
│   │   ├── app/globals.css             ← dot-grid, gradient-text, card-shine
│   │   ├── app/docs/page.tsx
│   │   ├── app/templates/[slug]/page.tsx
│   │   ├── components/TemplateGrid.tsx  ← live search + filter ('use client')
│   │   ├── components/TemplateCard.tsx  ← richer cards with complexity badges
│   │   ├── components/Navigation.tsx
│   │   ├── components/Footer.tsx
│   │   └── data/templates.ts           ← 10 template objects
│   ├── wrangler.toml
│   └── public/_headers                 ← Cloudflare security headers
│
└── templates/
    ├── 01-lead-capture-to-crm/workflow.json+README
    ├── 02-invoice-automation/workflow.json+README
    ├── 03-slack-project-notifications/workflow.json+README    ← 12 nodes
    ├── 04-ai-email-triage/workflow.json+README
    ├── 05-real-estate-lead-nurture/workflow.json+README
    ├── 06-support-ticket-classifier/workflow.json+README      ← 11 nodes
    ├── 07-weekly-report-generator/workflow.json+README        ← 7 nodes
    ├── 08-client-onboarding-sequence/workflow.json+README     ← 13 nodes
    ├── 09-web-scraping-business-analysis/workflow.json+README ← 15 nodes
    └── 10-b2b-lead-gen-pipeline/
        ├── workflow.json                ← 55 nodes, 11 sections
        ├── .env.template
        ├── docker-compose.yml
        ├── diagram.html                ← Mermaid.js flowchart
        └── README.md
```

---

## NEXT STEPS / OPEN ITEMS

```yaml
open_items:
  - id: OI1
    priority: low
    item: >
      preview.png screenshots for each template (mentioned in CONTRIBUTING.md).
      Not yet created — would require running n8n and screenshotting each workflow canvas.

  - id: OI2
    priority: medium
    item: >
      Vercel deployment for showcase site. wrangler.toml targets Cloudflare Pages;
      if switching to Vercel, update next.config.js output mode.

  - id: OI3
    priority: medium
    item: >
      Cron setup for automation #21 (social-trend-newsletter).
      Add to system crontab: 0 7 * * 1 cd /path/to/claude-automations && python 21-.../main.py

  - id: OI4
    priority: low
    item: >
      Showcase website deployment + custom domain. Site is built but not yet deployed.
      Run: cd showcase && npx wrangler pages deploy .next/

  - id: OI5
    priority: low
    item: >
      Template 10 requires real API keys before first run:
      APIFY_TOKEN, BUILTWITH_API_KEY, PAGESPEED_API_KEY, OPEN_PAGERANK_KEY,
      Google Sheets OAuth2, Gmail OAuth2, VERCEL_TOKEN, LLM_API_KEY
```

---

<!-- graphify:end | generated: 2026-06-02 | session: ai-automation-solutions -->
