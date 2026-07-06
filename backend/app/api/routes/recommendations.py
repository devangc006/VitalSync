from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import Recommendation, User
from app.schemas.recommendation import RecommendationRead, RecommendationResponse
from app.services.recommendations import build_recommendations
from app.services.weather_client import fetch_weather

router = APIRouter(tags=["Recommendations"])


@router.get("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    city = current_user.health_profile.city if current_user.health_profile and current_user.health_profile.city else 'London'
    weather = await fetch_weather(city)
    recommendations = build_recommendations(
        temperature_c=float(weather['temperature_c']),
        humidity_percent=float(weather['humidity_percent']),
        uv_index=float(weather['uv_index']),
        weather_condition=str(weather['weather_condition']),
        skin_type=current_user.health_profile.skin_type if current_user.health_profile else 'Normal',
        weight_kg=current_user.health_profile.weight_kg if current_user.health_profile else 70,
    )

    stored_recommendations: list[Recommendation] = []
    for item in recommendations:
        stored_recommendations.append(
            Recommendation(
                user_id=current_user.id,
                recommendation=item['recommendation'],
                category=item['category'],
            )
        )
    if stored_recommendations:
        db.add_all(stored_recommendations)
        db.commit()

    return RecommendationResponse(
        recommendations=[
            RecommendationRead(
                id=index + 1,
                recommendation=item['recommendation'],
                category=item['category'],
                created_at=weather['timestamp'],
            )
            for index, item in enumerate(recommendations)
        ]
    )
