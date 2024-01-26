"""
Logic for handaling each tweet
"""

import tweepy

# https://python.plainenglish.io/how-to-create-a-twitter-retweet-bot-using-python-e2cac0f2cab7
class Stream(tweepy.StreamingClient):
    def __init__(self, api):
        self.api = api
        self.me = api.verify_credentials()

    # If tweet successful
    def on_status(self, tweet):
        # If bot tries to retweet replies or itself
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        
        # If bot has not retweeted yet
        if not tweet.retweeted:
            try:
                tweet.retweet()
                print("Retweeted successfully")
            except Exception as e:
                print(e)

        # If bot has not favorited tweet yet
        if not tweet.favorited():
            try:
                tweet.favorite()
                print("Favorited successfully")
            except Exception as e:
                print(e)

    # If tweet encounters an error
    def on_error(self, status):
        print(f"Error while retweeting: {status}")
