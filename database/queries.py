from database.db_connection import get_connection
import sqlite3

# Try to detect psycopg2 for Postgres connections
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


def _get_cursor_for_conn(conn):
    """Return a cursor appropriate for the connection type.

    For psycopg2 connections return a RealDictCursor so callers get dict-like
    rows. For sqlite return a normal cursor (row_factory on the connection
    provides sqlite3.Row objects).
    """
    if HAS_PSYCOPG2:
        try:
            if isinstance(conn, psycopg2.extensions.connection):
                return conn.cursor(cursor_factory=RealDictCursor)
        except Exception:
            pass
    return conn.cursor()


def get_user_by_email(email):
    conn = get_connection()
    cursor = _get_cursor_for_conn(conn)
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        else:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = _get_cursor_for_conn(conn)
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_user_settings(user_id):
    conn = get_connection()
    cursor = _get_cursor_for_conn(conn)
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM user_settings WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def insert_audit_log(user_id, action, ip_address=None):
    conn = get_connection()
    cursor = _get_cursor_for_conn(conn)
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("""
                INSERT INTO audit_logs (user_id, action, ip_address)
                VALUES (?, ?, ?)
            """, (user_id, action, ip_address))
        else:
            cursor.execute("""
                INSERT INTO audit_logs (user_id, action, ip_address)
                VALUES (%s, %s, %s)
            """, (user_id, action, ip_address))
        conn.commit()
    except Exception as e:
        print(f"Error logging audit record: {e}")
    finally:
        cursor.close()
        conn.close()


def get_recommendation_history(user_id):
    conn = get_connection()
    cursor = _get_cursor_for_conn(conn)
    try:
        if isinstance(conn, sqlite3.Connection):
            cursor.execute("SELECT * FROM recommendation_history WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        else:
            cursor.execute("SELECT * FROM recommendation_history WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
