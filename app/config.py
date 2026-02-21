import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "secret"
    API_KEY: str = "admin-secret-key"
    APP_URL: str = "http://localhost:8000"

    # Database
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    # Redis (Upstash)
    REDIS_URL: str

    # APIs
    GOOGLE_PLACES_API_KEY: str
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    # Email (Brevo)
    BREVO_SMTP_HOST: str = "smtp-relay.brevo.com"
    BREVO_SMTP_PORT: int = 587
    BREVO_SMTP_USER: str
    BREVO_SMTP_PASSWORD: str
    FROM_EMAIL: str
    FROM_NAME: str = "Lead Generation"
    REPLY_TO_EMAIL: str

    # Email Tracking (IMAP)
    IMAP_HOST: str = "imap.gmail.com"
    IMAP_USER: str
    IMAP_PASSWORD: str

    # Notifications
    ADMIN_EMAIL: str
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    WHATSAPP_NUMBER: str = ""
    CALLMEBOT_API_KEY: str = ""

    # Scheduler times
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

settings = Settings()
