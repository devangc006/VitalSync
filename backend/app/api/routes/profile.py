from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import HealthProfile, User
from app.schemas.profile import HealthProfileRead, ProfileResponse, ProfileUpdateRequest
from app.services.health_calculations import build_health_summary

router = APIRouter(tags=["Profile"])


def _serialize_profile(profile: HealthProfile | None) -> HealthProfileRead | None:
    if profile is None:
        return None
    return HealthProfileRead(
        id=profile.id,
        age=profile.age,
        gender=profile.gender,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        bmi=profile.bmi,
        bmi_category=build_health_summary(profile.weight_kg, profile.height_cm)["bmi_category"],
        skin_type=profile.skin_type,
        water_goal_liters=profile.water_goal_liters,
        city=profile.city,
    )


def _serialize_user(user: User) -> ProfileResponse:
    return ProfileResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        profile=_serialize_profile(user.health_profile),
    )


@router.get("/profile", response_model=ProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)) -> ProfileResponse:
    return _serialize_user(current_user)


@router.put("/profile", response_model=ProfileResponse)
def update_profile(
    payload: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    profile = current_user.health_profile
    if profile is None:
        profile = HealthProfile(user=current_user)
        current_user.health_profile = profile

    summary = build_health_summary(payload.weight_kg, payload.height_cm)

    current_user.name = payload.name.strip()
    profile.age = payload.age
    profile.gender = payload.gender.strip()
    profile.height_cm = payload.height_cm
    profile.weight_kg = payload.weight_kg
    profile.bmi = summary["bmi"]
    profile.skin_type = payload.skin_type.strip()
    profile.water_goal_liters = summary["water_goal_liters"]
    profile.city = payload.city.strip() if payload.city else None

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return _serialize_user(current_user)
