from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database.db_connection import get_connection
import sqlite3

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        flash("Please log in to access your profile.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        age = int(request.form.get('age') or 0)
        gender = request.form.get('gender')
        height = float(request.form.get('height') or 0)
        weight = float(request.form.get('weight') or 0)
        skin_type = request.form.get('skin_type')
        city = request.form.get('city')
        
        # Calculate BMI
        bmi = 0
        if height > 0:
            bmi = round(weight / ((height / 100.0) ** 2), 2)
            
        try:
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("""
                    UPDATE users 
                    SET name=?, phone=?, age=?, gender=?, height=?, weight=?, bmi=?, skin_type=?, city=?
                    WHERE id=?
                """, (name, phone, age, gender, height, weight, bmi, skin_type, city, user_id))
            else:
                cursor.execute("""
                    UPDATE users 
                    SET name=%s, phone=%s, age=%s, gender=%s, height=%s, weight=%s, bmi=%s, skin_type=%s, city=%s
                    WHERE id=%s
                """, (name, phone, age, gender, height, weight, bmi, skin_type, city, user_id))
            conn.commit()
            
            session['user_name'] = name
            session['user_city'] = city
            flash("Profile updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating profile: {e}", "error")
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('profile.index'))
        
    # GET request: load user data
    user = None
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    except Exception as e:
        flash(f"Error loading user profile: {e}", "error")
    finally:
        cursor.close()
        conn.close()
        
    if not user:
        return redirect(url_for('auth.login'))
        
    return render_template('profile.html', user=user)
