# Code Reviewer

Reviews any code snippet for security vulnerabilities, bugs, performance issues, and best practices — with line-specific fixes.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Input:** `code` (string), `language`, `context` (what the code does), `review_focus` (list of: security/performance/readability/best_practices/bugs).

**Output:** `overall_score` (0–100), `issues` (each with line_range/severity/category/description/suggestion/code_fix), security/performance/readability sub-scores, `positive_observations`, `refactor_suggestions`.

## Customization

- Set `review_focus: ["security"]` for a security-only audit before production deploys
- Integrate into a CI pipeline: read staged files, pass to `run()`, fail if any Critical/High issues found
- Change the language field to `typescript`, `go`, `java`, etc. — the model adjusts its idiom expectations
