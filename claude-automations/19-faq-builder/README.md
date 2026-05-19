# FAQ Builder

Transform product docs, support tickets, sales calls, or any source content into a structured, searchable FAQ knowledge base.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `source_content` (the raw content to extract FAQs from), `content_type` (Product Docs, Support Tickets, Sales Calls, Website, or Knowledge Base), `target_audience` (Customers, Developers, Sales Team, or Support Agents), `max_faqs` (integer cap on number of FAQs), and `brand_name`.

**Output:** A JSON object with a `faqs` array (each with question, answer, category, keywords, and helpful_for), a `categories` list, `knowledge_gaps` (topics users need but the source doesn't cover), and `suggested_additional_faqs` (recommended questions to add).

## Customization

- Change `target_audience` to shift language and depth — "Developers" generates technical FAQs with precise terminology, while "Customers" uses plain language and benefit-focused answers.
- Increase `max_faqs` up to ~25 for comprehensive coverage of large documentation sets.
- Paste support ticket text as `source_content` to build FAQs directly from real customer questions, which produces higher-quality results than docs alone.
