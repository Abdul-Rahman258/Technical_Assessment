import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"  # For weather and forecast
GEO_BASE_URL = "https://api.openweathermap.org/geo/1.0"  # Separate for geocoding

def get_coordinates(location):
    geo_url = f"{GEO_BASE_URL}/direct?q={location}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None

def get_current_weather(location):
    lat, lon = get_coordinates(location)
    if lat is None:
        return {"error": "Invalid location"}
    weather_url = f"{WEATHER_BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        return {
            "location": data['name'],
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon']
        }
    return {"error": "API error"}

def get_forecast(location):
    lat, lon = get_coordinates(location)
    if lat is None:
        return {"error": "Invalid location"}
    forecast_url = f"{WEATHER_BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for item in data['list'][:5*8:8]:  # Daily forecast (every 24 hours)
            forecast.append({
                "date": item['dt_txt'],
                "temp": item['main']['temp'],
                "description": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon']
            })
        return forecast

    return {"error": "API error"}
