from __future__ import annotations


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0:
        return 0.0
    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 1)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calculate_water_goal(weight_kg: float, temperature_c: float | None = None, humidity_percent: float | None = None) -> float:
    base_goal = weight_kg * 0.035
    if temperature_c is not None and temperature_c >= 35:
        base_goal += 0.5
    elif temperature_c is not None and temperature_c >= 30:
        base_goal += 0.25
    if humidity_percent is not None and humidity_percent >= 75:
        base_goal += 0.25
    return round(max(base_goal, 1.5), 2)
