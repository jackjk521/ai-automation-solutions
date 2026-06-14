import random
import time
from typing import Dict, List

from duckduckgo_search import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential


class DDGSearchSource:
    def __init__(self, delay: float = 2.0):
        self.delay = delay

    def build_queries(
        self, service_description: str, target_industry: str, location: str
    ) -> List[str]:
        return [
            f"{target_industry} companies in {location}",
            f"best {target_industry} businesses {location} contact",
            f'"{target_industry}" firms agencies {location} email',
            f"{target_industry} service providers {location} website",
            f"{target_industry} companies {location} looking for {service_description}",
            f"top {target_industry} startups {location}",
        ]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _search(self, query: str, max_results: int) -> List[Dict]:
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

    def search_all_queries(
        self,
        service_description: str,
        target_industry: str,
        location: str,
        max_per_query: int = 10,
    ) -> List[Dict]:
        queries = self.build_queries(service_description, target_industry, location)
        all_results: List[Dict] = []
        seen_urls: set = set()

        for query in queries:
            try:
                results = self._search(query, max_results=max_per_query)
                for r in results:
                    url = r.get("url", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        r["search_query"] = query
                        all_results.append(r)
            except Exception:
                continue

        return all_results
