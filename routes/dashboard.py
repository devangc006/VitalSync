from flask import Blueprint, render_template, session, redirect, url_for, flash
from database.db_connection import get_connection
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def index():
    if 'user_id' not in session:
        flash("Please log in to access your dashboard.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    user = None
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
    except Exception as e:
        flash(f"Error loading dashboard: {e}", "error")
        return redirect(url_for('auth.login'))
    finally:
        cursor.close()
        conn.close()
        
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    # Mock weather data for user's city (Real-time weather service will replace this in the next steps)
    weather_data = {
        'city': user['city'],
        'temperature': 29.5, # Celsius
        'humidity': 65,      # %
        'uv_index': 6.2,     # UV index
        'condition': 'Mostly Sunny',
        'wind_speed': 12.0   # km/h
    }
    
    # Calculate Water Intake Goal dynamically (Base: 35ml per kg + weather adjustments)
    # E.g. If Temp > 25°C, add 500ml. If UV Index > 5, add 300ml.
    weight = float(user['weight'] or 70)
    base_water = weight * 35 # ml
    if weather_data['temperature'] > 25:
        base_water += 500
    if weather_data['uv_index'] > 5:
        base_water += 300
    water_goal_liters = round(base_water / 1000.0, 1)

    # Determine BMI Category text & color
    bmi = float(user['bmi'] or 0)
    if bmi < 18.5:
        bmi_category = "Underweight"
        bmi_color = "var(--accent-blue)"
    elif bmi < 25:
        bmi_category = "Normal"
        bmi_color = "var(--accent-mint)"
    elif bmi < 30:
        bmi_category = "Overweight"
        bmi_color = "var(--accent-orange)"
    else:
        bmi_category = "Obese"
        bmi_color = "var(--accent-red)"

    # Recommendations based on Weather & Health Data
    recommendations = []
    
    # Hydration
    if weather_data['temperature'] > 28:
        recommendations.append({
            'icon': 'fa-tint',
            'title': 'High Heat Hydration',
            'text': f'Temperature is high ({weather_data["temperature"]}°C). Drink at least {water_goal_liters}L of water today.',
            'category': 'hydration'
        })
    else:
        recommendations.append({
            'icon': 'fa-tint',
            'title': 'Routine Hydration',
            'text': f'Keep hydrated. Goal is {water_goal_liters}L of water throughout the day.',
            'category': 'hydration'
        })
        
    # UV Alerts
    if weather_data['uv_index'] >= 6:
        recommendations.append({
            'icon': 'fa-sun',
            'title': 'High UV Sunscreen Advice',
            'text': 'UV index is high today. Use SPF 30+ sunscreen, wear protective sunglasses, and limit midday exposure.',
            'category': 'uv'
        })
    elif weather_data['uv_index'] >= 3:
        recommendations.append({
            'icon': 'fa-sun',
            'title': 'Moderate UV Protection',
            'text': 'Sun intensity is moderate. Consider sunscreen and a cap for longer outdoor sessions.',
            'category': 'uv'
        })
        
    # Skincare
    skin_type = user['skin_type']
    if 'Fair' in skin_type or 'Very Fair' in skin_type:
        if weather_data['uv_index'] >= 3:
            recommendations.append({
                'icon': 'fa-spa',
                'title': 'Sensitive Skin Protection',
                'text': 'Your skin type is fair/sensitive. Apply zinc oxide sunscreen and moisturize due to uv/wind factors.',
                'category': 'skincare'
            })
    else:
        recommendations.append({
            'icon': 'fa-spa',
            'title': 'Daily Skin Moisture',
            'text': f'Maintain hydration barrier. Skin Type is classified as {skin_type}.',
            'category': 'skincare'
        })

    # Activity/Exercise
    if weather_data['temperature'] > 32:
        recommendations.append({
            'icon': 'fa-running',
            'title': 'Indoor Exercise Recommended',
            'text': 'Outdoor temperature is unsafe for high-intensity training. Exercise in air-conditioned spaces.',
            'category': 'exercise'
        })
    else:
        recommendations.append({
            'icon': 'fa-running',
            'title': 'Ideal Outdoor Exercise',
            'text': 'Weather is suitable for jogging or cycling. Enjoy your workout session!',
            'category': 'exercise'
        })

    activities = [
        {'time': '08:30 AM', 'title': 'Morning Jogging', 'desc': 'Completed 3.5 km outdoor session'},
        {'time': '10:00 AM', 'title': 'Water Intake Logged', 'desc': 'Drank 500 ml glass'},
        {'time': '01:15 PM', 'title': 'UV Shield Applied', 'desc': 'SPF 30+ protection applied'}
    ]

    notifications = [
        {'title': 'Hydration Alert', 'text': 'Time to drink water! Keep up with your goal.', 'time': '5 min ago'},
        {'title': 'Sun Alert', 'text': 'UV Index peaked at 6.2. Apply protection.', 'time': '30 min ago'}
    ]

    return render_template(
        'dashboard.html', 
        user=user, 
        weather=weather_data, 
        water_goal=water_goal_liters, 
        bmi_cat=bmi_category,
        bmi_color=bmi_color,
        recommendations=recommendations,
        activities=activities,
        notifications=notifications
    )
