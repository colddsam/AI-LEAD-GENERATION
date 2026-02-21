"""
Application configuration module.
Defines the core settings, environment variables, and caching mechanisms
required for the operation of the AI Lead Generation System.
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings model managing all configuration parameters
    extracted from environment variables or default definitions.
    """
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "secret"
    API_KEY: str = "admin-secret-key"
    APP_URL: str = "http://localhost:8000"

    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    REDIS_URL: str

    GOOGLE_PLACES_API_KEY: str
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    BREVO_SMTP_HOST: str = "smtp-relay.brevo.com"
    BREVO_SMTP_PORT: int = 587
    BREVO_SMTP_USER: str
    BREVO_SMTP_PASSWORD: str
    FROM_EMAIL: str
    FROM_NAME: str = "Lead Generation"
    REPLY_TO_EMAIL: str

    IMAP_HOST: str = "imap.gmail.com"
    IMAP_USER: str
    IMAP_PASSWORD: str

    ADMIN_EMAIL: str
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    WHATSAPP_NUMBER: str = ""
    CALLMEBOT_API_KEY: str = ""
    DISCOVERY_HOUR: int = 6
    QUALIFICATION_HOUR: int = 7
    PERSONALIZATION_HOUR: int = 8
    OUTREACH_HOUR: int = 9
    REPORT_HOUR: int = 23
    REPORT_MINUTE: int = 30
    EMAIL_SEND_INTERVAL_SECONDS: int = 360

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    """
    Instantiates and returns the application settings.
    Utilizes lru_cache to ensure specific settings validation and extraction
    is executed only once per process lifecycle.

    Returns:
        Settings: The validated application settings.
    """
    return Settings()