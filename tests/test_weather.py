"""
Weather Service Tests - VitalSync
Tests for OpenWeatherMap API service and weather route.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from services.weather_service import get_weather_data, get_mock_weather_data, get_weather_icon_class


@pytest.fixture
def app():
    app = create_app('testing')
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


class TestWeatherService:
    """Test the weather service module functions."""
    
    def test_mock_weather_returns_complete_data(self):
        """Mock weather should return all required fields."""
        data = get_mock_weather_data('Mumbai')
        
        assert 'city' in data
        assert 'temperature' in data
        assert 'humidity' in data
        assert 'uv_index' in data
        assert 'condition' in data
        assert 'wind_speed' in data
        assert 'pressure' in data
        assert 'visibility' in data
        assert 'forecast' in data
    
    def test_mock_weather_city_variations(self):
        """Different cities should return region-appropriate conditions."""
        mumbai = get_mock_weather_data('Mumbai')
        delhi = get_mock_weather_data('Delhi')
        london = get_mock_weather_data('London')
        
        # Mumbai should be hot and rainy
        assert mumbai['condition'] == 'Rain'
        assert mumbai['temperature'] > 28
        
        # Delhi should be hot and clear
        assert delhi['condition'] == 'Clear'
        assert delhi['temperature'] > 35
        
        # London should be cool and drizzly
        assert london['condition'] == 'Drizzle'
        assert london['temperature'] < 20
    
    def test_mock_forecast_has_7_days(self):
        """Forecast should contain 7 day entries."""
        data = get_mock_weather_data('Test City')
        assert len(data['forecast']) == 7
    
    def test_weather_icon_class_mapping(self):
        """Weather conditions should map to FontAwesome icon classes."""
        assert get_weather_icon_class('Clear') == 'fa-sun'
        assert get_weather_icon_class('Rain') == 'fa-cloud-showers-heavy'
        assert get_weather_icon_class('Snow') == 'fa-snowflake'
        assert get_weather_icon_class('Unknown') == 'fa-cloud-sun'  # Default fallback
    
    def test_get_weather_data_fallback(self):
        """Without API key, get_weather_data should return mock data."""
        data = get_weather_data('Mumbai')
        assert data is not None
        assert 'temperature' in data


class TestWeatherRoute:
    """Test the /weather route endpoint."""
    
    def test_weather_page_redirects_without_login(self, client):
        """Weather page should redirect to login if not authenticated."""
        response = client.get('/weather', follow_redirects=False)
        assert response.status_code == 302
    
    def test_weather_page_accessible_when_logged_in(self, client):
        """Weather page should load when logged in."""
        # Register and login
        reg_data = {
            'name': 'Weather Tester',
            'email': 'weathertest@test.com',
            'phone': '',
            'age': 30,
            'gender': 'Male',
            'height': 175,
            'weight': 70,
            'skin_type': 'Type III (Medium)',
            'city': 'Mumbai',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }
        client.post('/register', data=reg_data)
        
        response = client.get('/weather')
        assert response.status_code == 200
        assert b'Weather' in response.data
