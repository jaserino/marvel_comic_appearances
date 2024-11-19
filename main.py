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

#declaring api url
base_api = "http://gateway.marvel.com/v1/public/characters"

#creating params for api request
params = {
    "apikey": public_key,
    "ts": timestamp_str,
    "hash": hash_value,
    "limit": 50
}

# making our api request
response = requests.get(base_api, params=params)
# putting our response in readable format
data = response.json()
print(data)