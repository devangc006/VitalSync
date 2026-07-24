from services.hydration import calculate_hydration
from services.uv_alert import calculate_uv_safety
from services.skin_care import calculate_skin_care

def generate_recommendations(user, weather):
    """
    Unified manager compiling recommendations from hydration, UV, skincare, exercise, and attire rules.
    """
    weight = float(user['weight'] or 70)
    skin_type = user['skin_type'] or "Type III (Medium)"
    
    temp = weather['temperature']
    humidity = weather['humidity']
    uv_index = weather['uv_index']
    condition = weather['condition'].lower()
    
    recs = []
    
    # 1. Hydration
    recs.append(calculate_hydration(weight, temp, humidity))
    
    # 2. UV Safety
    recs.append(calculate_uv_safety(uv_index))
    
    # 3. Skincare
    recs.append(calculate_skin_care(skin_type, uv_index, humidity))
    
    # 4. Umbrella Reminder (Attire/Precipitation)
    if 'rain' in condition or 'drizzle' in condition or 'thunderstorm' in condition:
        recs.append({
            'title': 'Umbrella Required',
            'text': f"Rain/precipitation detected ({weather['condition']}). Carry a waterproof umbrella and wear slip-resistant shoes.",
            'alert_level': 'danger',
            'category': 'attire',
            'icon': 'fa-umbrella'
        })
    elif 'snow' in condition:
        recs.append({
            'title': 'Heavy Winter Wear',
            'text': "Snowfall active. Wear thermal layers, gloves, and water-repellent boots.",
            'alert_level': 'warning',
            'category': 'attire',
            'icon': 'fa-snowflake'
        })
    else:
        recs.append({
            'title': 'No Umbrella Needed',
            'text': "No precipitation expected. Light, breathable clothing is suitable.",
            'alert_level': 'success',
            'category': 'attire',
            'icon': 'fa-tshirt'
        })
        
    # 5. Exercise suggestions
    if temp > 33:
        recs.append({
            'title': 'Heat Exhaustion Warning',
            'text': f"High outdoor temperatures ({temp}°C) increase heat stress risk. Restrict cardio training to indoor, air-conditioned environments.",
            'alert_level': 'danger',
            'category': 'exercise',
            'icon': 'fa-running'
        })
    elif temp < 5:
        recs.append({
            'title': 'Hypothermia Precaution',
            'text': f"Cold weather ({temp}°C). Perform warmups indoors and dress in wind-resistant layers if running outside.",
            'alert_level': 'warning',
            'category': 'exercise',
            'icon': 'fa-running'
        })
    elif 'rain' in condition or 'thunderstorm' in condition:
        recs.append({
            'title': 'Slippery Outdoor Conditions',
            'text': "Active rain will affect road traction. Transition your routines to yoga, core workouts, or indoor treadmill sessions today.",
            'alert_level': 'warning',
            'category': 'exercise',
            'icon': 'fa-running'
        })
    else:
        recs.append({
            'title': 'Optimal Outdoor Workouts',
            'text': f"Excellent atmospheric conditions ({temp}°C, {weather['condition']}). Ideal for cycling, running, or outdoor aerobics.",
            'alert_level': 'success',
            'category': 'exercise',
            'icon': 'fa-running'
        })
        
    return recs
