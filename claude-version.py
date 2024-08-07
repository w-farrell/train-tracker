import requests
import json

def get_train_locations(api_key, route_id='red'):
    url = f"http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={api_key}&rt={route_id}&outputType=JSON"
    
    response = requests.get(url)
    data = json.loads(response.text)
    
    if 'ctatt' in data and 'route' in data['ctatt']:
        trains = data['ctatt']['route'][0]['train']
        return trains
    else:
        return []

def process_train_data(trains):
    northbound_trains = {}
    southbound_trains = {}
    
    for train in trains:
        train_id = train['rn']  # Run number (train ID)
        next_station = train['nextStaNm']
        direction = train['trDr']  # '1' for North, '5' for South
        is_approaching = train['isApp'] == "1"
        is_delayed = train['isDly'] == "1"

        # Determine which station to associate with this train
        if is_delayed or is_approaching:
            station = next_station  # If delayed or approaching, associate with the next station
        else:
            # If in transit, use previous station if available, otherwise use next station
            station = train.get('prevStaNm', next_station)

        # Add the train to the appropriate direction dictionary
        if direction == "1":
            northbound_trains[train_id] = station
        elif direction == "5":
            southbound_trains[train_id] = station
    
    return northbound_trains, southbound_trains

def display_train_locations(northbound_trains, southbound_trains):
    print("Northbound trains:")
    for train_id, station in northbound_trains.items():
        print(f"Train {train_id} at or approaching {station}")
    
    print("\nSouthbound trains:")
    for train_id, station in southbound_trains.items():
        print(f"Train {train_id} at or approaching {station}")

def perform_consistency_checks(northbound_trains, southbound_trains):
    all_stations = set(northbound_trains.values()) | set(southbound_trains.values())
    
    # Check for duplicate train IDs
    all_train_ids = list(northbound_trains.keys()) + list(southbound_trains.keys())
    if len(all_train_ids) != len(set(all_train_ids)):
        print("Warning: Duplicate train IDs detected")
    
    # Check for unexpected stations
    expected_stations = {"Howard", "Jarvis", "Morse", "Loyola", "Granville", "Thorndale", "Bryn Mawr", "Berwyn", "Argyle", "Lawrence", "Wilson", "Sheridan", "Addison", "Belmont", "Fullerton", "North/Clybourn", "Clark/Division", "Chicago", "Grand", "Lake", "Monroe", "Jackson", "Harrison", "Roosevelt", "Cermak-Chinatown", "Sox-35th", "47th", "Garfield", "63rd", "69th", "79th", "87th", "95th/Dan Ryan"}
    unexpected_stations = all_stations - expected_stations
    if unexpected_stations:
        print(f"Warning: Unexpected stations detected: {unexpected_stations}")
    
    print(f"Total trains: {len(all_train_ids)}")
    print(f"Northbound trains: {len(northbound_trains)}")
    print(f"Southbound trains: {len(southbound_trains)}")

# Call this function in your main loop after processing train data

def main():
    api_key = "32873f6871244285b19ea056b65a2d25"  # Replace with your actual API key
    
    trains = get_train_locations(api_key)
    
    if trains:
        northbound_trains, southbound_trains = process_train_data(trains)
        perform_consistency_checks(northbound_trains, southbound_trains)
        display_train_locations(northbound_trains, southbound_trains)
        # Here you would call a function to control your LEDs
        # control_leds(northbound_trains, southbound_trains)
    else:
        print("No train data available or API error occurred.")

if __name__ == "__main__":
    main()