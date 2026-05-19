# Invoice Generator

Generates a complete, print-ready HTML invoice from client data and line items.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

The generated HTML is saved to `invoice_output.html` in the same directory.

## Input / Output

**Input:** `invoice_number`, `date`, `due_date`, `company` (name/address/email/ABN), `client` (name/address/email), `line_items` (description/qty/rate), `tax_rate`, `notes`, `bank_details`.

**Output:** `html` (complete standalone invoice), `subtotal`, `tax_amount`, `total`, `summary`.

## Customization

- Set `tax_rate: 0` for tax-exempt invoices, or `0.20` for UK VAT
- Add a `logo_url` field and update the prompt to embed it in the header
- Pipe `result["html"]` into a Gmail send node or WeasyPrint for PDF export
