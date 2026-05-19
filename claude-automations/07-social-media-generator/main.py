#!/usr/bin/env python3
"""Generate platform-native social media content for LinkedIn, Twitter, Instagram, and Facebook."""

import os
import json
import re
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a social media content expert who creates platform-native content that drives real engagement. You deeply understand the unique culture, algorithm, and audience expectations of each major platform.

Platform expertise:

LINKEDIN — Professional insights platform. Posts should lead with a bold insight or counterintuitive observation. Use short paragraphs (1-2 sentences max). Include a thought-provoking question to spark comments. Optimal length: 150-300 words. Professional but human. Never start with "Excited to share" or "Thrilled to announce". Use line breaks generously for white space. Hashtags go at the end.

TWITTER/X — Punchy and conversation-starting. The first tweet must stand alone as a hook that makes people want to read more or reply. Threads should have 3-5 tweets that each add incremental value. Each tweet under 240 characters. Lead with a strong opinion, surprising fact, or relatable observation. No fluff.

INSTAGRAM — Visual and story-driven. The caption should paint a picture even without the image. Open with a hook in the first line (before the "more" cutoff — under 125 characters). Then develop the story. End with a clear call to action. Emojis used purposefully for structure, not decoration. Hashtags grouped at the end: mix niche (5-10k posts) and broad (100k+ posts).

FACEBOOK — Community-oriented and conversational. Warmer tone than LinkedIn. Ask questions to encourage sharing. Longer format is acceptable. Personal anecdotes or relatable scenarios work well. Avoid hard sells.

Content pillars: identify which content pillars the post touches (e.g., Education, Inspiration, Behind-the-Scenes, Product, Social Proof, Entertainment, Thought Leadership).

You must output valid JSON only. No markdown, no preamble, no explanation outside the JSON object."""

def build_prompt(data: dict) -> str:
    platforms = data.get("platforms", ["linkedin", "twitter", "instagram", "facebook"])
    platforms_str = ", ".join(platforms)
    include_hashtags = data.get("include_hashtags", True)
    include_emoji = data.get("include_emoji", True)

    return f"""Create platform-native social media content for the following brief.

CONTENT BRIEF:
- Topic: {data.get("topic")}
- Brand Name: {data.get("brand_name")}
- Brand Voice: {data.get("brand_voice")}
- Target Audience: {data.get("target_audience")}
- Platforms needed: {platforms_str}
- Include hashtags: {include_hashtags}
- Include emoji: {include_emoji}

Output a JSON object with these keys (include only platforms requested: {platforms_str}):
- linkedin: object with "post" (string) and "hashtags" (array of strings)
- twitter: object with "tweet" (string, main tweet under 240 chars) and "thread" (array of 3-5 tweet strings for a thread)
- instagram: object with "caption" (string) and "hashtags" (array of strings, 15-20 hashtags mixing niche and broad)
- facebook: object with "post" (string)
- content_pillars_used: array of content pillar names identified (e.g. ["Education", "Thought Leadership"])"""

def run(input_data: dict) -> dict:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_prompt(input_data)}],
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
    )
    raw = response.content[0].text
    match = re.search(r'\{[\s\S]+\}', raw)
    return json.loads(match.group(0)) if match else {"raw": raw}

if __name__ == "__main__":
    example = {
        "topic": "Why most startups fail because of hiring too fast, not too slow — and what to do instead",
        "brand_name": "TalentOS",
        "brand_voice": "Confident, data-driven, slightly contrarian, speaks to founders and operators",
        "target_audience": "Early-stage startup founders and Head of People at Series A companies",
        "platforms": ["linkedin", "twitter", "instagram", "facebook"],
        "include_hashtags": True,
        "include_emoji": True
    }
    print(json.dumps(run(example), indent=2))
