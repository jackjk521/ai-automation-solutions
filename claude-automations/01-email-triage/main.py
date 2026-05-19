#!/usr/bin/env python3
"""Classify and triage incoming emails by category, priority, sentiment, and suggested action."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert email triage assistant working for a busy professional. Your job is to analyze incoming emails and classify them with precision to help the recipient manage their inbox efficiently.

When analyzing an email, consider the following dimensions carefully:

CATEGORY CLASSIFICATION:
- Urgent: Emails that require immediate attention within the same business day. Look for keywords like "ASAP", "urgent", "deadline today", "emergency", or time-sensitive requests from important stakeholders.
- Follow-up: Emails that require a response or action but not immediately. Pending decisions, awaiting information, or ongoing project discussions.
- Information: Newsletters, FYI emails, status updates, announcements, or informational content that does not require a direct response.
- Spam: Unsolicited commercial emails, phishing attempts, irrelevant mass mailings, or promotional content that is clearly not requested.

PRIORITY ASSESSMENT:
- High: C-suite executives, key clients, legal matters, financial issues, system outages, or anything with direct business impact.
- Medium: Team members, regular business contacts, project updates, or routine but important communications.
- Low: Mass emails, newsletters, social notifications, or low-impact informational content.

SENTIMENT ANALYSIS:
- Positive: Appreciative, enthusiastic, congratulatory, or constructive tone.
- Neutral: Matter-of-fact, informational, or balanced tone without strong emotion.
- Negative: Frustrated, angry, disappointed, complaining, or escalating tone.

SENDER DOMAIN ANALYSIS:
- Business domains (company.com): Generally higher priority than personal domains (gmail.com, yahoo.com).
- Known client or partner domains should be treated with higher priority.
- Unknown or suspicious domains may indicate spam or phishing.

Always output valid JSON only with no additional text, markdown, or explanation. The draft_reply should be professional, concise, and appropriate for the email's context and sentiment."""

def build_prompt(data: dict) -> str:
    return f"""Please analyze the following email and provide a triage classification.

From: {data.get('sender', 'Unknown')} <{data.get('sender_domain', 'unknown.com')}>
Subject: {data.get('subject', '(no subject)')}

Body:
{data.get('body', '(empty body)')}

Return a JSON object with exactly these fields:
{{
  "category": "Urgent|Follow-up|Information|Spam",
  "priority": "High|Medium|Low",
  "sentiment": "Positive|Neutral|Negative",
  "suggested_action": "brief description of what to do with this email",
  "draft_reply": "a professional draft reply if a response is needed, or empty string if not",
  "tags": ["array", "of", "relevant", "topic", "tags"]
}}"""

def run(input_data: dict) -> dict:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_prompt(input_data)}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r'\{[\s\S]+\}', raw)
    result = json.loads(match.group(0)) if match else {"raw": raw}
    return result


if __name__ == "__main__":
    example = {
        "subject": "URGENT: Server down in production - need immediate help",
        "body": (
            "Hi team,\n\n"
            "Our production server has been down for the last 30 minutes and we are losing "
            "approximately $5,000 per minute in revenue. The on-call engineer is not responding "
            "and we need escalation immediately.\n\n"
            "Please call me on my mobile: +1-555-0123.\n\n"
            "This is critical!\n\n"
            "Best,\nSarah Johnson\nCTO, Acme Corp"
        ),
        "sender": "sarah.johnson",
        "sender_domain": "acmecorp.com",
    }
    result = run(example)
    print(json.dumps(result, indent=2))
