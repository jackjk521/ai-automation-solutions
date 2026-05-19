# Web Presence Analyzer

Analyze a business's website and generate a scored assessment, identified issues, and a personalized agency outreach email — ready for cold outreach or discovery call prep.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `business_name`, `website_url`, `website_content` (scraped homepage text), `niche`, `location`, `has_website` (bool), `tech_stack` (list of detected technologies), and `has_ssl` (bool).

**Output:** A JSON object with `overall_score` (0–10), `priority` (High/Medium/Low), `website_quality` description, `tech_stack_age` (Modern/Current/Aging/Legacy), `modernisation_needed` (bool), `issues_found`, `opportunities`, `outreach_email` (subject + body), `estimated_project_value`, `talking_points` for discovery calls, and `competitor_comparison`.

## Customization

- Feed real scraped website content into `website_content` to get more specific, personalized outreach emails rather than generic assessments.
- Populate `tech_stack` from a tech-detection tool (e.g., Wappalyzer API) to get accurate `tech_stack_age` scoring.
- Use `priority` to triage your prospect list — High priority prospects have the most opportunity and urgency for a website overhaul.
