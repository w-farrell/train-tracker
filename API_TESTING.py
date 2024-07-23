import requests
import time
from datetime import datetime, timedelta

API_KEY = '32873f6871244285b19ea056b65a2d25'
MAP_ID = '40380'



stations = [
    {'name': 'Howard', 'mapid': '40380'},
    {'name': 'Jarvis', 'mapid': '40520'},
    {'name': 'Morse', 'mapid': '41300'},
    {'name': 'Loyola', 'mapid': '41200'},
    {'name': 'Granville', 'mapid': '40760'},
    {'name': 'Thorndale', 'mapid': '41160'},
    {'name': 'Bryn Mawr', 'mapid': '40540'},
    {'name': 'Berwyn', 'mapid': '41380'},
    {'name': 'Argyle', 'mapid': '41240'},
    {'name': 'Lawrence', 'mapid': '40770'},
    {'name': 'Wilson', 'mapid': '40550'},
    {'name': 'Sheridan', 'mapid': '40080'},
    {'name': 'Addison', 'mapid': '41420'},
    {'name': 'Belmont', 'mapid': '41220'},
    {'name': 'Fullerton', 'mapid': '40650'},
    {'name': 'North/Clybourn', 'mapid': '40630'},
    {'name': 'Clark/Division', 'mapid': '40660'},
    {'name': 'Chicago', 'mapid': '40640'},
    {'name': 'Grand', 'mapid': '40490'},
    {'name': 'Lake', 'mapid': '41660'},
    {'name': 'Monroe', 'mapid': '41090'},
    {'name': 'Jackson', 'mapid': '40560'},
    {'name': 'Harrison', 'mapid': '40850'},
    {'name': 'Roosevelt', 'mapid': '41400'},
    {'name': 'Cermak-Chinatown', 'mapid': '41670'},
    {'name': 'Sox-35th', 'mapid': '41130'},
    {'name': '47th', 'mapid': '41230'},
    {'name': '51st', 'mapid': '40050'},
    {'name': 'Garfield', 'mapid': '40290'},
    {'name': '63rd', 'mapid': '40910'},
    {'name': '69th', 'mapid': '40990'},
    {'name': '79th', 'mapid': '40240'},
    {'name': '87th', 'mapid': '41450'},
    {'name': '95th/Dan Ryan', 'mapid': '40450'}
]

def check_trains():
    url_template = "https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&mapid={}&outputType=JSON"
    time_window = timedelta(minutes=2)  # Define a 2-minute window for accuracy

    for station in stations:
        url = url_template.format(API_KEY, station['mapid'])
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            train_at_station = False
            train_just_left = False
            
            if 'ctatt' in data and 'eta' in data['ctatt']:
                arrivals = data['ctatt']['eta']
                current_time = datetime.now()

                for arrival in arrivals:
                    arrival_time = datetime.strptime(arrival['arrT'], "%Y-%m-%dT%H:%M:%S")
                    time_diff = arrival_time - current_time
                    
                    if timedelta(0) <= time_diff <= time_window:
                        train_at_station = True
                    elif -time_window <= time_diff < timedelta(0):
                        train_just_left = True

            if train_at_station:
                print(f"Train is currently at {station['name']}")
            elif train_just_left:
                print(f"Train has just left {station['name']}")
            else:
                print(f"No train arrivals at {station['name']} at the moment.")
        else:
            print(f"Error fetching data for {station['name']}: {response.status_code}")

        # Sleep to avoid hitting the API rate limit
        time.sleep(1)


check_trains()

