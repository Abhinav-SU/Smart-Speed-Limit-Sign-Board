import os
import requests
from sklearn.cluster import KMeans
import numpy as np
import tkinter as tk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variables
api_key = os.getenv('OPENWEATHER_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the OPENWEATHER_API_KEY environment variable.")

# Function to fetch weather data
def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data['cod'] != 200:
        print(f"Error fetching weather data: {weather_data['message']}")
        return None
    return weather_data

# Function to adjust speed limit based on weather classification
def adjust_speed_limit(weather_class):
    if weather_class == 0:
        return 60  # Clear weather
    elif weather_class == 1:
        return 45  # Moderate weather
    elif weather_class == 2:
        return 30  # Bad weather

# Function to display the speed limit using a GUI
def display_speed_limit(speed):
    window = tk.Tk()
    window.title("Smart Speed Limit Display")
    label = tk.Label(window, text=f"Speed Limit: {speed} km/h", font=("Arial", 40), padx=10, pady=10)
    label.pack(pady=20)
    window.mainloop()

# Main program
city = 'Syracuse'  # City for which weather data is to be fetched

# Step 1: Get real-time weather data
weather_data = get_weather_data(api_key, city)

if weather_data is not None:
    try:
        # Extract required data from the weather API response
        temp = weather_data['main']['temp']
        wind_speed = weather_data['wind']['speed']
        precipitation = weather_data['clouds']['all']
        weather_features = [temp, wind_speed, precipitation]

        # Step 2: Train K-Means for weather classification
        training_data = np.array([
            [30, 5, 0],  # Clear weather
            [25, 10, 20],  # Partly cloudy/moderate
            [20, 15, 50],  # Cloudy/rainy
            [15, 20, 80],  # Heavy rain/fog
            [10, 25, 100],  # Snow/fog
        ])
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(training_data)

        # Classify the current weather conditions
        current_weather = np.array([weather_features])
        classification = kmeans.predict(current_weather)

        # Step 3: Adjust speed limit based on classified weather
        current_class = classification[0]
        speed_limit = adjust_speed_limit(current_class)

        # Step 4: Display the adjusted speed limit
        display_speed_limit(speed_limit)
    
    except KeyError as e:
        print(f"Error extracting data from API response: {e}")
else:
    print("Weather data could not be fetched. Please check your API key or city name.")
