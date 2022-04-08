"""
Openweather API to display current weather information
"""
import os
import requests
from dotenv import find_dotenv, load_dotenv



load_dotenv(find_dotenv())

# Hardcoded the lat/lon until I can figure out best way to implement geolocation feature
LAT = 33.7499
LON = 84.4000
OPENWEATHER_URL = (
    f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid="
)

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")


def get_weather():
    """Recieves responses from openweather API for temperture, city and current weather."""
    responses = requests.get(OPENWEATHER_URL + OPENWEATHER_KEY)
    responses_json = responses.json()
    weather = responses_json["weather"][0]["main"]
    city = responses_json["name"]
    country = responses_json["sys"]["country"]
    kelvin = responses_json["main"]["temp"]
    fahrenheit = str(round(kelvin * 1.8 - 459.67, 2)) + " F°"
    weather_info = {
        "weather": weather,
        "city": city,
        "fahrenheit": fahrenheit,
        "country": country,
    }
    return weather_info
