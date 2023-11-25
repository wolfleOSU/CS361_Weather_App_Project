import tkinter
import customtkinter
from ..frontend.settings import Settings
from customtkinter import CTkImage
from PIL import Image, ImageTk

#from ..backend.weatherApp_API_Testing import WeatherDataFetcher
from ..backend.API import initialize



"""
Sets up some of the default settings
"""
class DefaultSettings:
    def __init__(self, app) -> None:
        self.app = app

    def set_theme(self, theme):
        customtkinter.set_default_color_theme(theme)
    
    def set_appearance_mode(self, mode):
        customtkinter.set_appearance_mode(mode)


"""
Sets up 3 icons: the left and right buttons to select different saved locations as well
as the gear icon that opens the settings menu.
"""
class Navigation:
    def __init__(self, app):
        self.app = app
        self.create_navigation_buttons()
        self.settings_clicked = False

    def create_navigation_buttons(self):
        # Settings gear button
        gear_image = Image.open("src/frontend/assets/gear.png").resize((30, 30), Image.BICUBIC)
        gear_icon = customtkinter.CTkImage(gear_image)
        self.settings_button = customtkinter.CTkButton(self.app, image=gear_icon, width=30, height=30, command=self.on_settings_click, text="")
        self.settings_button.grid(row=1, column=5, padx=10, pady=5, sticky="e")

        # Create and hide settings panel
        self.settingsframe = tkinter.Frame(self.app)
        self.settingsframe.grid(row=2, column=5, padx=10, pady=5)
        self.settings_box = Settings(self.settingsframe)
        self.settingsframe.grid_remove()

        # Left arrow button
        left_image = Image.open("src/frontend/assets/left.png").resize((20, 20), Image.BICUBIC)
        left_icon = customtkinter.CTkImage(left_image)
        self.left_button = customtkinter.CTkButton(self.app, image=left_icon, width=20, height=20, command=self.on_left_click, text="")
        self.left_button.grid(row=2, column=1, padx=10, pady=10)

        # Right arrow button
        right_image = Image.open("src/frontend/assets/right.png").resize((20, 20), Image.BICUBIC)
        right_icon = customtkinter.CTkImage(right_image)
        self.right_button = customtkinter.CTkButton(self.app, image=right_icon, width=20, height=20, command=self.on_right_click, text="")
        self.right_button.grid(row=2, column=4, padx=10, pady=10)

        # Location Display Box
        self.location_box = customtkinter.CTkLabel(self.app, text="Corvallis", fg_color="#4da6ff", font=("Verdana", 35),
                                                    corner_radius=7, text_color="black")
        self.location_box.grid(row=2, column=2, columnspan = 2, padx=5, pady=(50, 15))

    def on_settings_click(self):
        if self.settings_clicked:
            self.settingsframe.grid_remove()
            self.settings_clicked = False
        else:
            self.settingsframe.grid()
            self.settings_clicked = True
        
    def change_city(self, location):
        self.location_box.configure(text=location)

    def on_left_click(self):
        print("Left arrow clicked")

    def on_right_click(self):
        print("Right arrow clicked")

"""
Sets up the search bar.
"""
class Search:
    def __init__(self, app, weather_app):
        self.app = app
        self.weather_app = weather_app
        self.location = customtkinter.StringVar()
        self.create_search_entry()

    def create_search_entry(self):
        self.search_entry = customtkinter.CTkEntry(
            self.app, width=120, height=40, corner_radius=8, border_width=2,
            placeholder_text="Search for a Location", textvariable=self.location
        )
        self.search_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")
        """
        search_button = customtkinter.CTkButton(
            self.app, text="Search", command=self.on_search_submit
        )
        search_button.grid(row=1, column=4, padx=2, pady=1)
        """
        self.search_entry.bind("<Return>", lambda event=None: self.on_search_submit())

    def get_search_text(self):
        print("Location Searched: ", self.location.get())
        return self.location.get()
    
    def on_search_submit(self):
        city = self.get_search_text()
        self.weather_app.update_city(city)
        self.location.set("")
        original = self.search_entry.cget("fg_color")
        self.search_entry.configure(fg_color="light green")
        self.app.after(100, lambda: self.search_entry.configure(fg_color=original))

"""
This is the main box for the current weather to be displayed. There is the temp in F or C and a 
statement about the current conditions.
"""
class WeatherDisplay:
    def __init__(self, app):
        self.app = app
        self.create_display_labels()

    def create_display_labels(self):
        # Temperature Label
        self.temp_label = customtkinter.CTkLabel(self.app, text="Loading...", font=("Tahoma", 55), fg_color="light grey", height=175, corner_radius=15)
        self.temp_label.grid(row=3, column=2, padx=5, pady=(15,25), sticky="nsew")

        # Weather Condition Label
        self.weather_label = customtkinter.CTkLabel(self.app, text="Loading...", font=("Tahoma", 40), fg_color="light grey", height=175, corner_radius=15)
        self.weather_label.grid(row=3, column=3, padx=5, pady=(15,25), sticky="nsew")

    def update_weather(self, temperature, condition, unit="F"):
        if unit == "F":
            temperature = temperature * 1.8 + 32
        print(f"Updating weather: {temperature}° {unit}, {condition}")
        self.temp_label.configure(text=f"{temperature}° {unit}")
        self.weather_label.configure(text=condition)

"""
Sets up the buttons above the forecast box to switch between hourly and daily forecast.
"""
class Forecast:
    def __init__(self, app, data_loader, scrollable_area):
        self.app = app
        self.data_loader = data_loader
        self.scrollable_area = scrollable_area
        self.create_forecast_buttons()


    def create_forecast_buttons(self):
        self.hourly_button = customtkinter.CTkButton(
            self.app, text="Hourly", command=lambda: self.select_forecast("hourly"),
            text_color="black", border_width=1, font=("Verdana", 18)
        )
        self.hourly_button.grid(row=5, column=2, padx=0, pady=10)

        self.daily_button = customtkinter.CTkButton(
            self.app, text="Daily", command=lambda: self.select_forecast("daily"),
            text_color="black", border_width=0, font=("Verdana", 18)
        )
        self.daily_button.grid(row=5, column=3, padx=0, pady=10)

    def select_forecast(self, forecast_type, unit="F"):
        if forecast_type == "hourly":
            self.hourly_button.configure(fg_color="#4da6ff")  # Highlighted color
            self.daily_button.configure(fg_color="#F0F0F0")   # Default color
            self.hourly_button.configure(border_width=1)
            self.daily_button.configure(border_width=0)
            self.data_loader.update_hourly(unit)
        elif forecast_type == "daily":
            self.daily_button.configure(fg_color="#4da6ff")   # Highlighted color
            self.hourly_button.configure(fg_color="#F0F0F0")  # Default color
            self.daily_button.configure(border_width=1)
            self.hourly_button.configure(border_width=0)
            self.data_loader.update_daily(unit)


"""
Main frontend method to receive the API data from the backend and then put it into the correct area.
"""
class DataLoader:
    def __init__(self, weather_display, scrollable_area, city, unit="F"):
        self.city = city
        self.weather_fetcher = initialize(self.city)
        self.weather_display = weather_display
        self.scrollable_area = scrollable_area
        self.hourly_forecast = None
        self.daily_forecast = None
        self.current = None
        self.unit = unit

    def update_city(self, new_city):
        self.city = new_city
        self.weather_fetcher = initialize(self.city)

    def load_data(self):
        self.current = self.weather_fetcher.current
        print("Loading Current")

        self.hourly_forecast = self.weather_fetcher.hourly
        
        self.daily_forecast = self.weather_fetcher.daily
        
    def update_current(self, unit="F"):
        if self.current:
            self.weather_display.update_weather(self.current['Temperature'], self.current['Condition'], unit)  
            print("Updating current")

    def update_hourly(self, unit="F"):
        if self.hourly_forecast:
            self.scrollable_area.update_area(self.hourly_forecast, "hourly", unit)

    def update_daily(self, unit="F"):
        if self.daily_forecast:
            self.scrollable_area.update_area(self.daily_forecast, "daily", unit)
"""
Sets up the main box that holds the forecast info. Updates to take the API data and display it.
"""
class ScrollableArea:
    def __init__(self, app):
        self.app = app
        self.create_scrollable_area()

    def create_scrollable_area(self):
        self.forecast_container = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.forecast_container.grid(row=6, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Using CTKCanvas instead of the standard Canvas
        self.forecast_canvas = customtkinter.CTkCanvas(self.forecast_container)
        self.forecast_canvas.pack(side="left", fill="both", expand=True)

        # Using CTKScrollbar instead of the standard Scrollbar
        self.scrollbar = customtkinter.CTkScrollbar(self.forecast_container, command=self.forecast_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.forecast_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create the forecast_frame within the canvas
        self.forecast_frame = customtkinter.CTkFrame(self.forecast_canvas)
        canvas_window = self.forecast_canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")

        # Bind the <Configure> event of the forecast_frame to adjust the scrollregion of the canvas
        self.forecast_frame.bind('<Configure>', lambda e: self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all")))


    def adjust_canvas_scrollregion(self, event):
        # Update the scrollregion of the canvas
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

    def adjust_frame_width(self, event):
        # Update the width of the frame to match the canvas width
        self.forecast_frame.configure(width=event.width)
        # Update the scrollregion of the canvas
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

    def update_area(self, forecast, type, unit="F"):
        #print("Forecast data structure:", type(forecast_data), forecast_data) # For testing
        # Clear existing forecast widgets
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        if type in ["hourly", "daily"]:
            # Iterate over the indices of the forecast lists
            for i in range(len(forecast['Time'])):
                time = forecast['Time'][i]
                temp = forecast['Temperature'][i]
                if unit == "C":
                    temp = (temp - 32) * 5 / 9 
                condition = forecast['Conditions'][i]
                wind_speed = forecast['Wind Speed'][i]
                wind_dir = forecast['Wind Direction'][i]
                humidity = forecast['Humidity'][i]
                dew_point = forecast['Dew Point'][i]

                # Format the forecast information
                forecast_text = f"{time}: {temp}°{unit}, {condition}, Wind: {wind_speed} mph {wind_dir}, Humidity: {humidity}, Dew Point: {dew_point}° F"
                
                # Create a label for each entry and add to the scrollable frame
                label = customtkinter.CTkLabel(self.forecast_frame, text=forecast_text)
                label.pack(padx=10, pady=5, anchor='w', fill='x')

        self.forecast_frame.update_idletasks()  # Make sure the frame is updated and scrollbar works.
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))



"""
The main class, holds the other classes and holds the actually functionality to launch the window.
"""
class WeatherApp:
    def __init__(self):
        # Initialize the main window
        self.app = customtkinter.CTk()
        self.settings = DefaultSettings(self.app)
        self.setup_window()

        self.configure_layout()
        self.title = customtkinter.CTkLabel(self.app, text="The Weather App")
        self.title.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        self.navigation = Navigation(self.app)
        self.search = Search(self.app, self)
        self.weather_display = WeatherDisplay(self.app)
        self.scrollable_area = ScrollableArea(self.app)
        self.default_city = "Corvallis"
        self.data_loader = DataLoader(self.weather_display, self.scrollable_area, self.default_city)
        self.forecast = Forecast(self.app, self.data_loader, self.scrollable_area)
    
    def update_city(self, city):
        self.data_loader.update_city(city)
        self.data_loader.load_data()
        self.data_loader.update_current()
        self.data_loader.update_hourly()
        self.navigation.change_city(city)


    def setup_window(self):
        self.app.title("The Weather App")
        self.app.geometry("720x480")
        self.settings.set_appearance_mode("System")  
        self.settings.set_theme("blue")  

    def configure_layout(self):
        for i in range(6):
            self.app.grid_columnconfigure(i, weight=1)
        self.app.grid_rowconfigure(6, weight=1)
        

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    weather_app = WeatherApp()
    weather_app.update_city(weather_app.default_city)
    weather_app.run()