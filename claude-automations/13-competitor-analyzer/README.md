# Competitor Analyzer

Builds a sales battle card from competitor information — strengths, weaknesses, objection handlers, and strategic recommendations.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `your_company`, `your_product`, `your_strengths`, `competitor_name`, `competitor_description`, `competitor_website_content`, `market_segment`.

**Output:** `competitor_summary`, `their_strengths/weaknesses`, `battle_card` (when_you_win/lose, objection_handlers), `positioning_map`, `strategic_recommendations`.

## Customization

- Feed in scraped website copy, G2/Capterra reviews, or LinkedIn content as `competitor_website_content`
- Run weekly with fresh competitor content to keep battle cards up to date
- Export `battle_card` directly into your sales CRM or Notion wiki
