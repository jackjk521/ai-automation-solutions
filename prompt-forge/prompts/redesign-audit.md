# Redesign Audit — Improve Existing Site / Codebase

> When to use: a site or codebase already exists and needs systematic audit,
> redesign, and quality improvement without a full rebuild.

Use the **superpowers** workflow (brainstorm → plan → build → review).
Read `./toolchain-reference.md` for each tool's role before starting.

## Goal
Audit and redesign **{{existing_site_url_or_path}}**.

- **Pain points:** {{pain_points}}
- **Goals:** {{goals}}

---

## Phase 1 — Ingest (run FIRST)

STOP. Do not proceed to Phase 2 until you have read and summarized every ingestion output.

- If the target is a URL: `designlang {{existing_site_url_or_path}} --screenshots --full`
  → read design-language.md, tokens, and graded report card.
- If the target is a local path: run `npx impeccable detect {{existing_site_url_or_path}}`
  to get an immediate anti-pattern report.
- If source code is available: `codefetch --dir {{existing_site_url_or_path}} -o codefetch/existing.md`
  → read → summarize structure.

---

## Phase 2 — Multi-Layer Audit

1. **Design audit:** `redesign-skill` — audit UI first, then fix layout, spacing, hierarchy, styling.
2. **Industry audit:** If industry is known, run `ui-ux-pro-max-skill` design-system generator
   to compare the existing site against industry best practices.
3. **Motion audit:** `design-motion-principles` (Audit mode) — motion-gap analysis,
   anti-AI-slop checklist, branded HTML report.
4. **Technical audit:** `impeccable audit` — a11y, performance, responsive, UX writing.
5. **CRO audit:** `founder-skills:cro-optimization` — 13 principles, before/after.

---

## Phase 3 — Prioritized Fix List

Output a single table sorted by **Impact × Effort**:

| Priority | Layer | Issue | Current State | Recommended Fix | Effort |
|---|---|---|---|---|---|
| P0 | Design | … | … | … | Low |
| P1 | Motion | … | … | … | Medium |
| … | … | … | … | … | … |

---

## Phase 4 — Redesign (selected fixes)

- Apply the top P0–P2 fixes.
- Load **{{taste_guardrail}}** as the ONLY primary taste guardrail.
- Rebuild affected components/pages.
- Run all audits again to verify improvement.
- Bundle into a single HTML artifact via `web-artifacts-builder`.

---

## Phase 5 — Test

- Playwright: regression-test all affected flows.
- Screenshot before/after for every changed page.

---

## Constraints
- One taste guardrail only (loaded: {{taste_guardrail}}).
- Do not rebuild what doesn't need rebuilding. Targeted fixes only.
- If a skill/CLI is missing, log it and continue.
