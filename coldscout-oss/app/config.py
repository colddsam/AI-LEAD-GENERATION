"""
Cold Scout OSS — Configuration
All API keys are provided by the user. No authorization layer.
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Google Places
    GOOGLE_PLACES_API_KEY: str = ""

    # Groq LLM
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    # SMTP (Brevo)
    BREVO_SMTP_HOST: str = "smtp-relay.brevo.com"
    BREVO_SMTP_PORT: int = 587
    BREVO_SMTP_USER: str = ""
    BREVO_SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    FROM_NAME: str = "Cold Scout"
    REPLY_TO_EMAIL: str = ""

    # Admin
    ADMIN_EMAIL: str = ""

    # Telegram (optional)
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # Schedule
    DISCOVERY_HOUR: int = 6
    QUALIFICATION_HOUR: int = 7
    PERSONALIZATION_HOUR: int = 8
    OUTREACH_HOUR: int = 9
    REPORT_HOUR: int = 23
    REPORT_MINUTE: int = 30

    # Branding
    BOOKING_LINK: str = ""
    SENDER_ADDRESS: str = ""

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Pipeline status
    PIPELINE_STATUS: str = "RUN"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
