from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import User, WeatherSnapshot
from app.schemas.weather import WeatherResponse
from app.services.weather_client import fetch_weather

router = APIRouter(tags=["Weather"])


@router.get("/weather", response_model=WeatherResponse)
async def get_weather(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WeatherResponse:
    city = current_user.health_profile.city if current_user.health_profile and current_user.health_profile.city else 'London'
    payload = await fetch_weather(city)

    snapshot = WeatherSnapshot(
        user_id=current_user.id,
        city=str(payload['city']),
        temperature_c=float(payload['temperature_c']),
        humidity_percent=float(payload['humidity_percent']),
        uv_index=float(payload['uv_index']),
        weather_condition=str(payload['weather_condition']),
        wind_speed_mps=float(payload['wind_speed_mps']),
    )
    db.add(snapshot)
    db.commit()

    return WeatherResponse(**payload)
