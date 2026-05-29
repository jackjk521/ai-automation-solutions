# 21 – Social Trend Newsletter

## What it does

Weekly trend intelligence report across **F&B**, **Active Lifestyle**, and **Shopping** for both **Philippines** and **International** markets.

Two agents run in parallel each week:
- **Scraper agent** — 18 Google Custom Search queries scoped to `site:reddit.com`, `site:tiktok.com`, `site:instagram.com` → collects titles, URLs, snippets
- **Research agent** — Claude analyzes industry context, known trends, key players for each niche (no live search, pure LLM knowledge)

Both outputs feed a **Synthesis agent** → **Newsletter Generator** → branded HTML email.

## Prerequisites

- Python 3.10+
- Anthropic API key
- Google Custom Search API key + Programmable Search Engine ID (free, 100 queries/day)
- Gmail account with App Password enabled

## Setup

```bash
# 1. Clone and install dependencies
cd claude-automations
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Fill in all 5 keys (see below)

# 3. Run
python 21-social-trend-newsletter/main.py
```

## Environment Variables

Add to your `.env` file:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key

# Google Custom Search (free: 100 queries/day)
# 1. Enable "Custom Search JSON API" in Google Cloud Console
# 2. Create engine at https://programmablesearchengine.google.com
#    → Turn ON "Search the entire web"
# 3. Copy API key and Search Engine ID (cx) here
GOOGLE_CSE_API_KEY=your_google_cse_api_key
GOOGLE_CSE_ID=your_programmable_search_engine_id

# Gmail with App Password
# Enable 2FA → Google Account → Security → App Passwords → Mail
EMAIL_FROM=you@gmail.com
EMAIL_APP_PASSWORD=your_16_char_app_password
EMAIL_TO=you@gmail.com
```

## Search Queries Generated (18 total per run)

| Niche | Location | Platform |
|-------|----------|----------|
| F&B | Philippines | reddit.com, tiktok.com, instagram.com |
| F&B | International | reddit.com, tiktok.com, instagram.com |
| Active Lifestyle | Philippines | reddit.com, tiktok.com, instagram.com |
| Active Lifestyle | International | reddit.com, tiktok.com, instagram.com |
| Shopping | Philippines | reddit.com, tiktok.com, instagram.com |
| Shopping | International | reddit.com, tiktok.com, instagram.com |

Query format: `site:{platform} "{niche}" {location} trending`

**Free tier usage: 18 calls/week = 72/month (limit: 100/day)**

## Pipeline Architecture

```
Phase 1 (PARALLEL)
  ┌── Scraper Agent ──────────────────┐
  │  18 Google CSE calls              │
  │  → titles, URLs, snippets         │  ──→ Synthesis Agent
  └───────────────────────────────────┘         ↓ (×6 pairs)
  ┌── Research Agent ─────────────────┐    Newsletter Generator
  │  6 Claude calls (1 per pair)      │         ↓
  │  → context, trends, opportunities │    Email Sender
  └───────────────────────────────────┘
```

## Newsletter Sections

1. **Header** — week date, total sources analyzed
2. **Executive Summary** — 3-4 top signals across all niches
3. **Per-niche analysis** — F&B / Active Lifestyle / Shopping, each with Philippines vs International columns
4. **Cross-niche opportunities** — 5 actionable insights
5. **Sources table** — every search result with URL, platform, query used
6. **Footer** — generation metadata

## Cost Estimate

| Item | Per run | Per month (4 runs) |
|------|---------|--------------------|
| Google Custom Search | $0 (free tier) | $0 |
| Claude Sonnet — research (6 calls) | ~$0.015 | ~$0.06 |
| Claude Sonnet — synthesis (6 calls) | ~$0.045 | ~$0.18 |
| Claude Sonnet — newsletter (1 call) | ~$0.010 | ~$0.04 |
| **Total** | **~$0.07** | **~$0.28** |

Prompt caching reduces cost ~60% on repeated weekly runs.

## Customization

**Change niches or locations:**
```python
result = run({
    "niches": ["Real Estate", "Health & Wellness", "Tech Gadgets"],
    "locations": ["Philippines", "Singapore", "Global"],
})
```

**Preview without sending email:**
```python
result = run({"send_email": False, "save_preview": True})
# Open /tmp/newsletter_preview.html in browser
```

**Add platforms:**
Edit `PLATFORMS` at the top of `main.py`:
```python
PLATFORMS = ["reddit.com", "tiktok.com", "instagram.com", "twitter.com"]
```
Note: each extra platform adds 6 more CSE calls.

## Schedule with cron

```bash
# Every Monday at 7am
0 7 * * 1 cd /path/to/claude-automations && python 21-social-trend-newsletter/main.py
```

## Output

`run()` returns:
```json
{
  "week_ending": "June 02, 2025",
  "pairs_analyzed": 6,
  "total_sources": 147,
  "total_trends": 22,
  "syntheses": [...],
  "newsletter_html": "<html>...</html>",
  "email_sent": true
}
```
