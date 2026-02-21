import httpx
from typing import List, Dict, Any, Optional
from app.config import get_settings


class GooglePlacesClient:
    BASE_URL = "https://places.googleapis.com/v1/places:searchText"

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.GOOGLE_PLACES_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.googleMapsUri"
        }

    async def search_places(self, location: str, category: str, radius: int = 5000) -> List[Dict[str, Any]]:
        """
        Search for places given a location and category.
        """
        query = f"{category} in {location}"
        
        payload = {
            "textQuery": query,
            "languageCode": "en",
            "maxResultCount": 20
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.BASE_URL,
                    json=payload,
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("places", [])
            except Exception as e:
                print(f"Error fetching places from Google API: {e}")
                return []
