# Project Face-Off — Variant A vs Variant B

> When to use: the client wants to see two competing design directions before
> committing. Build both, screenshot, present side-by-side.

Use the **superpowers** workflow (brainstorm → plan → build → review).
Read `./toolchain-reference.md` for each tool's role before starting.

## Goal
Design **{{brief}}** as TWO competing variants for the client to choose.

---

## Phase 1 — Ingest (if references provided)

STOP. Do not proceed to Phase 2 until ingestion is complete.

{{#inspiration_urls}}
- `designlang {{.}} --screenshots --full` → read tokens/theme.
{{/inspiration_urls}}

---

## Phase 2 — Build Variants

### Variant A — {{variant_a_style}}
- Load `impeccable` as the primary taste guardrail.
- Build the full design. Run `npx impeccable detect` before screenshotting.
- Bundle into `variant-a.html` via `web-artifacts-builder`.

### Variant B — {{variant_b_style}}
- Load `taste-skill` (gpt-taste variant) as the primary taste guardrail.
- Load `design-motion-principles` (Create mode) for bold motion.
- Build the full design. Run the taste-skill anti-pattern check.
- Bundle into `variant-b.html` via `web-artifacts-builder`.

---

## Phase 3 — Capture

- Playwright: screenshot both variants at:
  - 1440×900 (desktop)
  - 768×1024 (tablet)
  - 375×812 (mobile)
- Save screenshots to `face-off/screenshots/`.

---

## Phase 4 — Present

Create a side-by-side comparison document with:
- Screenshot grid (desktop + mobile for each variant).
- 1-line rationale for each variant's design decisions.
- A recommendation: "We recommend Variant [A/B] because …"
- A note on which variant is faster to build, which has better accessibility,
  and which scales better to additional pages.

---

## Constraints
- Only ONE taste guardrail per variant (impeccable for A, taste-skill for B).
- If a skill/CLI is missing, log it and continue.
- Deliver screenshots + both HTML artifacts + comparison doc.
