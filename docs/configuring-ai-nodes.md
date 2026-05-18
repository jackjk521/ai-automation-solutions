# Configuring AI Nodes in n8n

This guide explains how to integrate AI language models into your n8n workflows using the **HTTP Request node**, covering Anthropic Claude, OpenAI, and Groq.

---

## Why HTTP Request Instead of a Dedicated AI Node

Using the **HTTP Request node** with a **Header Auth credential** gives you:

- Full control over every field in the request payload
- Immediate access to new models without waiting for an n8n update
- Easy provider switching by changing one URL and one header
- A consistent pattern across all AI providers (Anthropic, OpenAI, Groq, Mistral, etc.)

All AI-powered templates in this library (04, 06, 07, 09) use this pattern.

---

## Storing API Keys in n8n Credentials

1. Go to **Settings → Credentials → + Add Credential**
2. Select **Header Auth**
3. Enter a name (e.g., `Anthropic Claude API`)
4. **Name (header field):** `x-api-key` (Anthropic) or `Authorization` (OpenAI/Groq)
5. **Value:** Your API key
6. Click **Save**

Never paste API keys directly into node parameter fields.

---

## Anthropic Claude Setup

| Setting | Value |
|---|---|
| Method | POST |
| URL | `https://api.anthropic.com/v1/messages` |
| Authentication | Header Auth → your Anthropic credential |

Additional Headers:
- `anthropic-version: 2023-06-01`
- `content-type: application/json`

Body (JSON):
```json
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 512,
  "messages": [{"role": "user", "content": "={{ $json.prompt }}"}]
}
```

**Models:** `claude-haiku-4-5-20251001` (fast/cheap), `claude-sonnet-4-6` (balanced), `claude-opus-4-7` (best quality)

---

## OpenAI Setup

| Setting | Value |
|---|---|
| Method | POST |
| URL | `https://api.openai.com/v1/chat/completions` |
| Authorization header | `Bearer YOUR_OPENAI_KEY` |

Body (JSON):
```json
{
  "model": "gpt-4o-mini",
  "max_tokens": 512,
  "messages": [{"role": "user", "content": "={{ $json.prompt }}"}]
}
```

---

## Groq Setup

| Setting | Value |
|---|---|
| URL | `https://api.groq.com/openai/v1/chat/completions` |
| Authorization header | `Bearer YOUR_GROQ_KEY` |

Body format identical to OpenAI. Recommended model: `llama-3.3-70b-versatile`

Groq offers a generous free tier with very fast inference (~1s responses).

---

## Parsing AI Responses

**Anthropic response structure:**
```javascript
// In a Code node:
const text = $input.item.json.content[0].text;
```

**OpenAI/Groq response structure:**
```javascript
const text = $input.item.json.choices[0].message.content;
```

**Parsing JSON from AI response:**
```javascript
let parsed;
try {
  const match = text.match(/\{[\s\S]+\}/);
  parsed = match ? JSON.parse(match[0]) : { raw: text };
} catch(e) {
  parsed = { raw: text };
}
```

---

## Prompt Engineering Tips

### Template 04 — Email Triage
- Use low temperature (0.1) for consistent classification
- Instruct model to respond with JSON only
- Include sender domain to help distinguish internal vs external

### Template 06 — Support Ticket Classifier
- Define your category taxonomy explicitly in the system prompt
- Add a `confidence` field to route low-confidence tickets for human review
- Use `response_format: {type: 'json_object'}` with OpenAI GPT-4o

### Template 07 — Weekly Report
- Use higher temperature (0.4–0.6) for more natural prose
- Request specific sections: Executive Summary, Key Metrics, Trends, Actions
- Ask for HTML output if sending via Gmail HTML email

### Template 09 — Web Scraping Outreach
- Vary email tone based on has_website (Y/N) and site score
- Reference the specific niche and location naturally in the prompt
- Keep max_tokens at 1024 — outreach emails should be concise (under 200 words)
