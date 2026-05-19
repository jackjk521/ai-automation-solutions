# Resume Screener

Evaluates resumes against job requirements and produces a structured hiring recommendation with scores, matched and missing skills, red flags, strengths, and targeted interview questions.

## Usage

```bash
pip install anthropic python-dotenv
ANTHROPIC_API_KEY=your_key python main.py
```

## Input / Output

**Key inputs:** `job_title`, `job_description`, `required_skills` (list), `nice_to_have` (list), `experience_years` (int), `resume_text`, `candidate_name`

**Key outputs:** `overall_score` (0-100), `recommendation` (Strong Yes | Yes | Maybe | No), `experience_match`, `skills_match`, `education_match`, `matched_skills`, `missing_skills`, `red_flags`, `strengths`, `suggested_interview_questions`, `summary`

## Customization

- Pass multiple resumes in a loop and sort by `overall_score` for ranked shortlisting.
- Add a `must_have_skills` field for non-negotiable requirements that trigger an automatic "No".
- Extend the prompt with company culture criteria (e.g., remote-first, high-growth startup) for culture-fit signals.
