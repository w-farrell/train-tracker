import requests

# Your API key
API_KEY = '32873f6871244285b19ea056b65a2d25'


def fetch_stops():
    url = f"https://lapi.transitchicago.com/api/1.0/stops.aspx?key={API_KEY}&outputType=JSON"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def extract_stop_data():
    data = fetch_stops()
    if data is None:
        print("Error fetching data")
        return []

    # Check the structure of the response
    print("Response structure:", data)
    
    if 'ctatt' not in data or 'stop' not in data['ctatt']:
        print("Error parsing data")
        return []

    stops = []
    for stop in data['ctatt']['stop']:
        stop_id = stop.get('stop_id', 'Unknown')
        name = stop.get('name', 'Unknown')
        lat = stop.get('lat', 'Unknown')
        lon = stop.get('lon', 'Unknown')
        stops.append({'name': name, 'stop_id': stop_id, 'lat': lat, 'lon': lon})

    return stops

def print_stop_data():
    stops = extract_stop_data()
    if not stops:
        print("No stop data available")
        return

    print("Stops with stop_id and coordinates:")
    for stop in stops:
        print(f"Stop Name: {stop['name']}, Stop ID: {stop['stop_id']}, Latitude: {stop['lat']}, Longitude: {stop['lon']}")

# Run the function to print stop data
print_stop_data()