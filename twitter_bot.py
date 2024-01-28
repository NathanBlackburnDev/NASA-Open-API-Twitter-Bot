"""
Title: NASA Open API Twitter bot
Author: Nathan Blackburn <nblackburndeveloper@icloud.com>
Description: Twitter bot that uses some of the NASA Open APIs that tweets daily using a cron job
"""
import sys
import tweepy
from dotenv import load_dotenv
import os
from apod_api.apod_parser import apod_object_parser
from datetime import datetime

# Set enviroment variables
load_dotenv("keys.env")
consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("access_token")
access_token_secret = os.environ.get("access_token_secret")
bearer_token = os.environ.get("bearer_token")

# Authenticate API v2 for tweet creation endpoints
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Authenticate API v1 for media endpoints
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# NASA APOD API setup
# https://github.com/nasa/apod-api/blob/master/apod_parser/apod_parser_readme.md
apod_response = apod_object_parser.get_data(os.environ.get("nasa_key"))
apod_date = apod_object_parser.get_date(apod_response)
apod_title = apod_object_parser.get_title(apod_response)
apod_explanation = apod_object_parser.get_explaination(apod_response)
apod_url = apod_object_parser.get_url(apod_response)
apod_object_parser.download_image(apod_url, apod_date)

# Tweet APOD
# https://docs.tweepy.org/en/stable/client.html#tweets
cur_date = datetime.today().strftime("%Y-%m-%d")
# https://www.youtube.com/watch?v=r9DzYE5UD6M
media_id = api.media_upload(filename=f"{cur_date}.jpg").media_id_string
response1 = client.create_tweet(
    text=apod_title,
    media_ids=[media_id]
)

# Print response code of tweet
print(f"Tweet response: https://twitter.com/user/status/{response1.data['id']}")