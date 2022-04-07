import os
import requests


def twitter_trending():
    """Displays trending tags from twitter"""
    responses = requests.get("https://api.twitter.com/1.1/trends/place.json?id=1")
    responses_json = responses.json()
    
    print(responses_json)

twitter_trending()
