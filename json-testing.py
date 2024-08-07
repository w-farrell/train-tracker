import requests

# Your API key
API_KEY = '32873f6871244285b19ea056b65a2d25'

def fetch_train_data():
    url = f"https://lapi.transitchicago.com/api/1.0/ttfollow.aspx?key={API_KEY}&rt=Red&outputType=JSON"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        print("Raw response:", response.text)  # Debug: Print raw response content
        data = response.json()  # Attempt to parse JSON
        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request error: {e}")
    except ValueError as e:
        print(f"JSON parsing error: {e}")

def get_train_locations():
    data = fetch_train_data()
    if data is None:
        print("No data returned or error occurred")
        return []
    return data.get('ctatt', {}).get('vehicle', [])

def main():
    trains = get_train_locations()
    if not trains:
        print("No train data available")
        return
    
    for train in trains:
        print(train)  # Print train data for debugging

if __name__ == "__main__":
    main()