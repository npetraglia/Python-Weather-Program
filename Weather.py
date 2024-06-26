import requests
from geopy.adapters import GeocoderTimedOut
from geopy.geocoders import Nominatim

def get_coordinates(zip_code):
    geolocator = Nominatim(user_agent="Your Weather App")  
    try:
        location = geolocator.geocode(zip_code + ", USA")
        return location.latitude, location.longitude
    except GeocoderTimedOut as e:
        print(f"Geocoding error: {e}")
        return None

def get_weather(api_key, location, units="imperial"):
    base_url = "https://api.tomorrow.io/v4/timelines"
    params = {
        'location': location,  
        'fields': ['temperature', 'weatherCode'],  # Include weatherCode
        'timesteps': '1h',
        'units': units,
        'apikey': api_key   
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}") 
        return None  

def get_hourly_forecast(api_key, coordinates, units="imperial"):
    base_url = "https://api.tomorrow.io/v4/timelines"
    lat, lon = coordinates
    params = {
        'location': f"{lat},{lon}",
        'fields': 'temperature',
        'timesteps': '1h',
        'units': units,
        'apikey': api_key 
    }
    try:
        response = requests.get(base_url, params=params) 
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}") 
        return None  

if __name__ == "__main__":
    api_key = "r6sDaFLv3smSv12PsWFeNvqPChrFgbti"  
    zip_code = input("Enter a ZIP code: ")

    coordinates = get_coordinates(zip_code)
    if coordinates:
        # Get hourly forecast 
        hourly_data = get_hourly_forecast(api_key, coordinates)
        if hourly_data:
            hourly_forecasts = [] 
            for item in hourly_data['data']['timelines'][0]['intervals'][:12]:
                time = item['startTime']
                temperature = round(item['values']['temperature'])
                hourly_forecasts.append(f"{time}: {temperature}°F")
            print(f"Hourly weather forecast for ZIP code {zip_code}:\n" + "\n".join(hourly_forecasts))

        weather_descriptions = {
        1000: "Sunny",
        1100: "Mostly Sunny",
        1101: "Partly Cloudy",
        1102: "Mostly Cloudy",
        1103: "Cloudy",
        2100: "Light Fog",
        2000: "Fog",
        4000: "Drizzle",
        4001: "Light Rain",
        4002: "Rain",
        4003: "Heavy Rain",
        4004: "Light Snow",
        4005: "Snow",
        }
        # Fetch basic weather data
        weather_data = get_weather(api_key, f"{coordinates[0]},{coordinates[1]}", units="imperial")
        if weather_data: 
            current_temp = round(weather_data['data']['timelines'][0]['intervals'][0]['values']['temperature'])
            current_conditions = weather_data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
            current_code = weather_data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
            current_description = weather_descriptions.get(current_code, "Unknown")
            print(f"\nCurrent Temperature: {current_temp}°F ({current_description})") 
    else:
        print("Invalid ZIP code.")

