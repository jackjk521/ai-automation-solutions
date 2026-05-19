# Product Description Generator

Writes short, long, bullet-point, and SEO copy for e-commerce product listings from raw specs.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `product_name`, `product_type`, `key_features` (list), `target_audience`, `use_cases`, `price_point`, `brand_voice`, `platform` (Amazon/Shopify/WooCommerce/General).

**Output:** `short_description` (50 words), `long_description` (200 words), `bullet_points` (5), `amazon_backend_keywords`, `seo_title`, `meta_description`, `tagline`.

## Customization

- Change `platform` to get Amazon-style ALL CAPS bullets vs. Shopify storytelling tone
- Add `competitor_product` field and update the prompt to differentiate against it
- Run in batch mode by looping a product catalogue CSV through `run()`
