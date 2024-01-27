"""
Title: David Goggins Twitter bot
Author: Nathan Blackburn <nblackburndeveloper@icloud.com>
"""

from requests_oauthlib import OAuth1Session
import os
import json

# Set enviroment variables
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

payload = {"text": "They dont know me son!"}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Manage-Tweets/create_tweet.py
try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print("Error with either consumer_key or consumer_secret")

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print(f"Got OAuth token {resource_owner_key}")

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print(f"Authorize here: {authorization_url}")
verifier = input("Enter PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret
)

# Make the request
response = oauth.post(
    'https://api.twitter.com/2/tweets',
    json=payload
)

if response.status_code != 201:
    raise Exception(f"Request returned an error: {response.status_code} {response.text}")

print(f"Response code {response.status_code}")

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))

