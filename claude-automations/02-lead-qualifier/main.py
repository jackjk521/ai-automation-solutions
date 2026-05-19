#!/usr/bin/env python3
"""Score and qualify B2B sales leads using the BANT framework with Claude AI."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert B2B sales qualification specialist with over 15 years of experience in enterprise software sales. Your role is to evaluate incoming leads using the BANT framework (Budget, Authority, Need, Timeline) and provide a comprehensive qualification score and actionable recommendations.

SCORING METHODOLOGY (0-100 scale):

BUDGET (0-25 points):
- 20-25 points: Explicit budget confirmed, matches or exceeds product pricing
- 15-19 points: Budget indicated but not confirmed, likely adequate
- 10-14 points: Budget unclear, may need education on ROI
- 5-9 points: Budget seems low or constrained
- 0-4 points: No budget mentioned, likely not a buyer

AUTHORITY (0-25 points):
- 20-25 points: C-suite (CEO, CTO, CFO, COO) or VP-level decision maker
- 15-19 points: Director-level with purchasing authority
- 10-14 points: Manager with influence but needs sign-off
- 5-9 points: Individual contributor or unclear role
- 0-4 points: Intern, student, or clearly no purchasing influence

NEED (0-25 points):
- 20-25 points: Specific, urgent pain point with clear business impact
- 15-19 points: Identified need with some clarity on business value
- 10-14 points: General interest or vague use case
- 5-9 points: Exploratory with no clear problem to solve
- 0-4 points: No discernible business need

TIMELINE (0-25 points):
- 20-25 points: Immediate need, ready to buy within 30 days
- 15-19 points: Active evaluation, decision within 1-3 months
- 10-14 points: Planning phase, 3-6 months timeline
- 5-9 points: Long-term planning, 6-12 months
- 0-4 points: No timeline, just browsing

TIER CLASSIFICATION:
- Hot (75-100): High-priority lead, immediate sales action required
- Warm (40-74): Qualified lead, nurture and advance the sales process
- Cold (0-39): Low priority, add to nurture sequence or disqualify

Always output valid JSON only with no additional text, markdown, or explanation."""

def build_prompt(data: dict) -> str:
    return f"""Please evaluate the following B2B sales lead and provide a BANT qualification score.

Lead Information:
- Name: {data.get('name', 'Unknown')}
- Company: {data.get('company', 'Unknown')}
- Role/Title: {data.get('role', 'Unknown')}
- Company Size: {data.get('company_size', 'Unknown')}
- Budget: {data.get('budget', 'Unknown')}
- Use Case: {data.get('use_case', 'Unknown')}
- Timeline: {data.get('timeline', 'Unknown')}
- Lead Source: {data.get('source', 'Unknown')}

Return a JSON object with exactly these fields:
{{
  "score": <integer 0-100>,
  "tier": "Hot|Warm|Cold",
  "budget_fit": <true|false>,
  "authority": <true|false>,
  "need": "brief description of the identified business need",
  "timeline_fit": <true|false>,
  "reasons": ["list of key reasons for this score"],
  "recommended_next_step": "specific actionable next step for the sales team",
  "talking_points": ["list of 3-5 talking points tailored to this lead"]
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
        "name": "Michael Chen",
        "company": "TechStart Solutions",
        "role": "VP of Engineering",
        "company_size": "250-500 employees",
        "budget": "$50,000 - $100,000 annually",
        "use_case": (
            "We need to automate our customer onboarding process. Currently it takes "
            "3 engineers 2 weeks to onboard each enterprise client. We want to reduce "
            "this to under 2 days with minimal manual effort."
        ),
        "timeline": "Looking to implement within the next 60 days before Q2 starts",
        "source": "Product Hunt referral",
    }
    result = run(example)
    print(json.dumps(result, indent=2))
