# Client Onboarding Sequence

## What it does
Triggers when a new client is marked active. Sends a branded welcome email and creates a Notion onboarding workspace immediately. Across Days 1, 3, and 7, sends a Getting Started guide, notifies the account manager in Slack, and sends a week-one check-in — logging the completed sequence to Google Sheets.

## Use case
SaaS companies, agencies, and service businesses that want a consistent, professional onboarding experience for every new client without manual scheduling.

## Prerequisites
- n8n instance (self-hosted recommended for Wait nodes)
- Gmail / Google Workspace account
- Notion integration with onboarding database
- Slack workspace with bot token
- Google Sheets for completion logging

## How to import
1. Download and import `workflow.json`
2. Configure all credentials
3. Update `YOUR_NOTION_ONBOARDING_DB_ID` and `YOUR_ONBOARDING_SHEET_ID` in the respective nodes
4. Update company name/branding in each Gmail node's HTML
5. Activate the workflow

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| Gmail nodes (×3) | Gmail OAuth2 | OAuth2 with gmail.send scope |
| Create Notion Onboarding Page | Notion API | Internal integration token |
| Slack: Notify Account Manager | Slack API | Bot token with chat:write scope |
| Log Completion to Sheets | Google Sheets OAuth2 | OAuth2 with spreadsheets.append scope |

## Webhook Payload
```json
{
  "client_name": "Acme Corp",
  "contact_name": "Jane Smith",
  "email": "jane@acmecorp.com",
  "plan": "Professional",
  "account_manager": "Alex Johnson",
  "am_slack_id": "U0123456789"
}
```

## Google Sheets Completion Log
Sheet named **Onboarded Clients** with columns:
```
Client Name | Contact Name | Email | Plan | Account Manager | Onboarding Start | Sequence Completed | Status
```

## Customization
- Personalise email templates with your brand, Calendly links, product URLs
- Add Day 14/30 touchpoints for extended nurture
- Add HubSpot/Salesforce HTTP Request node to update deal stage automatically

## Notes
- n8n Wait nodes require the workflow to stay continuously active — use self-hosted n8n for production
- `am_slack_id` must be the Slack member ID, not username (right-click profile → Copy member ID)
- Welcome Email and Notion page creation run in parallel; both feed into Wait 1 Day
