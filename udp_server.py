# udp_server.py
import socket
import requests
import time
import numpy as np
import pandas as pd
from joblib import load

# Configuration
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
API_KEY = "5b960025d119e828e0c78e7885176e72"  # Replace with your OpenWeatherMap API key

# Load ML model
model = load("weather_model.joblib")

# Load city list with coordinates
cities_df = pd.read_csv("indian_cities.csv")

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("[SERVER] Sending real-time weather predictions with coordinates...\n")

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url, timeout=3)
        data = res.json()
        if res.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            windspeed = data['wind']['speed']
            pressure = data['main']['pressure']
            return [temp, humidity, windspeed, pressure], None
        else:
            return None, f"Error: {data.get('message', 'unknown error')}"
    except Exception as e:
        return None, f"Exception: {str(e)}"

while True:
    for _, row in cities_df.iterrows():
        city = row['city']
        lat = row['latitude']
        lon = row['longitude']
        features, error = get_weather(lat, lon)
        if features:
            input_data = np.array([features])
            prediction = model.predict(input_data)[0]
            label = "🌧️ Rain Expected" if prediction == 1 else "☀️ No Rain"
            msg = f"{city}: {label} | Temp: {features[0]}°C | Humidity: {features[1]}%"
        else:
            msg = f"{city}: ⚠️ {error}"
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
        print("[SENT]", msg)
        time.sleep(1)


