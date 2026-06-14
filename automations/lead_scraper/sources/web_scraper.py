import random
import re
from typing import Dict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

_SKIP_EMAIL_KEYWORDS = {"example", "schema", "test", "noreply", "no-reply", "sentry", "w3.org"}


def extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        return domain[4:] if domain.startswith("www.") else domain
    except Exception:
        return ""


def scrape_website(url: str, timeout: int = 10) -> Dict:
    result: Dict = {
        "url": url,
        "domain": extract_domain(url),
        "name": "",
        "description": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "employees": "",
        "error": None,
    }

    headers = {"User-Agent": random.choice(_USER_AGENTS)}

    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # Title
        title_tag = soup.find("title")
        result["name"] = title_tag.get_text(strip=True)[:200] if title_tag else ""

        # Meta/OG description
        for attr_name, attr_val in [("name", "description"), ("property", "og:description")]:
            tag = soup.find("meta", attrs={attr_name: re.compile(attr_val, re.I)})
            if tag and tag.get("content"):
                result["description"] = tag["content"][:500]
                break

        text = resp.text

        # Emails — skip obvious non-contact ones
        emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
        for email in emails:
            if not any(kw in email.lower() for kw in _SKIP_EMAIL_KEYWORDS):
                result["email"] = email
                break

        # Phone numbers
        phones = re.findall(
            r"(?:\+\d{1,3}[\s\-]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}", text
        )
        result["phone"] = phones[0] if phones else ""

        # LinkedIn company page
        linkedin_links = soup.find_all("a", href=re.compile(r"linkedin\.com/company", re.I))
        if linkedin_links:
            result["linkedin"] = linkedin_links[0].get("href", "")

        # Employee count hints
        for pattern in [
            r"(\d[\d,]*\+?\s*(?:to\s*\d[\d,]*)?\s*employees)",
            r"team\s+of\s+(\d+)",
            r"(\d+)\s*(?:people|professionals|staff|team members)",
        ]:
            m = re.search(pattern, text, re.I)
            if m:
                result["employees"] = m.group(0)[:100]
                break

    except Exception as e:
        result["error"] = str(e)[:200]

    return result
