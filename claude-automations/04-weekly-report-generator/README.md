# Weekly Report Generator

Generate insightful weekly business performance reports with trend analysis, WoW comparisons, executive summaries, and actionable recommendations — powered by Claude Sonnet for higher-quality prose.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

| Field | Type | Description |
|-------|------|-------------|
| **Input: week_ending** | string | ISO date string for the reporting week end |
| **Input: metrics** | object | Current week: revenue, new_deals, leads, conversion_rate, avg_deal_size, churn |
| **Input: prev_metrics** | object | Previous week's same metrics for WoW comparison |
| **Input: team_notes** | array | Free-text context from team members |
| **Output: executive_summary** | string | 2-3 sentence decision-focused summary |
| **Output: performance_rating** | string | Exceptional / Strong / On Track / Needs Attention / Critical |
| **Output: highlights** | array | Specific wins with numbers |
| **Output: concerns** | array | Issues requiring attention |
| **Output: recommendations** | array | Prioritized actionable next steps |
| **Output: week_over_week** | object | Formatted WoW changes for revenue, deals, and leads |
| **Output: narrative** | string | Full 3-paragraph HTML narrative |

## Customization

- **Additional metrics**: Extend the `metrics` dict and `build_prompt()` to include NPS score, support ticket volume, product usage metrics, or marketing spend for a more complete picture.
- **Rating thresholds**: Adjust the performance rating criteria in the `SYSTEM_PROMPT` to match your business's growth targets and seasonal patterns.
- **Email distribution**: Pipe the `narrative` HTML field into an email template and send via SendGrid or SES to distribute the report automatically to your leadership team each Monday morning.
