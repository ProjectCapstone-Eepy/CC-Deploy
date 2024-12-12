import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load Models
try:
    s_quality = joblib.load('/sleep_quality.pkl')
    s_duration = joblib.load('/sleep_duration.pkl')
    print("Models loaded successfully.")
except FileNotFoundError as e:
    print("Error: Model file not found. Ensure 'sleep_quality.pkl' and 'sleep_duration.pkl' exist.")
    s_quality = None
    s_duration = None
except Exception as e:
    print(f"Error loading models: {e}")
    s_quality = None
    s_duration = None

# Endpoint Default
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Sleep Analysis API!"})

# Endpoint Sleep Quality
@app.route('/quality', methods=['POST'])
def predict_quality():
    # Check if models are loaded
    if s_quality is None:
        return jsonify({"error": "Sleep quality model not loaded. Please check the server setup."}), 500

    # Get data from request
    try:
        data = request.json
        gender = float(data.get('gender'))  # Ensure numerical input
        age = float(data.get('age'))
        physical_activity = float(data.get('physical_activity'))
        stress_level = 10 - float(data.get('stress_level'))  # Invert stress level
        sleep_duration = float(data.get('sleep_duration')) * 30  # Scale sleep duration

        # Check if all fields are valid
        if not all(isinstance(x, (int, float)) for x in [gender, age, physical_activity, stress_level, sleep_duration]):
            return jsonify({"error": "Invalid input types. All inputs must be numeric."}), 400
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input format: {str(e)}"}), 400

    # Prepare input features
    input_features = np.array([[gender, age, physical_activity, stress_level, sleep_duration]], dtype='float32')

    try:
        prediction = s_quality.predict(input_features)
        prediction = float(prediction[0]) / 100  # Normalize prediction
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

# Endpoint Sleep Duration
@app.route('/duration', methods=['POST'])
def predict_duration():
    # Check if models are loaded
    if s_duration is None:
        return jsonify({"error": "Sleep duration model not loaded. Please check the server setup."}), 500

    # Get data from request
    try:
        data = request.json
        gender = float(data.get('gender'))  # Ensure numerical input
        age = float(data.get('age'))
        physical_activity = float(data.get('physical_activity'))
        stress_level = 10 - float(data.get('stress_level'))  # Invert stress level

        # Check if all fields are valid
        if not all(isinstance(x, (int, float)) for x in [gender, age, physical_activity, stress_level]):
            return jsonify({"error": "Invalid input types. All inputs must be numeric."}), 400
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input format: {str(e)}"}), 400

    # Prepare input features
    input_features = np.array([[gender, age, physical_activity, stress_level]], dtype='float32')

    try:
        prediction = s_duration.predict(input_features)
        prediction = float(prediction[0]) / 10  # Normalize prediction
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
