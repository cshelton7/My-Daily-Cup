# import the module
import os
import tweepy
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

def get_trends():
    # assign the values accordingly
    consumer_key = os.getenv("TWITTER_KEY")
    consumer_secret = os.getenv("TWITTER_SECRET")

    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # getting authorization for our keys
    api = tweepy.API(auth)

    # WOEID of the United States
    woeid = 23424977

    # fetching the trends
    trends = api.get_place_trends(id=woeid)

    # This will find the top 5 trending topics
    trending_topics = []
    i = 0
    for value in trends:
        for trend in value["trends"]:
            trending_topics.append(trend["name"])
            i += 1
            if i >= 5:
                break
    return trending_topics