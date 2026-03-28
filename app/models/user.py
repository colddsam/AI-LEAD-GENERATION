from sqlalchemy import Column, Integer, String, Boolean
from app.models import Base

class User(Base):
    """
    User model for authentication and authorization.

    Supports both legacy email/password authentication and Supabase Auth
    (social logins via Google, GitHub, Facebook, LinkedIn).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    supabase_uid = Column(String, unique=True, index=True, nullable=True)
    """UUID from Supabase Auth - used for social login users"""

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    """Nullable for social login users who don't have a password"""

    role = Column(String, default="freelancer")
    """User role: 'client' or 'freelancer' - determines redirect after login"""

    auth_provider = Column(String, default="email")
    """Authentication provider: 'email', 'google', 'github', 'facebook', 'linkedin'"""

    full_name = Column(String, nullable=True)
    """User's full name from OAuth provider or manual entry"""

    avatar_url = Column(String, nullable=True)
    """Profile avatar URL from OAuth provider"""

    plan = Column(String, default="free")
    """Subscription plan: 'free' | 'pro' | 'enterprise'. Managed by admin or payment webhook."""

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
