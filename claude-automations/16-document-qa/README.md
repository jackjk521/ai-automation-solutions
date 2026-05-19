# Document Q&A

Answer questions about any document with citations, confidence levels, and structured key-fact extraction.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `document_text` (full text of the document), `document_type` (Contract, Report, Manual, Policy, or Financial), and `questions` (list of questions to answer).

**Output:** A JSON object containing a `document_summary`, an `answers` array (each with question, answer, confidence level High/Medium/Low, and source excerpt), a `key_facts` list, and `document_metadata` (estimated pages, primary topic, date mentioned).

## Customization

- Swap in a longer document by replacing `document_text` — the system prompt instructs the model to flag if content is truncated.
- Add more question types in `questions`; the model will return `"This information is not present in the document"` for anything not found.
- Change `document_type` to shift analysis focus — "Financial" triggers tighter scrutiny of numbers and dates.
