from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ProfileUpdateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=1, le=120)
    gender: str = Field(min_length=1, max_length=20)
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    skin_type: str = Field(min_length=3, max_length=30)
    city: str | None = Field(default=None, max_length=120)


class HealthProfileRead(BaseModel):
    id: int
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    bmi: float
    bmi_category: str
    skin_type: str
    water_goal_liters: float
    city: str | None = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    profile: HealthProfileRead | None = None
