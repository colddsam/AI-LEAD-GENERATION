"""
Security and Cryptography Utilities.

Provides standard implementations for password hashing (via Passlib/Bcrypt) 
and session token generation (via JWT/Jose). These utilities form the 
backbone of the administrative authentication layer.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Generates a signed RS256 JWT representing a successful user session.
    
    Args:
        subject: Usually the unique user ID or email.
        expires_delta: Optional override for token lifespan (defaults to 7 days).
        
    Returns:
        str: An encoded JWT string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=60 * 24 * 7  # 7 days
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed representation.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a secure hash for a given password using bcrypt.
    """
    return pwd_context.hash(password)
