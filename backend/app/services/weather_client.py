from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256

from app.config.settings import get_settings

WEATHER_CONDITION_MAP = ["Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm", "Mist"]


def _fallback_weather(city: str) -> dict[str, object]:
    seed = int(sha256(city.strip().lower().encode('utf-8')).hexdigest()[:8], 16)
    temperature = 22 + (seed % 1800) / 100
    humidity = 35 + seed % 55
    uv_index = 2 + seed % 10
    wind_speed = 1 + (seed % 1200) / 100
    condition = WEATHER_CONDITION_MAP[seed % len(WEATHER_CONDITION_MAP)]
    return {
        'city': city,
        'temperature_c': round(temperature, 1),
        'humidity_percent': float(humidity),
        'uv_index': float(uv_index),
        'weather_condition': condition,
        'wind_speed_mps': round(wind_speed, 1),
        'source': 'fallback',
        'timestamp': datetime.now(timezone.utc),
    }


async def fetch_weather(city: str) -> dict[str, object]:
    settings = get_settings()
    if not settings.openweather_api_key:
        return _fallback_weather(city)

    import httpx

    params = {
        'q': city,
        'appid': settings.openweather_api_key,
        'units': 'metric',
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        response.raise_for_status()
        payload = response.json()

    temperature = float(payload['main']['temp'])
    humidity = float(payload['main']['humidity'])
    wind_speed = float(payload.get('wind', {}).get('speed', 0.0))
    condition = str(payload['weather'][0]['main'])
    uv_index = max(0.0, min(11.0, round((temperature / 5) + (humidity / 30), 1)))
    return {
        'city': payload.get('name', city),
        'temperature_c': round(temperature, 1),
        'humidity_percent': round(humidity, 1),
        'uv_index': uv_index,
        'weather_condition': condition,
        'wind_speed_mps': round(wind_speed, 1),
        'source': 'openweather',
        'timestamp': datetime.now(timezone.utc),
    }
