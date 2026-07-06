from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_token_expiry(minutes: int | None = None) -> datetime:
    settings = get_settings()
    expiry_minutes = minutes or settings.access_token_expire_minutes
    return datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)


def create_access_token(subject: str, expires_delta_minutes: int | None = None) -> str:
    settings = get_settings()
    expire = get_token_expiry(expires_delta_minutes)
    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise ValueError("Invalid authentication token") from exc

    subject = payload.get("sub")
    token_id = payload.get("jti")
    expiry = payload.get("exp")
    if not subject or not token_id or not expiry:
        raise ValueError("Malformed authentication token")
    return payload
