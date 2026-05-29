#!/usr/bin/env python3
"""
21 - Social Trend Newsletter
Weekly trend intelligence across F&B, Active Lifestyle, and Shopping
for Philippines and International markets.

Sources: Google Search scoped to Reddit, TikTok, Instagram
Outputs: Branded HTML newsletter emailed to configured recipient
"""
import os
import json
import re
import smtplib
import urllib.parse
import time
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic
import requests
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

NICHES = ["F&B", "Active Lifestyle", "Shopping"]
LOCATIONS = ["Philippines", "International"]
PLATFORMS = ["reddit.com", "tiktok.com", "instagram.com"]

PAIRS = [(niche, loc) for niche in NICHES for loc in LOCATIONS]

# ── Prompt templates ──────────────────────────────────────────────────────────

RESEARCH_SYSTEM = """You are a senior market research analyst specializing in Southeast Asian and global consumer trends.
Your role: Analyze the current state of a consumer niche for a given market and surface actionable intelligence.
Be specific and grounded. Do NOT fabricate statistics. Use directional language ("growing", "emerging", "declining") when exact data is unavailable.
Always respond with valid JSON only — no markdown fences, no commentary outside the JSON."""

SYNTHESIS_SYSTEM = """You are a strategic intelligence analyst who synthesizes live social media signals with industry context.
Your role: Given (a) real search results from Reddit/TikTok/Instagram and (b) expert industry research, identify the top trending topics and opportunities.
- Every trend you surface MUST be supported by at least one source URL from the search results.
- Quote exact titles/snippets as evidence.
- Be concise and business-focused.
Always respond with valid JSON only — no markdown fences, no commentary outside the JSON."""

NEWSLETTER_SYSTEM = """You are an expert newsletter writer for business professionals and market researchers.
Your role: Transform trend intelligence data into a polished weekly HTML newsletter.
Style: Insightful, analytical, slightly conversational. Data-driven. No fluff.
Requirements:
- Use inline CSS only (email-client safe — no <style> blocks, no external CSS)
- Section structure: header → executive summary → per-niche analysis (PH and Intl side-by-side) → opportunities → sources table → footer
- Highlight the 2-3 most important signals per niche
- Keep each niche section to 150-200 words
Always return ONLY the complete HTML string — no JSON wrapper, no markdown."""


# ── Phase 1a: Search ──────────────────────────────────────────────────────────

def scrape_trends(niche: str, location: str) -> dict:
    """Search Google (via Custom Search API) scoped to TikTok, Reddit, Instagram."""
    api_key = os.environ.get("GOOGLE_CSE_API_KEY", "")
    cx = os.environ.get("GOOGLE_CSE_ID", "")
    all_results = []

    for platform in PLATFORMS:
        query = f'site:{platform} "{niche}" {location} trending'
        params = {
            "key": api_key,
            "cx": cx,
            "q": query,
            "num": 10,
        }
        url = "https://www.googleapis.com/customsearch/v1"
        try:
            resp = requests.get(url, params=params, timeout=15)
            data = resp.json()
            items = data.get("items", [])
            for item in items:
                all_results.append({
                    "platform": platform.split(".")[0],
                    "query": query,
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "display_url": item.get("displayLink", ""),
                })
        except Exception as e:
            all_results.append({
                "platform": platform.split(".")[0],
                "query": query,
                "error": str(e),
            })
        # Respect API rate limits
        time.sleep(0.3)

    return {"niche": niche, "location": location, "results": all_results}


# ── Phase 1b: Research Agent ──────────────────────────────────────────────────

def research_niche_context(niche: str, location: str) -> dict:
    """Claude analyzes industry context for the niche × location pair."""
    prompt = f"""Analyze current trends and opportunities for the following market segment:

Niche: {niche}
Market: {location}
Analysis Date: {datetime.now().strftime('%B %Y')}

Return a JSON object with this exact structure:
{{
  "niche": "{niche}",
  "location": "{location}",
  "market_overview": "2-3 sentence description of the current state",
  "known_trends": [
    {{"trend": "trend name", "description": "why it matters", "momentum": "growing|stable|declining"}}
  ],
  "key_players": ["brand or creator name", "..."],
  "consumer_behaviors": ["specific behavior or preference", "..."],
  "seasonal_signals": "any time-sensitive factors for this month",
  "opportunity_gaps": ["specific gap or unmet need", "..."]
}}

Provide 3-5 items per array. Be specific to {location} context."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=[{"type": "text", "text": RESEARCH_SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r"\{[\s\S]+\}", raw)
    return json.loads(match.group(0)) if match else {"niche": niche, "location": location, "raw": raw}


# ── Phase 2: Synthesis Agent ──────────────────────────────────────────────────

def synthesize_findings(scrape_result: dict, research_result: dict) -> dict:
    """Merge live search results + LLM research → top trends with cited sources."""
    sources_text = ""
    for r in scrape_result.get("results", []):
        if "error" not in r:
            sources_text += f'[{r["platform"].upper()}] {r["title"]}\nURL: {r["url"]}\nSnippet: {r["snippet"]}\nQuery: {r["query"]}\n\n'

    if not sources_text:
        sources_text = "No search results available for this pair."

    niche = scrape_result["niche"]
    location = scrape_result["location"]

    prompt = f"""Synthesize trend intelligence for:
Niche: {niche}
Market: {location}

=== LIVE SEARCH RESULTS (Reddit / TikTok / Instagram) ===
{sources_text}

=== INDUSTRY RESEARCH CONTEXT ===
{json.dumps(research_result, indent=2)}

Return a JSON object with this exact structure:
{{
  "niche": "{niche}",
  "location": "{location}",
  "top_trends": [
    {{
      "name": "trend name",
      "why_it_matters": "business implication in 1-2 sentences",
      "momentum_signal": "rising|hot|established",
      "evidence": "direct quote or paraphrase from search results",
      "source_urls": ["url1", "url2"]
    }}
  ],
  "opportunities": [
    {{"opportunity": "specific actionable opportunity", "rationale": "why now"}}
  ],
  "watch_out": ["risk or counter-signal to monitor"],
  "source_count": {len([r for r in scrape_result.get("results", []) if "error" not in r])}
}}

Rules:
- Include 3-5 top_trends. Each MUST reference at least one URL from the search results.
- Include 2-3 opportunities.
- If search results are sparse, note this honestly in why_it_matters."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=[{"type": "text", "text": SYNTHESIS_SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r"\{[\s\S]+\}", raw)
    return json.loads(match.group(0)) if match else {"niche": niche, "location": location, "raw": raw}


# ── Phase 3: Newsletter Generator ────────────────────────────────────────────

def generate_newsletter(all_syntheses: list[dict], all_scrape_results: list[dict], week_ending: str) -> str:
    """Generate the full branded HTML newsletter from all 6 synthesis results."""

    # Build per-niche sections for the prompt
    niche_sections = {}
    for s in all_syntheses:
        key = s["niche"]
        if key not in niche_sections:
            niche_sections[key] = {}
        niche_sections[key][s["location"]] = s

    # Collect all sources for the sources table
    all_sources = []
    for sr in all_scrape_results:
        for r in sr.get("results", []):
            if "error" not in r and r.get("url"):
                all_sources.append({
                    "niche": sr["niche"],
                    "location": sr["location"],
                    "platform": r["platform"],
                    "title": r["title"][:80] + ("…" if len(r["title"]) > 80 else ""),
                    "url": r["url"],
                    "query": r["query"],
                })

    total_sources = len(all_sources)
    sources_json = json.dumps(all_sources[:60], indent=2)  # cap at 60 for prompt size
    synthesis_json = json.dumps(niche_sections, indent=2)

    prompt = f"""Create a weekly trend intelligence newsletter.

Week Ending: {week_ending}
Total Sources Analyzed: {total_sources} posts/threads across Reddit, TikTok, Instagram

=== TREND ANALYSIS DATA ===
{synthesis_json}

=== ALL SOURCES (for sources table) ===
{sources_json}

Generate a complete, self-contained HTML email newsletter with INLINE CSS ONLY (no <style> blocks).

Required structure and styling:
1. Header bar: dark navy (#0f1117) background, white title "📊 Weekly Trend Intelligence", subtitle "Week of {week_ending}", indigo accent line
2. Executive Summary box: 3-4 bullet points of the most important signals across all niches
3. For each niche (F&B, Active Lifestyle, Shopping): a 2-column row showing Philippines left, International right
   - Each column: niche name chip, top 3 trends as bullets with momentum badge (🔥 hot / 📈 rising / ✅ established), key opportunity callout box
4. Opportunities section: top 5 cross-niche opportunities as cards
5. Sources table: niche | location | platform | title (hyperlinked) | query used — show top 20 most relevant
6. Footer: "Generated by Claude Sonnet + Google Custom Search · {week_ending}" in small gray text

Color palette (inline):
- Background: #f8fafc
- Card background: #ffffff
- Header: #0f1117
- Accent: #4f46e5
- F&B accent: #dc2626
- Active Lifestyle accent: #16a34a
- Shopping accent: #d97706
- Philippines badge: #1d4ed8 text on #dbeafe
- International badge: #7c3aed text on #ede9fe

Max width: 700px, centered. Font: Arial, sans-serif. Must render well in Gmail."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=[{"type": "text", "text": NEWSLETTER_SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    return response.content[0].text


# ── Phase 4: Email Sender ─────────────────────────────────────────────────────

def send_email(html_body: str, subject: str) -> bool:
    """Send HTML email via Gmail SMTP with app password."""
    from_addr = os.environ.get("EMAIL_FROM", "")
    to_addr = os.environ.get("EMAIL_TO", "")
    password = os.environ.get("EMAIL_APP_PASSWORD", "")

    if not all([from_addr, to_addr, password]):
        print("⚠️  Email not sent — EMAIL_FROM, EMAIL_TO, or EMAIL_APP_PASSWORD not set.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
        print(f"✅ Newsletter sent to {to_addr}")
        return True
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        return False


# ── Orchestrator ──────────────────────────────────────────────────────────────

def run(input_data: dict = None) -> dict:
    """
    Main orchestrator. Runs all phases and returns the newsletter result.

    input_data keys (all optional — defaults used if omitted):
      niches: list of niche strings (default: ["F&B", "Active Lifestyle", "Shopping"])
      locations: list of location strings (default: ["Philippines", "International"])
      send_email: bool (default: True)
      save_preview: bool (default: False) — saves newsletter.html to /tmp/
    """
    if input_data is None:
        input_data = {}

    niches = input_data.get("niches", NICHES)
    locations = input_data.get("locations", LOCATIONS)
    should_send = input_data.get("send_email", True)
    save_preview = input_data.get("save_preview", False)

    pairs = [(n, l) for n in niches for l in locations]
    week_ending = (datetime.now() + timedelta(days=(6 - datetime.now().weekday()))).strftime("%B %d, %Y")

    print(f"\n🚀 Social Trend Newsletter — Week ending {week_ending}")
    print(f"   Analyzing {len(pairs)} niche×location pairs × {len(PLATFORMS)} platforms")
    print(f"   Total search queries: {len(pairs) * len(PLATFORMS)}\n")

    # ── Phase 1: Parallel scraping + research ─────────────────────────────────
    print("⏳ Phase 1: Scraping + Research (running in parallel)...")

    scrape_results = {}
    research_results = {}

    with ThreadPoolExecutor(max_workers=min(len(pairs) * 2, 12)) as executor:
        scrape_futures = {
            executor.submit(scrape_trends, niche, loc): (niche, loc)
            for niche, loc in pairs
        }
        research_futures = {
            executor.submit(research_niche_context, niche, loc): (niche, loc)
            for niche, loc in pairs
        }

        for future in as_completed(scrape_futures):
            niche, loc = scrape_futures[future]
            try:
                result = future.result()
                scrape_results[(niche, loc)] = result
                count = len([r for r in result.get("results", []) if "error" not in r])
                print(f"   ✅ Scraped  {niche} × {loc}: {count} results")
            except Exception as e:
                print(f"   ❌ Scrape failed {niche} × {loc}: {e}")
                scrape_results[(niche, loc)] = {"niche": niche, "location": loc, "results": []}

        for future in as_completed(research_futures):
            niche, loc = research_futures[future]
            try:
                result = future.result()
                research_results[(niche, loc)] = result
                print(f"   ✅ Research {niche} × {loc}: done")
            except Exception as e:
                print(f"   ❌ Research failed {niche} × {loc}: {e}")
                research_results[(niche, loc)] = {"niche": niche, "location": loc}

    # ── Phase 2: Sequential synthesis (needs both phase 1 outputs) ────────────
    print("\n⏳ Phase 2: Synthesis (merging search + research per pair)...")
    all_syntheses = []
    for niche, loc in pairs:
        sr = scrape_results.get((niche, loc), {"niche": niche, "location": loc, "results": []})
        rr = research_results.get((niche, loc), {"niche": niche, "location": loc})
        try:
            synthesis = synthesize_findings(sr, rr)
            all_syntheses.append(synthesis)
            trend_count = len(synthesis.get("top_trends", []))
            print(f"   ✅ Synthesized {niche} × {loc}: {trend_count} trends identified")
        except Exception as e:
            print(f"   ❌ Synthesis failed {niche} × {loc}: {e}")
            all_syntheses.append({"niche": niche, "location": loc, "top_trends": [], "opportunities": []})

    # ── Phase 3: Newsletter generation ────────────────────────────────────────
    print("\n⏳ Phase 3: Generating HTML newsletter...")
    all_sr_list = list(scrape_results.values())
    newsletter_html = generate_newsletter(all_syntheses, all_sr_list, week_ending)
    print("   ✅ Newsletter HTML generated")

    # ── Save preview ──────────────────────────────────────────────────────────
    if save_preview:
        preview_path = "/tmp/newsletter_preview.html"
        with open(preview_path, "w") as f:
            f.write(newsletter_html)
        print(f"   💾 Preview saved to {preview_path}")

    # ── Phase 4: Send email ───────────────────────────────────────────────────
    subject = f"📊 Weekly Trend Intelligence — {week_ending}"
    email_sent = False
    if should_send:
        print("\n⏳ Phase 4: Sending email...")
        email_sent = send_email(newsletter_html, subject)

    # ── Summary ───────────────────────────────────────────────────────────────
    total_sources = sum(
        len([r for r in sr.get("results", []) if "error" not in r])
        for sr in all_sr_list
    )
    total_trends = sum(len(s.get("top_trends", [])) for s in all_syntheses)

    print(f"\n📊 Run complete:")
    print(f"   Sources analyzed : {total_sources}")
    print(f"   Trends identified: {total_trends}")
    print(f"   Pairs covered    : {len(all_syntheses)}")
    print(f"   Email sent       : {'yes' if email_sent else 'no'}")

    return {
        "week_ending": week_ending,
        "pairs_analyzed": len(all_syntheses),
        "total_sources": total_sources,
        "total_trends": total_trends,
        "syntheses": all_syntheses,
        "newsletter_html": newsletter_html,
        "email_sent": email_sent,
    }


if __name__ == "__main__":
    result = run({
        "niches": ["F&B", "Active Lifestyle", "Shopping"],
        "locations": ["Philippines", "International"],
        "send_email": True,
        "save_preview": True,   # saves /tmp/newsletter_preview.html to inspect before email
    })
    print(f"\n✅ Done. Newsletter: {len(result['newsletter_html'])} chars")
    print(f"   Open preview: open /tmp/newsletter_preview.html")
