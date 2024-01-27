import tweepy
from dotenv import load_dotenv
import os

load_dotenv("keys.env")

# Set enviroment variables
consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("access_token")
access_token_secret = os.environ.get("access_token_secret")
bearer_token = os.environ.get("bearer_token")

# Authenticate API
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

response = client.create_tweet(
    text="Whos gonna carry the boats and the logs ?!"
)

print(f"https://twitter.com/user/status/{response.data['id']}")