# SEO Content Optimizer

Analyses existing content against a target keyword and returns an SEO score, actionable improvement recommendations, optimised meta data, a heading structure, and a rewritten intro paragraph.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Key inputs:** `title`, `content` (full text), `target_keyword`, `secondary_keywords` (list), `target_audience`, `content_type` (Blog Post | Landing Page | Product Page)

**Key outputs:** `seo_score` (0-100), `optimized_title`, `meta_description`, `slug`, `heading_structure`, `keyword_density`, `readability_score`, `improvements` (with severity), `optimized_intro`, `internal_link_suggestions`, `schema_type`

## Customization

- Pass `content_type: "Landing Page"` for conversion-focused copy that prioritises commercial intent signals.
- Add competitor URLs to the prompt for a gap analysis against ranking pages.
- Filter `improvements` by `severity: "High"` to prioritise the most impactful fixes first.
