# Support Ticket Classifier

Automatically classify incoming customer support tickets by category, priority, and sentiment, then generate professional auto-replies and route them to the correct team.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

| Field | Type | Description |
|-------|------|-------------|
| **Input: ticket_id** | string | Unique identifier for the ticket |
| **Input: subject** | string | Ticket subject line |
| **Input: body** | string | Full ticket body text |
| **Input: customer_name** | string | Customer's name for personalized replies |
| **Input: account_tier** | string | Enterprise / Premium / Standard / Free |
| **Output: category** | string | Billing / Technical / Feature Request / Bug Report / General |
| **Output: priority** | string | Critical / High / Medium / Low |
| **Output: sentiment** | string | Angry / Frustrated / Neutral / Satisfied |
| **Output: estimated_effort** | string | Quick Fix / Standard / Complex |
| **Output: assigned_team** | string | Team name for routing |
| **Output: sla_hours** | int | Hours until first response required |
| **Output: auto_reply** | string | Ready-to-send customer-facing reply |
| **Output: internal_notes** | string | Private notes for the handling agent |

## Customization

- **Team names and routing rules**: Update the `SYSTEM_PROMPT` to match your actual team names and routing logic, including any specialized sub-teams (e.g. "iOS Engineering" vs "Backend Engineering").
- **SLA configuration**: Adjust the SLA hours in the prompt to match your support contracts and tier commitments.
- **Help desk integration**: Pass ticket data from Zendesk, Freshdesk, or Intercom webhooks into `run()` and write the output back as ticket tags, priority, and canned responses via their APIs.
