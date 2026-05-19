#!/usr/bin/env python3
"""Generate insightful weekly business performance reports with trends, analysis, and recommendations."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert business analyst and report writer with deep expertise in SaaS metrics, financial analysis, and executive communication. Your role is to generate concise, insightful weekly business performance reports that help leadership make data-driven decisions.

ANALYTICAL APPROACH:

PERCENTAGE CHANGE CALCULATIONS:
- Always calculate week-over-week (WoW) changes as: ((current - previous) / previous) * 100
- Present positive changes with a + prefix, negative changes with a - prefix
- Round percentages to one decimal place for readability
- Highlight significant changes (>10% swing) as noteworthy

KEY METRICS INTERPRETATION:
- Revenue: Core health indicator. Look for trends, not just absolute values
- New Deals: Pipeline health and sales team effectiveness
- Leads: Top-of-funnel health and marketing effectiveness
- Conversion Rate: Sales efficiency and qualification quality (new_deals / leads * 100)
- Average Deal Size: Product/market positioning and sales quality
- Churn: Customer retention health (higher churn = serious concern requiring immediate attention)

PERFORMANCE RATING CRITERIA:
- Exceptional: Revenue +10% WoW, deals up, churn low/zero, conversion improving
- Strong: Revenue +5-10% WoW, most metrics positive, minor concerns manageable
- On Track: Revenue 0-5% WoW, mixed metrics, expected seasonal patterns
- Needs Attention: Revenue flat or slightly negative (-5-0%), concerning trends in 2+ metrics
- Critical: Revenue down >5% WoW, churn spike, multiple metrics deteriorating

REPORT WRITING STANDARDS:
- Executive summary should be 2-3 sentences, decision-focused, not descriptive
- Highlights should celebrate genuine wins with specific numbers
- Concerns should be frank and actionable, not alarmist
- Recommendations should be specific, prioritized, and executable
- HTML narrative should be professional, use <p> tags for paragraphs, <strong> for emphasis
- Avoid filler phrases like "it is worth noting" or "it should be mentioned"

NARRATIVE STRUCTURE (3 paragraphs):
1. Overall performance assessment with key headline numbers
2. Deep dive into the most significant movement (positive or negative) with context
3. Forward-looking recommendations and next steps

Always output valid JSON only with no additional text, markdown, or explanation."""

def build_prompt(data: dict) -> str:
    metrics = data.get("metrics", {})
    prev = data.get("prev_metrics", {})
    team_notes = data.get("team_notes", [])

    notes_text = "\n".join(f"- {note}" for note in team_notes) if team_notes else "None provided"

    return f"""Please generate a weekly business performance report for the week ending {data.get('week_ending', 'Unknown')}.

CURRENT WEEK METRICS:
- Revenue: ${metrics.get('revenue', 0):,.2f}
- New Deals Closed: {metrics.get('new_deals', 0)}
- Leads Generated: {metrics.get('leads', 0)}
- Conversion Rate: {metrics.get('conversion_rate', 0):.1f}%
- Average Deal Size: ${metrics.get('avg_deal_size', 0):,.2f}
- Churned Customers: {metrics.get('churn', 0)}

PREVIOUS WEEK METRICS:
- Revenue: ${prev.get('revenue', 0):,.2f}
- New Deals Closed: {prev.get('new_deals', 0)}
- Leads Generated: {prev.get('leads', 0)}
- Conversion Rate: {prev.get('conversion_rate', 0):.1f}%
- Average Deal Size: ${prev.get('avg_deal_size', 0):,.2f}
- Churned Customers: {prev.get('churn', 0)}

TEAM NOTES:
{notes_text}

Return a JSON object with exactly these fields:
{{
  "executive_summary": "2-3 sentence executive summary focused on key decisions",
  "performance_rating": "Exceptional|Strong|On Track|Needs Attention|Critical",
  "highlights": ["list of 3-5 specific achievements with numbers"],
  "concerns": ["list of concerns requiring attention, empty array if none"],
  "recommendations": ["list of 3-5 specific, actionable recommendations"],
  "week_over_week": {{
    "revenue_change": "+X.X% to $Y,YYY",
    "deals_change": "+X deals (XX% increase)",
    "leads_change": "+X leads (XX% increase)"
  }},
  "narrative": "<p>Full HTML narrative paragraph 1...</p><p>Paragraph 2...</p><p>Paragraph 3...</p>"
}}"""

def run(input_data: dict) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
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
        "week_ending": "2024-11-08",
        "metrics": {
            "revenue": 142500.00,
            "new_deals": 18,
            "leads": 94,
            "conversion_rate": 19.1,
            "avg_deal_size": 7916.67,
            "churn": 2,
        },
        "prev_metrics": {
            "revenue": 128300.00,
            "new_deals": 14,
            "leads": 87,
            "conversion_rate": 16.1,
            "avg_deal_size": 9164.29,
            "churn": 5,
        },
        "team_notes": [
            "Launched new enterprise tier pricing on Monday which drove larger deal volume",
            "Marketing ran a targeted LinkedIn campaign reaching 12,000 CTOs",
            "Two enterprise deals expected to close next week worth $45,000 combined",
            "Lost one large customer due to competitor pricing - flagged for win/loss analysis",
        ],
    }
    result = run(example)
    print(json.dumps(result, indent=2))
