# Design Prompts Library

75 curated design prompts for web and UI work, drawn from designprompts.dev and tisatech.in. Browse and filter via `index.html`.

## How to open

Open `index.html` through any local server:
- **VS Code**: Right-click → Open with Live Server
- **Python**: `python -m http.server 8080` then visit `http://localhost:8080/prompt-forge/design-prompts/`
- **Node**: `npx serve .` in this folder

> Direct `file://` open will fail (browser blocks `fetch()` of local JSON). Use a local server.

## Prompt schema

Each entry in `prompts.json` follows this shape:

```json
{
  "id": "dp-001",
  "title": "Minimal SaaS Landing Page",
  "body": "The full prompt text…",
  "source": "designprompts.dev",
  "category": "Landing Page",
  "tags": ["landing-page", "saas", "dark-mode", "hero"],
  "difficulty": "intermediate"
}
```

## Categories

| Category | Description |
|---|---|
| Landing Page | Marketing, SaaS, startup, and product landing pages |
| Mobile App | iOS/Android app screens and flows |
| Dashboard | Analytics, admin, and data-heavy UIs |
| E-Commerce | Product pages, carts, checkout flows |
| Component | Isolated UI components (buttons, cards, modals, etc.) |
| Web App | Full web application UIs |
| Portfolio | Designer, developer, and agency portfolio layouts |
| Design System | Style guides, token systems, component libraries |
| Content | Blogs, editorial, content-heavy layouts |

## Difficulty levels

| Level | Meaning |
|---|---|
| `beginner` | Clear layout, standard patterns, little ambiguity |
| `intermediate` | Multiple sections, some nuance in UX requirements |
| `advanced` | Complex data, animation, multi-state, or system-level design |

## Sources

| Source | IDs | Count |
|---|---|---|
| designprompts.dev | `dp-001` → `dp-040` | 40 |
| tisatech.in | `tt-001` → `tt-035` | 35 |

## Tag system

Tags are lowercase kebab-case phrases extracted from the prompt body and category. They cover:

**Visual style**: `dark-mode`, `glassmorphism`, `neumorphism`, `brutalism`, `minimal`, `gradient`, `illustration`

**Layout**: `hero`, `grid`, `sidebar`, `card`, `table`, `modal`, `navigation`, `form`

**UX patterns**: `animation`, `microinteraction`, `filter`, `search`, `accessibility`, `responsive`

**Domain**: `saas`, `fintech`, `e-commerce`, `startup`, `portfolio`, `design-system`

**Tech type**: `mobile`, `dashboard`, `landing-page`, `component`, `data-display`, `chart`

## Adding prompts

1. Append an entry to the `prompts` array in `prompts.json`
2. Follow the schema above — `id` must be unique (`dp-NNN` for designprompts.dev, `tt-NNN` for tisatech.in, or `custom-NNN` for your own)
3. Update `meta.total` at the top of the file
4. Reload `index.html`

No build step needed.
