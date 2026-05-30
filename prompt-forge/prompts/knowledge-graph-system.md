# Knowledge-Graph System Design — Build on Existing Codebase

> When to use: adding a feature to a large or complex existing codebase where
> understanding the architecture first is critical.

Use the **superpowers** workflow (brainstorm → plan → build → review).
Read `./toolchain-reference.md` for each tool's role before starting.

## Goal
Understand the existing system, then design and build **{{target_feature}}**
on top of it.

---

## Phase 1 — Deep Ingest (run FIRST)

STOP. Do not proceed to Phase 2 until you have read and summarized every ingestion output.

{{#github_refs}}
- `codefetch --url {{.}} -o codefetch/{{slug}}.md` → read codebase.
- `graphify ./codefetch/{{slug}}.md -o graphify/GRAPH_REPORT.md`
  → read the knowledge graph report (modules, dependencies, entry points, data flow).
{{/github_refs}}

{{#documents}}
- `markitdown {{.}} > ingest/{{slug}}.md` → read for requirements and architecture notes.
{{/documents}}

---

## Phase 2 — System Design

1. From the knowledge graph, identify:
   - Entry points and public APIs
   - Data models and state management patterns
   - Where the new feature should plug in
2. Write a lightweight system design doc:
   - Feature scope (IN and OUT)
   - Data entities affected
   - API changes (if any)
   - UI/UX changes
3. Generate PRD via `founder-skills:prd-generator` if the feature is user-facing.

---

## Phase 3 — Build

- Load **{{taste_guardrail}}** as the ONLY primary taste guardrail.
- Build the feature consistent with the existing codebase's patterns.
- Use `design-motion-principles` (Create mode) if the feature involves new UI motion.
- Run the taste guardrail's anti-pattern check.

---

## Phase 4 — Test

- Playwright: test the new feature's happy path.
- Run `graphify` again on the modified codebase to verify the graph reflects
  the new architecture correctly.
- If any test fails, fix before delivery.

---

## Phase 5 — Ship

- Bundle the feature (or the full updated app) into a single HTML artifact
  via `web-artifacts-builder` if appropriate.
- Deliver with:
  - The feature implementation
  - Updated knowledge graph report
  - Test results + screenshots

---

## Constraints
- One taste guardrail only (loaded: {{taste_guardrail}}).
- Match existing codebase patterns. Do not introduce conflicting architectures.
- If a skill/CLI is missing, log it and continue.
- Final deliverable includes the updated knowledge graph.
