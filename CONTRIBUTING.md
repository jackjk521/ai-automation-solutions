# Contributing to the n8n Automation Template Library

Thank you for considering a contribution! This guide explains everything you need to know to submit a new n8n workflow template or improve an existing one.

---

## Template Requirements

Every template submitted must include three components inside its own folder under `templates/`:

### 1. `workflow.json`
- Valid, parseable JSON (no trailing commas, no comments)
- Must contain top-level fields: `nodes`, `connections`, and `meta`
- Use **placeholder credentials** — never commit real API keys or tokens
- Export directly from n8n using the built-in export/download function

### 2. `README.md`
Must include: What it does, Use case, Prerequisites, How to import, Credentials table, Customization tips, Notes/caveats.

### 3. `preview.png`
Screenshot of the n8n workflow canvas. Minimum 1200px wide. No credentials visible.

---

## Template Naming Convention

```
NN-kebab-case-name
```

Examples: `01-lead-capture-to-crm`, `09-web-scraping-business-analysis`

Rules:
- Two-digit zero-padded prefix (`01`, `09`, `10`)
- Lowercase letters, numbers, hyphens only
- Use the next available number

---

## JSON Validation Requirements

Required top-level fields:

| Field | Type | Description |
|---|---|---|
| `nodes` | Array | All n8n nodes in the workflow |
| `connections` | Object | Node connection mapping |
| `meta` | Object | Workflow metadata |

Validate locally before submitting:
```bash
python3 -c "
import json
d = json.load(open('templates/NN-your-template/workflow.json'))
assert 'nodes' in d and 'connections' in d and 'meta' in d
print('Validation passed.')
"
```

---

## How to Export a Workflow from n8n

1. Open the workflow in n8n editor
2. Click the **three-dot menu** (⋮) → **Download**
3. Rename the file to `workflow.json`
4. Replace any real API keys with `YOUR_API_KEY_HERE`
5. Confirm `nodes`, `connections`, and `meta` fields are present

---

## How to Submit a Pull Request

1. Fork this repository
2. Create a branch: `git checkout -b add-NN-your-template-name`
3. Create your template folder with all 3 files
4. Run JSON validation locally
5. Commit: `git commit -m "Add NN-your-template-name"`
6. Push and open a PR against `main`
7. Fill in the PR description: what it does, integrations, AI-powered (y/n), special setup

CI will automatically validate your JSON. A maintainer will review before merging.

---

## Code of Conduct

Be respectful and constructive. Harassment or abusive behaviour will result in removal. Report issues to aceinternational.solutions.
