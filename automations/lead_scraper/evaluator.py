import json
import re
from typing import Dict

import anthropic


class LeadEvaluator:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def evaluate(
        self, company_data: Dict, service_description: str, target_industry: str
    ) -> Dict:
        prompt = f"""You are a senior sales qualification expert. Evaluate whether this company is a legitimate potential buyer.

OFFERED SERVICE/PRODUCT:
{service_description}

TARGET INDUSTRY: {target_industry}

COMPANY DATA:
- URL: {company_data.get("url", "N/A")}
- Name/Title: {company_data.get("name", "N/A")}
- Description: {company_data.get("description", "N/A")}
- Search Snippet: {company_data.get("snippet", "N/A")}
- Email: {company_data.get("email", "N/A")}
- Phone: {company_data.get("phone", "N/A")}
- LinkedIn: {company_data.get("linkedin", "N/A")}
- Employees: {company_data.get("employees", "N/A")}

Respond with ONLY a valid JSON object — no markdown fences, no extra text:
{{
  "is_legitimate": true,
  "score": 75,
  "company_type": "Digital marketing agency",
  "fit_reason": "One-sentence reason why they would or would not need this service",
  "positive_indicators": ["indicator 1", "indicator 2"],
  "red_flags": ["flag 1"],
  "recommended_approach": "Brief, specific outreach strategy"
}}

Scoring guide:
- 0-30:  Not a buyer — competitor, spam, totally irrelevant
- 31-59: Unlikely — weak signals, poor industry match
- 60-79: Possible — some fit, worth a cold outreach
- 80-100: Strong — clear need, good match, decision-maker likely reachable

Be strict: only 60+ when there is genuine buying potential for the stated service."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass

        return {
            "is_legitimate": False,
            "score": 0,
            "company_type": "Unknown",
            "fit_reason": "Evaluation failed",
            "positive_indicators": [],
            "red_flags": ["Could not evaluate"],
            "recommended_approach": "",
        }
