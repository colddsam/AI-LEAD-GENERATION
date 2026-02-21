"""
Large Language Model (LLM) integration module.
Facilitates asynchronous communication with the Groq API to drive dynamic 
discovery targeting and individualized content generation.
"""
import json
from loguru import logger
from groq import AsyncGroq
from app.config import get_settings
settings = get_settings()

class GroqClient:
    """
    Client for interfacing with the Groq LLM API.
    Manages authentication, model selection, and standardized prompt construction.
    """
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_email_content(self, lead_data: dict) -> dict:
        """
        Invokes the LLM to generate highly personalized outreach email content and 
        prospective benefits tailored strictly to the provided lead context.
        
        Args:
            lead_data (dict): Dictionary comprising the target business's public profile and web footprint.
            
        Returns:
            dict: Structured JSON encapsulating the suggested subject line, HTML body, and specific benefits.
        """
        prompt = f"""
You are a professional business development writer. Write a short, warm outreach email for:

Business: {lead_data.get('business_name')}
Category: {lead_data.get('category')}
Location: {lead_data.get('location')}
Rating: {lead_data.get('rating')} stars on Google ({lead_data.get('review_count')} reviews)
Current web presence: {lead_data.get('web_presence_notes')}

Requirements:
- Subject line: Compelling, mentions business name, max 60 chars
- Email body: 3 short paragraphs, conversational but professional (in HTML format)
- Paragraph 1: Acknowledge their business specifically
- Paragraph 2: Explain what a custom platform/website could do for their specific business type
- Paragraph 3: Soft CTA - ask if they'd like a free consultation
- Include 3 specific ROI benefits for a {lead_data.get('category')}
- Tone: Helpful partner, not salesy
- Length: 150-200 words max

Return ONLY a valid JSON object in the following format:
{{
  "subject": "...",
  "body_html": "<p>...</p>",
  "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"]
}}
"""
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
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
        Invokes the LLM to strategically determine novel geographic and categorical targets
        for daily discovery operations, explicitly bypassing recently utilized combinations.
        
        Args:
            exclude_cities (list): A list of geographic locations to omit from selection.
            exclude_categories (list): A list of business archetypes to omit from selection.
            
        Returns:
            dict: Structured JSON payload containing an array of derived target combinations.
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
