from datetime import datetime

from pydantic import BaseModel, Field


class HealthCreateRequest(BaseModel):
    weight_kg: float = Field(gt=0)
    height_cm: float = Field(gt=0)
    water_intake_liters: float | None = Field(default=None, ge=0)


class HealthRead(BaseModel):
    id: int
    weight_kg: float
    height_cm: float
    bmi: float
    water_intake_liters: float | None = None
    recorded_at: datetime


class HealthHistoryResponse(BaseModel):
    records: list[HealthRead]
