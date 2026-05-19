# Content Calendar Generator

Generate a complete monthly content calendar with post ideas, scroll-stopping hooks, and hashtags tailored to your brand and platforms.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `brand_name`, `industry`, `target_audience`, `content_goals` (list), `platforms` (list), `posting_frequency` (dict with counts per platform), `brand_voice`, `avoid_topics` (list), `month`, and `year`.

**Output:** A JSON object with a `calendar` array (each entry has week, day, date, platform, content type, topic, angle, caption hook, and hashtags), plus `content_themes`, `campaign_ideas`, and `best_posting_times`.

## Customization

- Adjust `posting_frequency` to set how many posts per platform per month — set a platform to 0 to skip it entirely.
- Modify `brand_voice` to shift tone from formal/professional to casual/playful; this directly shapes the caption hooks generated.
- Add entries to `avoid_topics` to enforce brand-safety guardrails around sensitive subjects or competitor mentions.
