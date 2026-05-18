# Weekly Report Generator

## What it does
Runs every Friday at 5pm, pulls weekly KPIs from Google Sheets, calculates metrics (revenue, conversion rate, avg deal size), asks Claude AI to write an executive narrative, compiles a branded HTML report, and emails it to your distribution list.

## Use case
Sales managers, founders, and ops teams who want a zero-effort weekly business intelligence report delivered to their inbox with AI-written narrative.

## Prerequisites
- n8n instance
- Google Sheets with weekly activity data
- Gmail / Google Workspace for sending
- Anthropic or OpenAI API key

## Configuring the AI Provider

**For Anthropic Claude (recommended):**
- URL: `https://api.anthropic.com/v1/messages`
- Header: `x-api-key: YOUR_KEY`
- Header: `anthropic-version: 2023-06-01`

**For OpenAI:**
- URL: `https://api.openai.com/v1/chat/completions`
- Header: `Authorization: Bearer YOUR_KEY`

Store in n8n: Settings → Credentials → New → Header Auth

## Google Sheets Data Format
Create a sheet named **Weekly Data** with columns:
```
Date | Type | Status | DealValue | SalesRep | Client | Notes
```
- **Type:** Lead, Demo, Proposal, Deal
- **Status:** Open, Closed, Lost
- **DealValue:** numeric (e.g. 5000)

## How to import
1. Download and import `workflow.json` into n8n
2. Configure credentials
3. Set `REPORT_SHEET_ID` in Settings → Variables
4. Update recipient emails in Gmail node
5. Activate

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| Fetch Weekly Data | Google Sheets OAuth2 | OAuth2 with spreadsheets.readonly scope |
| Generate AI Narrative | Header Auth | `x-api-key: YOUR_ANTHROPIC_KEY` |
| Send Report Email | Gmail OAuth2 | OAuth2 with gmail.send scope |

## Customization
- Add custom KPIs in the Code node (churn rate, NPS, pipeline velocity)
- Change cron `0 17 * * 5` — e.g., `0 8 * * 1` for Monday 8am
- Edit AI prompt tone: "be optimistic" or "be direct and critical"

## Notes
- Rows capped at 20 for AI prompt — adjust the slice in Code node for more data
- HTML report uses inline CSS for maximum email client compatibility
- Add a second Sheets read for last week's data to calculate week-over-week delta
