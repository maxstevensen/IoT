import os
import time
from datetime import timedelta, datetime

import requests
import json

import pandas as pd

API_KEY = "9f6c9e60-2e6c-4773-bc16-24369834f0e8"
BASE = "http://datapoint.metoffice.gov.uk/public/data/"

DATATYPE = "json"
LOCATION = "3590"  # Wattisham (closest observation station to home address)
RESOURCE = f"val/wxobs/all/{DATATYPE}/{LOCATION}"

ENDPOINT = BASE + RESOURCE + f"?res=hourly&key={API_KEY}"

FILENAME = "observation_data.csv"
DATE_FMT = "%Y-%m-%dT%H:%M:%SZ"
#%%
os.chdir('##') #I have removed this for privacy
#%%

def get_data(endpoint):
    print("GET", endpoint)
    json_data = requests.get(endpoint).text
    data = json.loads(json_data)['SiteRep']
    return data


def update_data_file():
    data = get_data(ENDPOINT)

    frame_data = {}
    periods = data["DV"]["Location"]["Period"]
    for period in periods:
        base_dt = datetime.strptime(period["value"][:-1], "%Y-%m-%d")
        for rep in period["Rep"]:
            minutes_after_midnight = rep["$"]
            del rep["$"]
            dt = base_dt + timedelta(minutes=int(minutes_after_midnight))
            frame_data[dt] = rep

    df = pd.DataFrame(frame_data).transpose()
    if os.path.exists(FILENAME):
        read = pd.read_csv(FILENAME, index_col=0)
        df = pd.concat([read, df])

    df.to_csv(FILENAME)
    print("Data Saved at", datetime.now().strftime(DATE_FMT))


while True:
    # Get last 24 hours of data and merge it with the data we already have
    update_data_file()
    # Sleep for a day
    day = 86400
    time.sleep(day)
