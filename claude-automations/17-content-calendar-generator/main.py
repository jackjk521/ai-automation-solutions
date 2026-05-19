#!/usr/bin/env python3
"""Generate a monthly content calendar with post ideas, hooks, and hashtags for multiple platforms."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert content strategist and social media manager with over a decade of
experience building brand audiences across LinkedIn, Twitter/X, Instagram, and long-form blog content.
You create data-driven content calendars that consistently grow engagement and convert followers into
customers.

Your content calendars follow proven principles:
- The 80/20 rule: 80% value-driven content (educational, inspirational, entertaining), 20% promotional
- Content variety: mix Educational, Promotional, Engagement, Story, and Case Study post types
- Platform-specific optimization: LinkedIn favors professional insights and thought leadership; Twitter
  excels with punchy observations and threads; Instagram thrives on visual storytelling and aspirational content
- The hook is everything: the first line must stop the scroll and compel a read
- Hashtag strategy: 3-5 highly relevant tags per post, mixing broad (#marketing) and niche (#b2bsaas)
- Consistent themes: 3-5 overarching monthly themes that tie content together into a cohesive narrative
- Campaign integration: identify opportunities for coordinated multi-platform campaigns

When generating a calendar, consider the month's context (seasons, holidays, industry events) and
align content timing with the brand's goals. Each post should have a specific, actionable angle — not
just a vague topic, but a concrete perspective or takeaway.

Your output must always be valid JSON only. Do not include any text outside the JSON structure."""

def build_prompt(data: dict) -> str:
    brand_name = data.get("brand_name", "")
    industry = data.get("industry", "")
    target_audience = data.get("target_audience", "")
    content_goals = data.get("content_goals", [])
    platforms = data.get("platforms", [])
    posting_frequency = data.get("posting_frequency", {})
    brand_voice = data.get("brand_voice", "")
    avoid_topics = data.get("avoid_topics", [])
    month = data.get("month", "")
    year = data.get("year", 2025)

    goals_str = ", ".join(content_goals)
    platforms_str = ", ".join(platforms)
    avoid_str = ", ".join(avoid_topics) if avoid_topics else "none"
    freq_str = json.dumps(posting_frequency)

    return f"""Create a full content calendar for {month} {year} for the following brand:

BRAND: {brand_name}
INDUSTRY: {industry}
TARGET AUDIENCE: {target_audience}
CONTENT GOALS: {goals_str}
ACTIVE PLATFORMS: {platforms_str}
POSTING FREQUENCY: {freq_str}
BRAND VOICE: {brand_voice}
AVOID THESE TOPICS: {avoid_str}

Generate a realistic calendar for the month. Distribute posts across weeks and days logically.
Include only posts for the platforms listed, respecting the posting frequency for each.

Return valid JSON with this structure:
{{
  "calendar": [
    {{
      "week": 1,
      "day": "Monday",
      "date": "2025-01-06",
      "platform": "LinkedIn",
      "content_type": "Educational",
      "topic": "specific topic title",
      "angle": "the unique angle or perspective for this post",
      "caption_hook": "compelling first line to stop the scroll",
      "hashtags": ["#tag1", "#tag2", "#tag3"]
    }}
  ],
  "content_themes": ["theme 1", "theme 2", "theme 3"],
  "campaign_ideas": ["campaign idea 1", "campaign idea 2"],
  "best_posting_times": [{{"platform": "LinkedIn", "time": "8:00 AM Tuesday"}}]
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
        "brand_name": "GrowthStack",
        "industry": "B2B SaaS / Marketing Technology",
        "target_audience": "Marketing managers and CMOs at mid-market companies (50-500 employees)",
        "content_goals": [
            "Increase brand awareness",
            "Generate demo requests",
            "Establish thought leadership in marketing analytics"
        ],
        "platforms": ["linkedin", "twitter"],
        "posting_frequency": {
            "linkedin": 3,
            "twitter": 5,
            "instagram": 0,
            "blog": 1
        },
        "brand_voice": "Data-driven, approachable, slightly witty — like a smart colleague, not a corporate press release",
        "avoid_topics": ["politics", "competitor bashing", "unverified statistics"],
        "month": "February",
        "year": 2025
    }
    print(json.dumps(run(example), indent=2))
