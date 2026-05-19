#!/usr/bin/env python3
"""Extract structured data from unstructured text according to a user-defined schema."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert data extraction specialist with extensive experience processing
emails, invoices, forms, reports, articles, and transcripts. Your role is to extract structured
data from unstructured or semi-structured text with extreme precision and reliability.

Core principles for extraction:
- Extract ONLY what is explicitly stated or unambiguously implied in the source text
- Never infer, guess, or hallucinate values — if a field is not present, return null
- When a field is ambiguous (multiple plausible values), flag it in ambiguous_fields rather than guessing
- Preserve original formatting for extracted values (e.g., phone numbers as written, not reformatted)
- For dates, extract as written in the source (do not convert formats)
- For monetary values, include the currency symbol/code if present
- Pay attention to context: "John Smith" as a sender vs. a recipient are different fields
- Handle common variations: "RE:", "Fwd:", subject lines, salutations, and signatures in emails
- For invoices: distinguish bill-to vs. ship-to, line items vs. totals, invoice date vs. due date
- Flag any fields where extraction confidence is moderate or low in the ambiguous_fields list

Extraction confidence (overall score 0.0 to 1.0):
- 1.0: All fields clearly present, no ambiguity
- 0.7-0.9: Most fields present, minor ambiguity on 1-2 fields
- 0.4-0.6: Several fields missing or ambiguous
- Below 0.4: Significant uncertainty, many missing fields

Your output must always be valid JSON. Output ONLY the JSON object, no other text."""

def build_prompt(data: dict) -> str:
    text = data.get("text", "")
    schema = data.get("extraction_schema", {})
    source_type = data.get("source_type", "Document")
    output_format = data.get("output_format", "json")

    schema_desc = "\n".join(
        f'  - "{field}": {description}' for field, description in schema.items()
    )

    return f"""Extract structured data from the following {source_type}.

SOURCE TYPE: {source_type}
OUTPUT FORMAT: {output_format}

EXTRACTION SCHEMA (fields to extract):
{schema_desc}

SOURCE TEXT:
---
{text}
---

Return a JSON object that includes:
1. All fields from the schema above (use null for fields not found)
2. Three meta-fields appended to the result:
   - "extraction_confidence": float between 0.0 and 1.0
   - "missing_fields": list of field names that could not be found
   - "ambiguous_fields": list of objects with "field" and "options" keys for uncertain extractions

Example meta structure:
{{
  ...extracted fields...,
  "extraction_confidence": 0.85,
  "missing_fields": ["phone"],
  "ambiguous_fields": [{{"field": "company", "options": ["Acme Inc", "Acme Corporation"]}}]
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
        "source_type": "Email",
        "output_format": "json",
        "extraction_schema": {
            "sender_name": "Full name of the person who sent the email",
            "sender_email": "Email address of the sender",
            "company": "Company or organization the sender represents",
            "phone": "Phone number if provided",
            "requested_service": "The service or product the sender is inquiring about",
            "urgency": "How urgent the request is (High/Medium/Low) based on tone and language",
            "budget_mentioned": "Any budget figure mentioned, or null if not mentioned",
            "preferred_contact_method": "How they prefer to be contacted (email/phone/either)"
        },
        "text": """From: Sarah Mitchell <s.mitchell@technova-solutions.com>
To: sales@yourcompany.com
Subject: Urgent: Need enterprise CRM proposal by Friday

Hi there,

My name is Sarah Mitchell and I'm the VP of Operations at TechNova Solutions. We're a 200-person
technology consulting firm and we're in the process of replacing our outdated CRM system.

We've been evaluating several options and your platform came highly recommended by a colleague
at DataBridge Inc. I'm particularly interested in your enterprise tier with API integrations
and custom reporting capabilities.

Here's the thing — our current system contract expires on March 31st, so we're under a tight
deadline. I'd need a detailed proposal with pricing by this Friday if possible. Our budget is
in the $50,000-$80,000/year range for the right solution.

The best way to reach me is by phone — I'm available at (415) 882-3947 most mornings until noon.
Alternatively you can reply to this email.

Looking forward to hearing from you soon.

Best regards,
Sarah Mitchell
VP Operations | TechNova Solutions
(415) 882-3947"""
    }
    print(json.dumps(run(example), indent=2))
