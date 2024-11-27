import os
import hashlib
import requests

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

#loading out keys from hidden file
public_key = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")

#creating a timestamp for authorization
timestamp = datetime.now()
timestamp_str = timestamp.strftime("%m/%d/%Y, %H:%M:%S")

#hashing our calls made with our keys
hash_value = hashlib.md5((timestamp_str+private_key+public_key).encode()).hexdigest()


#function to make our API call


#declaring api url
base_api = "http://gateway.marvel.com/v1/public/characters"



#creating params for api request
params = {
    "apikey": public_key,
    "ts": timestamp_str,
    "hash": hash_value,
    "limit": 100
}

# making our api request
data = get_request(base_api, params=params)
# manipulating our response data
characters = data['data']['results']
for char in characters:
    name = char['name']
    #getting rid of the apostrophe
    name = name.replace("'",'')
    description = char['description']
    description = description.replace("'",'')
    resourceURI = char['resourceURI']
    thumbnail = char['thumbnail']['path']+'.'+['thumbnail']['extension']
    comics = char['comics']['available']

    results_str = f"{name}{description}{resourceURI}{thumbnail}{comics}"

    print(results_str)

# putting our response in readable format
# data = response.json()
# print(data)