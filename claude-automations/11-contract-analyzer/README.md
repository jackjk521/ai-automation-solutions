# Contract Analyzer

Extract key terms, risks, obligations, and negotiation opportunities from any commercial contract in seconds.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `contract_text` (full contract string), `contract_type` (Service Agreement | NDA | Employment | SaaS | Partnership), `your_role` (Client | Vendor | Employee | Employer), `jurisdiction` (e.g. "England and Wales").

**Output:** Structured JSON including `contract_summary`, `parties`, `key_dates`, `payment_terms`, `termination_conditions`, `liability_caps`, `ip_ownership`, `non_compete`, `risks` (each with severity), `missing_clauses`, `negotiation_points`, and an `overall_risk_score` (0–100).

## Customization

- Adjust `your_role` to shift risk assessment perspective between Client, Vendor, Employee, or Employer.
- Extend the prompt to focus on specific clause types (e.g. GDPR data-processing addenda, SLA schedules).
- Pipe multiple contracts through `run()` in a loop to build a risk dashboard across a contract portfolio.
