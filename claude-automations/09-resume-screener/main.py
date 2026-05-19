#!/usr/bin/env python3
"""Screen resumes against job requirements and produce structured candidate assessments."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert talent acquisition specialist and HR professional with 15+ years of experience screening candidates across technology, operations, finance, and creative roles. You apply structured, objective assessment frameworks to evaluate candidates fairly and thoroughly.

Your screening methodology:

EXPERIENCE MATCH (0-100): Evaluate years of experience, relevance of industries and company sizes worked at, career progression trajectory, and whether the candidate has directly performed the core responsibilities of this role. Weight recent experience more heavily.

SKILLS MATCH (0-100): Compare required and nice-to-have skills against what is demonstrated in the resume. Look for skills evidenced by achievements, not just listed. Distinguish between claimed and demonstrated skills.

EDUCATION MATCH (0-100): Assess formal education, certifications, and professional development relative to role requirements. Note if experience compensates for education gaps.

RED FLAGS to actively look for (only genuine concerns, not bias):
- Unexplained employment gaps over 6 months
- Frequent short tenures (under 1 year at multiple consecutive roles) without clear reason
- Significant title inflation or inconsistencies
- Claims without any supporting evidence or metrics
- Missing critical requirements that are non-negotiable
- Skills listed but no related experience or achievement

STRENGTHS to highlight:
- Quantified achievements (%, $, scale)
- Relevant industry or domain experience
- Leadership or cross-functional experience
- Evidence of learning and growth
- Notable companies, clients, or projects

INTERVIEW QUESTIONS: Generate probing questions that specifically target identified weaknesses or gaps — not generic questions. Each question should have a clear reason it was chosen based on the resume review.

CRITICAL: Never discriminate based on name, apparent nationality, ethnicity, gender, age, religion, or any other protected characteristic. Assess only professional qualifications and demonstrated capabilities. Your recommendation must be defensible on merit alone.

Scoring guide: 85-100 = Strong Yes, 70-84 = Yes, 50-69 = Maybe, 0-49 = No

You must output valid JSON only. No markdown, no preamble, no explanation outside the JSON object."""

def build_prompt(data: dict) -> str:
    required_skills_str = "\n".join(f"- {s}" for s in data.get("required_skills", []))
    nice_to_have_str = "\n".join(f"- {s}" for s in data.get("nice_to_have", []))
    return f"""Screen the following candidate's resume against this job opening.

JOB DETAILS:
- Job Title: {data.get("job_title")}
- Minimum Experience Required: {data.get("experience_years")} years

Required Skills:
{required_skills_str}

Nice-to-Have Skills:
{nice_to_have_str}

Job Description:
{data.get("job_description")}

CANDIDATE: {data.get("candidate_name")}

RESUME TEXT:
{data.get("resume_text")}

Output a JSON object with exactly these keys:
- overall_score: integer 0-100 (weighted average of all dimensions)
- recommendation: exactly one of "Strong Yes", "Yes", "Maybe", or "No"
- experience_match: integer 0-100
- skills_match: integer 0-100
- education_match: integer 0-100
- matched_skills: array of strings — required or nice-to-have skills the candidate demonstrably has
- missing_skills: array of strings — required skills absent from the resume
- red_flags: array of strings — genuine concerns found (empty array if none)
- strengths: array of strings — notable positives that differentiate this candidate
- suggested_interview_questions: array of 4-5 specific questions targeting identified gaps or weaknesses
- summary: 2-3 sentence executive summary of the hiring recommendation"""

def run(input_data: dict) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_prompt(input_data)}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r'\{[\s\S]+\}', raw)
    return json.loads(match.group(0)) if match else {"raw": raw}

if __name__ == "__main__":
    example = {
        "job_title": "Senior Python Backend Engineer",
        "job_description": """We are looking for a Senior Python Backend Engineer to join our platform team. You will design and build scalable microservices, own backend architecture decisions, mentor junior engineers, and collaborate with product managers to deliver high-quality features. Our stack includes Python 3.11, FastAPI, PostgreSQL, Redis, and AWS.""",
        "required_skills": ["Python", "REST API design", "PostgreSQL", "AWS", "Docker", "System design"],
        "nice_to_have": ["FastAPI", "Redis", "Kubernetes", "Kafka", "Team leadership"],
        "experience_years": 5,
        "candidate_name": "Jordan Rivera",
        "resume_text": """Jordan Rivera | jordan.rivera@email.com | linkedin.com/in/jordanrivera

EXPERIENCE

Senior Software Engineer — DataFlow Inc. (2021–Present, 3 years)
- Built Python microservices processing 2M+ events/day using Flask and Celery
- Reduced API response time by 40% through PostgreSQL query optimisation and Redis caching
- Led migration of 3 legacy services to AWS ECS, cutting infrastructure costs by $120k/year
- Mentored team of 4 junior engineers; conducted weekly code reviews

Software Engineer — TechBase (2019–2021, 2 years)
- Developed REST APIs in Python (Django) serving 500k daily active users
- Implemented CI/CD pipelines using GitHub Actions and Docker
- Collaborated with product team on 3 major feature launches

Junior Developer — WebStart Agency (2018–2019, 1 year)
- Built client websites and basic REST integrations in Python and JavaScript

EDUCATION
B.S. Computer Science — State University (2018)

SKILLS
Python, Django, Flask, FastAPI, PostgreSQL, MySQL, Redis, AWS (ECS, Lambda, RDS), Docker, Git, REST APIs, Celery, GitHub Actions"""
    }
    print(json.dumps(run(example), indent=2))
