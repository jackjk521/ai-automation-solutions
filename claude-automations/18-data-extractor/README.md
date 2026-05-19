# Data Extractor

Extract structured data from any unstructured text (emails, invoices, forms, articles) using a custom schema you define.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `text` (the raw source text), `extraction_schema` (dict mapping field names to descriptions), `source_type` (Email, Invoice, Report, Form, Article, or Conversation), and `output_format` (json or csv_row).

**Output:** A JSON object containing all schema fields with extracted values (null if not found), plus `extraction_confidence` (0.0–1.0 float), `missing_fields` (list of fields not found), and `ambiguous_fields` (list of fields with multiple plausible values and their options).

## Customization

- Define any `extraction_schema` fields you need — the model follows the field descriptions precisely, so detailed descriptions yield more accurate extraction.
- Set `source_type` to match your document format; this helps the model apply the right parsing heuristics (e.g., email headers vs. invoice line items).
- For batch processing, loop over a list of texts and call `run()` for each, collecting results into a list or CSV.
