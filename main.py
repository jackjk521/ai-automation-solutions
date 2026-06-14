#!/usr/bin/env python3
"""AI Automation Solutions — CLI entry point."""
import os
import sys
from pathlib import Path

# Ensure project root is always on sys.path
sys.path.insert(0, str(Path(__file__).parent))

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm, Prompt

load_dotenv()
console = Console()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_api_key() -> str:
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key:
        console.print("[red bold]Error:[/red bold] ANTHROPIC_API_KEY is not set.")
        console.print("  1. Copy [cyan].env.example[/cyan] to [cyan].env[/cyan]")
        console.print("  2. Add your key from https://console.anthropic.com")
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
def cli():
    """AI Automation Solutions

    \b
    Commands:
      scrape-leads     Find potential buyers for your service/product
      market-research  Generate a comprehensive market research report
      view-leads       Browse saved leads from the database
    """
    pass


# ---------------------------------------------------------------------------
# scrape-leads
# ---------------------------------------------------------------------------

@cli.command("scrape-leads")
@click.option("--service",    "-s", default=None, help="Service/product you offer")
@click.option("--industry",   "-i", default=None, help="Target buyer industry")
@click.option("--location",   "-l", default=None, help="Target location/region")
@click.option("--max-leads",  "-n", default=50,   help="Max leads to qualify (default 50)")
@click.option("--min-score",        default=None,  help="Min legitimacy score 0-100 (default from .env)")
def scrape_leads(service, industry, location, max_leads, min_score):
    """Scrape the web for potential buyers of your service or product.

    \b
    The automation will:
      1. Search DuckDuckGo for companies matching your criteria
      2. Skip any company already in the database (deduplication)
      3. Scrape each company website for contact details
      4. Use AI to score legitimacy and fit (0-100)
      5. Save qualified leads to SQLite + export CSV
    """
    from config import DB_PATH, LEAD_EVAL_MODEL, MIN_LEGITIMACY_SCORE, REQUEST_DELAY
    from database import LeadsDatabase
    from automations.lead_scraper.evaluator import LeadEvaluator
    from automations.lead_scraper.scraper import LeadScraper

    console.rule("[bold blue]Lead Scraping Automation")

    # Interactive prompts for missing options
    if not service:
        service = Prompt.ask(
            "[cyan]What service/product do you offer?[/cyan]",
            default="digital marketing services",
        )
    if not industry:
        industry = Prompt.ask(
            "[cyan]What industry are your target buyers in?[/cyan]",
            default="ecommerce",
        )
    if not location:
        location = Prompt.ask(
            "[cyan]Target location / region[/cyan]",
            default="Singapore",
        )

    effective_min_score = int(min_score) if min_score is not None else MIN_LEGITIMACY_SCORE

    api_key = _get_api_key()
    db = LeadsDatabase(DB_PATH)
    evaluator = LeadEvaluator(api_key=api_key, model=LEAD_EVAL_MODEL)
    scraper = LeadScraper(
        db=db,
        evaluator=evaluator,
        min_score=effective_min_score,
        request_delay=REQUEST_DELAY,
    )

    output_path = scraper.run(
        service_description=service,
        target_industry=industry,
        location=location,
        max_leads=max_leads,
    )

    console.print(f"\n[bold green]Done![/bold green] Leads saved to [cyan]{output_path}[/cyan]")
    db.close()


# ---------------------------------------------------------------------------
# market-research
# ---------------------------------------------------------------------------

@cli.command("market-research")
@click.option("--niche",              "-n", default=None, help="Market niche to research")
@click.option("--sources-per-topic",        default=3,    help="Web sources per topic (default 3)")
def market_research(niche, sources_per_topic):
    """Research a market niche and generate a comprehensive report.

    \b
    The automation will:
      1. Build targeted search queries across 10 research dimensions
      2. Fetch and parse content from credible web sources
      3. Synthesise findings into a structured Markdown report via AI
      4. Save the report to data/reports/
    """
    from config import RESEARCH_MODEL
    from automations.market_research.report_builder import ReportBuilder
    from automations.market_research.researcher import MarketResearcher

    console.rule("[bold blue]Market Research Automation")

    if not niche:
        niche = Prompt.ask(
            "[cyan]What market niche do you want to research?[/cyan]",
            default="sustainable fashion",
        )

    api_key = _get_api_key()

    # Step 1: Gather research data
    console.print(f"\n[bold]Step 1:[/bold] Gathering data for [cyan]{niche}[/cyan]...")
    researcher = MarketResearcher(delay=2.0)
    research_data = researcher.gather_research(niche, max_sources_per_topic=sources_per_topic)

    total_sources = sum(len(v) for v in research_data.values())
    console.print(
        f"\n  Collected [green]{total_sources}[/green] sources across "
        f"[green]{len(research_data)}[/green] topics\n"
    )

    # Step 2: Build AI report
    console.print("[bold]Step 2:[/bold] Synthesising report with AI (this may take a minute)...")
    builder = ReportBuilder(api_key=api_key, model=RESEARCH_MODEL)
    report_content = builder.build_report(niche, research_data)

    # Step 3: Save
    output_path = builder.save_report(niche, report_content)

    console.rule("[bold green]Research Complete")
    console.print(f"[bold green]Report saved:[/bold green] [cyan]{output_path}[/cyan]")
    console.print(f"[dim]Sources: {total_sources}  |  Topics: {len(research_data)}  |  Model: {RESEARCH_MODEL}[/dim]")

    # Optional preview
    if Confirm.ask("\nShow a preview of the report?", default=False):
        preview = "\n".join(report_content.splitlines()[:40])
        console.print(f"\n{preview}\n[dim]... (truncated — open {output_path} for full report)[/dim]")


# ---------------------------------------------------------------------------
# view-leads
# ---------------------------------------------------------------------------

@cli.command("view-leads")
@click.option("--min-score", default=60, help="Minimum score to display (default 60)")
@click.option("--limit",     default=50, help="Max rows to show (default 50)")
def view_leads(min_score, limit):
    """Browse qualified leads stored in the database."""
    from config import DB_PATH
    from database import LeadsDatabase
    from rich.table import Table

    db = LeadsDatabase(DB_PATH)
    leads = db.get_all_leads(min_score=min_score)
    stats = db.get_stats()

    console.rule("[bold blue]Leads Database")
    console.print(
        f"Total in DB: [bold]{stats['total']}[/bold]  |  "
        f"Avg score: [bold]{stats['avg_score']}[/bold]  |  "
        f"Top score: [bold]{stats['max_score']}[/bold]\n"
    )

    if not leads:
        console.print(f"[yellow]No leads found with score >= {min_score}[/yellow]")
        db.close()
        return

    table = Table(title=f"Leads (score >= {min_score})", show_lines=True)
    table.add_column("#",       style="dim",  width=4)
    table.add_column("Company", style="cyan", no_wrap=True, max_width=35)
    table.add_column("Score",   justify="right", style="green", width=6)
    table.add_column("Type",    max_width=22)
    table.add_column("Email",   max_width=28)
    table.add_column("Phone",   max_width=16)
    table.add_column("Approach")

    for i, lead in enumerate(leads[:limit], 1):
        table.add_row(
            str(i),
            (lead.get("company_name") or lead.get("domain", ""))[:35],
            str(lead.get("legitimacy_score", 0)),
            lead.get("company_type", "")[:22],
            lead.get("email", "")[:28],
            lead.get("phone", "")[:16],
            lead.get("recommended_approach", "")[:55],
        )

    console.print(table)
    console.print(f"\n[dim]Showing {min(limit, len(leads))} of {len(leads)} leads with score >= {min_score}[/dim]")
    db.close()


if __name__ == "__main__":
    cli()
