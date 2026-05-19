#!/usr/bin/env python3
"""Analyse and optimise content for SEO, readability, and search intent alignment."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert SEO content strategist and editor with deep knowledge of Google's ranking algorithms, E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) principles, and modern search intent optimisation.

Your analysis framework covers:

SEARCH INTENT ALIGNMENT — Does the content match what users actually want when they search this keyword? Identify if the intent is informational, navigational, transactional, or commercial, and whether the content serves it.

KEYWORD OPTIMISATION — Analyse primary keyword placement (title, H1, first 100 words, meta description, URL slug), density (ideal: 0.5-2.5%), and natural secondary keyword integration. Flag keyword stuffing and missed opportunities.

HEADING HIERARCHY — Evaluate H1, H2, H3 structure for logical flow, keyword inclusion, and featured snippet eligibility. Recommend a complete heading structure that could win position-zero snippets.

META DATA — Title tag (50-60 chars), meta description (150-160 chars), and URL slug should be compelling, keyword-rich, and click-worthy.

READABILITY — Assess sentence length, paragraph structure, active vs passive voice, and Flesch-Kincaid grade level. Content should be readable at the appropriate level for the target audience.

E-E-A-T SIGNALS — Look for: author credentials, citations and statistics, original research or data, expert quotes, publication date, and trust signals. These are critical for YMYL (Your Money Your Life) topics.

INTERNAL LINKING OPPORTUNITIES — Suggest anchor text and conceptually related content that should be linked for topical authority.

SCHEMA MARKUP — Recommend the most appropriate Schema.org type for rich result eligibility.

SEO SCORE: Rate the overall SEO quality 0-100 based on all factors.

Severity levels for issues: High (will significantly hurt rankings), Medium (missing opportunities), Low (minor refinements).

You must output valid JSON only. No markdown, no preamble, no explanation outside the JSON object. Ensure all string values are properly escaped."""

def build_prompt(data: dict) -> str:
    secondary_keywords = ", ".join(data.get("secondary_keywords", []))
    return f"""Perform a comprehensive SEO analysis and optimisation for the following content.

CONTENT DETAILS:
- Title: {data.get("title")}
- Target Keyword: {data.get("target_keyword")}
- Secondary Keywords: {secondary_keywords}
- Target Audience: {data.get("target_audience")}
- Content Type: {data.get("content_type", "Blog Post")}

CONTENT TO ANALYSE:
{data.get("content")}

Output a JSON object with exactly these keys:
- seo_score: integer 0-100 representing overall SEO quality
- optimized_title: improved title tag (50-60 characters) with keyword
- meta_description: compelling meta description (150-160 characters) with keyword and CTA
- slug: SEO-friendly URL slug (lowercase, hyphens, keyword-first)
- heading_structure: array of objects, each with "level" ("h2" or "h3") and "text" (suggested heading), forming a complete article outline
- keyword_density: string describing current density and whether it is optimal (e.g. "0.8% — within optimal range")
- readability_score: string describing reading level and ease (e.g. "Grade 9 — appropriate for general audience")
- improvements: array of objects, each with "issue" (description), "severity" ("High", "Medium", or "Low"), and "fix" (specific action to take)
- optimized_intro: rewritten opening paragraph (first 150 words) optimised for search intent and keyword placement
- internal_link_suggestions: array of strings, each a suggested anchor text phrase to link to related content
- schema_type: recommended Schema.org type (e.g. "Article", "HowTo", "FAQPage", "Product")"""

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
        "title": "How to Start Investing in Index Funds",
        "content": """Investing can seem complicated but index funds make it simple. An index fund is a type of investment that tracks a market index like the S&P 500. They are popular because of their low fees and diversification.

To get started you need to open a brokerage account. There are many options available including Vanguard, Fidelity, and Schwab. Once you have your account you can deposit money and buy fund shares.

The main benefit is that you don't need to pick individual stocks. The fund automatically holds all the stocks in the index. This reduces risk through diversification.

Many experts recommend putting money in index funds regularly over time. This strategy is called dollar cost averaging. It helps smooth out market volatility.

For retirement accounts consider a target date fund which automatically adjusts over time. These are great for beginners who don't want to manage their portfolio.""",
        "target_keyword": "how to invest in index funds",
        "secondary_keywords": ["index fund investing for beginners", "best index funds", "S&P 500 index fund", "dollar cost averaging"],
        "target_audience": "Millennials aged 25-35 new to investing",
        "content_type": "Blog Post"
    }
    print(json.dumps(run(example), indent=2))
