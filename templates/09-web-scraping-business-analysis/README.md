# Web Scraping Business Analysis & Outreach

Manually-triggered workflow that scrapes Google for businesses with missing or outdated websites, analyses their tech stack via BuiltWith, scores each site 0–10, generates personalised outreach emails via Claude AI, and stores everything in Google Sheets.

**Trigger:** Manual (review AI-generated emails before sending)
**Target:** 3 niches/week × 10 leads = 30–40 qualified prospects/month

---

## Workflow Steps

| Node | What It Does |
|------|-------------|
| Manual Trigger | Start run on demand |
| Set Config | Set niche, region, target count, week number |
| SerpAPI Google Search | Search Google for businesses in niche + region |
| Parse Search Results | Extract company, URL, domain, address, phone, rating |
| Loop Over Businesses | Process one lead at a time |
| Has Website? | Branch: existing site vs. no site |
| BuiltWith Tech Stack | Analyse CMS, frameworks, SSL, hosting (TRUE branch) |
| Score Website Quality | Score 0–10 based on SSL, tech age, modernity |
| Mark No Website | Score = 0, Priority = High (FALSE branch) |
| Merge Paths | Rejoin both branches |
| Generate Outreach Email | Claude AI writes personalised email per lead |
| Parse Email + Build Record | Extract subject line, set follow-up date (+7 days) |
| Store Lead in Google Sheets | Append all 20 columns to Leads tab |
| Draft Outreach Email | **DISABLED by default** — enable after reviewing drafts |
| Log Status | Record completion timestamp |

---

## Scoring Logic

| Factor | Points Deducted |
|--------|----------------|
| No SSL (HTTP only) | −3 |
| Outdated CMS (WordPress 3/4, Joomla, Drupal 6/7) | −3 |
| No modern framework (React, Vue, Angular, Next.js) | −2 |
| Very sparse tech stack (<3 technologies) | −2 |
| **Max score** | **10** |

Priority: High (0–3) · Medium (4–6) · Low (7–10)

---

## Google Sheets Schema (20 columns)

| Column | Description |
|--------|-------------|
| Date Added | ISO date |
| Week | Week number of the year |
| Business Name | Company name from Google |
| Website URL | Full URL |
| Niche | e.g. dental clinic |
| Location | e.g. London, UK |
| Has Website | Yes / No |
| Tech Stack | Comma-separated tech list |
| Site Score | 0–10 |
| Priority | High / Medium / Low |
| Has SSL | Yes / No |
| Phone | Phone number |
| Address | Street address |
| Email Subject | AI-generated subject line |
| Email Body | AI-generated email body |
| Outreach Status | Draft / Sent / Replied / Closed |
| Follow-up Date | Date + 7 days from run |
| Contract Value | Fill in manually after contact |
| Notes | Free-form notes |

---

## Prerequisites

- n8n instance (cloud or self-hosted)
- SerpAPI account + API key → [serpapi.com](https://serpapi.com)
- BuiltWith API key → [builtwith.com](https://builtwith.com)
- Anthropic API key stored in n8n Header Auth credential
- Google Sheets with Leads tab (column headers from schema above)
- Gmail account (for the disabled outreach node)

---

## Credentials to Configure

| Node | Credential Type | Notes |
|------|----------------|-------|
| SerpAPI Google Search | Header Auth | `api_key` as query param or `Authorization: Bearer KEY` |
| BuiltWith Analyse Tech Stack | Header Auth | `KEY` as query param |
| Generate Outreach Email | Header Auth | `x-api-key: YOUR_ANTHROPIC_KEY` + `anthropic-version: 2023-06-01` |
| Store Lead in Google Sheets | Google Sheets OAuth2 | OAuth2 with spreadsheets read/write scope |
| Draft Outreach Email | Gmail OAuth2 | OAuth2 with gmail.compose scope — **node disabled by default** |

---

## Weekly Niche Strategy

| Week | Monday | Wednesday | Friday |
|------|--------|-----------|--------|
| 1 | Dental Clinic (AU) | Law Firm (UK) | Restaurant (USA) |
| 2 | Accounting (CA) | Gym (UAE) | Real Estate (AU) |
| 3 | Spa/Salon (USA) | Vet Clinic (UK) | Plumber (CA) |
| 4 | Chiropractor (NZ) | Insurance Agent (US) | Car Repair (SG) |

---

## Customization

- Change `niche` and `target_region` in the **Set Config** node for each run
- Edit the Claude prompt in **Generate Outreach Email** to adjust email tone and length
- Enable the **Draft Outreach Email** Gmail node only after reviewing AI drafts in Sheets
- Increase `target_count` in Set Config to fetch more than 10 results per niche

---

## License

MIT © 2024 Jed Abner Chu ([aceinternational.solutions](https://aceinternational.solutions))
