# Meeting Summarizer

Converts raw meeting transcripts into structured summaries with action items, decisions, and next steps.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `meeting_title`, `date`, `attendees` (list), `meeting_type` (Team Standup/Client Call/Strategy/Sales Call), `transcript` (raw text).

**Output:** `executive_summary`, `key_decisions` (with owners), `action_items` (task/owner/due_date/priority), `discussion_points`, `risks_raised`, `next_meeting_agenda`, `sentiment`.

## Customization

- Pipe transcripts from Otter.ai, Fireflies, or Zoom auto-transcripts directly into `transcript`
- Add `attendee_roles` dict to help the model assign owners more accurately
- Set `meeting_type: "Sales Call"` for CRM-ready output formatting
