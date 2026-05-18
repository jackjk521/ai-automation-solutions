# Real Estate Lead Nurture

## What it does
Automatically captures new property inquiries via webhook, logs them to a Google Sheets CRM, sends a personalised introduction email, waits 3 days, checks whether the lead replied, and sends a tailored follow-up email.

## Use case
Real estate agents and property agencies who receive leads from web forms, Typeform, or listing portals. Eliminates manual follow-up and ensures no lead falls through the cracks during the critical first 72 hours.

## Prerequisites
- n8n instance (self-hosted or cloud)
- Google account with Sheets and Gmail API access
- A Google Sheet named **Leads** with the columns listed below

## How to import
1. Download `workflow.json`
2. Open n8n → Workflows → Import
3. Upload the JSON file
4. Configure credentials
5. Update the Google Sheet ID in both Sheets nodes
6. Activate the workflow

## Google Sheets columns
```
Lead ID | First Name | Last Name | Email | Phone | Property Interest | Budget | Location | Source | Inquiry Date | Status | Message | Replied | Last Contact Date | Next Action
```

Set **Replied** = `Yes` for a row to prevent the follow-up email from sending.

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| Add to CRM Sheet | Google Sheets OAuth2 | Connect your Google account |
| Check Reply Status | Google Sheets OAuth2 | Same credential |
| Log Outcome | Google Sheets OAuth2 | Same credential |
| Send Intro Email | Gmail OAuth2 | The sending agent's Gmail |
| Send Follow-up Email | Gmail OAuth2 | Same Gmail credential |

## Customization
- **Agent details:** Update sender name, phone, email signature, and Calendly links in both Gmail nodes
- **Follow-up timing:** Change the Wait node from 3 days to suit your sales process
- **Third touchpoint:** Add a Day 7 email node after the follow-up for high-value leads

## Notes
- The `Replied` column must be manually updated (or via another automation) when a lead responds
- Requires n8n to remain active for Wait nodes to function — use self-hosted for production
- For production, consider Gmail API reply detection instead of a manual `Replied` column
