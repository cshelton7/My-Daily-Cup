"""Nasa API"""
import os
import requests
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
NASA_KEY = os.getenv("NASA_KEY")


def nasa_picture():
    """Displays the daily picture from nasa"""
    responses = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}")
    responses_json = responses.json()
    picture = responses_json["hdurl"]
    explanation = responses_json["explanation"]

    nasa_result = {
        "picture": picture,
        "explanation": explanation,
    }

    return nasa_result
