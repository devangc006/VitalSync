from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.health_profile import HealthProfile
    from app.models.health_record import HealthRecord
    from app.models.recommendation import Recommendation
    from app.models.revoked_token import RevokedToken
    from app.models.weather_snapshot import WeatherSnapshot


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    health_profile: Mapped["HealthProfile | None"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    revoked_tokens: Mapped[list["RevokedToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    health_records: Mapped[list["HealthRecord"]] = relationship(cascade="all, delete-orphan")
    weather_snapshots: Mapped[list["WeatherSnapshot"]] = relationship(cascade="all, delete-orphan")
    recommendations: Mapped[list["Recommendation"]] = relationship(cascade="all, delete-orphan")
