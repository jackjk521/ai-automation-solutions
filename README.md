# n8n Automation Template Library

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Templates](https://img.shields.io/badge/templates-9-indigo.svg)](#template-index)
[![AI Powered](https://img.shields.io/badge/AI--powered-4-orange.svg)](#ai-powered-templates)

Production-ready n8n workflow templates for lead generation, AI email triage, invoice automation, web scraping, and more. Free, open source, and ready to import in 60 seconds.

**Author:** Jed Abner Chu · [aceinternational.solutions](https://aceinternational.solutions)

---

## Quick Start

Import any template in 3 steps:

1. **Download** the `workflow.json` from the template folder
2. **Import** in n8n → Workflows → Import from File
3. **Configure** credentials for the services used (see each template's README)

---

## Template Index

| # | Template | Integrations | AI-Powered | Trigger |
|---|---------|-------------|-----------|-------|
| 01 | [Lead Capture to CRM](templates/01-lead-capture-to-crm/) | Gmail · Slack · Airtable | No | Webhook |
| 02 | [Invoice Automation](templates/02-invoice-automation/) | Google Sheets · Gmail | No | Schedule |
| 03 | [Slack Project Notifications](templates/03-slack-project-notifications/) | Slack · Google Sheets | No | Webhook |
| 04 | [AI Email Triage](templates/04-ai-email-triage/) | Gmail · Notion · Slack | ✅ Yes | Gmail |
| 05 | [Real Estate Lead Nurture](templates/05-real-estate-lead-nurture/) | Google Sheets · Gmail | No | Webhook |
| 06 | [Support Ticket Classifier](templates/06-support-ticket-classifier/) | Slack · Gmail | ✅ Yes | Webhook |
| 07 | [Weekly Report Generator](templates/07-weekly-report-generator/) | Google Sheets · Gmail | ✅ Yes | Schedule |
| 08 | [Client Onboarding Sequence](templates/08-client-onboarding-sequence/) | Gmail · Notion · Slack · Google Sheets | No | Webhook |
| 09 | [Web Scraping Business Analysis & Outreach](templates/09-web-scraping-business-analysis/) | Google Sheets · Gmail · SerpAPI · BuiltWith | ✅ Yes | Manual |

---

## AI-Powered Templates

Templates 04, 06, 07, and 09 call AI providers via an **HTTP Request node**. Swap providers by changing one URL and one header:

**Anthropic Claude:**
```
URL: https://api.anthropic.com/v1/messages
Header: x-api-key: YOUR_KEY
Header: anthropic-version: 2023-06-01
```

**OpenAI:**
```
URL: https://api.openai.com/v1/chat/completions
Header: Authorization: Bearer YOUR_KEY
```

**Groq:**
```
URL: https://api.groq.com/openai/v1/chat/completions
Header: Authorization: Bearer YOUR_KEY
```

Store your API key in n8n: Settings → Credentials → New → Header Auth.

---

## Template 09 — Web Scraping Business Analysis

The flagship automation for finding businesses that need a website or redesign:

- **Scrapes Google** via SerpAPI for businesses in any niche + region
- **Analyses tech stacks** via BuiltWith API
- **Scores each website** (0–10) based on SSL, framework, tech stack age
- **Generates personalised outreach emails** via Claude AI
- **Stores all leads** in Google Sheets with 20-column tracking schema
- **Target:** 3 niches/week × 10 leads each = 30–40 qualified prospects/month

### Weekly Niche Strategy
| Run | Niche | Region |
|-----|-------|--------|
| Tuesday | Dental Clinic | Australia |
| Wednesday | Law Firm | United Kingdom |
| Thursday | Restaurant | United States |

**Top target niches globally:** Dental/Medical (AU/UK/USA), Law Firms (UK/AU), Restaurants (USA/UK), Real Estate (USA/AU/UAE), Accounting (UK/AU/CA), Gyms (USA/UAE), Beauty Salons (USA/UK), Plumbers/Electricians (USA/CA/AU)

### Lead Tracker Columns
`Date Added · Business Name · Website URL · Niche · Location · Has Website · Tech Stack · Site Score · Priority · Has SSL · Phone · Address · Email Subject · Email Body · Outreach Status · Follow-up Date · Contract Value · Notes`

---

## Showcase Website

A Next.js 14 + Tailwind CSS static showcase site is in the `/showcase` directory.

```bash
cd showcase
npm install
npm run dev
```

Deploy to Vercel: connect repo, set root directory to `showcase`, no env vars needed.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Requirements: `workflow.json` + `README.md` + `preview.png`, valid JSON with `nodes`, `connections`, and `meta` fields, no hardcoded credentials.

---

## License

MIT © 2024 Jed Abner Chu ([aceinternational.solutions](https://aceinternational.solutions))
