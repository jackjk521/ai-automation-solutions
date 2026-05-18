# Support Ticket Classifier

## What it does
Receives support tickets via webhook, sends content to Claude AI to extract Category (Billing/Technical/Feature Request/Bug), Priority (High/Medium/Low), and Sentiment, routes to the appropriate Slack channel, assigns a team member, and sends an auto-acknowledgement email.

## Use case
SaaS companies and support teams who receive tickets from multiple channels and need consistent triage, routing, and fast customer acknowledgement without manual intervention.

## Prerequisites
- n8n instance
- Slack workspace with category channels (`#billing-support`, `#tech-support`, `#feature-requests`, `#bug-reports`)
- Gmail for auto-acknowledgements
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

## How to import
1. Download `workflow.json` and import into n8n
2. Configure all credentials
3. Update Slack channel IDs in each Slack node
4. Activate and point your ticketing system to the webhook URL

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| HTTP Request - AI Classify Ticket | Header Auth | `x-api-key: YOUR_ANTHROPIC_KEY` |
| Slack (×4 channels) | Slack API | Bot token with `chat:write` scope |
| Gmail - Auto Acknowledgement | Gmail OAuth2 | OAuth2 with `gmail.send` scope |

## Webhook Payload
```json
{
  "ticket_id": "TKT-12345",
  "customer_email": "user@example.com",
  "customer_name": "Jane Smith",
  "subject": "Can't access my account",
  "body": "I've been trying to log in for the past hour...",
  "plan": "Pro"
}
```

## Customization
- Edit the AI prompt to use your own ticket categories
- Add Jira/Linear HTTP Request node after routing to auto-create project tickets
- Add Slack DM to manager for Critical priority tickets

## Notes
- Slack channel IDs must be updated post-import (Settings → Channel → Copy channel ID)
- AI response parsing handles malformed JSON gracefully via try/catch in the Set node
- For high volume, add a rate-limit Wait node before the AI call
