# Claude AI Automation Library

20 standalone Python automations powered by the [Anthropic Claude API](https://docs.anthropic.com/). Each script runs independently — no n8n, no workflow engine, no infrastructure required. Just Python, your API key, and a terminal.

**Author:** Jed Abner Chu · [aceinternational.solutions](https://aceinternational.solutions)

---

## Quick Start

```bash
cd claude-automations
pip install -r requirements.txt
cp .env.example .env         # add your ANTHROPIC_API_KEY
python 01-email-triage/main.py
```

All scripts run the built-in example data by default. Pass your own data by importing the `run()` function.

---

## Automation Index

| # | Automation | Category | Model | Use Case |
|---|-----------|----------|-------|----------|
| 01 | [Email Triage](#01-email-triage) | Email | Haiku | Classify & draft replies for incoming email |
| 02 | [Lead Qualifier](#02-lead-qualifier) | Sales | Haiku | BANT score leads from form submissions |
| 03 | [Support Ticket Classifier](#03-support-ticket-classifier) | Support | Haiku | Route tickets by category, priority & sentiment |
| 04 | [Weekly Report Generator](#04-weekly-report-generator) | Analytics | Sonnet | KPI data → executive narrative report |
| 05 | [Invoice Generator](#05-invoice-generator) | Finance | Sonnet | Client + line items → branded HTML invoice |
| 06 | [Cold Outreach Generator](#06-cold-outreach-generator) | Sales | Sonnet | Prospect data → personalised email sequence |
| 07 | [Social Media Generator](#07-social-media-generator) | Marketing | Haiku | Topic → LinkedIn, Twitter, Instagram posts |
| 08 | [SEO Content Optimizer](#08-seo-content-optimizer) | Marketing | Sonnet | Blog post → SEO improvements + meta tags |
| 09 | [Resume Screener](#09-resume-screener) | HR | Sonnet | JD + CV → fit score + interview questions |
| 10 | [Meeting Summarizer](#10-meeting-summarizer) | Productivity | Sonnet | Transcript → summary + action items |
| 11 | [Contract Analyzer](#11-contract-analyzer) | Legal | Sonnet | Contract text → risks + negotiation points |
| 12 | [Customer Review Analyzer](#12-customer-review-analyzer) | CX | Sonnet | Batch reviews → insights + response drafts |
| 13 | [Competitor Analyzer](#13-competitor-analyzer) | Strategy | Sonnet | Competitor info → battle card |
| 14 | [Product Description Generator](#14-product-description-generator) | E-commerce | Sonnet | Specs → SEO-optimised product copy |
| 15 | [Code Reviewer](#15-code-reviewer) | Dev Tools | Sonnet | Code snippet → issues + fixes |
| 16 | [Document Q&A](#16-document-qa) | Research | Sonnet | Document + questions → cited answers |
| 17 | [Content Calendar Generator](#17-content-calendar-generator) | Marketing | Sonnet | Brand info → 30-day content calendar |
| 18 | [Data Extractor](#18-data-extractor) | Data | Sonnet | Unstructured text → structured JSON |
| 19 | [FAQ Builder](#19-faq-builder) | Support | Sonnet | Source docs → searchable FAQ pairs |
| 20 | [Web Presence Analyzer](#20-web-presence-analyzer) | Lead Gen | Sonnet | Business data → score + outreach email |

---

## Models Used

| Model | When | Cost |
|-------|------|------|
| `claude-haiku-4-5-20251001` | Fast, high-volume tasks (triage, classification) | ~$0.001 per run |
| `claude-sonnet-4-6` | Quality-sensitive tasks (reports, analysis, code review) | ~$0.01–0.05 per run |

All scripts use **prompt caching** (`cache_control: ephemeral`) on the system prompt, reducing costs by up to 90% on repeated runs.

---

## Using as a Module

Every automation exposes a `run(input_data: dict) -> dict` function:

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from automations import run  # or import directly

from 01_email_triage.main import run as triage
result = triage({
    "subject": "Urgent: Invoice overdue",
    "body": "...",
    "sender": "client@example.com",
    "sender_domain": "example.com"
})
print(result["category"])   # "Urgent"
print(result["draft_reply"])
```

---

## Automation Details

### 01 Email Triage
Classifies incoming emails by category (Urgent/Follow-up/Information/Spam), priority, and sentiment, then drafts a reply.

### 02 Lead Qualifier
Applies BANT scoring (Budget, Authority, Need, Timeline) to lead form data. Returns a 0–100 score, tier, and recommended next step.

### 03 Support Ticket Classifier
Routes tickets by category and priority, generates SLA commitments, and drafts a customer auto-reply.

### 04 Weekly Report Generator
Turns raw KPI metrics into an executive narrative with highlights, concerns, and recommendations.

### 05 Invoice Generator
Produces a complete print-ready HTML invoice from client and line-item data.

### 06 Cold Outreach Generator
Creates a personalised email sequence (initial + 2 follow-ups) plus a LinkedIn message from prospect data.

### 07 Social Media Generator
Generates platform-native posts for LinkedIn, Twitter, Instagram, and Facebook from a topic brief.

### 08 SEO Content Optimizer
Audits blog posts for keyword density, readability, and meta data, then returns specific fixes and an optimised intro.

### 09 Resume Screener
Scores CVs against a job description across experience, skills, and education, and suggests targeted interview questions.

### 10 Meeting Summarizer
Converts raw meeting transcripts into structured summaries with action items, owners, due dates, and risks.

### 11 Contract Analyzer
Identifies parties, key terms, payment conditions, termination clauses, liability caps, and risks in any contract.

### 12 Customer Review Analyzer
Aggregates sentiment, surfaces themes, drafts response copy, and extracts product insights from batches of reviews.

### 13 Competitor Analyzer
Builds a sales battle card with strengths, weaknesses, objection handlers, and strategic recommendations.

### 14 Product Description Generator
Writes short, long, and bullet-point product descriptions plus SEO title and meta description for e-commerce platforms.

### 15 Code Reviewer
Reviews code for bugs, security issues (OWASP Top 10), performance bottlenecks, and style, with line-specific fixes.

### 16 Document Q&A
Answers a list of questions from a document with cited source excerpts and confidence levels.

### 17 Content Calendar Generator
Plans a month of social and blog content with topics, angles, hooks, and optimal posting times.

### 18 Data Extractor
Extracts structured fields from unstructured text (emails, invoices, reports) according to a schema you define.

### 19 FAQ Builder
Mines source content (docs, tickets, calls) to generate categorised, keyword-tagged FAQ pairs and identifies knowledge gaps.

### 20 Web Presence Analyzer
Scores business web presence (0–10), identifies modernisation opportunities, and generates a personalised outreach email.

---

## License

MIT © 2024 Jed Abner Chu ([aceinternational.solutions](https://aceinternational.solutions))
