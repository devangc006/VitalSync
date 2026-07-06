from app.utils.health import bmi_category, calculate_bmi, calculate_water_goal


def build_health_summary(
    weight_kg: float,
    height_cm: float,
    temperature_c: float | None = None,
    humidity_percent: float | None = None,
) -> dict[str, float | str]:
    bmi = calculate_bmi(weight_kg, height_cm)
    return {
        'bmi': bmi,
        'bmi_category': bmi_category(bmi),
        'water_goal_liters': calculate_water_goal(weight_kg, temperature_c, humidity_percent),
    }
