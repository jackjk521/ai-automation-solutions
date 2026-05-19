#!/usr/bin/env python3
"""Answer questions about uploaded documents with citations and confidence levels."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert document analyst with deep experience in reviewing contracts,
financial reports, technical manuals, policy documents, and business reports. Your role is to read
documents carefully and answer questions accurately, always grounding your responses in the actual
text of the document provided.

When answering questions:
- Read the document thoroughly before attempting any answers
- Only answer based on what is explicitly stated or can be directly inferred from the document
- If a question cannot be answered from the document, say clearly: "This information is not present in the document"
- Provide source excerpts (direct quotes or close paraphrases) to back up each answer
- Assign a confidence level: High (directly stated), Medium (implied or inferrable), Low (uncertain or tangential)
- Extract key facts as a structured list, including dates, names, numbers, and obligations
- Estimate the document length based on word count and content density
- Identify the primary topic and any dates mentioned in the document

Your output must always be valid JSON. Do not include any text outside the JSON structure.
Never fabricate information that is not in the document. Accuracy and honesty are paramount.
Cite specific sections, clauses, or paragraphs when possible to help the user locate the source.
If a document appears to be truncated or incomplete, note this in your analysis."""

def build_prompt(data: dict) -> str:
    document_text = data.get("document_text", "")
    document_type = data.get("document_type", "Document")
    questions = data.get("questions", [])

    questions_formatted = "\n".join(
        f"{i+1}. {q}" for i, q in enumerate(questions)
    )

    return f"""Please analyze the following {document_type} and answer the questions provided.

DOCUMENT TYPE: {document_type}

DOCUMENT TEXT:
---
{document_text}
---

QUESTIONS TO ANSWER:
{questions_formatted}

Return your analysis as a JSON object with this exact structure:
{{
  "document_summary": "2-3 sentence summary of the document",
  "answers": [
    {{
      "question": "the question text",
      "answer": "your detailed answer",
      "confidence": "High|Medium|Low",
      "source_excerpt": "relevant quote or paraphrase from the document"
    }}
  ],
  "key_facts": ["fact 1", "fact 2", "fact 3"],
  "document_metadata": {{
    "estimated_pages": 1,
    "primary_topic": "main subject",
    "date_mentioned": "any date found or null"
  }}
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
        "document_type": "Contract",
        "document_text": """SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of January 15, 2024, between Acme Corp
("Client") and TechSolutions Ltd ("Provider").

1. SERVICES
Provider agrees to deliver custom software development services, including design, development,
testing, and deployment of a customer relationship management (CRM) system.

2. TERM
This Agreement commences on February 1, 2024 and continues for twelve (12) months unless
terminated earlier in accordance with Section 7.

3. COMPENSATION
Client shall pay Provider a monthly retainer of $15,000, due on the first business day of each
month. Late payments shall accrue interest at 1.5% per month.

4. INTELLECTUAL PROPERTY
All work product created under this Agreement shall be the exclusive property of Client upon
full payment of all fees.

5. CONFIDENTIALITY
Both parties agree to maintain strict confidentiality of all proprietary information shared
during the term of this Agreement and for two (2) years thereafter.

6. LIMITATION OF LIABILITY
Provider's total liability shall not exceed the total fees paid in the three months preceding
the claim.

7. TERMINATION
Either party may terminate this Agreement with 30 days written notice. Client may terminate
immediately for cause if Provider materially breaches this Agreement.""",
        "questions": [
            "What is the monthly payment amount?",
            "Who owns the intellectual property created?",
            "How long is the confidentiality obligation after the contract ends?",
            "What is the termination notice period?"
        ]
    }
    print(json.dumps(run(example), indent=2))
