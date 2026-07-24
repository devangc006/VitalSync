def calculate_hydration(weight, temperature, humidity):
    """
    Computes daily water intake recommendations.
    Base requirement: 35ml per kg of body weight.
    Adjustments:
      - Add 500ml if temp > 25°C.
      - Add 1000ml if temp > 32°C.
      - Subtract 200ml if humidity > 80% (lower evaporation rate, less immediate fluid loss from sweat evaporation, though high humidity + high heat requires careful monitoring).
    """
    base_ml = weight * 35
    
    if temperature > 32:
        base_ml += 1000
    elif temperature > 25:
        base_ml += 500
        
    if humidity > 80 and temperature < 22:
        base_ml -= 200
        
    goal_liters = round(base_ml / 1000.0, 2)
    
    # Generate message
    if temperature > 32:
        title = "Critical Heat Hydration Alert"
        text = f"Extreme weather ({temperature}°C) detected. Drink {goal_liters}L of water throughout the day. Avoid sugary drinks."
        alert_level = "danger"
    elif temperature > 25:
        title = "Increased Hydration Required"
        text = f"Warm conditions detected. Boost water intake to {goal_liters}L to offset perspiration losses."
        alert_level = "warning"
    else:
        title = "Normal Hydration Goal"
        text = f"Maintain standard hydration. Aim for {goal_liters}L of water divided evenly across the day."
        alert_level = "info"
        
    return {
        'title': title,
        'text': text,
        'goal_liters': goal_liters,
        'alert_level': alert_level,
        'category': 'hydration',
        'icon': 'fa-tint'
    }
