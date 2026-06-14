import csv
import json
import random
import time
from datetime import datetime
from pathlib import Path
from typing import List

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table

from automations.lead_scraper.evaluator import LeadEvaluator
from automations.lead_scraper.sources.ddg_search import DDGSearchSource
from automations.lead_scraper.sources.web_scraper import extract_domain, scrape_website

console = Console()


class LeadScraper:
    def __init__(
        self,
        db,
        evaluator: LeadEvaluator,
        min_score: int = 60,
        request_delay: float = 2.0,
    ):
        self.db = db
        self.evaluator = evaluator
        self.min_score = min_score
        self.searcher = DDGSearchSource(delay=request_delay)

    def run(
        self,
        service_description: str,
        target_industry: str,
        location: str,
        max_leads: int = 50,
    ) -> str:
        session_id = self.db.start_session(service_description, target_industry, location)

        console.print(f"  [cyan]Service:[/cyan]         {service_description}")
        console.print(f"  [cyan]Target industry:[/cyan] {target_industry}")
        console.print(f"  [cyan]Location:[/cyan]        {location}")
        console.print(f"  [cyan]Min score:[/cyan]       {self.min_score}/100")
        console.print()

        # Step 1: Search
        console.print("[bold]Step 1:[/bold] Searching for companies via DuckDuckGo...")
        raw_results = self.searcher.search_all_queries(
            service_description, target_industry, location, max_per_query=10
        )
        console.print(f"  Found [green]{len(raw_results)}[/green] raw URLs to evaluate\n")

        # Step 2: Scrape + evaluate
        console.print("[bold]Step 2:[/bold] Scraping websites and evaluating each lead...")

        total_processed = 0
        total_skipped_dup = 0
        total_qualified = 0
        qualified_leads: List[dict] = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing...", total=len(raw_results))

            for result in raw_results:
                if total_qualified >= max_leads:
                    progress.update(task, description="[green]Max leads reached, stopping.")
                    break

                url = result.get("url", "")
                if not url or not url.startswith("http"):
                    progress.advance(task)
                    continue

                domain = extract_domain(url)
                if not domain:
                    progress.advance(task)
                    continue

                # Deduplication check
                if self.db.is_scraped(domain):
                    total_skipped_dup += 1
                    progress.update(task, description=f"[yellow]Duplicate — skip: {domain[:45]}")
                    progress.advance(task)
                    continue

                total_processed += 1
                progress.update(task, description=f"Scraping: {domain[:45]}")
                web_data = scrape_website(url)

                progress.update(task, description=f"Evaluating: {domain[:45]}")
                combined = {**result, **web_data}
                evaluation = self.evaluator.evaluate(combined, service_description, target_industry)

                score = evaluation.get("score", 0)
                lead = {
                    "domain": domain,
                    "company_name": (web_data.get("name") or result.get("title", ""))[:200],
                    "description": (web_data.get("description") or result.get("snippet", ""))[:500],
                    "industry": target_industry,
                    "location": location,
                    "website": url,
                    "email": web_data.get("email", ""),
                    "phone": web_data.get("phone", ""),
                    "linkedin": web_data.get("linkedin", ""),
                    "employees": web_data.get("employees", ""),
                    "legitimacy_score": score,
                    "legitimacy_reason": evaluation.get("fit_reason", ""),
                    "company_type": evaluation.get("company_type", ""),
                    "recommended_approach": evaluation.get("recommended_approach", ""),
                    "positive_indicators": json.dumps(evaluation.get("positive_indicators", [])),
                    "red_flags": json.dumps(evaluation.get("red_flags", [])),
                    "search_query": result.get("search_query", ""),
                }

                saved = self.db.save_lead(lead)

                if score >= self.min_score and saved:
                    total_qualified += 1
                    qualified_leads.append(lead)
                    progress.update(
                        task,
                        description=f"[green]Qualified ({score}/100): {domain[:40]}",
                    )
                else:
                    progress.update(
                        task,
                        description=f"[red]Rejected ({score}/100): {domain[:40]}",
                    )

                progress.advance(task)
                time.sleep(random.uniform(0.5, 1.5))

        self.db.complete_session(session_id, total_processed, total_qualified)
        output_path = self._export_csv(qualified_leads, target_industry, location)
        self._show_summary(qualified_leads, total_processed, total_skipped_dup, total_qualified, output_path)
        return output_path

    # ------------------------------------------------------------------
    def _export_csv(self, leads: list, industry: str, location: str) -> str:
        Path("data").mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = "".join(c if c.isalnum() else "_" for c in f"{industry}_{location}")
        filename = f"data/leads_{safe}_{timestamp}.csv"

        fieldnames = [
            "company_name", "domain", "website", "email", "phone", "linkedin",
            "employees", "legitimacy_score", "legitimacy_reason", "company_type",
            "recommended_approach", "positive_indicators", "red_flags",
        ]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(leads)

        return filename

    def _show_summary(
        self,
        leads: list,
        total_processed: int,
        total_skipped_dup: int,
        total_qualified: int,
        output_path: str,
    ):
        console.print()
        console.rule("[bold green]Scraping Complete")

        stats = Table(title="Run Summary", show_header=False, box=None)
        stats.add_column("Metric", style="cyan")
        stats.add_column("Value", style="bold white")
        stats.add_row("Companies processed", str(total_processed))
        stats.add_row("Duplicates skipped", str(total_skipped_dup))
        stats.add_row("Qualified leads", str(total_qualified))
        if total_processed:
            rate = (total_qualified / total_processed) * 100
            stats.add_row("Qualification rate", f"{rate:.1f}%")
        stats.add_row("Output CSV", output_path)
        console.print(stats)

        if leads:
            console.print()
            top = Table(title="Top Qualified Leads", show_lines=True)
            top.add_column("#", style="dim", width=3)
            top.add_column("Company", style="cyan", no_wrap=True)
            top.add_column("Score", justify="right", style="green", width=6)
            top.add_column("Type", width=25)
            top.add_column("Email", width=30)
            top.add_column("Approach")

            for i, lead in enumerate(
                sorted(leads, key=lambda x: x["legitimacy_score"], reverse=True)[:10], 1
            ):
                top.add_row(
                    str(i),
                    (lead.get("company_name") or lead.get("domain", ""))[:40],
                    str(lead.get("legitimacy_score", 0)),
                    lead.get("company_type", "")[:25],
                    lead.get("email", "")[:30],
                    lead.get("recommended_approach", "")[:50],
                )
            console.print(top)
