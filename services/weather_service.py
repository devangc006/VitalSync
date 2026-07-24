import os
import requests

API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")

def get_weather_data(city):
    """
    Fetches real-time weather and forecast data for the specified city from OpenWeatherMap.
    Falls back to high-quality mock data if API key is not configured or queries fail.
    """
    if not API_KEY:
        return get_mock_weather_data(city)

    try:
        # 1. Fetch Current Weather
        current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(current_url, timeout=5)
        if response.status_code != 200:
            return get_mock_weather_data(city)
            
        data = response.json()
        
        # 2. Get coords to fetch UV index and forecast (mocking UV or calling secondary API if required)
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        
        # UV index is part of OneCall API, which requires subscription. 
        # We will query openuv or estimate based on weather conditions to avoid user billing issues.
        # Let's estimate UV index dynamically based on cloudiness/condition.
        clouds = data.get('clouds', {}).get('all', 0)
        estimated_uv = max(1.0, round(10.0 - (clouds / 12.0), 1))
        
        # 3. Weather Details
        weather_info = {
            'city': data.get('name', city),
            'temperature': round(data['main']['temp'], 1),
            'humidity': data['main']['humidity'],
            'uv_index': estimated_uv,
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'].capitalize(),
            'wind_speed': round(data['wind']['speed'] * 3.6, 1), # convert m/s to km/h
            'pressure': data['main']['pressure'],
            'visibility': round(data.get('visibility', 10000) / 1000.0, 1), # km
            'forecast': get_forecast_forecast(lat, lon)
        }
        return weather_info
        
    except Exception as e:
        print(f"Weather API error: {e}. Using mock fallback.")
        return get_mock_weather_data(city)

def get_forecast_forecast(lat, lon):
    """
    Queries forecast or provides structured 7-day weather expectations.
    """
    if not API_KEY:
        return []
    try:
        # Fetch 5-day / 3-hour forecast as free tier fallback
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        res = requests.get(forecast_url, timeout=5)
        if res.status_code != 200:
            return get_mock_forecast()
            
        data = res.json()
        # Group by days (every 8th slot approx 24h)
        daily_forecasts = []
        slots = data.get('list', [])
        for idx in range(0, len(slots), 8):
            slot = slots[idx]
            dt_txt = slot.get('dt_txt', '').split(' ')[0]
            # Convert date to weekday
            from datetime import datetime
            day_name = datetime.strptime(dt_txt, "%Y-%m-%d").strftime("%A") if dt_txt else "Day"
            
            daily_forecasts.append({
                'day': day_name,
                'temp_high': round(slot['main']['temp_max'], 1),
                'temp_low': round(slot['main']['temp_min'], 1),
                'condition': slot['weather'][0]['main'],
                'icon': get_weather_icon_class(slot['weather'][0]['main'])
            })
        return daily_forecasts
    except:
        return get_mock_forecast()

def get_weather_icon_class(main_cond):
    mapping = {
        'Clear': 'fa-sun',
        'Clouds': 'fa-cloud',
        'Rain': 'fa-cloud-showers-heavy',
        'Drizzle': 'fa-cloud-rain',
        'Thunderstorm': 'fa-bolt',
        'Snow': 'fa-snowflake',
        'Mist': 'fa-smog',
        'Smoke': 'fa-smog',
        'Haze': 'fa-smog',
        'Dust': 'fa-smog',
        'Fog': 'fa-smog',
        'Sand': 'fa-smog',
        'Ash': 'fa-smog',
        'Squall': 'fa-wind',
        'Tornado': 'fa-tornado'
    }
    return mapping.get(main_cond, 'fa-cloud-sun')

def get_mock_weather_data(city):
    """
    Produces realistic weather stats depending on the city name.
    """
    city_lower = city.lower()
    
    # Defaults
    temp = 22.0
    cond = 'Clouds'
    desc = 'broken clouds'
    humid = 60
    uv = 4.5
    wind = 10.0
    press = 1012
    vis = 10.0
    
    if 'mumbai' in city_lower or 'chennai' in city_lower or 'kolkata' in city_lower:
        temp = 31.5
        cond = 'Rain'
        desc = 'moderate rain'
        humid = 88
        uv = 3.0
        wind = 22.0
    elif 'delhi' in city_lower or 'phoenix' in city_lower or 'sahara' in city_lower:
        temp = 39.0
        cond = 'Clear'
        desc = 'clear sky'
        humid = 25
        uv = 9.5
        wind = 14.0
    elif 'london' in city_lower or 'seattle' in city_lower:
        temp = 14.5
        cond = 'Drizzle'
        desc = 'light intensity drizzle'
        humid = 82
        uv = 2.1
        wind = 18.0
        
    return {
        'city': city.capitalize(),
        'temperature': temp,
        'humidity': humid,
        'uv_index': uv,
        'condition': cond,
        'description': desc,
        'wind_speed': wind,
        'pressure': press,
        'visibility': vis,
        'forecast': get_mock_forecast()
    }

def get_mock_forecast():
    return [
        {'day': 'Monday', 'temp_high': 28, 'temp_low': 20, 'condition': 'Clear', 'icon': 'fa-sun'},
        {'day': 'Tuesday', 'temp_high': 29, 'temp_low': 21, 'condition': 'Clouds', 'icon': 'fa-cloud'},
        {'day': 'Wednesday', 'temp_high': 27, 'temp_low': 20, 'condition': 'Rain', 'icon': 'fa-cloud-showers-heavy'},
        {'day': 'Thursday', 'temp_high': 26, 'temp_low': 19, 'condition': 'Clear', 'icon': 'fa-sun'},
        {'day': 'Friday', 'temp_high': 28, 'temp_low': 20, 'condition': 'Clouds', 'icon': 'fa-cloud-sun'},
        {'day': 'Saturday', 'temp_high': 30, 'temp_low': 22, 'condition': 'Clear', 'icon': 'fa-sun'},
        {'day': 'Sunday', 'temp_high': 31, 'temp_low': 23, 'condition': 'Clear', 'icon': 'fa-sun'}
    ]
