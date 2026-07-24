from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import get_connection
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        conn = get_connection()
        cursor = conn.cursor()
        
        user = None
        try:
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
        except Exception as e:
            flash(f"Database error: {e}", "error")
            return render_template('login.html')
        finally:
            cursor.close()
            conn.close()
            
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_city'] = user['city']
            flash("Welcome back!", "success")
            return redirect(url_for('dashboard.index'))
        else:
            flash("Invalid email or password", "error")
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age = int(request.form.get('age') or 0)
        gender = request.form.get('gender')
        height = float(request.form.get('height') or 0) # in cm
        weight = float(request.form.get('weight') or 0) # in kg
        skin_type = request.form.get('skin_type')
        city = request.form.get('city')
        password = request.form.get('password')
        
        # Calculate BMI: weight (kg) / (height(m) ^ 2)
        bmi = 0
        if height > 0:
            bmi = round(weight / ((height / 100.0) ** 2), 2)
            
        password_hash = generate_password_hash(password)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("""
                    INSERT INTO users (name, email, phone, age, gender, height, weight, bmi, skin_type, city, password_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, email, phone, age, gender, height, weight, bmi, skin_type, city, password_hash))
            else:
                cursor.execute("""
                    INSERT INTO users (name, email, phone, age, gender, height, weight, bmi, skin_type, city, password_hash)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, email, phone, age, gender, height, weight, bmi, skin_type, city, password_hash))
            conn.commit()
            
            # Fetch the newly created user to log them in automatically
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            else:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_city'] = user['city']
            
            flash("Account registered and logged in successfully!", "success")
            return redirect(url_for('dashboard.index'))
            
        except Exception as e:
            flash(f"Error registering user (Email may already exist): {e}", "error")
        finally:
            cursor.close()
            conn.close()
            
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Successfully signed out.", "success")
    return redirect(url_for('landing'))
