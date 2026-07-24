"""
Recommendation Engine Tests - VitalSync
Tests for hydration, UV alerts, skin care, and the unified engine.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.hydration import calculate_hydration
from services.uv_alert import calculate_uv_safety
from services.skin_care import calculate_skin_care
from services.recommendation_engine import generate_recommendations


class TestHydration:
    """Test hydration calculation service."""
    
    def test_normal_temperature_water_goal(self):
        """At moderate temperatures, base hydration should apply."""
        result = calculate_hydration(70, 22, 50)
        assert result['category'] == 'hydration'
        assert result['goal_liters'] == 2.45  # 70kg * 35ml = 2450ml = 2.45L
        assert result['alert_level'] == 'info'
    
    def test_warm_temperature_increases_goal(self):
        """At warm temperatures (>25°C), water goal should increase by 500ml."""
        result = calculate_hydration(70, 28, 50)
        assert result['goal_liters'] == 2.95  # 2450 + 500 = 2950ml = 2.95L
        assert result['alert_level'] == 'warning'
    
    def test_extreme_heat_increases_goal(self):
        """At extreme temperatures (>32°C), water goal should increase by 1000ml."""
        result = calculate_hydration(70, 36, 50)
        assert result['goal_liters'] == 3.45  # 2450 + 1000 = 3450ml
        assert result['alert_level'] == 'danger'
    
    def test_high_humidity_cold_reduces_slightly(self):
        """At high humidity + cold temp, small reduction applies."""
        result = calculate_hydration(70, 18, 85)
        assert result['goal_liters'] == 2.25  # 2450 - 200 = 2250ml


class TestUVAlert:
    """Test UV safety alert service."""
    
    def test_low_uv(self):
        """UV <3 should return low risk."""
        result = calculate_uv_safety(2.0)
        assert result['alert_level'] == 'success'
    
    def test_moderate_uv(self):
        """UV 3-5.9 should return moderate."""
        result = calculate_uv_safety(4.5)
        assert result['alert_level'] == 'info'
    
    def test_high_uv(self):
        """UV 6-7.9 should return high."""
        result = calculate_uv_safety(7.0)
        assert result['alert_level'] == 'warning'
    
    def test_extreme_uv(self):
        """UV >=8 should return extreme."""
        result = calculate_uv_safety(9.5)
        assert result['alert_level'] == 'danger'


class TestSkinCare:
    """Test skin care recommendation service."""
    
    def test_sensitive_skin_high_uv(self):
        """Fair skin types with high UV should get warning."""
        result = calculate_skin_care('Type I (Very Fair)', 6.0, 50)
        assert result['alert_level'] == 'warning'
        assert result['category'] == 'skincare'
    
    def test_dark_skin_dry_air(self):
        """Darker skin in dry air should get moisturizer advice."""
        result = calculate_skin_care('Type V (Dark Brown)', 2.0, 30)
        assert 'Dry' in result['title']
    
    def test_normal_conditions(self):
        """Standard conditions should return success level."""
        result = calculate_skin_care('Type IV (Olive)', 2.0, 55)
        assert result['alert_level'] == 'success'


class TestRecommendationEngine:
    """Test the unified recommendation engine."""
    
    def test_generates_multiple_recommendations(self):
        """Engine should produce at least 4 recommendation categories."""
        # Mock user-like dict
        user = {
            'weight': 70,
            'skin_type': 'Type III (Medium)'
        }
        weather = {
            'temperature': 30,
            'humidity': 65,
            'uv_index': 6.0,
            'condition': 'Clear'
        }
        
        recs = generate_recommendations(user, weather)
        assert len(recs) >= 4
        
        categories = [r['category'] for r in recs]
        assert 'hydration' in categories
        assert 'uv' in categories
        assert 'skincare' in categories
        assert 'exercise' in categories
    
    def test_rain_produces_umbrella_recommendation(self):
        """Rainy conditions should trigger umbrella recommendation."""
        user = {
            'weight': 70,
            'skin_type': 'Type III (Medium)'
        }
        weather = {
            'temperature': 22,
            'humidity': 85,
            'uv_index': 2.0,
            'condition': 'Rain'
        }
        
        recs = generate_recommendations(user, weather)
        attire_recs = [r for r in recs if r['category'] == 'attire']
        assert len(attire_recs) > 0
        assert 'Umbrella' in attire_recs[0]['title']
    
    def test_extreme_heat_indoor_exercise(self):
        """Extreme heat should suggest indoor exercise."""
        user = {
            'weight': 70,
            'skin_type': 'Type III (Medium)'
        }
        weather = {
            'temperature': 40,
            'humidity': 30,
            'uv_index': 9.0,
            'condition': 'Clear'
        }
        
        recs = generate_recommendations(user, weather)
        exercise_recs = [r for r in recs if r['category'] == 'exercise']
        assert exercise_recs[0]['alert_level'] == 'danger'
