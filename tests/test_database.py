"""
Database Tests - VitalSync
Tests for database connection, schema initialization, and CRUD queries.
"""

import pytest
import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import get_connection, init_db
from database.queries import get_user_by_email, get_user_by_id, insert_audit_log


@pytest.fixture(autouse=True)
def setup_db():
    """Ensure fresh database tables exist before each test."""
    init_db()
    yield


class TestDatabaseConnection:
    """Test database connectivity and initialization."""
    
    def test_get_connection_returns_sqlite(self):
        """Without Postgres env, should return SQLite connection."""
        conn = get_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_init_db_creates_tables(self):
        """init_db should create all 6 tables."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        assert 'users' in tables
        assert 'weather' in tables
        assert 'recommendations' in tables
        assert 'recommendation_history' in tables
        assert 'user_settings' in tables
        assert 'audit_logs' in tables


class TestCRUDOperations:
    """Test database create/read/update/delete operations."""
    
    def test_insert_and_read_user(self):
        """Inserting a user and reading it back should work."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (name, email, phone, age, gender, height, weight, bmi, skin_type, city, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ('DB Test', 'dbtest@test.com', '', 25, 'Male', 180, 75, 23.15, 'Type III (Medium)', 'NYC', 'fakehash'))
        conn.commit()
        
        user = get_user_by_email('dbtest@test.com')
        assert user is not None
        assert user['name'] == 'DB Test'
        assert float(user['bmi']) == 23.15
        
        cursor.close()
        conn.close()
    
    def test_insert_audit_log(self):
        """Audit log insertion should succeed."""
        # First insert a user
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        """, ('Audit Test', 'audit@test.com', 'fakehash'))
        conn.commit()
        
        user = get_user_by_email('audit@test.com')
        insert_audit_log(user['id'], 'Test Action', '127.0.0.1')
        
        cursor.execute("SELECT * FROM audit_logs WHERE user_id = ?", (user['id'],))
        logs = cursor.fetchall()
        assert len(logs) >= 1
        
        cursor.close()
        conn.close()
    
    def test_delete_user_cascades(self):
        """Deleting a user should cascade to settings and history."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Insert user
        cursor.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        """, ('Cascade Test', 'cascade@test.com', 'fakehash'))
        conn.commit()
        
        user = get_user_by_email('cascade@test.com')
        uid = user['id']
        
        # Insert settings for user
        cursor.execute("INSERT INTO user_settings (user_id) VALUES (?)", (uid,))
        # Insert history for user
        cursor.execute("""
            INSERT INTO recommendation_history (user_id, city, temperature, uv_index, category, title, recommendation_text)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (uid, 'Test', 25, 3, 'hydration', 'Test Rec', 'Test text'))
        conn.commit()
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (uid,))
        conn.commit()
        
        # Settings and history should be gone
        cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (uid,))
        assert cursor.fetchone() is None
        
        cursor.execute("SELECT * FROM recommendation_history WHERE user_id = ?", (uid,))
        assert cursor.fetchone() is None
        
        cursor.close()
        conn.close()
    
    def test_weather_table_insert(self):
        """Weather log insertions should work."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO weather (city, temperature, humidity, uv_index, condition, wind_speed, pressure, visibility)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ('TestCity', 28.5, 60, 5.0, 'Clear', 12.0, 1015, 10.0))
        conn.commit()
        
        cursor.execute("SELECT * FROM weather WHERE city = ?", ('TestCity',))
        row = cursor.fetchone()
        assert row is not None
        
        cursor.close()
        conn.close()
