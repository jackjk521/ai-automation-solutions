#!/usr/bin/env python3
"""Meeting summarizer — raw transcript → structured summary, action items, and decisions."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert executive assistant and meeting facilitator with years of experience
summarising high-stakes business meetings for C-suite executives.

Your role is to transform raw meeting transcripts into structured, scannable summaries that busy leaders
can act on in under two minutes.

Guidelines:
- Extract only decisions that were explicitly agreed, not just discussed
- Action items must have a clear owner (the person who committed, or "Team" if collective)
- Infer due dates from context: "by end of week" → next Friday, "next sprint" → 2 weeks, "ASAP" → 3 days
- Risks are things mentioned as potential problems, blockers, or concerns
- Next meeting agenda should reflect open items and follow-ups
- Sentiment: Positive (productive, aligned), Neutral (routine, informational), Tense (conflict, disagreement)
- Keep the executive summary to 2-3 sentences maximum
- Do not include filler content or repeat information

Always output valid JSON matching the requested schema. Do not include any text outside the JSON object."""

def build_prompt(data: dict) -> str:
    attendees_str = ", ".join(data.get("attendees", ["Unknown"]))
    return f"""Summarise the following {data.get('meeting_type', 'Meeting')} meeting.

Title: {data.get('meeting_title', 'Team Meeting')}
Date: {data.get('date', 'Today')}
Attendees: {attendees_str}

TRANSCRIPT:
{data.get('transcript', '')}

Return JSON:
{{
  "executive_summary": "2-3 sentence summary",
  "key_decisions": [{{"decision": "...", "owner": "..."}}],
  "action_items": [{{"task": "...", "owner": "...", "due_date": "YYYY-MM-DD or relative", "priority": "High|Medium|Low"}}],
  "discussion_points": ["main topics covered"],
  "risks_raised": ["blockers or concerns mentioned"],
  "next_meeting_agenda": ["suggested agenda items"],
  "sentiment": "Positive|Neutral|Tense",
  "duration_minutes": 0
}}"""


def run(input_data: dict) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_prompt(input_data)}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r'\{[\s\S]+\}', raw)
    return json.loads(match.group(0)) if match else {"raw": raw}


if __name__ == "__main__":
    example = {
        "meeting_title": "Q1 Product Roadmap Planning",
        "date": "2024-01-26",
        "attendees": ["Sarah (PM)", "James (Engineering Lead)", "Priya (Design)", "Mark (CEO)"],
        "meeting_type": "Strategy",
        "transcript": """
Mark: Alright, let's kick off. Sarah, can you walk us through where we landed on the Q1 priorities?

Sarah: Sure. So we've narrowed it down to three core initiatives: the mobile app redesign, the API v2 launch,
and the customer dashboard improvements. We need to pick which gets the most resources.

James: From engineering's perspective, API v2 is the blocker. We have three enterprise clients waiting on it.
If we don't ship by March 15th we risk losing the Acme contract — that's $200k ARR.

Mark: That has to be priority one then. James, what do you need to hit that date?

James: Two more senior engineers. Priya's team also needs to finalize the API docs design by February 9th.

Priya: We can do that. I'll need the endpoint specifications from James by January 31st though.

James: Done. I'll send them over by end of next week.

Sarah: What about the mobile app? We promised the board a beta in Q1.

Mark: We push the full launch to Q2 but keep a small team doing prototype work. We can show the board a
mockup in March. Priya, can you prioritize a 5-screen prototype?

Priya: Yes, I can have that ready by March 1st if I have two designers on it.

Mark: Approved. Sarah, can you update the roadmap doc and send it to the board by Monday?

Sarah: Will do.

James: One risk I want to flag — we're relying on a third-party auth library that hasn't been updated in
8 months. We should evaluate replacing it before the API v2 launch.

Mark: Good catch. James, can you own that evaluation and report back next week?

James: Yes, I'll have a recommendation by Friday.

Mark: Great. Let's meet again next Thursday to check in on progress. Same time?

All: Works for us.
""",
    }
    print(json.dumps(run(example), indent=2))
