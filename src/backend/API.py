import requests
import sys
from datetime import datetime, timedelta


class current_Weather:
    def __init__(self, location):
        self.API_Key = 'bf6343dd97ac4f83b1602239230111'

        self.url = f'http://api.weatherapi.com/v1/current.json?key={self.API_Key}&q={location}'
        self.response = requests.get(self.url)

    def print_weather(self):
        if self.response.status_code == 200:
            data = self.response.json()
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


class geo_Location: 
    def __init__(self, location):
        self.url = "https://nominatim.openstreetmap.org/search"
        self.params = {
            "q": location,
            "format": "json"
        }
        self.lattitude = None
        self.longitude = None

        self.response = requests.get(self.url, params=self.params)

        if self.response.status_code == 200:
            data = self.response.json()
            if data:
                first_result = data[0]
                self.lattitude = first_result["lat"]
                self.longitude = first_result["lon"]

class NWS_API:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.grid_x = None
        self.grid_y = None
        self.grid_ID = None
        self.url = f'https://api.weather.gov/points/{self.latitude},{self.longitude}'
        response = requests.get(self.url)

        if response.status_code == 200:
            nws_data = response.json()
            self.grid_ID = nws_data.get('properties', {}).get('gridId')
            self.grid_x = nws_data.get('properties', {}).get('gridX')
            self.grid_y = nws_data.get('properties', {}).get('gridY')


class weekly_Forcast:
    def __init__(self, lattitude, longitude):
        self.lattitude = lattitude
        self.longitude = longitude
        self.url = f'https://api.weather.gov/points/{self.lattitude},{self.longitude}'


    def print_weather(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            data = response.json()
            
            # Extract the location name
            location_name = data['properties']['relativeLocation']['properties']['city']
            
            # Print the location name
            print()
            print(f"Location Name: {location_name}")
            

            # Extract the grid point URL and forecast hourly URL
            grid_data_url = data['properties']['forecast']

            # Fetch weather forecast data for the grid point
            forecast_response = requests.get(grid_data_url)
            
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                
                # Extract and print relevant weather information
                properties = forecast_data['properties']
                periods = properties['periods']
                print("{:<20} {:<15} {:<45} {:<20} {:<20} {:<20} {:<15}".format("Time", "Temperature", "Conditions", "Wind Speed", "Wind Direction", "Humidity", "Dew Point"))
                for period in periods:
                    time = period['name']
                    temperature = f"{period['temperature']}°F"
                    conditions = period['shortForecast']
                    wind_speed = period['windSpeed']
                    wind_direction = period['windDirection']
                    humidity = f"{period['relativeHumidity']['value']}%"
                    dew_point = f"{round(period['dewpoint']['value'], 2)}°C"

                    print("{:<20} {:<15} {:<45} {:<20} {:<20} {:<20} {:<15}".format(time, temperature, conditions, wind_speed, wind_direction, humidity, dew_point))
            else:
                print("Failed to fetch weather forecast data")
        else:
            print("Failed to fetch grid point data")

class hourly_Forcast:
    def __init__(self, grid_x, grid_y, grid_ID):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_ID = grid_ID
        self.url = f'https://api.weather.gov/gridpoints/{self.grid_ID}/{self.grid_x},{self.grid_y}/forecast/hourly'

    def print_weather(self):
        forecast_response = requests.get(self.url)
        
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            
            # Extract and print relevant weather information
            properties = forecast_data['properties']
            periods = properties['periods']
            print()
            print("{:<20} {:<15} {:<45} {:<20} {:<20} {:<20} {:<15}".format("Time", "Temperature", "Conditions", "Wind Speed", "Wind Direction", "Humidity", "Dew Point"))
            for period in periods:
                time_string = period['startTime']
                time_convert = datetime.fromisoformat(time_string)
                time = time_convert.strftime("%m/%d/%y %H:%M")
                temperature = f"{period['temperature']}°F"
                conditions = period['shortForecast']
                wind_speed = period['windSpeed']
                wind_direction = period['windDirection']
                humidity = f"{period['relativeHumidity']['value']}%"
                dew_point = f"{round(period['dewpoint']['value'], 2)}°C"

                print("{:<20} {:<15} {:<45} {:<20} {:<20} {:<20} {:<15}".format(time, temperature, conditions, wind_speed, wind_direction, humidity, dew_point))
        else:
            print("Failed to fetch weather forecast data")

        


location = sys.argv[1]
weather = current_Weather(location)
weather.print_weather()
geolocation = geo_Location(location)
print(geolocation.lattitude, geolocation.longitude)
forecast = weekly_Forcast(geolocation.lattitude, geolocation.longitude)
forecast.print_weather()
API = NWS_API(geolocation.lattitude, geolocation.longitude)
hourly = hourly_Forcast(API.grid_x, API.grid_y, API.grid_ID)
hourly.print_weather()
        