from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    temperatures = db.Column(db.Text, nullable=False)  # JSON string

def validate_dates(start, end):
    try:
        start_dt = datetime.strptime(start, '%Y-%m-%d').date()
        end_dt = datetime.strptime(end, '%Y-%m-%d').date()
        if start_dt > end_dt:
            raise ValueError("Start date after end date")
        return start_dt, end_dt
    except ValueError as e:
        print(f"Date validation error: {e}")  # Debug
        return None, None

def get_historical_temps(location, start, end):
    # Simulated (replace with real historical API call if needed)
    try:
        # Placeholder logic
        return {"temps": f"Simulated for {start} to {end}: 20-25°C"}
    except Exception as e:
        print(f"Historical temps error: {e}")
        return {}