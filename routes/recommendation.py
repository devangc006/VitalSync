from flask import Blueprint, render_template, session, redirect, url_for, flash
from database.db_connection import get_connection
from services.weather_service import get_weather_data
from services.recommendation_engine import generate_recommendations
import sqlite3

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendations')
def index():
    if 'user_id' not in session:
        flash("Please log in to view wellness recommendations.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    user = None
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
    finally:
        cursor.close()
        conn.close()
        
    if not user:
        return redirect(url_for('auth.login'))
        
    # Get weather
    weather_info = get_weather_data(user['city'])
    
    # Calculate recommendations
    recs = generate_recommendations(user, weather_info)
    
    # Log to history
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for rec in recs:
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("""
                    INSERT INTO recommendation_history (user_id, city, temperature, uv_index, category, title, recommendation_text)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, weather_info['city'], weather_info['temperature'], weather_info['uv_index'], rec['category'], rec['title'], rec['text']))
            else:
                cursor.execute("""
                    INSERT INTO recommendation_history (user_id, city, temperature, uv_index, category, title, recommendation_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, weather_info['city'], weather_info['temperature'], weather_info['uv_index'], rec['category'], rec['title'], rec['text']))
        conn.commit()
    except Exception as e:
        print(f"Error logging recommendation history: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return render_template('recommendations.html', recommendations=recs, weather=weather_info)
