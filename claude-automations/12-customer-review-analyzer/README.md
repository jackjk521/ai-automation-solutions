# Customer Review Analyzer

Transform raw customer reviews into sentiment breakdowns, recurring themes, drafted responses, and marketing copy — all in one pass.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `product_name` (string), `reviews` (list of objects each with `id`, `rating`, `text`, `date`, `platform`), and optionally `competitor_reviews` (list of `text` + `rating` objects for competitive benchmarking).

**Output:** Structured JSON with `total_reviews`, `average_rating`, `sentiment_breakdown`, `top_themes` (each with frequency and sentiment direction), `improvement_areas`, `competitive_advantages`, a ready-to-post `review_responses` list, `product_insights`, and `marketing_copy_suggestions`.

## Customization

- Pass `competitor_reviews` to get automatic comparative analysis and identify where you win or lose on sentiment.
- Increase `max_tokens` to 4000 when processing large review batches (50+ reviews) to ensure complete output.
- Add a `date_range` filter in `build_prompt()` to focus analysis on reviews from a specific time window, useful for measuring impact after a product update.
