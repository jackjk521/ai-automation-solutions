# Social Media Generator

Creates platform-native content for LinkedIn, Twitter/X, Instagram, and Facebook from a single topic brief, respecting each platform's unique tone, format, and algorithm preferences.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Key inputs:** `topic`, `brand_name`, `brand_voice`, `target_audience`, `platforms` (list), `include_hashtags` (bool), `include_emoji` (bool)

**Key outputs:** Per-platform content objects — `linkedin` (post + hashtags), `twitter` (tweet + thread array), `instagram` (caption + hashtags), `facebook` (post), plus `content_pillars_used`

## Customization

- Pass only the platforms you need in the `platforms` list to skip unused networks.
- Set `include_emoji: false` for brands with a strictly formal voice.
- Add a `content_type` field (e.g., "product launch", "thought leadership") to the prompt to tune content pillar selection.
