import requests
import sys

# Define the place or address you want to geocode
CITY = sys.argv[1]
# Replace 'YOUR_API_KEY' and 'YOUR_CITY' with your actual API key and city
API_KEY = 'bf6343dd97ac4f83b1602239230111'

url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    location = data['location']
    current = data['current']

    print(f"Weather in {location['name']}, {location['region']}, {location['country']}")
    print(f"Local Time: {location['localtime']}")
    print(f"Condition: {current['condition']['text']}")
    print(f"Temperature: {current['temp_c']}°C")
    print(f"Feels Like: {current['feelslike_c']}°C")
    print(f"Wind Speed: {current['wind_kph']} km/h")
else:
    print("Failed to fetch weather data")


# Replace 'YOUR_API_KEY' and 'YOUR_CITY' with your actual API key and city
API_KEY = '1b174bad0a1d248f9af22a5632dd9f63'

url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&cnt=7&appid={API_KEY}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print()
    print("Location:", CITY)
    print("{:<19} {:<25} {:<15} {:<15}".format("Date", "Condition", "Max Temp (°C)", "Min Temp (°C)"))
    
    for forecast in data['list']:
        date = forecast['dt_txt']
        condition = forecast['weather'][0]['description']
        max_temp = forecast['main']['temp_max'] - 273.15  # Convert temperature from Kelvin to Celsius
        min_temp = forecast['main']['temp_min'] - 273.15

        print("{:<19} {:<25} {:<15.2f} {:<15.2f}".format(date, condition, max_temp, min_temp))
else:
    print("Failed to fetch weather forecast")


# Make the Nominatim API request
base_url = "https://nominatim.openstreetmap.org/search"
params = {
    "q": CITY,
    "format": "json"
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    if data:
        first_result = data[0]
        latitude = first_result["lat"]
        longitude = first_result["lon"]
    else:
        print("No results found.")
else:
    print(f"Error: {response.status_code}")


# Construct the NWS API URL using the coordinates
url = f'https://api.weather.gov/points/{latitude},{longitude}'

# Send a request to obtain the grid point information
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Extract the location name
    location_name = data['properties']['relativeLocation']['properties']['city']
    
    # Print the location name
    print()
    print(f"Location Name: {location_name}")
    

    # Extract the grid point URL and forecast hourly URL
    grid_data_url = data['properties']['forecast']
    forecast_hourly_url = data['properties']['forecastHourly']

    # Fetch weather forecast data for the grid point
    forecast_response = requests.get(grid_data_url)
    
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        
        # Extract and print relevant weather information
        properties = forecast_data['properties']
        periods = properties['periods']
        print("{:<20} {:<15} {:<45} {:<20} {:<20} {:<15}".format("Time", "Temperature", "Conditions", "Wind Speed", "Humidity", "Dew Point"))
        for period in periods:
            time = period['name']
            temperature = f"{period['temperature']}°F"
            conditions = period['shortForecast']
            wind_speed = period['windSpeed']
            humidity = f"{period['relativeHumidity']['value']}%"
            dew_point = f"{round(period['dewpoint']['value'], 2)}°F"

            print("{:<20} {:<15} {:<45} {:<20} {:<20} {:<15}".format(time, temperature, conditions, wind_speed, humidity, dew_point))
    else:
        print("Failed to fetch weather forecast data")
else:
    print("Failed to fetch grid point data")
