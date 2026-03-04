"""
Large Language Model (LLM) integration module.
Communicates with the Groq API for target discovery and content generation.
"""
import json
from loguru import logger
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import get_settings
settings = get_settings()

class GroqClient:
    """
    Client for interfacing with the Groq LLM API.
    """
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_email_content(self, lead_data: dict) -> dict:
        """
        Generates personalized outreach email content and benefits
        based on the provided lead context and deep enrichment data.
        """
        prompt_template = f"""
You are a professional business development writer. Write a short, warm outreach email for:

Business: {{business_name}}
Category: {{category}}
Location: {{location}}
Rating: {{rating}} stars on Google ({{review_count}} reviews)
Current web presence: {{web_presence_notes}}

Deep Enrichment Context:
- Website Title: {{website_title}}
- Services Mentioned: {{website_services}}
- Copyright Year: {{website_year}}
- Target Competitor: {{competitor_name}}

Requirements:
- Subject line: Compelling, mentions business name, max 60 chars
- Email body: 3 short paragraphs, conversational but professional (in HTML format)
- Paragraph 1: Acknowledge their business specifically. Mention something from the Deep Enrichment Context if useful (e.g., complementing their specific services or noting they might need an update compared to a local competitor).
- Paragraph 2: Explain what a custom platform/website could do for their specific business type
- Paragraph 3: Soft CTA - ask if they'd like a free consultation
- Include 3 specific ROI benefits for a {{category}}
- Tone: Helpful partner, not salesy
- Length: 150-200 words max

Return ONLY a valid JSON object in the following format:
{{{{
  "subject": "...",
  "body_html": "<p>...</p>",
  "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"]
}}}}
"""
        from app.core.database import get_session_maker
        from app.models.prompt_config import PromptConfig
        from sqlalchemy import select
        
        try:
            async with get_session_maker()() as db:
                stmt = select(PromptConfig).where(PromptConfig.prompt_type == "initial_outreach", PromptConfig.is_active == True)
                res = await db.execute(stmt)
                db_prompt = res.scalars().first()
                if db_prompt:
                    prompt_template = db_prompt.prompt_text
        except Exception as e:
            logger.warning(f"Could not load dynamic prompt, using fallback: {e}")
            
        prompt = prompt_template.format(
            business_name=lead_data.get('business_name', 'your business'),
            category=lead_data.get('category', 'business'),
            location=lead_data.get('location', 'your area'),
            rating=lead_data.get('rating', 'good'),
            review_count=lead_data.get('review_count', 'some'),
            web_presence_notes=lead_data.get('web_presence_notes', 'needs improvement'),
            website_title=lead_data.get('website_title', 'None'),
            website_services=', '.join(lead_data.get('website_services', [])),
            website_year=lead_data.get('website_year', 'None'),
            competitor_name=lead_data.get('competitor_name', 'None')
        )
        
        @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
        async def _call_groq(prompt_text):
            return await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt_text,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.7,
            )

        try:
            chat_completion = await _call_groq(prompt)
            result = chat_completion.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            logger.exception("Error calling Groq API for personalization")
            return {
                "subject": f"Enhance {lead_data.get('business_name')} Digital Presence",
                "body_html": "<p>Hi,</p><p>We help businesses like yours build a strong digital presence.</p><p>Let's chat?</p>",
                "benefits": ["Increased visibility", "Better customer engagement", "More sales"]
            }

    async def generate_daily_targets(self, exclude_cities: list, exclude_categories: list) -> dict:
        """
        Determines novel geographic and categorical targets for discovery,
        bypassing recently utilized combinations.
        """
        prompt = f"""
You are an expert sales strategist targeting local businesses in India.
Generate 2 random mid-tier or tier-2 cities in India and 2 specific local business categories 
that would benefit from having a modern website and digital presence. 

AVOID these cities (recently used): {exclude_cities}
AVOID these categories (recently used): {exclude_categories}

Good category examples: Dentists, Bakeries, Salons, Boutique Hotels, Fitness Trainers, Gyms, Pet Clinics, Accounting Firms, Law Firms, Wedding Planners, Real Estate Agencies. 

Return ONLY a JSON object with a key "targets" containing exactly 2 objects with "city" and "category".
Example format:
{{
  "targets": [
    {{"city": "Nagpur", "category": "Pet Clinics"}},
    {{"city": "Jaipur", "category": "Wedding Planners"}}
  ]
}}
"""
        try:
            logger.info("Calling Groq to generate dynamic daily targets")
            chat_completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.8,
            )
            data = json.loads(chat_completion.choices[0].message.content)
            return data.get("targets", [])
        except Exception as e:
            logger.exception("Error generating daily targets with Groq")
            return [
                {"city": "Pune", "category": "Gyms"},
                {"city": "Ahmedabad", "category": "Cafes"}
            ]

    async def generate_followup_email(self, lead_data: dict, followup_number: int) -> dict:
        """
        followup_number: 1, 2, or 3
        """
        if followup_number == 1:
            angle = "A brief, polite check-in asking if they had a chance to see the proposal."
        elif followup_number == 2:
            angle = "Share a brief valuable stat or tip about their industry regarding digital presence."
        else:
            angle = "A final, polite 'break-up' email. If they aren't interested, that's fine, but leave the door open."

        prompt = f"""
You are a professional business development writer. Write a short, personalized follow-up email #{followup_number} for:

Business: {lead_data.get('business_name')}
Category: {lead_data.get('category')}
Location: {lead_data.get('location')}

Angle: {angle}

Requirements:
- Subject line: Relevant to the angle, max 60 chars ("Re: " is good)
- Email body: 2-3 short paragraphs, conversational, in HTML format (<p> tags)
- Include a clear but very low-pressure CTA
- Keep it under 150 words

Return ONLY a valid JSON object in the following format:
{{
  "subject": "...",
  "body_html": "<p>...</p>"
}}
"""
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception:
            logger.exception("Error calling Groq API for followup")
            return {
                "subject": f"Re: {lead_data.get('business_name')} website",
                "body_html": "<p>Hi,</p><p>Just checking in on my previous email. Let me know if you'd like to chat!</p>"
            }
