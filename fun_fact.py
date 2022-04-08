"""Fun Fact API retreives fun facts from host"""
import requests


def fun_fact():
    """Displays a random fun fact"""
    responses = requests.get("https://api.aakhilv.me/fun/facts")
    responses_json = responses.json()
    return responses_json[0]
