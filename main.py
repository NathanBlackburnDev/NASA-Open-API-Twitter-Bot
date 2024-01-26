"""
Title: David Goggins Twitter bot
Author: Nathan Blackburn <nblackburndeveloper@icloud.com>
"""

import tweepy
import time
from dotenv import load_dotenv
import os
from streamlistener import Stream

# Assign enviroment variables
load_dotenv("keys.env")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

# Instantiate Oauth handler and set access token
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Instantiate API object
twt_api = tweepy.API(auth)

def main():
    # Test credential validation
    # https://python.plainenglish.io/how-to-create-a-twitter-retweet-bot-using-python-e2cac0f2cab7
    try:
        print(f"{twt_api.verify_credentials()}\n")
        print("Successfully logged in")
    except tweepy.TweepError as e:
        print(e)
    except Exception as e:
        print(e)

    listener = Stream(twt_api)
    stream_retwt = tweepy.Stream(auth=twt_api.auth, listener=listener)

    stream_retwt.filter(track=["from:davidgoggins"])

if __name__ == "__main__":
    main()


