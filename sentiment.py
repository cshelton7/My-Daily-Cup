import os
import paralleldots
from paralleldots import config, similarity, ner, taxonomy, sentiment
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# set the key
config.set_api_key(os.getenv("SENTIMENT_KEY"))

# get the emotion of the text
def get_emotion(entry):
    tones = []
    emotions = paralleldots.emotion(entry)

    # access data of each emotion
    emotions = emotions["emotion"].items()
    print(emotions)

    max = {"emotion": "None", "data": -1}  # hold highest emotion
    for data in emotions:
        # find maximum emotion value in case there is no value higher than 0.25
        if data[1] > max["data"]:
            max["emotion"] = data[0]
            max["data"] = data[1]
        # threshold for possible emotions conveyed
        if data[1] > 0.25:
            tones.append(data[0])
    # case to make sure a tone is shown
    if len(tones) == 0:
        try:
            tones.append(max["emotion"])
        except:
            tones.append("Bored")

    # correcting the 'fear' to 'fearful' for a better sound
    for i in range(len(tones)):
        if tones[i] == "Fear":
            tones[i] = "Fearful"

    return tones
