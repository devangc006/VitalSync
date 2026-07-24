from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database.db_connection import get_connection
import sqlite3

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
def index():
    if 'user_id' not in session:
        flash("Please log in to view recommendation logs.", "error")
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    logs = []
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("""
                SELECT * FROM recommendation_history 
                WHERE user_id = ? 
                ORDER BY created_at DESC
            """, (user_id,))
        else:
            cursor.execute("""
                SELECT * FROM recommendation_history 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """, (user_id,))
        logs = cursor.fetchall()
    except Exception as e:
        flash(f"Error loading logs: {e}", "error")
    finally:
        cursor.close()
        conn.close()
        
    return render_template('history.html', logs=logs)

@history_bp.route('/history/delete/<int:log_id>', methods=['POST'])
def delete_log(log_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("DELETE FROM recommendation_history WHERE id = ? AND user_id = ?", (log_id, user_id))
        else:
            cursor.execute("DELETE FROM recommendation_history WHERE id = %s AND user_id = %s", (log_id, user_id))
        conn.commit()
        flash("History log deleted successfully.", "success")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@history_bp.route('/history/clear', methods=['POST'])
def clear_history():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("DELETE FROM recommendation_history WHERE user_id = ?", (user_id,))
        else:
            cursor.execute("DELETE FROM recommendation_history WHERE user_id = %s", (user_id,))
        conn.commit()
        flash("All recommendation history cleared.", "success")
    except Exception as e:
        flash(f"Error clearing logs: {e}", "error")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('history.index'))
