from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_token_payload
from app.auth.security import create_access_token, get_password_hash, verify_password
from app.database.session import get_db
from app.models import HealthProfile, RevokedToken, User
from app.schemas.auth import LoginRequest, MessageResponse, RegisterRequest, TokenResponse
from app.services.health_calculations import build_health_summary

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = payload.email.lower().strip()
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    summary = build_health_summary(payload.weight_kg, payload.height_cm)
    user = User(
        name=payload.name.strip(),
        email=email,
        password=get_password_hash(payload.password),
    )
    user.health_profile = HealthProfile(
        age=payload.age,
        gender=payload.gender.strip(),
        height_cm=payload.height_cm,
        weight_kg=payload.weight_kg,
        bmi=summary["bmi"],
        skin_type=payload.skin_type.strip(),
        water_goal_liters=summary["water_goal_liters"],
        city=payload.city.strip() if payload.city else None,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = payload.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if user is None or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/logout", response_model=MessageResponse)
def logout_user(token_payload=Depends(get_token_payload), db: Session = Depends(get_db)) -> MessageResponse:
    token_jti = token_payload["jti"]
    already_revoked = db.query(RevokedToken).filter(RevokedToken.token_jti == token_jti).first()
    if already_revoked is None:
        expires_at = datetime.fromtimestamp(token_payload["exp"], tz=timezone.utc)
        db.add(
            RevokedToken(
                user_id=int(token_payload["sub"]),
                token_jti=token_jti,
                expires_at=expires_at,
            )
        )
        db.commit()

    return MessageResponse(message="Logged out successfully")
