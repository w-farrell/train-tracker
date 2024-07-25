import requests
import time
from datetime import datetime, timedelta

API_KEY = '32873f6871244285b19ea056b65a2d25'




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

def fetch_train_data():
    url = f"https://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={API_KEY}&rt=red&outputType=JSON"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_train_locations():
    data = fetch_train_data()
    if data is None or 'ctatt' not in data or 'route' not in data['ctatt']:
        print("Error fetching or parsing data")
        return []

    # Get the current time
    current_time = datetime.now()

    # List to store active train indicators
    active_trains = []

    # Extract train locations
    for route in data['ctatt']['route']:
        for train in route['train']:
            if 'arrT' not in train or 'nextStaId' not in train:
                print(f"Missing data in train entry: {train}")
                continue
            
            arrival_time = datetime.strptime(train['arrT'], "%Y-%m-%dT%H:%M:%S")
            station_id = train['nextStaId']

            # Check if the train is within a reasonable time frame
            if arrival_time >= current_time:
                active_trains.append(station_id)

    return active_trains

def display_train_locations(stations):
    active_trains = get_train_locations()
    
    # Limit the number of active indicators to the number of unique trains
    unique_stations = list(set(active_trains))
    
    print("Active train indicators:")
    for station_id in unique_stations:
        station_name = next((station['name'] for station in stations if station['mapid'] == station_id), f"Unknown {station_id}")
        print(f"Train at {station_name}")

# Run the function
display_train_locations(stations)