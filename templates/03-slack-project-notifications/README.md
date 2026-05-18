# Slack Project Notifications

## What it does
Receives webhooks from GitHub, Jira, or Trello, identifies the event type, formats a clean Slack message, posts it to the correct project channel, and logs every event to a Google Sheets audit trail.

## Use case
Engineering and product teams who want real-time Slack visibility into PR activity, issue updates, and task completions — without configuring multiple native integrations per tool.

## Prerequisites
- n8n instance (self-hosted or cloud)
- Slack workspace with a bot token
- GitHub / Jira / Trello webhook configured to POST to the n8n webhook URL
- Google Sheets for the audit log

## How to import
1. Download `workflow.json`
2. Open n8n → Workflows → Import
3. Upload the JSON file
4. Configure credentials
5. Activate and copy the webhook URL into GitHub/Jira/Trello webhook settings

## Credentials to configure
| Node | Credential Type | Notes |
|---|---|---|
| Slack (all branches) | Slack API | Bot token with `chat:write` and `channels:read` scopes |
| Google Sheets Log | Google OAuth2 | OAuth2 with spreadsheets.append scope |

## Audit Log Schema
Create a sheet named **Events** with columns:
```
Timestamp | Event Type | Repository/Project | Actor | Title | URL | Channel Posted
```

## Customization
- **Add event types:** Extend the Switch node with extra branches for `push`, `deployment`, `comment`
- **Multiple projects:** Add a sub-Switch on repo/project name to route to different channels
- **Rich formatting:** Replace plain text Slack messages with Block Kit JSON for icons and buttons

## Notes
- GitHub webhooks can optionally use signature verification via `X-Hub-Signature-256` — add an IF node to validate in production
- Jira and Trello payload structures differ from GitHub — inspect raw webhook output and adjust Set node mappings
- Slack Bot must be invited to each target channel before it can post
