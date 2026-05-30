# {{client_name}} — Client Website (Brand + SEO + CRO)

> When to use: building a client-ready marketing site where brand consistency,
> search visibility, and conversion are all required.

Use the **superpowers** workflow (brainstorm → plan → build → review).
Read `./toolchain-reference.md` for each tool's role before starting.

## Brief
{{brief}}
- **Audience:** {{target_audience}}
- **Pages:** {{pages}}
- **Primary CTA:** {{primary_cta}}
- **Brand:** {{brand_assets}}
- **Industry:** {{industry_type}}

---

## Phase 1 — Ingest (run FIRST)

STOP. Do not proceed to Phase 2 until you have read and summarized every ingestion output below.

{{#github_refs}}
- `codefetch --url {{.}} -o codefetch/{{slug}}.md` → read → summarize architecture and patterns.
  If the repo is large (>20 files) or architecturally complex, ALSO run:
  `graphify ./codefetch/{{slug}}.md -o graphify/GRAPH_REPORT.md` → read the knowledge graph.
{{/github_refs}}

{{#documents}}
- `markitdown {{.}} > ingest/{{slug}}.md` → read for requirements.
  If the document is a brand guide, synthesize a `brand-guidelines` skill file from it.
{{/documents}}

{{#inspiration_urls}}
- `designlang {{.}} --screenshots --full` → DESIGN FROM the emitted *-design-tokens.json,
  *-shadcn-theme.css, and *-design-language.md. Do NOT invent palettes.
{{/inspiration_urls}}

{{#video_refs}}
- Ingest `{{.}}` via `claude-video /watch {{.}}` (transcribe + summarize frames).
  Skip gracefully if claude-video is unavailable.
{{/video_refs}}

---

## Phase 2 — Shape

1. Generate a PRD/spec using `founder-skills:prd-generator`.
2. {{#industry_type}}If industry is known ("{{industry_type}}"), run `ui-ux-pro-max-skill`
   design-system generator for industry-specific rules, palette, and typography.{{/industry_type}}
3. Confirm sitemap, content blocks, CTA flow, and page hierarchy.

---

## Phase 3 — Build

- Load **{{taste_guardrail}}** as the ONLY primary taste guardrail.
- Load `brand-guidelines` and apply tokens from ingestion.
- {{#motion_heavy}}Load `design-motion-principles` (Create mode) for purposeful motion.{{/motion_heavy}}
- Build every page. Design from extracted tokens, never from imagination.
- Run `npx impeccable detect` (or the equivalent audit from the loaded taste guardrail)
  as a QA gate before proceeding to Phase 4.

---

## Phase 4 — Optimize

- **SEO:** Run `ai-seo` audit (Structure / Authority / Presence pillars).
  Run `seo-audit` for traditional technical/on-page checks.
  Apply `schema` markup (FAQ, Article, Organization, Product as relevant).
- **CRO:** Run `founder-skills:cro-optimization` against the 13 principles.
  Output before/after rationale for each change.

---

## Phase 5 — Package

- Bundle into ONE self-contained HTML artifact using `web-artifacts-builder`.
- Ensure all assets are inlined; no external dependencies required to open the file.

---

## Phase 6 — Test

- Playwright: smoke-test links, forms, responsive breakpoints (375/768/1024/1440),
  Lighthouse-ish checks, capture screenshots of each page.
- If any test fails, fix before delivery.

---

## Phase 7 — Deliver

- Optional: render a 20–30s Remotion demo clip of the finished site.
  Check remotion.dev/license before using on paid client work.
- Present the artifact + test report + screenshot gallery to the client.

---

## Constraints
- One taste guardrail only (loaded: {{taste_guardrail}}).
- Design from extracted tokens, never invented palettes.
- If a skill/CLI is missing, log it and continue — never fail the whole run.
- Final deliverable is a single self-contained artifact + passing tests.
