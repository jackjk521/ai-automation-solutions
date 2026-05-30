# Prompts Library

> Parameterized Markdown prompt templates for the Prompt Forge generator.
> Each template uses `{{double_brace}}` placeholders and encodes wiring rules
> that auto-insert ingestion steps, skills, and guardrails.

## Wiring Rules (enforced in every template)

1. **Ingest before generate.** If inputs are provided, the generated prompt ALWAYS
   prepends an ingestion phase that runs BEFORE any design decision.
2. **One taste guardrail only.** Never load `impeccable` + `taste-skill` + `ui-ux-pro-max-skill`
   simultaneously. Choose ONE primary. `design-motion-principles` may load as secondary.
3. **Conditional CLI calls.** No wasted calls — `codefetch`, `markitdown`, `designlang`,
   `graphify`, and `claude-video` lines only appear when their input field is non-empty.
4. **Hard stop.** Every template inserts: "STOP. Do not proceed to Phase 2 until you
   have read and summarized every ingestion output above."
5. **Graceful degradation.** If a referenced skill/CLI is missing, log it and continue.
   Never fail the whole run.
6. **Deliverable = single artifact + tests.** Every template ends with: bundle into one
   self-contained HTML artifact → Playwright smoke tests → optional Remotion demo.

## Placeholder Glossary

| Placeholder | Used In | Description |
|---|---|---|
| `{{client_name}}` | 1,5,7 | Project or client name |
| `{{brief}}` | 1,2,6,7,8 | One-line brief and goal |
| `{{brand_assets}}` | 1,4,7 | Brand colors, fonts, voice notes |
| `{{inspiration_urls}}` | 1,2,4,6 | Reference sites for designlang extraction |
| `{{documents}}` | 1,2,3,8 | Files to ingest via markitdown |
| `{{github_refs}}` | 1,2,3,8 | Repos to fetch via codefetch |
| `{{pages}}` | 1 | Site pages list |
| `{{target_audience}}` | 1 | Who the site is for |
| `{{primary_cta}}` | 1 | Main call-to-action |
| `{{industry_type}}` | 1 | e.g. "fintech", "spa", "SaaS" |
| `{{product_name}}` | 2 | Product name |
| `{{problem}}` | 2 | Problem statement |
| `{{core_user}}` | 2 | Core user persona |
| `{{must_have_features}}` | 2 | MVP feature list |
| `{{data_entities}}` | 2 | Data model entities |
| `{{output_name}}` | 3 | Name for consolidated output file |
| `{{video_refs}}` | 3 | Video files/URLs for claude-video |
| `{{reference_url}}` | 4 | Site to extract design from |
| `{{target}}` | 4 | Component or page to rebuild |
| `{{site_target}}` | 5 | Existing site to optimize |
| `{{top_queries}}` | 5 | Target search queries |
| `{{competitors}}` | 5 | Competitor names |
| `{{variant_a_style}}` | 6 | Style description for variant A |
| `{{variant_b_style}}` | 6 | Style description for variant B |
| `{{existing_site_url_or_path}}` | 7 | Existing site to audit/redesign |
| `{{pain_points}}` | 7 | What's wrong with current site |
| `{{goals}}` | 7 | Redesign goals |
| `{{target_feature}}` | 8 | Feature to build on existing codebase |

## Templates

| # | File | When to Use |
|---|---|---|
| 1 | `client-website-brand-seo.md` | Client-ready marketing site with brand + SEO + CRO |
| 2 | `mvp-webapp-artifact.md` | MVP scope → system design → testable HTML artifact |
| 3 | `ingest-inputs.md` | Standalone ingestion of repos/docs/URLs/video |
| 4 | `design-from-reference.md` | Extract reference site tokens → rebuild on-brand |
| 5 | `seo-cro-pass.md` | AEO/GEO + CRO optimization on existing build |
| 6 | `project-face-off.md` | Generate 2 variants, screenshot, side-by-side |
| 7 | `redesign-audit.md` | Audit and redesign an existing site/codebase |
| 8 | `knowledge-graph-system.md` | Ingest complex codebase → graph → build feature |
