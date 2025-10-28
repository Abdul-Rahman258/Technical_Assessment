import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('dc09e17cd3dfd7bd1b54e8f8857e4396')
if not API_KEY:
    print("ERROR: API_KEY not loaded from .env")  # Debug for key issues

WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
GEO_BASE_URL = "https://api.openweathermap.org/geo/1.0"

def get_coordinates(location):
    geo_url = f"{GEO_BASE_URL}/direct?q={location}&limit=1&appid={API_KEY}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()  # Raise error for bad status
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    except Exception as e:
        print(f"Geocode error for {location}: {e}")  # Debug print
    return None, None

def get_current_weather(location):
    lat, lon = get_coordinates(location)
    if lat is None:
        return {"error": "Invalid location"}
    weather_url = f"{WEATHER_BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()
        return {
            "location": data['name'],
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon']
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return {"error": "API error"}

def get_forecast(location):
    lat, lon = get_coordinates(location)
    if lat is None:
        return {"error": "Invalid location"}
    forecast_url = f"{WEATHER_BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(forecast_url)
        response.raise_for_status()
        data = response.json()
        forecast = []
        for item in data['list'][:5*8:8]:  # Daily forecast
            forecast.append({
                "date": item['dt_txt'],
                "temp": item['main']['temp'],
                "description": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon']
            })
        return forecast
    except Exception as e:
        print(f"Forecast API error: {e}")
        return {"error": "API error"}