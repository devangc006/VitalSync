from datetime import datetime

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature_c: float
    humidity_percent: float
    uv_index: float
    weather_condition: str
    wind_speed_mps: float
    source: str
    timestamp: datetime
