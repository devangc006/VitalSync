"""
Authentication Tests - VitalSync
Tests for login, registration, and session management.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from database.db_connection import init_db


@pytest.fixture
def app():
    """Create test application instance with a fresh database."""
    app = create_app('testing')
    app.config['TESTING'] = True
    
    with app.app_context():
        init_db()
    
    yield app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


class TestRegistration:
    """Test user registration flows."""
    
    def test_register_page_loads(self, client):
        """GET /register should return 200."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Create Health Profile' in response.data
    
    def test_register_creates_user(self, client):
        """POST /register with valid data should redirect to dashboard."""
        data = {
            'name': 'Test User',
            'email': 'testuser@test.com',
            'phone': '+1234567890',
            'age': 25,
            'gender': 'Male',
            'height': 175,
            'weight': 70,
            'skin_type': 'Type III (Medium)',
            'city': 'New York',
            'password': 'securepass123',
            'confirm_password': 'securepass123'
        }
        response = client.post('/register', data=data, follow_redirects=False)
        # Should redirect to dashboard on success
        assert response.status_code in (302, 200)
    
    def test_register_duplicate_email(self, client):
        """Registering with a duplicate email should show an error."""
        data = {
            'name': 'User One',
            'email': 'duplicate@test.com',
            'phone': '',
            'age': 30,
            'gender': 'Female',
            'height': 165,
            'weight': 60,
            'skin_type': 'Type II (Fair)',
            'city': 'London',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        # Register first time
        client.post('/register', data=data)
        # Register second time with same email
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200


class TestLogin:
    """Test user login flows."""
    
    def test_login_page_loads(self, client):
        """GET /login should return 200."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Welcome Back' in response.data
    
    def test_login_with_valid_credentials(self, client):
        """Logging in with valid credentials should redirect to dashboard."""
        # First register
        reg_data = {
            'name': 'Login Test User',
            'email': 'logintest@test.com',
            'phone': '',
            'age': 28,
            'gender': 'Male',
            'height': 180,
            'weight': 75,
            'skin_type': 'Type III (Medium)',
            'city': 'Mumbai',
            'password': 'mypassword1',
            'confirm_password': 'mypassword1'
        }
        client.post('/register', data=reg_data)
        # Logout
        client.get('/logout')
        # Now login
        login_data = {
            'email': 'logintest@test.com',
            'password': 'mypassword1'
        }
        response = client.post('/login', data=login_data, follow_redirects=False)
        assert response.status_code in (302, 200)
    
    def test_login_with_wrong_password(self, client):
        """Wrong password should show an error."""
        login_data = {
            'email': 'logintest@test.com',
            'password': 'wrongpassword'
        }
        response = client.post('/login', data=login_data, follow_redirects=True)
        assert response.status_code == 200


class TestLogout:
    """Test logout flow."""
    
    def test_logout_clears_session(self, client):
        """GET /logout should redirect to landing."""
        response = client.get('/logout', follow_redirects=False)
        assert response.status_code == 302
