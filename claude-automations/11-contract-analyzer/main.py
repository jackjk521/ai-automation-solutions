#!/usr/bin/env python3
"""Analyse contracts to extract key terms, risks, obligations, and negotiation opportunities."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert contract lawyer and legal analyst with over 20 years of experience
reviewing commercial, employment, SaaS, NDA, and partnership agreements across multiple jurisdictions.
Your role is to analyse contracts with precision and surface every meaningful risk, obligation, and
opportunity for the user's benefit.

When reviewing a contract you will:
1. Identify all parties and their roles with clarity.
2. Extract every date, deadline, and renewal window — missed dates can be catastrophic.
3. Summarise payment terms including amounts, schedules, late-payment penalties, and currency.
4. Map termination conditions in plain language, distinguishing convenience vs cause terminations.
5. Identify liability caps, indemnification clauses, and limitation-of-liability exclusions.
6. Determine who owns intellectual property created during or as a result of the agreement.
7. Flag non-compete, non-solicitation, and exclusivity clauses with their scope and duration.
8. Assess each identified risk and assign a severity of High, Medium, or Low.
9. Call out standard protective clauses that are absent (e.g. force majeure, dispute resolution,
   governing law, data protection, confidentiality, warranties).
10. Provide actionable negotiation points that would improve the user's position.
11. Produce an overall risk score from 0 (no risk) to 100 (extreme risk).

Always present findings in plain English — avoid unnecessary jargon. When a clause is ambiguous,
say so explicitly. Prioritise the user's role (Client, Vendor, Employee, or Employer) when assessing
risk direction. This analysis is for informational purposes only and does not constitute legal advice.

Output a single valid JSON object that exactly matches the requested schema. Do not include any text
outside the JSON object."""

def build_prompt(data: dict) -> str:
    return f"""Please analyse the following contract and return your findings as a JSON object.

Contract Type: {data.get('contract_type', 'Unknown')}
Your Role: {data.get('your_role', 'Unknown')}
Jurisdiction: {data.get('jurisdiction', 'Not specified')}

CONTRACT TEXT:
{data.get('contract_text', '')}

Return a JSON object with these exact keys:
{{
  "contract_summary": "string — 3-5 sentence plain-English overview",
  "parties": [{{"name": "string", "role": "string"}}],
  "key_dates": [{{"event": "string", "date": "string"}}],
  "payment_terms": "string",
  "termination_conditions": ["string"],
  "liability_caps": "string",
  "ip_ownership": "string",
  "non_compete": "string",
  "risks": [{{"risk": "string", "severity": "High|Medium|Low", "clause": "string"}}],
  "missing_clauses": ["string"],
  "negotiation_points": ["string"],
  "overall_risk_score": integer 0-100
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
        "contract_type": "SaaS",
        "your_role": "Client",
        "jurisdiction": "England and Wales",
        "contract_text": """SOFTWARE AS A SERVICE AGREEMENT

This Agreement is entered into as of January 1, 2025, between Acme Corp ("Vendor") and Beta Ltd ("Client").

1. SERVICES. Vendor will provide access to its cloud-based analytics platform ("Service") for the term of this Agreement.

2. PAYMENT. Client shall pay £2,400 per year, billed annually in advance. Payments are non-refundable. Late payments accrue interest at 8% per annum.

3. TERM. This Agreement commences on January 1, 2025 and continues for one (1) year, automatically renewing for successive one-year terms unless either party provides 90 days written notice prior to renewal.

4. DATA. All data uploaded by Client remains Client's property. Vendor may use aggregated, anonymised data to improve the Service. Vendor will not sell Client data to third parties.

5. LIABILITY. Vendor's total liability under this Agreement shall not exceed the fees paid in the preceding three (3) months. Neither party shall be liable for indirect, incidental, or consequential damages.

6. TERMINATION FOR CAUSE. Either party may terminate immediately if the other commits a material breach and fails to remedy it within 30 days of written notice.

7. INTELLECTUAL PROPERTY. All rights in the Service remain with Vendor. Client retains all rights in Client data and any custom configurations developed solely by Client.

8. GOVERNING LAW. This Agreement is governed by the laws of England and Wales.""",
    }
    print(json.dumps(run(example), indent=2))
