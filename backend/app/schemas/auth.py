from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    age: int = Field(ge=1, le=120)
    gender: str = Field(min_length=1, max_length=20)
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    skin_type: str = Field(min_length=3, max_length=30)
    city: str | None = Field(default=None, max_length=120)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str
