from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import get_connection
import sqlite3

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        flash("Please log in to access settings.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'preferences':
            email_notif = 1 if request.form.get('email_notif') else 0
            sms_notif = 1 if request.form.get('sms_notif') else 0
            dark_mode = 1 if request.form.get('dark_mode') else 0
            refresh_interval = int(request.form.get('refresh_interval') or 60)
            
            try:
                # Check if settings record exists
                if isinstance(conn, sqlite3.Connection):
                    cursor.execute("SELECT id FROM user_settings WHERE user_id = ?", (user_id,))
                else:
                    cursor.execute("SELECT id FROM user_settings WHERE user_id = %s", (user_id,))
                exists = cursor.fetchone()
                
                if exists:
                    if isinstance(conn, sqlite3.Connection):
                        cursor.execute("""
                            UPDATE user_settings 
                            SET email_notifications = ?, sms_notifications = ?, dark_mode = ?, weather_refresh_interval = ?
                            WHERE user_id = ?
                        """, (email_notif, sms_notif, dark_mode, refresh_interval, user_id))
                    else:
                        cursor.execute("""
                            UPDATE user_settings 
                            SET email_notifications = %s, sms_notifications = %s, dark_mode = %s, weather_refresh_interval = %s
                            WHERE user_id = %s
                        """, (email_notif, sms_notif, dark_mode, refresh_interval, user_id))
                else:
                    if isinstance(conn, sqlite3.Connection):
                        cursor.execute("""
                            INSERT INTO user_settings (user_id, email_notifications, sms_notifications, dark_mode, weather_refresh_interval)
                            VALUES (?, ?, ?, ?, ?)
                        """, (user_id, email_notif, sms_notif, dark_mode, refresh_interval))
                    else:
                        cursor.execute("""
                            INSERT INTO user_settings (user_id, email_notifications, sms_notifications, dark_mode, weather_refresh_interval)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (user_id, email_notif, sms_notif, dark_mode, refresh_interval))
                
                conn.commit()
                flash("Settings saved successfully.", "success")
            except Exception as e:
                flash(f"Error saving settings: {e}", "error")
                
        elif action == 'password':
            old_pwd = request.form.get('old_password')
            new_pwd = request.form.get('new_password')
            
            try:
                if isinstance(conn, sqlite3.Connection):
                    cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
                else:
                    cursor.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['password_hash'], old_pwd):
                    new_hash = generate_password_hash(new_pwd)
                    if isinstance(conn, sqlite3.Connection):
                        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
                    else:
                        cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash, user_id))
                    conn.commit()
                    flash("Password changed successfully.", "success")
                else:
                    flash("Invalid current password.", "error")
            except Exception as e:
                flash(f"Error changing password: {e}", "error")
                
        cursor.close()
        conn.close()
        return redirect(url_for('settings.index'))
        
    # GET: Load settings values
    settings_data = {
        'email_notifications': 1,
        'sms_notifications': 0,
        'dark_mode': 0,
        'weather_refresh_interval': 60
    }
    
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM user_settings WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            settings_data = {
                'email_notifications': row['email_notifications'],
                'sms_notifications': row['sms_notifications'],
                'dark_mode': row['dark_mode'],
                'weather_refresh_interval': row['weather_refresh_interval']
            }
    except Exception as e:
        print(f"Error loading user settings: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return render_template('settings.html', settings=settings_data)

@settings_bp.route('/settings/delete', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Delete user record (foreign keys cascade deletes history and settings)
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        else:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        session.clear()
        flash("Your account has been deleted permanently.", "success")
        return redirect(url_for('landing'))
    except Exception as e:
        flash(f"Error deleting account: {e}", "error")
        return redirect(url_for('settings.index'))
    finally:
        cursor.close()
        conn.close()
