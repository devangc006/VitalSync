from __future__ import annotations

from app.utils.health import calculate_water_goal


def build_recommendations(
    *,
    temperature_c: float,
    humidity_percent: float,
    uv_index: float,
    weather_condition: str,
    skin_type: str,
    weight_kg: float,
) -> list[dict[str, str]]:
    recommendations: list[dict[str, str]] = []

    if temperature_c > 38:
        recommendations.append({"category": "Heat", "recommendation": "Avoid outdoor activity between 11 AM and 3 PM."})
    elif temperature_c > 35:
        recommendations.append({"category": "Hydration", "recommendation": "Increase water intake to around 3.5L today."})

    if humidity_percent >= 75:
        recommendations.append({"category": "Comfort", "recommendation": "Expect a muggy day and keep extra water nearby."})

    if uv_index > 8:
        recommendations.append({"category": "Sun Safety", "recommendation": "Use SPF 50 sunscreen and avoid direct midday sun."})
    elif uv_index > 6:
        recommendations.append({"category": "Sun Safety", "recommendation": "Use sunscreen before going outside."})

    if weather_condition.lower() in {"rain", "drizzle", "thunderstorm"}:
        recommendations.append({"category": "Weather", "recommendation": "Carry an umbrella and waterproof essentials."})

    skin_type_lower = skin_type.lower()
    if skin_type_lower == 'dry':
        recommendations.append({"category": "Skin", "recommendation": "Use a moisturizer and hydrate consistently."})
    elif skin_type_lower == 'oily':
        recommendations.append({"category": "Skin", "recommendation": "Prefer oil-free sunscreen and non-comedogenic products."})
    elif skin_type_lower == 'sensitive':
        recommendations.append({"category": "Skin", "recommendation": "Choose fragrance-free skincare and gentle sunscreen."})
    else:
        recommendations.append({"category": "Skin", "recommendation": "Maintain your routine and reapply sunscreen when outdoors."})

    water_goal = calculate_water_goal(weight_kg, temperature_c, humidity_percent)
    recommendations.append({"category": "Hydration", "recommendation": f"Target about {water_goal:.1f}L of water today."})
    return recommendations
