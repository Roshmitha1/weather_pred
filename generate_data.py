# generate_data.py
import pandas as pd
import numpy as np

def generate_weather_data(num_samples=100):
    np.random.seed(42)
    data = {
        'Temperature': np.random.uniform(20, 40, num_samples),
        'Humidity': np.random.uniform(30, 90, num_samples),
        'WindSpeed': np.random.uniform(0, 20, num_samples),
        'Pressure': np.random.uniform(950, 1050, num_samples),
        'Rain': np.random.randint(0, 2, num_samples)  # Binary classification: 0 = No, 1 = Yes
    }
    df = pd.DataFrame(data)
    df.to_csv('weather_data.csv', index=False)
    print(f"[+] Generated {num_samples} rows of weather data.")

if __name__ == "__main__":
    generate_weather_data()

