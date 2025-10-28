from flask import Flask, request, jsonify
from weather_api import get_current_weather, get_forecast

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

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

if __name__ == '__main__':
    app.run(debug=True)