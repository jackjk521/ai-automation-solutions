# {{product_name}} — MVP / Web App + Testable Artifact

> When to use: scoping an MVP, designing a lightweight system, and shipping a
> single-file interactive artifact for user testing.

Use the **superpowers** workflow (brainstorm → plan → build → review).
Read `./toolchain-reference.md` for each tool's role before starting.

## Brief
- **Product:** {{product_name}}
- **Problem:** {{problem}}
- **Core user:** {{core_user}}
- **Must-have features:** {{must_have_features}}
- **Data entities:** {{data_entities}}

---

## Phase 1 — Ingest (run FIRST)

STOP. Do not proceed to Phase 2 until you have read and summarized every ingestion output below.

{{#github_refs}}
- `codefetch --url {{.}} -o codefetch/{{slug}}.md` → read → summarize.
  If the repo is large or complex, ALSO run:
  `graphify ./codefetch/{{slug}}.md -o graphify/GRAPH_REPORT.md` → read the knowledge graph.
{{/github_refs}}

{{#documents}}
- `markitdown {{.}} > ingest/{{slug}}.md` → read for requirements.
{{/documents}}

{{#inspiration_urls}}
- `designlang {{.}} --screenshots --full` → DESIGN FROM the emitted tokens/theme.
{{/inspiration_urls}}

---

## Phase 2 — Spec & System Design

1. Generate a PRD via `founder-skills:prd-generator`.
2. Define data entities, routes, state shape, and API surface.
3. Keep scope to must-haves only (YAGNI). Document explicitly what is OUT of scope.
4. If competitive positioning matters, run `founder-skills:competitor-intel`.

---

## Phase 3 — Build

- Load **{{taste_guardrail}}** as the ONLY primary taste guardrail.
- Build an interactive artifact with in-memory mock/seed data.
- {{#generative_hero}}Use `algorithmic-art` for a generative hero background or brand texture.{{/generative_hero}}
- Every interactive element must have hover/focus/active states.
- Run the taste guardrail's anti-pattern check before Phase 4.

---

## Phase 4 — Test

- Playwright happy-path tests for EACH must-have feature.
- Screenshot desktop + mobile breakpoints.
- If a test fails, fix before proceeding.

---

## Phase 5 — Ship

- Bundle into ONE testable HTML artifact using `web-artifacts-builder`.
- Include a 30-second "how to try it" note at the top of the artifact.
- Deliver for user testing.

---

## Constraints
- One taste guardrail only (loaded: {{taste_guardrail}}).
- If a skill/CLI is missing, log it and continue.
- Final deliverable is a single self-contained artifact + passing tests.
