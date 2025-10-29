from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from jose import jwt
from app.core.config import settings
import logging


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a hash using SHA256 and salt."""
    try:
        salt, pwd_hash = hashed_password.split("$")
        return pwd_hash == hashlib.sha256((plain_password + salt).encode()).hexdigest()
    except (ValueError, TypeError) as e:
        logging.exception(f"Error verifying password: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hashes a password using SHA256 with a random salt."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${pwd_hash}"