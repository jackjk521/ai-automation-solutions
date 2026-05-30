# Toolchain Reference

> Read this file before starting any build. It defines each tool's exact role,
> when to use it, its output, and how it wires with other tools.

---

## Ingestion CLIs

### `codefetch`
**Role:** Converts a GitHub repository or local directory into a single consolidated Markdown file for LLM consumption.

**When to use:**
- Any time `{{github_refs}}` is non-empty.
- When you need to understand an existing codebase before modifying or extending it.
- When building on top of a third-party library or reference implementation.

**Commands:**
```bash
# Remote repo
codefetch --url https://github.com/org/repo -o codefetch/repo.md

# Local directory
codefetch --dir ./src -o codefetch/src.md
```

**Output:** `codefetch/<name>.md` — full file tree + file contents, filtered by `.codefetchignore`.

**Wires with:** `graphify` (for complex repos), Claude's context window (read the output before designing).

**Graceful degradation:** If `codefetch` is not on PATH, note it and summarize the repo structure manually from a `git ls-tree`.

---

### `markitdown`
**Role:** Converts rich documents (PDF, PPTX, DOCX, XLSX, HTML, images, audio) into clean Markdown for ingestion.

**When to use:**
- Any time `{{documents}}` is non-empty.
- To ingest brand guides, briefs, RFPs, specs, or slide decks.

**Command:**
```bash
markitdown ./brief.pdf > ingest/brief.md
markitdown ./brand-guide.pptx > ingest/brand-guide.md
```

**Install:** `pip install 'markitdown[all]'`

**Output:** `ingest/<name>.md` — structured Markdown preserving headings, tables, lists, and captions.

**Special case:** If the document is a brand guide, after ingestion synthesize a `brand-guidelines` skill file from the extracted tokens, colors, fonts, and voice notes.

**Graceful degradation:** If unavailable, paste document content into the conversation manually and note the limitation.

---

### `designlang` (alias: `design-extract`)
**Role:** Visits a URL, takes screenshots, and emits a full design-language extraction: color tokens, typography scale, spacing system, motion language, component inventory, and a graded report card.

**When to use:**
- Any time `{{inspiration_urls}}` or `{{reference_url}}` is non-empty.
- To lift another site's design system before rebuilding a component for a client.
- As part of a Redesign Audit to score the existing site.

**Command:**
```bash
designlang https://stripe.com --screenshots --full
```

**Output files:**
- `stripe-design-language.md` — readable summary with grades (A–F per axis)
- `stripe-design-tokens.json` — W3C DTCG-format token file
- `stripe-shadcn-theme.css` — ready-to-use CSS custom properties
- `stripe-screenshot-*.png` — viewport screenshots

**Critical rule:** After running `designlang`, DESIGN FROM the emitted token files. Never invent palettes, type scales, or spacing from imagination.

**Graceful degradation:** If unavailable, take manual screenshots and document tokens by inspection.

---

### `graphify`
**Role:** Builds a structured knowledge graph from a codebase or Markdown document, outputting a human- and LLM-readable graph report that maps modules, dependencies, data flow, entry points, and architectural patterns.

**When to use:**
- On any repo with >20 files or complex cross-module dependencies.
- When `complexRepo` is checked in the generator.
- After `codefetch`, before system design: `graphify ./codefetch/<name>.md -o graphify/GRAPH_REPORT.md`
- After completing a build, re-run to verify the graph reflects the new architecture.

**Command:**
```bash
graphify ./codefetch/repo.md -o graphify/GRAPH_REPORT.md
```

**Output:** `graphify/GRAPH_REPORT.md` — graph of modules, their public APIs, dependency edges, and data-flow annotations.

**Always read GRAPH_REPORT.md before system design.** Identify: entry points, data models, plugin points for the new feature.

**Graceful degradation:** If unavailable, manually map modules from the codefetch output.

---

### `claude-video`
**Role:** Ingests video files or URLs, transcribes audio, summarizes key frames, and returns a Markdown brief of the video content.

**When to use:**
- Any time `{{video_refs}}` is non-empty.
- Client walkthroughs, recorded demos, or tutorial references.

**Command:**
```bash
claude-video /watch ./walkthrough.mp4
claude-video /watch https://youtube.com/watch?v=...
```

**Output:** Markdown transcript + frame summary.

**Graceful degradation:** If unavailable, note it in the output and ask the user to paste a written summary.

---

## Orchestration

### `superpowers` (plugin)
**Role:** Orchestrates the full build lifecycle using TDD: brainstorm → plan → build → review → finish. Prevents skipping phases and enforces the hard-stop ingestion rule.

**Install:** Add to `.claude/plugins/` per the superpowers docs.

**Phases it enforces:**
1. **Brainstorm** — generate 3+ approaches, pick the best one.
2. **Plan** — write a scoped spec with tasks and test cases before touching code.
3. **Build** — implement against the spec, running tests incrementally.
4. **Review** — self-review against the taste guardrail + constraints.
5. **Finish** — deliver the artifact, test report, and screenshots.

**Rule:** Never skip phases. Never proceed to Build without a written Plan.

---

## Taste Guardrails (pick exactly ONE primary)

### `impeccable` (default)
**Role:** Primary taste guardrail for refined, functional, production-quality interfaces. Enforces: whitespace discipline, type hierarchy, color restraint, accessibility, semantic HTML, no AI-slop patterns (floating cards with gradients, emoji abuse, border-radius overload).

**Install:** Copy `impeccable/` into `.claude/skills/`

**Commands:**
- `npx impeccable detect` — scan for anti-patterns, output a scored report
- `npx impeccable audit` — full a11y + performance + UX writing + component audit

**When to use:** Default for all client work. Use for: corporate, SaaS, e-commerce, editorial, fintech, healthcare.

**Conflicts with:** `taste-skill`, `ui-ux-pro-max-skill` — never load simultaneously.

---

### `taste-skill` (gpt-taste variant)
**Role:** Primary taste guardrail tuned for bold, award-winning, Awwwards-adjacent aesthetics. Prioritizes visual impact, motion richness, and genre-defining originality.

**Install:** `npx skills add https://github.com/Leonxlnx/taste-skill`

**When to use:** Face-Off Variant B, projects where client explicitly wants "award-winning" look, creative agencies, high-fashion, entertainment.

**Conflicts with:** `impeccable`, `ui-ux-pro-max-skill`.

---

### `ui-ux-pro-max-skill`
**Role:** Primary taste guardrail that generates an industry-specific design system (palette, type scale, component inventory, UX patterns) based on the target industry. Includes a competitor benchmarking layer.

**Install:** `npx skills add https://github.com/ognjengt/founder-skills` (bundled)

**When to use:** When `{{industry_type}}` is known and you want industry-calibrated design rules (e.g. "spa" → muted neutrals + serif; "fintech" → trust signals + dense data tables; "healthtech" → accessibility-first + clinical clarity).

**Conflicts with:** `impeccable`, `taste-skill`.

---

### `design-motion-principles` (secondary — may combine with any primary)
**Role:** Adds purposeful motion design. Two modes:
- **Create mode** — generate motion choreography (entrance, exit, scroll, micro-interactions) that reinforces the brand personality.
- **Audit mode** — score existing motion against principles; flag AI-slop transitions (generic easing, excessive bounce, unmotivated parallax).

**Does NOT conflict** with primary taste guardrails. Load as a secondary skill.

**When to use:** Any project with animation, scroll effects, page transitions, or motion-heavy Variant B.

---

## Founder Skills (via `founder-skills` plugin)

**Install:** `npx skills add https://github.com/ognjengt/founder-skills`

### `founder-skills:prd-generator`
Generates a scoped Product Requirements Document: problem statement, user stories, acceptance criteria, out-of-scope list, success metrics. Run before any Build phase.

### `founder-skills:cro-optimization`
Audits a page against 13 Conversion Rate Optimization principles (above-the-fold value prop, social proof placement, CTA clarity, friction reduction, urgency/scarcity, trust signals, etc.). Outputs before/after rationale for every change.

### `founder-skills:competitor-intel`
Researches and summarizes competitive positioning, feature gaps, pricing models, and messaging strategies. Run during Spec phase.

### `founder-skills:pricing-strategist`
Optimizes the pricing page: tier naming, anchor pricing, feature packaging, decoy pricing effects, FAQ objection handling.

### `founder-skills:brand-copywriter`
Writes on-brand marketing copy (headlines, taglines, feature descriptions, CTAs, meta descriptions) consistent with the brand voice defined in brand assets.

---

## SEO & Schema Skills

### `ai-seo`
**Role:** Audits and optimizes for AI-Era Search (AEO/GEO/LLMO). Checks three pillars:
- **Structure** — 40–60 word answer blocks, FAQ tables, comparison tables, definition boxes, "What is X?" sections.
- **Authority** — citations, expert quotes, linked stats, Wikipedia/Reddit presence strategy.
- **Presence** — coverage on third-party review sites, social platforms, AI training-data sources.

Also verifies `robots.txt` allows AI crawlers: `GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`.
Drafts `llms.txt` for LLM-accessible site summary.

### `seo-audit`
**Role:** Traditional technical and on-page SEO: indexability, canonical tags, robots.txt, Core Web Vitals, mobile-friendliness, page speed, internal linking, meta tags, heading hierarchy, image alt text.

### `schema`
**Role:** Generates JSON-LD structured data markup. Selects appropriate schemas based on page type:
- `FAQ` — for FAQ sections
- `HowTo` — for guides and tutorials
- `Product` — for product/pricing pages
- `Article` — for blog posts
- `Organization` — for About/Contact pages
- `BreadcrumbList` — for multi-level sites

---

## Packaging & Testing

### `web-artifacts-builder`
**Role:** Bundles the finished build into ONE self-contained HTML file. Inlines all CSS, JS, fonts, and images. The output file opens without any server, build step, or external dependencies — paste the URL into a browser tab or email it to a client.

**When to use:** Always. Every template ends with: bundle → single artifact → deliver.

### `playwright`
**Role:** Browser automation for smoke testing. Standard test suite per template:
- Follow all links (assert no 404s)
- Submit all forms (happy path)
- Screenshot desktop (1440px), tablet (768px), mobile (375px)
- Measure Lighthouse-ish performance (CLS, LCP proxies)
- Assert key text / CTA elements are visible

**Rule:** If any Playwright test fails, fix before delivery. Never ship with failing tests.

### `algorithmic-art`
**Role:** Generates generative, code-driven visual backgrounds and textures (canvas-based or SVG). Use for hero sections, loading screens, or brand textures that need visual interest without stock photos.

**When to use:** `{{generative_hero}}` flag, or when client brief mentions "dynamic", "generative", "data-viz", "particle", "procedural".

### `remotion`
**Role:** Renders a short MP4 demo clip of the finished artifact using React-based video composition.

**When to use:** Optional — when a client needs a demo video of the built product for a pitch or launch.

**License note:** Verify `remotion.dev/license` terms before using on paid client work. The free license applies to personal and open-source projects.

---

## Quality & Brand Skills

### `output-skill`
**Role:** Enforces complete, production-ready output. No placeholder comments like `// TODO`, `...`, `/* rest of component */`, or half-finished code blocks. Claude must write the full implementation.

**When to use:** Any time completeness is non-negotiable (client delivery, artifact output).

### `brand-guidelines`
**Role:** Loads and enforces the client's brand system across all generated components. Checks: correct color usage, typography tokens, logo clearspace, tone of voice, and component naming conventions.

**Source:** Generated from ingested brand documents via `markitdown`. If no document exists, built manually from `{{brand_assets}}` field.

---

## Wiring Summary

| Input field | Auto-triggers | Secondary trigger |
|---|---|---|
| `github_refs` | `codefetch` | `graphify` (if complex repo checked) |
| `documents` | `markitdown` | `brand-guidelines` (if document is brand guide) |
| `inspiration_urls` | `designlang` | — |
| `reference_url` | `designlang` | — |
| `video_refs` | `claude-video` | — |

**Hard stop rule:** After every Phase 1 ingestion, Claude must output a bullet-point summary of every file read before proceeding to Phase 2. This is enforced by the line: `"STOP. Do not proceed to Phase 2 until you have read and summarized every ingestion output above."`

**Taste conflict rule:** Never load `impeccable` + `taste-skill` + `ui-ux-pro-max-skill` simultaneously. `design-motion-principles` is a secondary skill and does not count as a primary guardrail.

**Graceful degradation rule:** If any CLI or skill is not found on PATH or in `.claude/skills/`, log the missing tool and continue. Never crash or block the entire run.
