#!/usr/bin/env python3
"""Invoice generator — client + line items → branded print-ready HTML invoice."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert invoice designer and financial document specialist.
Generate clean, professional, print-ready HTML invoices with inline CSS only (no external stylesheets).

Design requirements:
- Dark header with company name and "INVOICE" title
- Clean white body with a well-structured line-items table
- Subtotal, tax, and TOTAL rows clearly separated
- Payment terms section with bank details
- Footer with "Thank you for your business"
- Professional typography using system fonts (Arial, Helvetica)
- Mobile-friendly layout
- All amounts formatted to 2 decimal places with currency symbol

Always calculate: subtotal = sum of (qty * rate), tax_amount = subtotal * tax_rate, total = subtotal + tax_amount.

Output valid JSON only. Do not include any text outside the JSON object."""

def build_prompt(data: dict) -> str:
    items = data.get("line_items", [])
    subtotal = sum(item["qty"] * item["rate"] for item in items)
    tax_rate = data.get("tax_rate", 0.1)
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount

    line_items_str = "\n".join(
        f"  - {item['description']}: {item['qty']} x ${item['rate']:.2f} = ${item['qty']*item['rate']:.2f}"
        for item in items
    )

    company = data.get("company", {})
    client_info = data.get("client", {})
    bank = data.get("bank_details", {})

    return f"""Generate a professional HTML invoice with these details:

INVOICE: #{data.get('invoice_number', 'INV-001')}
DATE: {data.get('date', '2024-01-26')}
DUE DATE: {data.get('due_date', '2024-02-09')}

FROM (Your Company):
  Name: {company.get('name', 'Acme Solutions')}
  Address: {company.get('address', '123 Business St, Sydney NSW 2000')}
  Email: {company.get('email', 'billing@acme.com')}
  ABN/Tax ID: {company.get('abn', '12 345 678 901')}

TO (Client):
  Name: {client_info.get('name', 'Client Corp')}
  Address: {client_info.get('address', '456 Client Ave, Melbourne VIC 3000')}
  Email: {client_info.get('email', 'accounts@client.com')}

LINE ITEMS:
{line_items_str}

TOTALS:
  Subtotal: ${subtotal:.2f}
  Tax ({tax_rate*100:.0f}%): ${tax_amount:.2f}
  TOTAL: ${total:.2f}

PAYMENT DETAILS:
  Bank: {bank.get('bank', 'Commonwealth Bank')}
  Account Name: {bank.get('account_name', company.get('name', 'Acme Solutions'))}
  BSB: {bank.get('bsb', '062-000')}
  Account: {bank.get('account', '12345678')}

NOTES: {data.get('notes', 'Payment due within 14 days. Thank you for your business.')}

Return JSON:
{{
  "html": "complete standalone HTML invoice with inline CSS",
  "subtotal": {subtotal:.2f},
  "tax_amount": {tax_amount:.2f},
  "total": {total:.2f},
  "summary": "one-line summary e.g. Invoice #INV-001 for $X total"
}}"""


def run(input_data: dict) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_prompt(input_data)}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r'\{[\s\S]+\}', raw)
    return json.loads(match.group(0)) if match else {"raw": raw}


if __name__ == "__main__":
    example = {
        "invoice_number": "INV-2024-042",
        "date": "2024-01-26",
        "due_date": "2024-02-09",
        "company": {
            "name": "Ace International Solutions",
            "address": "88 Collins St, Melbourne VIC 3000, Australia",
            "email": "billing@aceinternational.solutions",
            "abn": "12 345 678 901",
        },
        "client": {
            "name": "Brightside Marketing Ltd",
            "address": "14 Queen St, Auckland 1010, New Zealand",
            "email": "accounts@brightside.co.nz",
        },
        "line_items": [
            {"description": "Website Redesign — Discovery & Strategy", "qty": 1, "rate": 2500.00},
            {"description": "UI/UX Design (5 pages)", "qty": 1, "rate": 3500.00},
            {"description": "Front-end Development", "qty": 20, "rate": 150.00},
            {"description": "SEO Setup & On-page Optimisation", "qty": 1, "rate": 800.00},
        ],
        "tax_rate": 0.10,
        "notes": "Payment due within 14 days via bank transfer. Late payments incur 1.5% monthly interest.",
        "bank_details": {
            "bank": "Commonwealth Bank of Australia",
            "account_name": "Ace International Solutions",
            "bsb": "062-000",
            "account": "12345678",
        },
    }
    result = run(example)
    print(f"Summary: {result.get('summary')}")
    print(f"Total: ${result.get('total', 0):.2f}")
    # Save HTML to file
    if "html" in result:
        with open("invoice_output.html", "w") as f:
            f.write(result["html"])
        print("Invoice saved to invoice_output.html")
