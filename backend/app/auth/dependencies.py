from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.database.session import get_db
from app.models import RevokedToken, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_token_payload(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    try:
        return decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(
    token_payload: Annotated[dict[str, Any], Depends(get_token_payload)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        user_id = int(token_payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    token_jti = token_payload.get("jti")
    if not token_jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )

    revoked = db.query(RevokedToken).filter(RevokedToken.token_jti == token_jti).first()
    if revoked is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
