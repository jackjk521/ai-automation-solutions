#!/usr/bin/env python3
"""Build a structured FAQ knowledge base from product docs, support tickets, or any source content."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert knowledge base architect and technical writer with deep experience
building FAQ systems for SaaS products, e-commerce platforms, enterprise software, and customer support
teams. You understand what customers actually ask versus what companies think they ask, and you bridge
that gap.

Your approach to building FAQs:
- Extract questions that real users would actually type into a search box or support chat
- Write answers that are complete yet scannable — use plain language, avoid jargon unless defining it
- Group questions into logical categories that map to user mental models, not company org charts
- Identify "knowledge gaps" — topics that users clearly need information about but the source content
  doesn't adequately address
- Suggest additional FAQs that would be valuable based on common patterns in the content type
- Tag each FAQ with searchable keywords that capture synonyms and alternate phrasings
- Note who each FAQ is most helpful for (e.g., "new customers", "technical users", "billing questions")

Quality standards for FAQ answers:
- Each answer should be self-contained — users should not need to read other FAQs to understand it
- Lead with the direct answer, then provide supporting detail
- Use numbered steps for processes, bullet points for lists of items
- Keep answers between 50-200 words — long enough to be useful, short enough to scan
- Avoid phrases like "Great question!" or corporate filler language

For the audience adaptation:
- Customers: plain language, benefit-focused, avoid technical implementation details
- Developers: precise technical language, include code concepts, API references welcome
- Sales Team: focus on differentiators, competitive positioning, objection handling
- Support Agents: include edge cases, escalation criteria, internal procedures

Your output must always be valid JSON. Do not include any text outside the JSON structure."""

def build_prompt(data: dict) -> str:
    source_content = data.get("source_content", "")
    content_type = data.get("content_type", "Website")
    target_audience = data.get("target_audience", "Customers")
    max_faqs = data.get("max_faqs", 10)
    brand_name = data.get("brand_name", "")

    return f"""Build a FAQ knowledge base from the following source content.

BRAND: {brand_name}
SOURCE CONTENT TYPE: {content_type}
TARGET AUDIENCE: {target_audience}
MAXIMUM NUMBER OF FAQs: {max_faqs}

SOURCE CONTENT:
---
{source_content}
---

Generate up to {max_faqs} FAQs optimized for {target_audience}. Prioritize the most valuable and
commonly-needed questions first.

Return valid JSON with this exact structure:
{{
  "faqs": [
    {{
      "question": "the question as a user would phrase it",
      "answer": "clear, complete answer",
      "category": "logical category name",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "helpful_for": "description of who benefits most from this FAQ"
    }}
  ],
  "categories": ["list", "of", "all", "unique", "categories"],
  "knowledge_gaps": ["topic not covered but users would need", "another gap"],
  "suggested_additional_faqs": ["question worth adding", "another question worth adding"]
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
        "brand_name": "CloudVault",
        "content_type": "Product Docs",
        "target_audience": "Customers",
        "max_faqs": 8,
        "source_content": """CloudVault Backup Service — Product Overview

CloudVault is an automated cloud backup solution for small and medium businesses. It continuously
backs up your files, databases, and server configurations to our secure, geo-redundant data centers.

STORAGE PLANS:
- Starter: 500 GB for $9/month
- Business: 2 TB for $29/month
- Enterprise: 10 TB for $99/month
All plans include unlimited file versions and 30-day retention by default.

SUPPORTED PLATFORMS:
CloudVault supports Windows Server 2016+, Ubuntu 18.04+, macOS 12+, and major Linux distributions.
Database support includes MySQL, PostgreSQL, MongoDB, and Microsoft SQL Server.

BACKUP FREQUENCY:
By default, backups run every 4 hours. Business and Enterprise plans can configure custom schedules
down to 15-minute intervals. Real-time sync is available for the Enterprise plan.

RECOVERY:
Files can be restored to any point in time within your retention window. The average recovery time
for a single file is under 2 minutes. Full server restoration typically takes 30-90 minutes depending
on data size. Recovery is free and unlimited for all plans.

SECURITY:
All data is encrypted with AES-256 at rest and TLS 1.3 in transit. We are SOC 2 Type II certified
and HIPAA compliant. Customer encryption keys can be self-managed on Enterprise plans.

SUPPORT:
Starter plan: email support (response within 24 hours)
Business plan: priority email and chat (response within 4 hours)
Enterprise plan: 24/7 phone support with dedicated account manager

CANCELLATION:
You can cancel anytime. Your data is retained for 30 days after cancellation, then permanently deleted.
No refunds for partial months."""
    }
    print(json.dumps(run(example), indent=2))
