#!/usr/bin/env python3
"""Analyze a business's web presence and generate a personalized agency outreach email."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert web developer and digital agency sales consultant with 15+ years of
experience building and selling web solutions to businesses across industries. You have a sharp eye for
identifying technical debt, missed opportunities, and quick wins that businesses can act on.

Your role is to analyze a business's web presence and produce a detailed assessment that:
1. Scores their web presence honestly on a 0-10 scale
2. Identifies specific technical and strategic issues (framed as opportunities)
3. Generates a compelling, personalized outreach email that doesn't sound like a template
4. Estimates realistic project value based on the scope of work identified
5. Produces talking points for a discovery call

Scoring rubric (0-10 overall):
- 9-10: Modern stack, excellent UX, fast, mobile-first, strong SEO foundations
- 7-8: Good baseline with minor improvements needed
- 5-6: Functional but clearly dated, missing several best practices
- 3-4: Significant issues affecting user experience and conversions
- 1-2: Major problems — old CMS, no SSL, broken elements, very slow
- 0: No website or completely non-functional

Technology age assessment:
- Modern (2022+): React, Next.js, Vue 3, Nuxt, SvelteKit, Astro, Remix
- Current (2018-2021): WordPress 5+, Shopify, Webflow, standard React/Vue
- Aging (2014-2017): WordPress pre-Gutenberg, Bootstrap 3, jQuery-heavy sites
- Legacy (pre-2014): Old PHP, Flash, table layouts, deprecated frameworks

Outreach email principles:
- Open with a specific observation about THEIR business, not a generic compliment
- Mention 1-2 concrete issues you spotted (shows you did your homework)
- Frame all issues as revenue/growth opportunities, never as criticism
- Include a low-commitment CTA (15-minute call, not "hire us now")
- Keep it under 200 words — busy owners don't read walls of text
- Sound like a person, not a marketing department

Project value estimation (USD/year or one-time):
- Basic refresh: $3,000-$8,000
- Full redesign (SMB): $8,000-$25,000
- E-commerce build: $15,000-$50,000+
- Enterprise/custom: $50,000+
- Monthly retainer (SEO + maintenance): $500-$3,000/month

Your output must always be valid JSON. Do not include any text outside the JSON structure."""

def build_prompt(data: dict) -> str:
    business_name = data.get("business_name", "")
    website_url = data.get("website_url", "")
    website_content = data.get("website_content", "")
    niche = data.get("niche", "")
    location = data.get("location", "")
    has_website = data.get("has_website", True)
    tech_stack = data.get("tech_stack", [])
    has_ssl = data.get("has_ssl", True)

    tech_str = ", ".join(tech_stack) if tech_stack else "unknown/not detected"

    return f"""Analyze the following business's web presence and generate a sales outreach package.

BUSINESS NAME: {business_name}
WEBSITE URL: {website_url}
NICHE/INDUSTRY: {niche}
LOCATION: {location}
HAS WEBSITE: {has_website}
DETECTED TECH STACK: {tech_str}
HAS SSL CERTIFICATE: {has_ssl}

WEBSITE CONTENT SAMPLE:
---
{website_content if website_content else "No content provided — assess based on other signals."}
---

Based on this information, produce a complete web presence analysis.

Return valid JSON with this exact structure:
{{
  "overall_score": 6,
  "priority": "High",
  "website_quality": "brief assessment of current quality",
  "tech_stack_age": "Modern|Current|Aging|Legacy",
  "modernisation_needed": true,
  "issues_found": [
    "specific issue 1",
    "specific issue 2"
  ],
  "opportunities": [
    "framed opportunity 1",
    "framed opportunity 2"
  ],
  "outreach_email": {{
    "subject": "compelling subject line",
    "body": "full email body text"
  }},
  "estimated_project_value": "$8,000 - $15,000",
  "talking_points": [
    "talking point for discovery call 1",
    "talking point 2"
  ],
  "competitor_comparison": "brief note on how their web presence compares to typical competitors in this niche"
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
        "business_name": "Hartley's Plumbing & Heating",
        "website_url": "https://hartleysplumbing.co.uk",
        "niche": "Local plumbing and heating services",
        "location": "Manchester, UK",
        "has_website": True,
        "tech_stack": ["WordPress 4.9", "PHP 7.2", "jQuery 1.12", "Bootstrap 3"],
        "has_ssl": False,
        "website_content": """Welcome to Hartley's Plumbing

Est. 1987 | Serving Manchester and surrounding areas

Services:
- Emergency plumbing repairs
- Boiler installation and servicing
- Bathroom fitting
- Central heating

Call us: 0161 555 0123
Email: info@hartleysplumbing.co.uk

Copyright 2018 Hartley's Plumbing. All rights reserved.
Site designed by WebMagic 2018."""
    }
    print(json.dumps(run(example), indent=2))
