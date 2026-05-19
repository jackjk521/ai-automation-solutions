# Email Triage

Automatically classify and prioritize incoming emails by category, priority, sentiment, and suggested action using Claude AI.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

| Field | Type | Description |
|-------|------|-------------|
| **Input: subject** | string | Email subject line |
| **Input: body** | string | Full email body text |
| **Input: sender** | string | Sender's name or username |
| **Input: sender_domain** | string | Sender's email domain (e.g. acmecorp.com) |
| **Output: category** | string | Urgent / Follow-up / Information / Spam |
| **Output: priority** | string | High / Medium / Low |
| **Output: sentiment** | string | Positive / Neutral / Negative |
| **Output: suggested_action** | string | Brief recommended action |
| **Output: draft_reply** | string | A ready-to-send reply draft (or empty string) |
| **Output: tags** | array | Relevant topic tags for filtering |

## Customization

- **Adjust category thresholds**: Edit the `SYSTEM_PROMPT` to redefine what constitutes "Urgent" vs "Follow-up" based on your business context (e.g. VIP sender lists, keywords).
- **Domain-based rules**: Extend `build_prompt()` to pass a list of known client or partner domains so the model can apply higher-priority rules for specific senders.
- **Batch processing**: Call `run()` in a loop over a list of email dicts to triage a full inbox; results can be written to a JSON file or database for downstream filtering.
