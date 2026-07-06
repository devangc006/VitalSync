from datetime import datetime

from pydantic import BaseModel


class RecommendationRead(BaseModel):
    id: int
    recommendation: str
    category: str
    created_at: datetime


class RecommendationResponse(BaseModel):
    recommendations: list[RecommendationRead]
