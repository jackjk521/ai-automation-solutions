# {{output_name}} — Ingest Inputs (Consolidated Brief)

> When to use: turning any mix of repos, documents, URLs, and video into one
> clean Markdown brief + design tokens + knowledge graph.

Read `./toolchain-reference.md` for each tool's role before starting.

## Goal
Consolidate every input below into a single `{{output_name}}.md` brief,
a `design-tokens.json`, and (if repos are complex) a `GRAPH_REPORT.md`.

---

## Phase 1 — Ingest

{{#github_refs}}
- `codefetch --url {{.}} -o codefetch/{{slug}}.md`
  If the repo is large or complex, ALSO run:
  `graphify ./codefetch/{{slug}}.md -o graphify/{{slug}}-graph.md`
{{/github_refs}}

{{#documents}}
- `markitdown {{.}} > ingest/{{slug}}.md`
{{/documents}}

{{#inspiration_urls}}
- `designlang {{.}} --screenshots --full` → emit tokens, theme, and design-language.md.
{{/inspiration_urls}}

{{#video_refs}}
- Ingest `{{.}}` via `claude-video /watch {{.}}` (transcribe + summarize frames).
  Skip gracefully if unavailable.
{{/video_refs}}

---

## Phase 2 — Synthesize

1. Read every emitted Markdown file.
2. Write a 3-paragraph executive summary at the top of `{{output_name}}.md`.
3. Merge all requirements, constraints, and references into structured sections.
4. From inspiration URLs, extract the `design-tokens.json` (W3C DTCG format).
5. If knowledge graphs were generated, include a "System Architecture" section
   summarizing the graph's key modules and dependencies.

---

## Output
- `{{output_name}}.md` — consolidated brief with executive summary
- `design-tokens.json` — from inspiration URLs (if any)
- `graphify/` — knowledge graph reports (if complex repos were ingested)

---

## Constraints
- If a CLI is missing, note it in the output and continue.
- Do not hallucinate requirements not present in the ingested materials.
