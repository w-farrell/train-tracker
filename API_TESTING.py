import requests
from geopy.distance import great_circle
import time
from datetime import datetime, timedelta


API_KEY = '32873f6871244285b19ea056b65a2d25'




stations = [
    {'name': '47th', 'lat': 41.810318, 'lon': -87.63094, 'parent_stop_id': 41230},
    {'name': '63rd', 'lat': 41.780536, 'lon': -87.630952, 'parent_stop_id': 40910},
    {'name': '69th', 'lat': 41.768367, 'lon': -87.625724, 'parent_stop_id': 40990},
    {'name': '79th', 'lat': 41.750419, 'lon': -87.625112, 'parent_stop_id': 40240},
    {'name': '87th', 'lat': 41.735372, 'lon': -87.624717, 'parent_stop_id': 41430},
    {'name': '95th/Dan Ryan', 'lat': 41.722377, 'lon': -87.624342, 'parent_stop_id': 40450},
    {'name': 'Addison', 'lat': 41.947428, 'lon': -87.653626, 'parent_stop_id': 41420},
    {'name': 'Argyle', 'lat': 41.973453, 'lon': -87.65853, 'parent_stop_id': 41200},
    {'name': 'Belmont', 'lat': 41.939751, 'lon': -87.65338, 'parent_stop_id': 41320},
    {'name': 'Berwyn', 'lat': 41.977984, 'lon': -87.658668, 'parent_stop_id': 40340},
    {'name': 'Bryn Mawr', 'lat': 41.983504, 'lon': -87.65884, 'parent_stop_id': 41380},
    {'name': 'Cermak-Chinatown', 'lat': 41.853206, 'lon': -87.630968, 'parent_stop_id': 41000},
    {'name': 'Chicago', 'lat': 41.896671, 'lon': -87.628176, 'parent_stop_id': 41450},
    {'name': 'Clark/Division', 'lat': 41.90392, 'lon': -87.631412, 'parent_stop_id': 40630},
    {'name': 'Fullerton', 'lat': 41.925051, 'lon': -87.652866, 'parent_stop_id': 41220},
    {'name': 'Garfield', 'lat': 41.79542, 'lon': -87.631157, 'parent_stop_id': 41170},
    {'name': 'Grand', 'lat': 41.891665, 'lon': -87.628021, 'parent_stop_id': 40330},
    {'name': 'Granville', 'lat': 41.993664, 'lon': -87.659202, 'parent_stop_id': 40760},
    {'name': 'Harrison', 'lat': 41.874039, 'lon': -87.627479, 'parent_stop_id': 41490},
    {'name': 'Howard', 'lat': 42.019063, 'lon': -87.672892, 'parent_stop_id': 40900},
    {'name': 'Jackson', 'lat': 41.878153, 'lon': -87.627596, 'parent_stop_id': 40560},
    {'name': 'Jarvis', 'lat': 42.015876, 'lon': -87.669092, 'parent_stop_id': 41190},
    {'name': 'Lake', 'lat': 41.884809, 'lon': -87.627813, 'parent_stop_id': 41660},
    {'name': 'Lawrence', 'lat': 41.969139, 'lon': -87.658493, 'parent_stop_id': 40770},
    {'name': 'Loyola', 'lat': 42.001073, 'lon': -87.661061, 'parent_stop_id': 41300},
    {'name': 'Monroe', 'lat': 41.880745, 'lon': -87.627696, 'parent_stop_id': 41090},
    {'name': 'Morse', 'lat': 42.008362, 'lon': -87.665909, 'parent_stop_id': 40100},
    {'name': 'North/Clybourn', 'lat': 41.910655, 'lon': -87.649177, 'parent_stop_id': 40650},
    {'name': 'Roosevelt', 'lat': 41.867405, 'lon': -87.62659, 'parent_stop_id': 41400},
    {'name': 'Sheridan', 'lat': 41.953775, 'lon': -87.654929, 'parent_stop_id': 40080},
    {'name': 'Sox-35th', 'lat': 41.831191, 'lon': -87.630636, 'parent_stop_id': 40190},
    {'name': 'Thorndale', 'lat': 41.990259, 'lon': -87.659076, 'parent_stop_id': 40880},
    {'name': 'Wilson', 'lat': 41.964273, 'lon': -87.657588, 'parent_stop_id': 40540}
]

def get_train_locations():
    url = f"https://lapi.transitchicago.com/api/1.0/vehicle.aspx?key={API_KEY}&rt=Red&outputType=JSON"
    response = requests.get(url)
    data = response.json()
    return data.get('ctatt', {}).get('vehicle', [])

def find_nearest_station(train_lat, train_lon):
    min_distance = float('inf')
    nearest_station = None
    for station in stations:
        station_lat = station['lat']
        station_lon = station['lon']
        distance = great_circle((train_lat, train_lon), (station_lat, station_lon)).miles
        if distance < min_distance:
            min_distance = distance
            nearest_station = station
    return nearest_station

def display_train_locations():
    trains = get_train_locations()
    if not trains:
        print("No train data available")
        return

    for train in trains:
        try:
            train_lat = float(train['lat'])
            train_lon = float(train['lon'])
            nearest_station = find_nearest_station(train_lat, train_lon)
            if nearest_station:
                print(f"Train {train['rn']} is closest to station {nearest_station['name']} (Parent Stop ID: {nearest_station['parent_stop_id']})")
            else:
                print(f"Train {train['rn']} location is unknown")
        except (KeyError, ValueError) as e:
            print(f"Missing or invalid data in train entry: {train}")

# Run the function to display train locations
display_train_locations()