#!/usr/bin/env python3
"""Code reviewer — paste any code snippet and get a structured review with fixes."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a senior software engineer and security specialist with 15+ years of experience
conducting code reviews across Python, JavaScript, TypeScript, Go, Java, and more.

Your review covers:
- SECURITY: OWASP Top 10 vulnerabilities (SQL injection, XSS, CSRF, insecure deserialization,
  hardcoded credentials, exposed secrets, improper auth, path traversal)
- BUGS: Logic errors, off-by-one errors, null pointer risks, race conditions, unhandled exceptions
- PERFORMANCE: N+1 queries, unnecessary loops, memory leaks, blocking I/O in async code
- READABILITY: Naming conventions, function length, complexity, dead code, magic numbers
- BEST PRACTICES: Language-specific idioms, design patterns, error handling, logging

Severity levels:
- Critical: Security vulnerabilities or data-loss bugs — must fix before deployment
- High: Bugs that will cause failures in production under normal use
- Medium: Code quality issues that will cause problems at scale
- Low: Style and readability improvements
- Info: Suggestions and modern alternatives

Always provide a specific code_fix example. Be direct and technical. Do not praise the code excessively.

Output valid JSON only. Do not include any text outside the JSON object."""

def build_prompt(data: dict) -> str:
    focus = ", ".join(data.get("review_focus", ["security", "performance", "readability", "best_practices", "bugs"]))
    return f"""Review the following {data.get('language', 'code')} code.

Context: {data.get('context', 'No additional context provided')}
Review focus areas: {focus}

CODE TO REVIEW:
```{data.get('language', '')}
{data.get('code', '')}
```

Return JSON:
{{
  "overall_score": 0,
  "overall_summary": "2-sentence summary of the code quality",
  "issues": [
    {{
      "line_range": "e.g. 12-15",
      "severity": "Critical|High|Medium|Low|Info",
      "category": "Security|Bug|Performance|Readability|Best Practice",
      "description": "clear description of the problem",
      "suggestion": "how to fix it",
      "code_fix": "corrected code snippet"
    }}
  ],
  "security_score": 0,
  "performance_score": 0,
  "readability_score": 0,
  "positive_observations": ["things done well"],
  "refactor_suggestions": ["larger structural improvements"],
  "test_coverage_suggestions": ["what to test"]
}}"""


def run(input_data: dict) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_prompt(input_data)}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r'\{[\s\S]+\}', raw)
    return json.loads(match.group(0)) if match else {"raw": raw}


if __name__ == "__main__":
    example = {
        "language": "python",
        "context": "Flask login endpoint for a SaaS application",
        "review_focus": ["security", "bugs", "best_practices"],
        "code": """
import sqlite3
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "mysecretkey123"
app.debug = True

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        session['username'] = username
        return {'status': 'success', 'user': username}
    else:
        return {'status': 'error', 'message': 'Invalid credentials'}
""",
    }
    result = run(example)
    print(f"Overall score: {result.get('overall_score')}/100")
    print(f"Issues found: {len(result.get('issues', []))}")
    for issue in result.get("issues", []):
        print(f"  [{issue['severity']}] {issue['category']}: {issue['description'][:80]}")
