import json
from groq import AsyncGroq
from app.config import settings

class GroqClient:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_email_content(self, lead_data: dict) -> dict:
        """
        Calls Groq API to generate email subject, body, and benefits based on the lead data.
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
            print(f"Error calling Groq API: {e}")
            return {
                "subject": f"Enhance {lead_data.get('business_name')} Digital Presence",
                "body_html": "<p>Hi,</p><p>We help businesses like yours build a strong digital presence.</p><p>Let's chat?</p>",
                "benefits": ["Increased visibility", "Better customer engagement", "More sales"]
            }
