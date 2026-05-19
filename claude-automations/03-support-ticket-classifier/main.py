#!/usr/bin/env python3
"""Classify customer support tickets by category, priority, sentiment, and auto-generate replies."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert customer support triage specialist with deep experience in SaaS and enterprise software support operations. Your responsibility is to classify incoming support tickets accurately, assign appropriate priorities, and generate professional auto-replies that set proper customer expectations.

CATEGORY DEFINITIONS:
- Billing: Invoices, charges, refunds, subscription changes, payment failures, pricing questions
- Technical: Software bugs, integration issues, performance problems, API errors, configuration help
- Feature Request: Requests for new functionality, product improvements, enhancement suggestions
- Bug Report: Confirmed reproducible defects with steps to reproduce, unexpected behavior
- General: Questions about how to use the product, best practices, documentation requests

PRIORITY LEVELS (consider account tier heavily):
- Critical: System completely down, data loss risk, security breach, or Enterprise/Premium tier with severe impact. SLA: 1 hour response
- High: Major feature broken, significant productivity impact, or Professional tier with high impact. SLA: 4 hours response
- Medium: Feature partially working, workaround available, or Standard tier with moderate impact. SLA: 8 hours response
- Low: Minor inconvenience, cosmetic issues, general questions, or Free tier. SLA: 24 hours response

ACCOUNT TIER PRIORITY BOOST:
- Enterprise tier: Automatically elevate priority by one level
- Premium tier: Maintain stated priority
- Standard tier: Maintain stated priority
- Free tier: Consider lowering priority if queue is long

SENTIMENT INDICATORS:
- Angry: Demands, threats to cancel, profanity, ALL CAPS, multiple exclamation points, mentions of legal action
- Frustrated: Repeated contacts about same issue, expressions of disappointment, "this is unacceptable"
- Neutral: Factual description, polite but business-like tone
- Satisfied: Appreciative even when reporting issues, positive framing, thank you messages

TEAM ROUTING:
- Billing → Billing & Finance Team
- Technical/Bug Report → Engineering Support Team
- Feature Request → Product Team
- General → Customer Success Team

AUTO-REPLY GUIDELINES:
- Always acknowledge the customer by name
- Reference the specific issue they mentioned
- Provide the SLA/expected response time based on priority
- For Angry/Frustrated sentiment, add empathy and escalation acknowledgment
- Never promise specific fixes or timelines for bugs
- For Enterprise accounts, mention dedicated support contact if applicable

Always output valid JSON only with no additional text, markdown, or explanation."""

def build_prompt(data: dict) -> str:
    return f"""Please classify the following customer support ticket and generate an appropriate auto-reply.

Ticket Details:
- Ticket ID: {data.get('ticket_id', 'Unknown')}
- Customer Name: {data.get('customer_name', 'Unknown')}
- Account Tier: {data.get('account_tier', 'Standard')}
- Subject: {data.get('subject', '(no subject)')}

Ticket Body:
{data.get('body', '(empty body)')}

Return a JSON object with exactly these fields:
{{
  "category": "Billing|Technical|Feature Request|Bug Report|General",
  "priority": "Critical|High|Medium|Low",
  "sentiment": "Angry|Frustrated|Neutral|Satisfied",
  "estimated_effort": "Quick Fix|Standard|Complex",
  "assigned_team": "name of the team to handle this ticket",
  "sla_hours": <integer number of hours for first response>,
  "auto_reply": "professional customer-facing auto-reply message",
  "internal_notes": "brief internal notes for the support agent picking up this ticket"
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
        "ticket_id": "TKT-20241105-8842",
        "subject": "API rate limit errors breaking our production integration",
        "body": (
            "We are an Enterprise customer and have been experiencing consistent 429 rate limit "
            "errors from your API since 9 AM this morning. This is completely breaking our "
            "production pipeline which processes over 10,000 transactions per hour for our "
            "banking clients.\n\n"
            "We have not changed anything on our end. Our current plan is supposed to support "
            "1000 requests/minute but we are seeing limits at around 200 requests/minute.\n\n"
            "This is causing significant financial and reputational damage. I need this resolved "
            "IMMEDIATELY or we will be escalating to our account executive and considering "
            "contract termination.\n\n"
            "Error: HTTP 429 - Rate limit exceeded\n"
            "Endpoint: POST /v1/transactions\n"
            "Account ID: ENT-4471"
        ),
        "customer_name": "David Martinez",
        "account_tier": "Enterprise",
    }
    result = run(example)
    print(json.dumps(result, indent=2))
