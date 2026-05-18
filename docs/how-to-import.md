# How to Import an n8n Template

This guide walks you through importing any workflow template from this library into your n8n instance.

---

## Prerequisites

- A running n8n instance (self-hosted or n8n Cloud).
- Access to the credentials required by the specific template (see the template's own `README.md` for a list).
- The `workflow.json` file downloaded from the template folder.

---

## Step 1: Download the Workflow JSON

1. Navigate to the template folder you want to use inside `templates/` (e.g., `templates/04-ai-email-triage/`).
2. Open the `workflow.json` file on GitHub.
3. Click the **Raw** button to view the raw file content.
4. Right-click and choose **Save As**, or use the download button, to save the file as `workflow.json` on your local machine.

Alternatively, clone the entire repository and locate the file locally:

```bash
git clone https://github.com/jackjk521/ai-automation-solutions.git
```

---

## Step 2: Open Your n8n Instance

1. Open your browser and navigate to your n8n instance URL.
2. Log in with your credentials if prompted.

---

## Step 3: Import the Workflow

1. From the n8n dashboard, click **Workflows** in the left sidebar.
2. Click **Import from File** in the top-right menu (or three-dot menu → Import).
3. In the file picker dialog, locate and select the `workflow.json` file.
4. The workflow will load onto the canvas with all nodes and connections visible.

> **Tip:** In n8n v1.x+, you can drag and drop `workflow.json` directly onto the canvas.

---

## Step 4: Configure Credentials

Nodes that require credentials will show a warning indicator. Click each node and configure the credential:

| Service | Credential Type | Where to get it |
|---|---|---|
| Gmail / Google Sheets | Google OAuth2 | Google Cloud Console → OAuth2 credentials |
| Slack | Slack API (Bot Token) | api.slack.com/apps → Install → Bot Token |
| Airtable | Airtable API | airtable.com/create/tokens |
| Notion | Notion API | notion.so/my-integrations |
| SerpAPI | Header Auth | serpapi.com dashboard |
| BuiltWith | Header Auth | builtwith.com/account |
| Anthropic/OpenAI | Header Auth | platform.anthropic.com or platform.openai.com |

---

## Step 5: Test the Workflow

1. Click **Execute Workflow** (play button) in the editor.
2. For webhook triggers, send a test request via curl or Postman.
3. Inspect each node's output — green = success, red = error.
4. Check **Executions** in the sidebar for full run history.

---

## Step 6: Enable the Workflow

1. Toggle the **Active** switch to green in the top-right corner.
2. Give the workflow a descriptive name.
3. Click **Save**.

Your workflow is now live.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Red credential warning | Set up the credential for that node |
| Webhook not receiving requests | Use ngrok for local instances; confirm URL is publicly accessible |
| OAuth2 redirect error | Match redirect URI in Google Cloud Console exactly to your n8n URL |
| AI node error | Check API key, quota, and request body format |
| Empty data from trigger | Verify the trigger is receiving input in the expected format |
