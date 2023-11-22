import requests
from datetime import datetime


class current_Weather:
    def __init__(self, location):
        self.API_Key = 'bf6343dd97ac4f83b1602239230111'

        self.url = f'http://api.weatherapi.com/v1/current.json?key={self.API_Key}&q={location}'
        self.response = requests.get(self.url)
        self.data = {}

    def fetch_weather_data(self):
        if self.response.status_code == 200:
            data = self.response.json()
            location = data['location']
            current = data['current']

            self.data = {
                'Location': f"{location['name']}, {location['region']}, {location['country']}",
                'Local Time': location['localtime'],
                'Condition': current.get('condition', {}).get('text'),
                'Temperature': int(current.get('temp_c')),
                'Feels Like': int(current.get('feelslike_c')),
                'Wind Speed': int(current.get('wind_mph'))
            }

    def get_weather_data(self):
        return self.data


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
        self.data = {}


    def fetch_weather_data(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            data = response.json()
            
            # Extract the location name
            location_name = data['properties']['relativeLocation']['properties']['city']
            

            # Extract the grid point URL and forecast hourly URL
            grid_data_url = data['properties']['forecast']

            # Fetch weather forecast data for the grid point
            forecast_response = requests.get(grid_data_url)
            
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                
                properties = forecast_data['properties']
                periods = properties['periods']
                
                for period in periods:
                    time = period.get('name', None)
                    temperature = int(f"{period.get('temperature', None)}")
                    conditions = period.get('shortForecast', None)
                    wind_speed_str = period.get('windSpeed', None)
                    wind_speed = int(wind_speed_str.split(' ')[0]) if wind_speed_str else None
                    wind_direction = period.get('windDirection', None)
                    humidity = f"{period['relativeHumidity']['value']}%" if 'relativeHumidity' in period else None
                    dew_point_c = f"{round(period['dewpoint']['value'], 2)}" if 'dewpoint' in period else None
                    dew_point = None
                    if dew_point_c is not None:
                        dew_point = round((float(dew_point_c) * 9/5) + 32, 2)

                    # Organize data by type, initializing with None
                    self.data.setdefault('Time', []).append(time)
                    self.data.setdefault('Temperature', []).append(temperature)
                    self.data.setdefault('Conditions', []).append(conditions)
                    self.data.setdefault('Wind Speed', []).append(wind_speed)
                    self.data.setdefault('Wind Direction', []).append(wind_direction)
                    self.data.setdefault('Humidity', []).append(humidity)
                    self.data.setdefault('Dew Point', []).append(dew_point)

    def get_weather_data(self):
        return self.data

class hourly_Forcast:
    def __init__(self, grid_x, grid_y, grid_ID):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_ID = grid_ID
        self.url = f'https://api.weather.gov/gridpoints/{self.grid_ID}/{self.grid_x},{self.grid_y}/forecast/hourly'
        self.data = {}

    def fetch_weather_data(self):
        forecast_response = requests.get(self.url)
        
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            properties = forecast_data['properties']
            periods = properties['periods']

            for period in periods:
                time_string = period['startTime']
                time_convert = datetime.fromisoformat(time_string)
                time = time_convert.strftime("%m/%d/%y %H:%M")
                temperature = int(f"{period.get('temperature', None)}")
                conditions = period.get('shortForecast', None)
                wind_speed_str = period.get('windSpeed', None)
                wind_speed = int(wind_speed_str.split(' ')[0]) if wind_speed_str else None
                wind_direction = period.get('windDirection', None)
                humidity = f"{period['relativeHumidity']['value']}%" if 'relativeHumidity' in period else None
                dew_point_c = f"{round(period['dewpoint']['value'], 2)}" if 'dewpoint' in period else None
                dew_point = None
                if dew_point_c is not None:
                    dew_point = round((float(dew_point_c) * 9/5) + 32, 2)

                # Organize data by type, initializing with None
                self.data.setdefault('Time', []).append(time)
                self.data.setdefault('Temperature', []).append(temperature)
                self.data.setdefault('Conditions', []).append(conditions)
                self.data.setdefault('Wind Speed', []).append(wind_speed)
                self.data.setdefault('Wind Direction', []).append(wind_direction)
                self.data.setdefault('Humidity', []).append(humidity)
                self.data.setdefault('Dew Point', []).append(dew_point)

    def get_weather_data(self):
        return self.data

class initialize:
    def __init__(self, location):
        self.location = location
        self.current = None
        self.daily = None
        self.hourly = None
        weather = current_Weather(location)
        weather.fetch_weather_data()
        self.current = weather.data
        geolocation = geo_Location(location)
        forecast = weekly_Forcast(geolocation.lattitude, geolocation.longitude)
        forecast.fetch_weather_data()
        self.daily = forecast.data
        API = NWS_API(geolocation.lattitude, geolocation.longitude)
        hourly = hourly_Forcast(API.grid_x, API.grid_y, API.grid_ID)
        hourly.fetch_weather_data()
        self.hourly = hourly.data

    def hourly(self):
        return self.hourly
    
    def daily(self):
        return self.daily
    
    def current(self):
        return self.current
    
        
        
