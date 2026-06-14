import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MIN_LEGITIMACY_SCORE = int(os.getenv("MIN_LEGITIMACY_SCORE", "60"))
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "2.0"))

DATA_DIR = "data"
REPORTS_DIR = "data/reports"
DB_PATH = "data/leads.db"

# Sonnet for many evaluations (cost-efficient), Opus for one-time deep research
LEAD_EVAL_MODEL = "claude-sonnet-4-6"
RESEARCH_MODEL = "claude-opus-4-8"
