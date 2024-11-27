import os
import hashlib
import requests
import pyodbc
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
#global variables
limit=25
#looping through and incrementing the offset by 25 everytime we pull from the API
offset=0
#loading out keys from hidden file
public_key = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")
#creating a timestamp for authorization
timestamp = datetime.now()
timestamp_str = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
#hashing our calls made with our keys
hash_value = hashlib.md5((timestamp_str+private_key+public_key).encode()).hexdigest()
#create database connection
db_conn = os.getenv("DB_CONNECTION")

if db_conn:
    conn = pyodbc.connect(db_conn)
    cursor = conn.cursor()
    print("Successfully Connected")
else:
    raise EnvironmentError("Db conn not found")

#function to make our API call
def get_request(hash_value):
    #declaring api url
    base_api = "http://gateway.marvel.com/v1/public/characters"

    params = {
        "apikey": public_key,
        "ts": timestamp_str,
        "hash": hash_value,
        "offset": offset,
        "limit": limit
    }

    try:
        r = requests.get(base_api, params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return None
        
# making our api request
data = get_request(hash_value)

#manipulating our response data
#will constantly pull data
while True:
    #handling no data returned
    if data is None or not data['data']['results']:
        break

    characters = data['data']['results']

    for char in characters:
        name = char['name']
        #getting rid of the apostrophe
        name = name.replace("'",'')
        description = char['description']
        description = description.replace("'",'')
        resourceURI = char['resourceURI']
        thumbnail = char['thumbnail']['path']+'.'+char['thumbnail']['extension']
        comics = char['comics']['available']

        results_str = f"{name}**{description}**{resourceURI}**{thumbnail}**{comics}"

        print(results_str)
