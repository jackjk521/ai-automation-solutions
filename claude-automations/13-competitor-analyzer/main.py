#!/usr/bin/env python3
"""Build a detailed competitor battle card with positioning analysis and objection handlers."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert competitive intelligence analyst and go-to-market strategist with
extensive experience advising B2B SaaS companies, consumer brands, and professional services firms.
You have built hundreds of battle cards that have directly contributed to sales win-rate improvements.

When analysing a competitor your job is to:
1. Produce a concise but comprehensive summary of the competitor — who they are, what they sell, who
   they serve, and how they position themselves in the market.
2. Identify their genuine strengths — capabilities, brand reputation, customer base, integrations, pricing
   advantages, or go-to-market motions that represent real competitive threats.
3. Identify their real weaknesses — gaps in product, poor reviews, limited support, pricing complexity,
   technical debt, or customer segments they underserve.
4. Define their target customer profile with specificity: industry, company size, buyer persona, and
   use case.
5. Describe their pricing model and, where inferable, approximate price points.
6. List their unique selling points as they would describe them in their own marketing.
7. Identify feature or capability gaps compared to the user's product based on provided information.
8. Create a simple two-axis positioning map, choosing axes that best differentiate the two companies,
   and place each company on that map in plain language.
9. Build a sales battle card with: scenarios where you typically win, scenarios where you lose, and
   specific objection handlers for the 3-5 most common objections a prospect would raise when comparing
   the two products.
10. Provide 4-6 strategic recommendations the user's company should act on to widen their competitive
    advantage or protect against the competitor's strengths.

Be rigorous and honest — do not inflate your company's position or unfairly disparage the competitor.
Sales teams need accurate intelligence to have credible conversations. Output a single valid JSON object
that exactly matches the requested schema. Do not include any text outside the JSON object."""

def build_prompt(data: dict) -> str:
    strengths_list = "\n".join(f"- {s}" for s in data.get("your_strengths", []))
    return f"""Analyse the following competitor and build a battle card. Return your findings as a JSON object.

OUR COMPANY: {data.get('your_company', 'Unknown')}
OUR PRODUCT: {data.get('your_product', 'Unknown')}
OUR STRENGTHS:
{strengths_list}

MARKET SEGMENT: {data.get('market_segment', 'Unknown')}

COMPETITOR NAME: {data.get('competitor_name', 'Unknown')}
COMPETITOR DESCRIPTION: {data.get('competitor_description', '')}
COMPETITOR WEBSITE / CONTENT:
{data.get('competitor_website_content', 'No content provided')}

Return a JSON object with these exact keys:
{{
  "competitor_summary": "string",
  "their_strengths": ["string"],
  "their_weaknesses": ["string"],
  "their_target_customer": "string",
  "pricing_model": "string",
  "unique_selling_points": ["string"],
  "feature_gaps": ["string"],
  "positioning_map": {{
    "x_axis": "string — axis label",
    "y_axis": "string — axis label",
    "their_position": "string — plain language position on the map",
    "your_position": "string — plain language position on the map"
  }},
  "battle_card": {{
    "when_you_win": ["string"],
    "when_you_lose": ["string"],
    "objection_handlers": [{{"objection": "string", "response": "string"}}]
  }},
  "strategic_recommendations": ["string"]
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
        "your_company": "DataPulse",
        "your_product": "DataPulse Analytics — real-time business intelligence platform for mid-market e-commerce",
        "your_strengths": [
            "Sub-second query response times on datasets up to 10 billion rows",
            "No-code dashboard builder loved by non-technical users",
            "Native Shopify, WooCommerce, and Amazon Seller Central integrations",
            "Flat-rate pricing from $299/month with unlimited seats",
            "24/7 live chat support with under 2-minute response times",
        ],
        "competitor_name": "InsightFlow",
        "competitor_description": "InsightFlow is a business intelligence and data visualisation platform targeting mid-to-large e-commerce and retail businesses. Founded in 2018, they have raised $45M in Series B funding.",
        "market_segment": "Mid-market e-commerce analytics (50-500 employee companies)",
        "competitor_website_content": """InsightFlow — Smarter Data for Growing Retailers

Turn your data into decisions. InsightFlow connects to 200+ data sources and gives your team
the analytics superpowers they need to grow faster.

PRICING: Starter $499/month (5 users), Growth $1,199/month (20 users), Enterprise — contact sales.

KEY FEATURES:
- 200+ pre-built connectors including Shopify, Magento, Salesforce, and Google Ads
- AI-powered forecasting and anomaly detection
- Customisable dashboards with drag-and-drop builder
- Automated weekly email digests for executives
- SOC 2 Type II certified, GDPR compliant
- Dedicated customer success manager on Growth and Enterprise plans

CUSTOMERS: Over 800 mid-market and enterprise retail brands including RetailCo, ShopBig, and FashionFirst.
Average customer saves 15 hours per week on manual reporting.

LIMITATIONS NOTED IN REVIEWS: Setup can take 4-6 weeks for enterprise clients. SQL knowledge helpful
for advanced queries. Some users report dashboard load times of 8-12 seconds on large datasets.""",
    }
    print(json.dumps(run(example), indent=2))
