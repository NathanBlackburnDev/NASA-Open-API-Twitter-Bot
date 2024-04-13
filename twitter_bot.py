import sys
import tweepy
from dotenv import load_dotenv
import os
from apod_api.apod_parser import apod_object_parser
from datetime import datetime
import requests
import json
from pprint import pprint
from urllib.request import urlretrieve

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
cur_date = datetime.today().strftime("%Y-%m-%d")
# https://www.youtube.com/watch?v=r9DzYE5UD6M
media_id = api.media_upload(filename=f"{cur_date}.jpg").media_id_string
response1 = client.create_tweet(
    text="NASA Astronomy Picture of The Day - " + apod_date + "\n" + apod_title + "\n",
    media_ids=[media_id]
)

# https://holypython.com/api-2-mars-weather
# Retrieve InSight Weather data (InSight is retired)
def marsweather():
    api_url = r"https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0"
    data = requests.get(api_url)
    jso = json.loads(data.text)
    # If no sensors with data for any Sols
    if not jso["sol_keys"]:
        return "No Sols"
    else:
        for i in jso:
            at = jso[i]["AT"] + "\n"                                                       # per-Sol atmospheric temperature sensor summary data
            hws = jso[i]["HWS"] + "\n"                                                     # per-Sol horizontal wind speed sensor summary data
            pre = jso[i]["PRE"] + "\n"                                                     # per-Sol atmospheric pressure sensor summary data
            wd = jso[i]["WD"] + "\n"                                                       # per-Sol wind direction sensor summary data
            first_ut = jso[i]["First_UTC"]                                                 # UTC range; season
            return at, hws, pre, wd, first_ut, jso[i]
        
# Retireve EPIC data
# https://medium.com/daily-python/consuming-nasa-api-using-python-part-1-daily-python-17-4ce104fa47ab
def epic_data():
    epic_url = "https://epic.gsfc.nasa.gov/api/natural"
    params = {"nasa_key":os.environ.get("nasa_key")}
    epic_response = requests.get(epic_url, params=params).json()
    caption = epic_response[0]["caption"]
    date = epic_response[0]["date"]
    identifier = epic_response[0]["identifier"]
    image = epic_response[0]["image"]
    dscovr_j2000_pos = epic_response[0]["dscovr_j2000_position"]
    lunar_j2000_pos = epic_response[0]["lunar_j2000_position"]
    sun_j2000_pos = epic_response[0]["sun_j2000_position"]
    centroid_cords = epic_response[0]["centroid_coordinates"]
    return [caption, date, identifier, image, lunar_j2000_pos, sun_j2000_pos, centroid_cords, dscovr_j2000_pos]

# Download the EPIC image
def fetch_epic_img():
    data_arr = epic_data()
    date_obj = datetime.strptime(data_arr[1], '%Y-%m-%d %H:%M:%S')
    img_id = data_arr[3]
    epic_url = f"https://epic.gsfc.nasa.gov/archive/natural/{date_obj.strftime("%Y")}/{date_obj.strftime("%m")}/{date_obj.strftime("%d")}/png/{img_id}.png"
    # https://stackoverflow.com/questions/30229231/python-save-image-from-url
    img_data = requests.get(epic_url).content
    with open('epic_img.jpg', 'wb') as handler:
        handler.write(img_data)

fetch_epic_img()
epic_arr = epic_data()

# EPIC Tweet
media_id_epic = api.media_upload(filename="epic_img.jpg").media_id_string
response2 = client.create_tweet(
    text=f"{epic_arr[0]} at {epic_arr[1]}\nLongitue: {epic_arr[-2]["lon"]} | Latitude: {epic_arr[-2]["lat"]}\nPosition of satellite (X, Y, Z): {epic_arr[-1]["x"]}, {epic_arr[-1]["y"]}, {epic_arr[-1]["z"]}",
    media_ids=[media_id_epic]
)

# Get Mars Rover data
def mars_rover():
    mars_url = r'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key=' + os.environ.get("nasa_key")
    mars_data = requests.get(mars_url)
    mars_jso = json.loads(mars_data.text)
    name = mars_jso["latest_photos"][0]["camera"]["full_name"]
    earth_date = mars_jso["latest_photos"][0]["earth_date"]
    mars_img_url = mars_jso["latest_photos"][0]["img_src"]
    sol_date = mars_jso["latest_photos"][0]["sol"]
    rover = mars_jso["latest_photos"][0]["rover"]["name"]
    mars_img = requests.get(mars_img_url).content
    with open('mars_img.jpg', 'wb') as handler:
        handler.write(mars_img)

    return [name, earth_date, sol_date, rover]

mars_results = mars_rover()

# Tweet Mars Rover
media_id_rover = api.media_upload(filename="mars_img.jpg").media_id_string
response3 = client.create_tweet(
    text=f"{mars_results[0]} on {mars_results[1]} (Sol: {mars_results[2]}), taken by {mars_results[3]}",
    media_ids=[media_id_rover]
)

# APOD response
print(f"Tweet response: https://twitter.com/user/status/{response1.data['id']}")

# EPIC response
print(f"Tweet response: https://twitter.com/user/status/{response2.data['id']}")

# Mars rover response
print(f"Tweet response: https://twitter.com/user/status/{response3.data['id']}")
