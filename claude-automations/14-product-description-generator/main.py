#!/usr/bin/env python3
"""Product description generator — specs → SEO-optimised e-commerce copy."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert e-commerce copywriter who has written product listings generating
millions in sales across Amazon, Shopify, and WooCommerce stores globally.

Your copy philosophy:
- Lead with the transformation and benefit, not the feature
- Use sensory and emotional language that helps the reader picture using the product
- Address the top 3 customer objections before they arise
- Write benefit-focused bullet points, not feature lists
- The SEO title must include the primary keyword naturally
- Short descriptions convert browsers — keep them punchy and benefit-first
- Long descriptions tell the full story: problem → solution → proof → CTA
- Amazon bullet points must start with a CAPITALISED KEY BENEFIT

Platform-specific guidelines:
- Amazon: 5 bullets, each starting with ALL CAPS benefit phrase, max 200 chars each
- Shopify/WooCommerce: conversational tone, storytelling approach
- General: balanced, professional tone

Always output valid JSON only. Do not include any text outside the JSON object."""

def build_prompt(data: dict) -> str:
    features = "\n".join(f"  - {f}" for f in data.get("key_features", []))
    use_cases = "\n".join(f"  - {u}" for u in data.get("use_cases", []))

    return f"""Write product descriptions for the following item.

Product Name: {data.get('product_name', 'Product')}
Product Type: {data.get('product_type', 'Consumer product')}
Target Audience: {data.get('target_audience', 'General consumers')}
Brand Voice: {data.get('brand_voice', 'Professional and friendly')}
Price Point: {data.get('price_point', 'Mid-range')}
Platform: {data.get('platform', 'General')}

Key Features:
{features}

Primary Use Cases:
{use_cases}

Return JSON:
{{
  "short_description": "50-word benefit-first description",
  "long_description": "200-word storytelling description with problem/solution/proof",
  "bullet_points": ["5 benefit-focused bullets, ALL CAPS lead phrase for Amazon"],
  "amazon_backend_keywords": ["10-15 relevant search terms"],
  "seo_title": "SEO-optimised product title with primary keyword",
  "meta_description": "155-char meta description",
  "tagline": "memorable 8-word tagline",
  "comparison_table_row": {{"Feature": "...", "Benefit": "...", "USP": "..."}}
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
        "product_name": "ProStand Elite — Adjustable Laptop Stand",
        "product_type": "Desk Accessory / Ergonomic Equipment",
        "key_features": [
            "6 height positions from 15° to 60°",
            "Aluminium alloy construction — holds up to 17-inch laptops",
            "Foldable and portable — weighs only 450g",
            "Non-slip silicone pads protect your laptop",
            "Compatible with MacBook, Dell, HP, Lenovo, and all laptops",
        ],
        "target_audience": "Remote workers, digital nomads, and office professionals",
        "use_cases": [
            "Reducing neck and back strain during long work sessions",
            "Creating a dual-monitor setup at home or office",
            "Working from cafes, hotels, and coworking spaces",
        ],
        "price_point": "Premium ($49.99)",
        "brand_voice": "Clean, professional, and results-focused",
        "platform": "Amazon",
    }
    print(json.dumps(run(example), indent=2))
