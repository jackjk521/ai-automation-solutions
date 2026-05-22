# AI Lead Gen Pipeline — B2B Web Services Outreach

Automated B2B lead generation pipeline that finds, scores, and prepares outreach for local businesses that need web services or ready-to-deploy software products.

**Runs:** Monday + Wednesday at 07:00 Manila time (or manual trigger)
**Output per run:** Top 10 scored leads in Google Sheets + deployed MVP preview pages + email digest

---

## What It Does

| Step | What Happens |
|------|-------------|
| **Search** | Apify Google Maps scraper fetches 30 businesses per niche/location |
| **Deduplicate** | Strips any URL already in your Sheets — every lead is new |
| **Industry Brief** | LLM produces one market overview per niche (common pain points, outreach angle) |
| **Enrich** | PageSpeed (mobile score, LCP, HTTPS) + Open PageRank — both free APIs |
| **Score** | LLM scores each lead across 5 dimensions (tech, SEO, brand, sales readiness, expansion) |
| **Rank** | Top 10 by total score, local businesses win tiebreaks |
| **Generate** | Source-protected HTML MVP preview page deployed to Vercel for each high-score lead |
| **Digest** | HTML email summary with all leads, scores, expansion signals, and error fixes |

---

## Setup Order

**Do these steps exactly in order.**

### 1. Google Sheets
Create a new Google Sheet with 3 tabs:

**Config tab** — headers in row 1:
```
Niche | Location | Status | Last Run | Run Count
```
Add your first row: `Dental Clinic | London, UK | Active | | `

**Leads tab** — headers in row 1:
```
Run ID | Company | URL | Phone | Email | Address | Rating | Review Count |
Tech Score | SEO Score | Brand Score | Sales Readiness | Expansion Score |
Total Score | Is Local Business | Top 3 Flaws | Opportunity Summary |
Recommended Service | Expansion Opps | Status | MVP URL | Date Added
```

**Errors tab** — headers in row 1:
```
Run ID | Timestamp | Node | Company/URL | Error Message | Resolved
```

Copy the Sheet ID from the URL: `docs.google.com/spreadsheets/d/**SHEET_ID**/edit`

### 2. API Keys

| Key | Where to Get | Cost |
|-----|-------------|------|
| `APIFY_TOKEN` | [apify.com](https://apify.com) → Account → Integrations | Free $5 credit |
| `PAGESPEED_API_KEY` | Google Cloud Console → APIs → PageSpeed Insights API | Free, unlimited |
| `OPEN_PAGERANK_KEY` | [domcop.com/openpagerank](https://www.domcop.com/openpagerank/) | Free |
| `LLM_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) (recommended) | ~$0.001/lead |
| `VERCEL_TOKEN` | [vercel.com/account/tokens](https://vercel.com/account/tokens) → deployments:write | Free |
| `GOOGLE_SHEETS_ID` | From your Sheet URL | Free |
| `ALERT_EMAIL` | Your email address | — |

### 3. Docker Setup
```bash
cp .env.template .env
# Fill in all values in .env
docker compose up -d
```

### 4. n8n Setup
1. Open n8n at `http://localhost:5678` (default: admin / changeme)
2. **Menu → Import from File** → select `workflow.json`
3. Set up **Google Sheets OAuth2** credential in n8n → Settings → Credentials
4. Set up **Gmail OAuth2** credential (for the digest email)
5. In the "Send Digest Email" node, select your Gmail credential

### 5. Test Run
1. Add a test row to Config tab: `Restaurant | Cebu City | Active`
2. In n8n, open the workflow and click **Execute Workflow** (manual test)
3. Watch the execution — each section has a Sticky Note label
4. Check your Sheets Leads tab for results

### 6. Enable Schedule
Toggle the **Active** switch in n8n — the pipeline now runs Mon + Wed at 07:00.

---

## Changing the LLM (4 values in .env, zero workflow changes)

```bash
# Switch to OpenAI
LLM_PROVIDER=openai
LLM_BASE_URL=https://api.openai.com/v1/chat/completions
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-...

# Switch to Anthropic Claude
LLM_PROVIDER=anthropic
LLM_BASE_URL=https://api.anthropic.com/v1/messages
LLM_MODEL=claude-sonnet-4-6
LLM_API_KEY=sk-ant-...

# Switch to Groq (free tier)
LLM_PROVIDER=groq
LLM_BASE_URL=https://api.groq.com/openai/v1/chat/completions
LLM_MODEL=llama-3.1-8b-instant
LLM_API_KEY=gsk_...
```

Then restart: `docker compose restart n8n`

---

## Adding Niches

Add a new row to the **Config tab**:
```
Spa & Salon | Dubai, UAE | Active
```
The pipeline picks it up on the next run automatically.

---

## Tuning Safety Limits

| Variable | Default | Increase if | Decrease if |
|----------|---------|------------|------------|
| `MAX_LEADS_FETCHED` | 30 | You want wider coverage | Server is slow/timing out |
| `TOP_LEADS_KEPT` | 10 | You want more rows per run | Sheets is getting crowded |
| `MAX_APIFY_POLL_ATTEMPTS` | 15 | Apify runs are timing out | You want faster failure |
| `MAX_ERRORS_BEFORE_ABORT` | 5 | You want more resilience | You want early failure alerts |
| `SCORE_THRESHOLD` | 70 | Too many MVPs generating | Not enough MVPs generating |

---

## Scoring Dimensions

| Dimension | Max | What Scores High |
|-----------|-----|-----------------|
| Tech Score | 25 | No SSL, outdated CMS, no CDN, poor mobile |
| SEO Score | 25 | Low PageRank, poor PageSpeed, no analytics |
| Brand Score | 25 | Few reviews, low rating, no social profiles |
| Sales Readiness | 25 | Local business, service-based, has contact info |
| **Total** | **100** | Sum of above four |
| Expansion Score | 25 | BONUS — software product fit (booking, loyalty, etc.) |

Leads with `Total ≥ SCORE_THRESHOLD` get an MVP preview page deployed to Vercel.
Local businesses win tiebreaks — they convert at higher rates.

---

## Cost Estimate Per Run (30 leads, DeepSeek)

| Item | Cost |
|------|------|
| Apify Google Maps (30 results) | ~$0.03 |
| Apify BuiltWith actor (30 domains) | ~$0.15 |
| PageSpeed API (30 calls) | Free |
| Open PageRank (30 calls) | Free |
| LLM — industry overview (1 call) | ~$0.001 |
| LLM — scoring (30 calls) | ~$0.03 |
| LLM — MVP HTML (10 calls) | ~$0.02 |
| Vercel deploys (10) | Free |
| **Total per run** | **~$0.23** |

Monthly (8 runs × 3 niches): **~$5.50**

---

## Integrations

| Service | Purpose | Credential in n8n |
|---------|---------|------------------|
| Apify | Google Maps scraping + BuiltWith | API key in `.env` |
| Google PageSpeed | Mobile performance scores | API key in `.env` |
| Open PageRank | Domain authority | API key in `.env` |
| LLM provider | Scoring + MVP generation | API key in `.env` |
| Google Sheets | Lead storage + config | OAuth2 credential |
| Gmail | Digest email | OAuth2 credential |
| Vercel | MVP page hosting | Token in `.env` |

---

## License

MIT © 2024 Jed Abner Chu ([aceinternational.solutions](https://aceinternational.solutions))
