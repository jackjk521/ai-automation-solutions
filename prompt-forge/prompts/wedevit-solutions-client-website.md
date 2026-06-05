# Client Website — WeDevIT Solutions

Use the **superpowers** workflow (brief brainstorm → plan → build → review). Read `./toolchain-reference.md` for each tool's role before starting.

## Brief

A premier software consultancy and SaaS provider specializing in ISO-standard architecture, AI-driven automation, and high-fidelity custom builds for the PH-Singapore corridor.

- **Audience:** Modern enterprises, small business owners, and scaling operators (ages 25–55) seeking technical prestige without sacrificing human-centric partnership.
- **Pages:** Home (Hero & Suite), About (Philosophy), Product Detail (WeBOOK It), Resources (Brand Guide)
- **Primary CTA:** Book a Consult / Explore the Suite
- **Industry:** Software Consultancy / SaaS / Enterprise Technology
- **Brand:**
  - **Wordmark:** "We\_\_\_ It" dynamic system — "We" and "It" anchor every mark; the central verb swaps per vertical (BUILD, CARE, MANAGE, BOOK, etc.)
  - **Colors:** Forest Green `#173124` (authority/depth) · Terracotta `#984623` (humanity/interaction) · Canvas `#0E1B14` (prestige/dimensionality) · Warm White `#FBF9F8` (clarity/breathability) · Sage Mist `#83A69C` (atmosphere/innovation)
  - **Type:** Literata Serif wt 600–700 (headlines, editorial authority) · Hanken Grotesk wt 400–600 (body & UI, technical precision)
  - **Voice:** Warm editorial soul with technical edge. Quiet confidence of a partner, not the noise of a vendor. "Focus on what matters."

## Product Ecosystem — The "We\_\_\_ It" Suite

Render as a scannable grid on the Home hero. Each tile uses the dynamic wordmark verb.

| Product     | Vertical                                                    |
| ----------- | ----------------------------------------------------------- |
| WeCARE It   | Clinic & Healthcare Management                              |
| WeMANAGE It | Property & Asset Management                                 |
| WeTRACK It  | Advanced CRM & Lead Logistics                               |
| WeRUN It    | Robust ERP & Operations                                     |
| WeFILE It   | Legal Case & Document Management                            |
| WeSERVE It  | Restaurant & Hospitality POS                                |
| WeBOOK It   | Wellness, Spa & Salon Appointments _(featured detail page)_ |
| WeSELL It   | E-commerce & Virtual Card Solutions                         |
| WeBUILD It  | Bespoke Software Consultancy & Engineering                  |

## Design Direction

- **Energy:** Warm editorial soul with kinetic, dimensional hero moments. Breathable light surfaces; dark canvas `#0E1B14` + sage glow `#83A69C` spotlight effects in key interaction zones for high-impact "wow factors."
- **Aesthetic target:** Glassmorphic elements, 3D organic forms, museum-grade whitespace. Positioned between "Too Corporate" and "Too Playful" — occupying **High-End Architectural** space.
- **Reference style:** Awwwards/Dribbble tier execution. No actual reference URLs provided — synthesize tokens from the brand palette and typographic system above. Do NOT invent palettes outside the five colors defined.

## Phase 1 — Ingest (run FIRST)

STOP. Do not proceed to Phase 2 until you have read and summarized every ingestion output below.

- No external repos or documents provided. Use brand tokens and product data above as the canonical source of truth.
- Synthesize a `brand-guidelines` skill file from the brand section above before building any component.

## Phase 2 — Shape

- Generate a PRD/spec via `founder-skills:prd-generator`; confirm sitemap, content blocks per page, and full CTA flow (Book a Consult → Explore the Suite → Product Detail → Contact).
- Run `ui-ux-pro-max-skill` design-system generator for industry-specific rules ("Software Consultancy / SaaS / Enterprise Technology").
- Define the dynamic wordmark animation rule: on page load / hover, the verb in "We\_\_\_ It" cycles or spotlights. Codify this as a reusable component.

## Phase 3 — Build

- Build all four pages with **impeccable** as the primary taste guardrail; honor every brand token exactly.
- Load `design-motion-principles` (Create mode) for purposeful motion — hero entrance, verb cycling, section reveals, CTA micro-interactions.
- Dark canvas hero sections use `#0E1B14` + sage mist glow `#83A69C`; body sections breathe on `#FBF9F8`; terracotta `#984623` reserved for interactive/CTA elements only.
- WeBOOK It detail page must include: feature highlights, booking flow walkthrough, and a prominent "Book a Consult" CTA.

## Phase 4 — Optimize

- SEO + CRO pass per loadout (see below).
- Add `llms.txt` and verify `robots.txt` for AEO/GEO discoverability.

## Phase 5 — Package

- One self-contained HTML artifact for client review.

## Phase 6 — Test

- Playwright: links, forms, responsive (mobile/tablet/desktop), accessibility checks; screenshot each page at all breakpoints.

## Phase 7 — Deliver

- Present artifact + test report + screenshots. Note any `[UNVERIFIED]` skills before automating.

## Skill & tool loadout

- `impeccable` — the ONLY primary taste guardrail; run its anti-pattern check before delivery
- `brand-guidelines` — synthesize from brand section above; keep every component on-brand
- `ai-seo` — apply the 3 pillars (structure / authority / presence)
- `seo-audit` — traditional technical + on-page SEO checks
- `schema` — structured data markup (Organization, SoftwareApplication, Service, FAQ)
- `founder:prd` — produce the PRD before building
- `founder:cro` — audit against the 13 CRO principles with before/after
- `superpowers` — orchestrate brainstorm → plan → build → review → finish (TDD)
- `web-artifacts-builder` — bundle result into ONE self-contained HTML artifact
- `playwright` — smoke-test flows, capture screenshots for the client
- `design-motion-principles` — purposeful motion (Create mode)

## Constraints

- One primary taste guardrail only (loaded: `impeccable`).
- Five brand colors are fixed — design from these tokens, never invented palettes.
- The dynamic wordmark "We\_\_\_ It" mechanic must be implemented as a real interactive/animated component, not a static image placeholder.
- If a skill/CLI is missing, log it and continue — never fail the whole run.
- Final deliverable is a single self-contained artifact + passing tests.
