"""
Groq LLM client for Cold Scout OSS.
Uses user-provided API key — no cost to the platform.
"""
import json
import re
from loguru import logger
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import get_settings

settings = get_settings()

_MAX_FIELD_LENGTH = 300


def _sanitize(value: str) -> str:
    if not isinstance(value, str):
        value = str(value)
    value = re.sub(r"[\x00-\x1f\x7f]", "", value)
    return value[:_MAX_FIELD_LENGTH]


class GroqClient:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_email_content(self, lead_data: dict) -> dict:
        from string import Template

        prompt_template = """
You are a professional business development writer. Write a short, warm outreach email for:

Business: $business_name
Category: $category
Location: $location
Rating: $rating stars on Google ($review_count reviews)
Current web presence: $qualification_notes

Requirements:
- Subject line: Compelling, mentions business name, max 60 chars
- Email body: 3 short paragraphs, conversational but professional (in HTML format)
- Include 3 specific ROI benefits for a $category
- Tone: Helpful partner, not salesy
- Length: 150-200 words max

Return ONLY a valid JSON object:
{
  "subject": "...",
  "body_html": "<p>...</p>",
  "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"]
}
"""
        mapping = {
            "business_name": _sanitize(lead_data.get('business_name', 'your business')),
            "category": _sanitize(lead_data.get('category', 'business')),
            "location": _sanitize(lead_data.get('location', 'your area')),
            "rating": _sanitize(str(lead_data.get('rating', 'good'))),
            "review_count": _sanitize(str(lead_data.get('review_count', 'some'))),
            "qualification_notes": _sanitize(lead_data.get('qualification_notes', 'needs improvement')),
        }

        prompt = Template(prompt_template).safe_substitute(mapping)

        @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
        async def _call(p):
            return await self.client.chat.completions.create(
                messages=[{"role": "user", "content": p}],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.7,
            )

        try:
            result = await _call(prompt)
            return json.loads(result.choices[0].message.content)
        except Exception:
            logger.exception("Groq API error for personalization")
            return {
                "subject": f"Enhance {lead_data.get('business_name')} Digital Presence",
                "body_html": "<p>Hi,</p><p>We help businesses like yours build a strong digital presence.</p><p>Let's chat?</p>",
                "benefits": ["Increased visibility", "Better customer engagement", "More sales"],
            }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_daily_targets(self, exclude_cities: list, exclude_categories: list) -> list:
        prompt = f"""
You are an expert sales strategist targeting local businesses in India.
Generate 2 random mid-tier cities and 2 specific local business categories
that would benefit from having a modern website.

AVOID these cities: {exclude_cities}
AVOID these categories: {exclude_categories}

Return ONLY a JSON object with key "targets" containing exactly 2 objects with "city" and "category".
Example: {{"targets": [{{"city": "Nagpur", "category": "Pet Clinics"}}, {{"city": "Jaipur", "category": "Wedding Planners"}}]}}
"""
        result = await self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.8,
        )
        data = json.loads(result.choices[0].message.content)
        return data.get("targets", [])
