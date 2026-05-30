# Design From Reference — Extract & Rebuild

> When to use: lifting a reference site's design language and rebuilding a
> chosen component or page on the client's brand.

Use the **superpowers** workflow (brief → plan → build → review).
Read `./toolchain-reference.md` for each tool's role before starting.

## Goal
Extract the design language of **{{reference_url}}**, then rebuild
**{{target}}** on the client's brand:
{{brand_assets}}

---

## Phase 1 — Extract (run FIRST)

STOP. Do not proceed to Phase 2 until you have read and summarized the extraction output.

- `designlang {{reference_url}} --screenshots --full`
  → Read *-design-language.md, *-design-tokens.json, *-shadcn-theme.css.
  → Summarize: type scale, palette, spacing system, radii, shadows, motion language.

---

## Phase 2 — Map

1. Map the reference's patterns onto the client's brand tokens.
2. Identify which reference patterns to adopt, adapt, or discard.
3. Write a short DESIGN_DECISIONS.md explaining every choice.

---

## Phase 3 — Rebuild

- Load **{{taste_guardrail}}** as the ONLY primary taste guardrail.
- Rebuild **{{target}}** using the mapped tokens.
- Use `design-motion-principles` (Create mode) if the reference has notable motion.
- Bundle into a single HTML artifact via `web-artifacts-builder`.

---

## Phase 4 — Audit

- Run `npx impeccable detect` (or equivalent from the loaded taste guardrail).
- Run `design-motion-principles` (Audit mode) if motion was used.
- Fix every flagged issue before delivery.

---

## Constraints
- One taste guardrail only (loaded: {{taste_guardrail}}).
- Design from extracted tokens, never from imagination.
- If a skill/CLI is missing, log it and continue.
