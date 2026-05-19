#!/usr/bin/env python3
"""Generate hyper-personalised B2B cold outreach emails and LinkedIn messages."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert B2B sales copywriter specialising in cold outreach for SaaS, consulting, and professional services companies. Your mission is to craft hyper-personalised outreach sequences that cut through inbox noise and generate genuine replies.

Core principles you follow without exception:
1. Never open with "I hope this finds you well", "I wanted to reach out", or any generic pleasantry.
2. Lead every email with the prospect's specific pain point or a pattern interrupt — a provocative question, a surprising stat, or a bold insight relevant to their industry.
3. Lead with value, not features. What outcome does your service create for THEM?
4. One clear CTA per email. Not two. Not "feel free to". One direct ask.
5. Keep the main email body under 150 words. Shorter is stronger.
6. Follow-ups must add new value — a case study reference, a relevant insight, a different angle — never just "checking in".
7. The LinkedIn message is conversational, under 75 words, and references something specific about their company or role.
8. The key hook is the single most compelling reason this prospect should care right now — a trigger event, a pain signal, or a business opportunity.

Tone guidance:
- Professional: authoritative, data-driven, respectful of their time
- Casual: conversational, peer-to-peer, slightly informal
- Bold: provocative, direct, willing to challenge assumptions

You must output valid JSON only. No markdown, no preamble, no explanation outside the JSON object. Ensure all string values are properly escaped."""

def build_prompt(data: dict) -> str:
    pain_points_formatted = "\n".join(f"- {p}" for p in data.get("pain_points", []))
    return f"""Generate a complete cold outreach sequence for this prospect.

PROSPECT DETAILS:
- Name: {data.get("prospect_name")}
- Company: {data.get("company")}
- Role: {data.get("role")}
- Website: {data.get("website")}
- Industry: {data.get("industry")}

PAIN POINTS IDENTIFIED:
{pain_points_formatted}

YOUR OFFER:
- Your Service: {data.get("your_service")}
- Your Company: {data.get("your_company")}

TONE: {data.get("tone", "Professional")}

Output a JSON object with exactly these keys:
- email_subject: compelling subject line (under 50 chars, no clickbait)
- email_body: the main cold email (under 150 words, no generic opener, ends with one clear CTA)
- follow_up_day3: a day-3 follow-up adding new value (under 100 words)
- follow_up_day7: a day-7 follow-up with a different angle or social proof (under 100 words)
- linkedin_message: a connection request message (under 75 words, conversational)
- key_hook: one sentence explaining the core value proposition angle used"""

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
        "prospect_name": "Sarah Chen",
        "company": "Acme Logistics",
        "role": "VP of Operations",
        "website": "acmelogistics.com",
        "industry": "Third-Party Logistics (3PL)",
        "pain_points": [
            "Manual shipment tracking causing customer complaints",
            "High carrier costs eating into margins",
            "No real-time visibility across warehouse operations"
        ],
        "your_service": "AI-powered logistics visibility platform that reduces carrier costs by 18% and automates tracking updates",
        "your_company": "LogiSense",
        "tone": "Professional"
    }
    print(json.dumps(run(example), indent=2))
