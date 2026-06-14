import random
import time
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

console = Console()

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36",
]

_RESEARCH_TOPICS = [
    ("Market Size & Revenue",     "{niche} market size revenue 2024 2025 statistics billion"),
    ("Growth Rate & Forecast",    "{niche} industry growth rate forecast CAGR 2025 2026"),
    ("Key Trends",                "{niche} market trends 2025 emerging"),
    ("Key Players & Competition", "top companies {niche} industry leaders market share 2024"),
    ("Target Customers",          "{niche} target customers demographics buyer persona"),
    ("Consumer Behaviour",        "{niche} consumer behaviour preferences survey insights"),
    ("Challenges & Risks",        "{niche} industry challenges risks problems barriers"),
    ("Opportunities & Gaps",      "{niche} market opportunities gaps underserved 2025"),
    ("Technology & Innovation",   "{niche} technology innovation digital transformation latest"),
    ("Pricing & Financials",      "{niche} pricing revenue model profit margin industry average"),
]


class MarketResearcher:
    def __init__(self, delay: float = 2.0):
        self.delay = delay

    def _topics_for(self, niche: str) -> List[Dict]:
        return [
            {"topic": label, "query": query.format(niche=niche)}
            for label, query in _RESEARCH_TOPICS
        ]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _search(self, query: str, max_results: int = 8) -> List[Dict]:
        time.sleep(self.delay + random.uniform(0, 1))
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    {
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    }
                )
        return results

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=8))
    def _fetch_article(self, url: str, timeout: int = 8) -> Optional[str]:
        headers = {"User-Agent": random.choice(_USER_AGENTS)}
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        for selector in ["article", "main", ".content", "#content", ".post-content", ".article-body"]:
            node = soup.select_one(selector)
            if node:
                return node.get_text(separator=" ", strip=True)[:4000]

        return soup.get_text(separator=" ", strip=True)[:4000]

    def gather_research(self, niche: str, max_sources_per_topic: int = 3) -> Dict:
        topics = self._topics_for(niche)
        research_data: Dict[str, List] = {}

        for item in topics:
            topic = item["topic"]
            query = item["query"]
            console.print(f"  Researching: [cyan]{topic}[/cyan]...")

            try:
                results = self._search(query)
            except Exception:
                results = []

            topic_sources = []
            for result in results[:max_sources_per_topic]:
                url = result.get("url", "")
                content = result["snippet"]  # fallback

                if url and url.startswith("http"):
                    try:
                        fetched = self._fetch_article(url)
                        if fetched:
                            content = fetched
                    except Exception:
                        pass

                topic_sources.append(
                    {
                        "title": result["title"],
                        "url": url,
                        "snippet": result["snippet"],
                        "content": content,
                    }
                )
                time.sleep(random.uniform(0.5, 1.2))

            research_data[topic] = topic_sources

        return research_data
