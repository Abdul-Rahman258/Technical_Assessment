from flask import Flask, request, jsonify
from weather_api import get_current_weather, get_forecast, get_coordinates
from database import db, WeatherRecord, validate_dates, get_historical_temps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

try:
    with app.app_context():
        db.create_all()
    print("DB initialized successfully")  # Debug print on start
except Exception as e:
    print(f"DB init error: {e}")  # Catch DB crashes

@app.route('/weather', methods=['GET'])
def weather():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location required"}), 400
    return jsonify(get_current_weather(location))

@app.route('/forecast', methods=['GET'])
def forecast():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location required"}), 400
    return jsonify(get_forecast(location))

@app.route('/create', methods=['POST'])
def create():
    try:
        data = request.json
        location = data.get('location')
        start = data.get('start_date')
        end = data.get('end_date')
        start_dt, end_dt = validate_dates(start, end)
        if not start_dt or not location:
            return jsonify({"error": "Invalid input"}), 400
        lat, lon = get_coordinates(location)
        if lat is None:
            return jsonify({"error": "Invalid location"}), 400
        temps = get_historical_temps(location, start, end)
        record = WeatherRecord(location=location, start_date=start_dt, end_date=end_dt, temperatures=str(temps))
        db.session.add(record)
        db.session.commit()
        return jsonify({"id": record.id})
    except Exception as e:
        print(f"Create error: {e}")  # Debug
        return jsonify({"error": "Server error"}), 500

@app.route('/read', methods=['GET'])
def read():
    try:
        records = WeatherRecord.query.all()
        return jsonify([{"id": r.id, "location": r.location, "start": str(r.start_date), "end": str(r.end_date), "temps": r.temperatures} for r in records])
    except Exception as e:
        print(f"Read error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    try:
        record = WeatherRecord.query.get(id)
        if not record:
            return jsonify({"error": "Not found"}), 404
        data = request.json
        if 'location' in data:
            lat, lon = get_coordinates(data['location'])
            if lat is None:
                return jsonify({"error": "Invalid location"}), 400
            record.location = data['location']
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(f"Update error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        record = WeatherRecord.query.get(id)
        if not record:
            return jsonify({"error": "Not found"}), 404
        db.session.delete(record)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(f"Delete error: {e}")
        return jsonify({"error": "Server error"}), 500

# Optional routes (comment out if not needed)
#@app.route('/youtube', methods=['GET'])
#def youtube():
#    location = request.args.get('location')
#    return jsonify({"videos": ["https://youtube.com/example"]})  # Simulated

@app.route('/export/csv', methods=['GET'])
def export_csv():
    try:
        records = WeatherRecord.query.all()
        csv = "id,location,start,end,temps\n"
        for r in records:
            csv += f"{r.id},{r.location},{r.start_date},{r.end_date},{r.temperatures}\n"
        return csv, 200, {'Content-Type': 'text/csv'}
    except Exception as e:
        print(f"Export error: {e}")
        return "Error exporting", 500

if __name__ == '__main__':
    app.run(debug=True)