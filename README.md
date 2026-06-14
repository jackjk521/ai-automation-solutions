# AI Automation Solutions

Two production-ready Python automations:

1. **Lead Scraper** — finds potential buyers for your services/products, deduplicates, and scores legitimacy with AI
2. **Market Research** — researches a niche across 10 dimensions and synthesises a comprehensive report

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run a command
python main.py scrape-leads
python main.py market-research
python main.py view-leads
```

---

## Commands

### `scrape-leads` — Find potential buyers

```bash
python main.py scrape-leads \
  --service "web design and SEO" \
  --industry "ecommerce" \
  --location "Singapore" \
  --max-leads 50 \
  --min-score 65
```

Run without flags for interactive prompts.

**What it does:**
1. Searches DuckDuckGo for companies matching your criteria
2. **Deduplicates** — skips any domain already in the SQLite database
3. Scrapes each company website (name, email, phone, LinkedIn)
4. **AI evaluation** — Claude scores each lead 0–100 for legitimacy and fit
5. Saves qualified leads to `data/leads.db` and exports a CSV to `data/`

**Output columns:** company name, domain, website, email, phone, LinkedIn, employees, score, reason, type, recommended approach

---

### `market-research` — Generate a market report

```bash
python main.py market-research \
  --niche "sustainable fashion" \
  --sources-per-topic 4
```

**What it does:**
1. Builds targeted queries across 10 research dimensions (market size, trends, competition, customers, etc.)
2. Fetches and parses content from credible web sources
3. Sends all data to Claude Opus to synthesise a structured report
4. Saves to `data/reports/<niche>_<timestamp>.md`

**Report sections:** Executive Summary · Market Size & Growth · Trends · Competition · Target Customers · Opportunities · Challenges · Technology · Financials · Strategic Recommendations · References

---

### `view-leads` — Browse saved leads

```bash
python main.py view-leads --min-score 70 --limit 25
```

---

## Configuration (`.env`)

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | required | Get from console.anthropic.com |
| `MIN_LEGITIMACY_SCORE` | `60` | Minimum score to qualify a lead |
| `REQUEST_DELAY` | `2.0` | Seconds between HTTP requests |

---

## Project Structure

```
ai-automation-solutions/
├── main.py                          # CLI entry point
├── config.py                        # Environment config
├── database.py                      # SQLite lead storage
├── requirements.txt
├── .env.example
├── automations/
│   ├── lead_scraper/
│   │   ├── scraper.py               # Orchestrates search → scrape → evaluate → save
│   │   ├── evaluator.py             # Claude-powered legitimacy scoring
│   │   └── sources/
│   │       ├── ddg_search.py        # DuckDuckGo search (no API key needed)
│   │       └── web_scraper.py       # Company website scraper
│   └── market_research/
│       ├── researcher.py            # Multi-topic web research
│       └── report_builder.py        # Claude-powered report synthesis
└── data/
    ├── leads.db                     # SQLite database (auto-created)
    ├── leads_*.csv                  # Exported lead CSVs
    └── reports/
        └── *.md                     # Generated market research reports
```

---

## AI Models Used

| Task | Model | Reason |
|---|---|---|
| Lead evaluation | `claude-sonnet-4-6` | Many calls — cost-efficient, still accurate |
| Market research | `claude-opus-4-8` | One deep synthesis — best quality |
