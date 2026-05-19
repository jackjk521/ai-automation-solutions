# Cold Outreach Generator

Generates hyper-personalised B2B cold email sequences and LinkedIn messages using prospect pain points, tone preferences, and your service offering.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Key inputs:** `prospect_name`, `company`, `role`, `industry`, `pain_points` (list), `your_service`, `tone` (Professional | Casual | Bold)

**Key outputs:** `email_subject`, `email_body` (under 150 words), `follow_up_day3`, `follow_up_day7`, `linkedin_message`, `key_hook`

## Customization

- Adjust `pain_points` with signals gathered from LinkedIn, news, or job postings for maximum personalisation.
- Change `tone` to `Bold` for disruptive industries or `Casual` for startup audiences.
- Extend the prompt to include a specific case study or social proof reference for higher-converting follow-ups.
