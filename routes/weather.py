from flask import Blueprint, render_template, session, redirect, url_for, flash
from database.db_connection import get_connection
from services.weather_service import get_weather_data
import sqlite3

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather')
def index():
    if 'user_id' not in session:
        flash("Please log in to view weather data.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    city = None
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT city FROM users WHERE id = ?", (user_id,))
        else:
            cursor.execute("SELECT city FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            city = row['city']
    except Exception as e:
        print(f"Error loading user location: {e}")
    finally:
        cursor.close()
        conn.close()
        
    if not city:
        city = session.get('user_city', 'New York')
        
    # Get current weather conditions & forecast
    weather_info = get_weather_data(city)
    
    return render_template('weather.html', weather=weather_info)
