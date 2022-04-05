import requests

def get_weather():
    """Displays a random fun fact"""
    responses = requests.get("https://api.aakhilv.me/fun/facts")
    responses_json = responses.json()
    return responses_json[0]

get_weather()