# Lead Qualifier

Score and qualify B2B sales leads automatically using the BANT framework (Budget, Authority, Need, Timeline) powered by Claude AI.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

| Field | Type | Description |
|-------|------|-------------|
| **Input: name** | string | Lead's full name |
| **Input: company** | string | Company name |
| **Input: role** | string | Job title / role |
| **Input: company_size** | string | Employee count range |
| **Input: budget** | string | Stated budget or budget range |
| **Input: use_case** | string | Described use case or pain point |
| **Input: timeline** | string | Purchasing or implementation timeline |
| **Input: source** | string | How the lead was acquired |
| **Output: score** | int (0-100) | Overall BANT qualification score |
| **Output: tier** | string | Hot / Warm / Cold |
| **Output: budget_fit** | bool | Whether budget aligns with product pricing |
| **Output: authority** | bool | Whether the lead has purchasing authority |
| **Output: need** | string | Summary of identified business need |
| **Output: timeline_fit** | bool | Whether timeline matches sales cycle |
| **Output: reasons** | array | Key reasons behind the score |
| **Output: recommended_next_step** | string | Specific action for the sales team |
| **Output: talking_points** | array | Tailored talking points for outreach |

## Customization

- **Adjust scoring thresholds**: Modify the `SYSTEM_PROMPT` to change what constitutes Hot/Warm/Cold based on your product's price point, sales cycle, and target market.
- **Add product context**: Prepend your product's pricing tiers, ideal customer profile, and key differentiators to the `SYSTEM_PROMPT` so scores are calibrated to your specific offering.
- **CRM integration**: Wrap `run()` to read leads from a CRM webhook and write results back as lead scores or custom fields using your CRM's API.
