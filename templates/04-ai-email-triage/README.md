# AI Email Triage

## What it does
Watches your Gmail inbox, passes each new email to Claude AI for classification into four categories (Urgent, Follow-up, Information, Spam), applies a Gmail label automatically, and for Urgent emails also creates a Notion task and fires a Slack alert.

## Use case
Founders, executives, and busy professionals who receive high email volume and need intelligent prioritisation without manual scanning.

## Prerequisites
- n8n instance (self-hosted or cloud)
- Gmail account with API access
- Notion integration token + task database
- Slack workspace with bot token
- API key from your preferred AI provider

## Configuring the AI Provider

This template uses an HTTP Request node to call an AI provider.

**For Anthropic Claude (recommended):**
- URL: `https://api.anthropic.com/v1/messages`
- Header: `x-api-key: YOUR_KEY`
- Header: `anthropic-version: 2023-06-01`

**For OpenAI:**
- URL: `https://api.openai.com/v1/chat/completions`
- Header: `Authorization: Bearer YOUR_KEY`

Store your API key in n8n: Settings → Credentials → New → Header Auth

## How to import
1. Download `workflow.json`
2. Open n8n → Workflows → Import
3. Upload the JSON file
4. Configure all credentials
5. Create Gmail labels: `URGENT`, `FOLLOW_UP`, `INFORMATION`, `SPAM` and update label IDs in nodes
6. Activate the workflow

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| Gmail Trigger | Google OAuth2 | `gmail.readonly` + `gmail.labels` scope |
| Classify Email (AI) | Header Auth | `x-api-key: YOUR_ANTHROPIC_KEY` |
| Label nodes (×4) | Google OAuth2 | Same Gmail credential |
| Create Notion Task | Notion API | Internal integration token |
| Slack: Urgent Alert | Slack API | Bot token with `chat:write` scope |

## Customization
- Add categories by extending the Switch node and adding corresponding Gmail labels
- Adjust the classification prompt in the HTTP Request body for your email patterns
- Swap claude-haiku for claude-sonnet for higher accuracy at higher cost

## Notes
- Label IDs are account-specific — update them in each Gmail Label node after import
- Email body truncated to 2,000 chars to control token usage
- Poll interval defaults to 1 minute — adjust in Gmail Trigger to reduce API calls
