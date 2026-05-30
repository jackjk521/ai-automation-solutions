# SEO + CRO Pass — Optimize Existing Build

> When to use: an existing site needs AI-search optimization (AEO/GEO/LLMO)
> and conversion-rate improvements. Output is a prioritized diff.

Read `./toolchain-reference.md` for each tool's role before starting.

## Goal
Optimize **{{site_target}}** for AI search + conversion.

- **Target queries:**
{{top_queries}}
- **Competitors cited:** {{competitors}}

---

## Phase 1 — Audit

1. **AI-SEO audit:** Run `ai-seo` — check Structure (40–60 word blocks, FAQ/comparison tables),
   Authority (citations, stats, expert quotes), Presence (Wikipedia, Reddit, review sites).
2. **Technical SEO:** Run `seo-audit` — indexability, Core Web Vitals, mobile, canonicals, robots.txt.
3. **Schema:** Run `schema` — check existing markup; recommend FAQ, HowTo, Product, Article, Organization.
4. **CRO:** Run `founder-skills:cro-optimization` — audit against the 13 CRO principles.
5. **Extractability check:** Verify each priority page has clear definitions, self-contained answer blocks,
   comparison tables, and FAQ sections.
6. **AI bot access:** Verify robots.txt allows GPTBot, PerplexityBot, ClaudeBot, Google-Extended.

---

## Phase 2 — Prioritized Diff

Output a single table sorted by **Impact × Effort** (highest-leverage first):

| Priority | Issue | Impact | Effort | Fix | Owner |
|---|---|---|---|---|---|
| P0 | … | High | Low | … | … |
| P1 | … | … | … | … | … |

Include:
- Before/after screenshots or code snippets for each fix.
- A `llms.txt` draft and `/pricing.md` draft (if applicable).
- Schema markup snippets ready to paste.

---

## Constraints
- Do not rewrite the entire site. Deliver a targeted, prioritized diff.
- If a skill/CLI is missing, log it and continue.
