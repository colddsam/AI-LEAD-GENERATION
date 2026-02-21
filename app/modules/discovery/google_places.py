"""
Google Places API integration module.
Provides an asynchronous client to facilitate geographic discovery of prospective leads.
"""
import httpx
from typing import List, Dict, Any, Optional
from loguru import logger
from app.config import get_settings


class GooglePlacesClient:
    """
    Client for interfacing with the Google Places API.
    Handles configuration, required headers, and execution of text-based place searches.
    """
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
        Executes an asynchronous query against the Google Places API to discover locations.
        
        Args:
            location (str): The target geographic area (e.g., city name).
            category (str): The target business archetype.
            radius (int, optional): The search radius limit. Defaults to 5000.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing discovered places with fields extracted based on the FieldMask.
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
                logger.exception(f"Error fetching places from Google API for {query}")
                return []
