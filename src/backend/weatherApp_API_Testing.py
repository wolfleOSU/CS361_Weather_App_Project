import requests
import sys
import os



class WeatherDataFetcher:
    def __init__(self, city):
        self.city = city
        self.weather_api_key = 'bf6343dd97ac4f83b1602239230111'
        self.openweather_api_key = '1b174bad0a1d248f9af22a5632dd9f63'
        


    def fetch_current_weather(self):
        url = f'http://api.weatherapi.com/v1/current.json?key={self.weather_api_key}&q={self.city}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.print_current_weather(data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current weather: {e}")

    def print_current_weather(self, data):
        location = data['location']
        current = data['current']
        print(f"Weather in {location['name']}, {location['region']}, {location['country']}")
        print(f"Local Time: {location['localtime']}")
        print(f"Condition: {current['condition']['text']}")
        print(f"Temperature: {current['temp_c']}°C")
        print(f"Feels Like: {current['feelslike_c']}°C")
        print(f"Wind Speed: {current['wind_kph']} km/h")

    def fetch_weather_forecast(self):
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={self.city}&cnt=7&appid={self.openweather_api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.print_weather_forecast(data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather forecast: {e}")

    def print_weather_forecast(self, data):
        print()
        print("Location:", self.city)
        print("{:<19} {:<25} {:<15} {:<15}".format("Date", "Condition", "Max Temp (°C)", "Min Temp (°C)"))
        for forecast in data['list']:
            date = forecast['dt_txt']
            condition = forecast['weather'][0]['description']
            max_temp = forecast['main']['temp_max'] - 273.15
            min_temp = forecast['main']['temp_min'] - 273.15
            print("{:<19} {:<25} {:<15.2f} {:<15.2f}".format(date, condition, max_temp, min_temp))

    def geocode_city(self):
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": self.city,
            "format": "json"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0]["lat"], data[0]["lon"]
            else:
                print("No results found.")
                return None, None
        except requests.exceptions.RequestException as e:
            print(f"Error in geocoding: {e}")
            return None, None

    def fetch_nws_weather_data(self):
        latitude, longitude = self.geocode_city()
        if latitude and longitude:
            url = f'https://api.weather.gov/points/{latitude},{longitude}'
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                self.print_nws_weather_data(data)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching NWS weather data: {e}")

    def print_nws_weather_data(self, data):
        location_name = data['properties']['relativeLocation']['properties']['city']
        print()
        print(f"Location Name: {location_name}")
        grid_data_url = data['properties']['forecast']
        forecast_hourly_url = data['properties']['forecastHourly']
        try:
            forecast_response = requests.get(grid_data_url)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            self.print_detailed_forecast(forecast_data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching detailed forecast: {e}")

    def print_detailed_forecast(self, forecast_data):
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

if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Corvallis"  
    weather_fetcher = WeatherDataFetcher(city)
    weather_fetcher.fetch_current_weather()
    weather_fetcher.fetch_weather_forecast()
    weather_fetcher.fetch_nws_weather_data()