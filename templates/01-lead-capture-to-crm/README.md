# Lead Capture to CRM

## What it does
Receives form submissions via webhook, deduplicates leads against Airtable, creates new records or updates existing ones, sends a personalised welcome email, and pings your sales team on Slack — all in real time.

## Use case
Sales and marketing teams that collect inbound leads from website contact forms, landing pages, or third-party tools (Typeform, Tally, Webflow) and need them instantly available in a CRM with zero manual entry.

## Prerequisites
- n8n instance (self-hosted or cloud)
- Airtable account with a **Leads** base
- Gmail account with API access enabled
- Slack workspace with bot token

## How to import
1. Download `workflow.json`
2. Open n8n → **Workflows** → **Import from file**
3. Upload `workflow.json`
4. Configure credentials (see below)
5. Set the `AIRTABLE_BASE_ID` variable under **Settings → Variables**
6. Activate the workflow and copy the generated webhook URL into your form

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| Search Existing Lead | Airtable API | Personal access token from airtable.com/create/tokens |
| Create Lead in Airtable | Airtable API | Same credential |
| Update Duplicate Lead | Airtable API | Same credential |
| Send Welcome Email | Gmail OAuth2 | Authorize via Google OAuth in n8n |
| Notify Sales on Slack | Slack API | Bot token with `chat:write` scope |
| Alert on Error | Slack API | Same credential; update channel to `#ops-alerts` |

## Airtable Schema
Create a table called **Leads** with these fields:

| Field | Type |
|---|---|
| First Name | Single line text |
| Last Name | Single line text |
| Email | Email |
| Company | Single line text |
| Phone | Phone number |
| Source | Single line text |
| Status | Single select (New, Re-Engaged, Qualified, Closed) |
| Created At | Date |
| Last Seen | Date |
| Touch Count | Number |
| Latest Source | Single line text |

## Customization
- **Duplicate logic:** Current check matches on email only. Add phone deduplication with `OR({Email}="...", {Phone}="...")`
- **Field mapping:** The `Normalize Fields` Set node is the single source of truth — add new fields there
- **Route by source:** Insert a Switch node after `Is Duplicate?` to send leads from different sources to different Slack channels

## Notes
- The webhook URL changes if you delete and re-import the workflow — update your form endpoint
- Airtable free tier: 5 requests/second. For bulk imports, add a Wait node (1-2s) inside loops
- Ensure the Gmail `From` address matches your domain's SPF/DKIM records to avoid spam filtering
