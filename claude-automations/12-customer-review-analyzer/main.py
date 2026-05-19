#!/usr/bin/env python3
"""Analyse customer reviews to extract sentiment, themes, and actionable product insights."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert product analyst and customer success specialist with deep experience
in voice-of-customer programmes, NPS analysis, and e-commerce optimisation. You have helped dozens of
product teams turn raw review data into roadmap decisions and revenue growth.

When analysing a set of customer reviews you will:
1. Count total reviews and calculate an accurate average rating to two decimal places.
2. Classify every review as Positive (4-5 stars or clearly satisfied tone), Neutral (3 stars or mixed
   sentiment), or Negative (1-2 stars or clearly dissatisfied tone).
3. Identify the top recurring themes across all reviews — both praise and complaints. For each theme
   note how frequently it appears and whether customer sentiment toward it is Positive, Negative, or Mixed.
4. List concrete improvement areas derived directly from negative or mixed feedback.
5. Surface competitive advantages — things customers explicitly love or compare favourably to alternatives.
6. Draft a professional, empathetic response for every review provided. Responses should acknowledge the
   specific feedback, thank the reviewer, and (for negatives) offer a path to resolution.
7. Synthesise a product insight paragraph summarising the most important strategic takeaways.
8. Suggest 3-5 marketing copy lines that can be used in ads or listing copy, grounded in real customer
   language and emotions from the reviews.
9. When competitor reviews are provided, compare sentiment and themes to identify relative strengths
   and weaknesses versus the competition.

Use precise, data-driven language. Never fabricate themes that aren't supported by the review text.
Output a single valid JSON object that exactly matches the requested schema. Do not include any text
outside the JSON object."""

def build_prompt(data: dict) -> str:
    reviews_text = "\n".join(
        f"[ID: {r['id']} | Rating: {r['rating']}/5 | Platform: {r.get('platform', 'Unknown')} | Date: {r.get('date', 'N/A')}]\n{r['text']}"
        for r in data.get("reviews", [])
    )
    competitor_section = ""
    if data.get("competitor_reviews"):
        comp_text = "\n".join(
            f"[Rating: {r['rating']}/5] {r['text']}"
            for r in data["competitor_reviews"]
        )
        competitor_section = f"\n\nCOMPETITOR REVIEWS (for comparison):\n{comp_text}"

    return f"""Analyse the following customer reviews for "{data.get('product_name', 'Unknown Product')}" and return your findings as a JSON object.

CUSTOMER REVIEWS:
{reviews_text}{competitor_section}

Return a JSON object with these exact keys:
{{
  "total_reviews": integer,
  "average_rating": float,
  "sentiment_breakdown": {{"positive": integer, "neutral": integer, "negative": integer}},
  "top_themes": [{{"theme": "string", "frequency": integer, "sentiment": "Positive|Negative|Mixed"}}],
  "improvement_areas": ["string"],
  "competitive_advantages": ["string"],
  "review_responses": [{{"review_id": "string", "response": "string"}}],
  "product_insights": "string",
  "marketing_copy_suggestions": ["string"]
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
        "product_name": "ProBrew Espresso Machine X200",
        "reviews": [
            {
                "id": "r001",
                "rating": 5,
                "text": "Absolutely love this machine! The espresso is rich and creamy every single time. Setup took about 20 minutes and the instructions were crystal clear. My only tiny gripe is the water tank could be a bit bigger.",
                "date": "2025-03-10",
                "platform": "Amazon",
            },
            {
                "id": "r002",
                "rating": 2,
                "text": "Looks great on the counter but the steam wand is really weak. Can't get proper microfoam for lattes. Customer service took a week to respond. Expected better for the price.",
                "date": "2025-03-15",
                "platform": "Amazon",
            },
            {
                "id": "r003",
                "rating": 4,
                "text": "Great espresso quality. The grinder is a bit loud in the mornings but the coffee taste makes up for it. Easy to clean — the drip tray pops out. Would buy again.",
                "date": "2025-03-20",
                "platform": "Trustpilot",
            },
            {
                "id": "r004",
                "rating": 1,
                "text": "Machine stopped working after 3 months. The pump makes a grinding noise and no coffee comes out. Sent it back for repair but was told it would take 6 weeks. Very disappointed.",
                "date": "2025-04-01",
                "platform": "Amazon",
            },
            {
                "id": "r005",
                "rating": 5,
                "text": "Upgraded from a basic machine and the difference is night and day. The pre-infusion feature really does improve extraction. Compact enough to fit under my kitchen cabinet. Highly recommend.",
                "date": "2025-04-05",
                "platform": "Shopify",
            },
        ],
        "competitor_reviews": [
            {"text": "The BrewMaster 3000 makes decent coffee but takes ages to heat up — at least 4 minutes every morning.", "rating": 3},
            {"text": "BrewMaster steam wand is excellent but the machine is huge and dominates the counter.", "rating": 4},
        ],
    }
    print(json.dumps(run(example), indent=2))
