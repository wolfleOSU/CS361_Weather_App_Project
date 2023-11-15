import tkinter
import customtkinter
from customtkinter import CTkImage
from PIL import Image, ImageTk
import sys
from pathlib import Path

#sys.path.append(str(Path(__file__).resolve().parent.parent))
#from backend.weatherApp_API_Testing.py import Class



class Settings:
    def __init__(self, app) -> None:
        self.app = app

    def set_theme(self, theme):
        customtkinter.set_default_color_theme(theme)
    
    def set_appearance_mode(self, mode):
        customtkinter.set_appearance_mode(mode)

class Navigation:
    def __init__(self, app):
        self.app = app
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        # Settings gear button
        gear_image = Image.open("assets/gear.png").resize((30, 30), Image.Resampling.LANCZOS)
        gear_icon = customtkinter.CTkImage(gear_image)
        self.settings_button = customtkinter.CTkButton(self.app, image=gear_icon, width=30, height=30, command=self.on_settings_click, text="")
        self.settings_button.grid(row=1, column=5, padx=10, pady=5, sticky="e")

        # Left arrow button
        left_image = Image.open("assets/left.png").resize((20, 20), Image.Resampling.LANCZOS)
        left_icon = customtkinter.CTkImage(left_image)
        self.left_button = customtkinter.CTkButton(self.app, image=left_icon, width=20, height=20, command=self.on_left_click, text="")
        self.left_button.grid(row=2, column=1, padx=10, pady=10)

        # Right arrow button
        right_image = Image.open("assets/right.png").resize((20, 20), Image.Resampling.LANCZOS)
        right_icon = customtkinter.CTkImage(right_image)
        self.right_button = customtkinter.CTkButton(self.app, image=right_icon, width=20, height=20, command=self.on_right_click, text="")
        self.right_button.grid(row=2, column=4, padx=10, pady=10)

    def on_settings_click(self):
        print("Settings clicked")

    def on_left_click(self):
        print("Left arrow clicked")

    def on_right_click(self):
        print("Right arrow clicked")

class Search:
    def __init__(self, app):
        self.app = app
        self.location = customtkinter.StringVar()
        self.create_search_entry()

    def create_search_entry(self):
        self.search_entry = customtkinter.CTkEntry(
            self.app, width=120, height=40, corner_radius=2, border_width=2,
            placeholder_text="Search for a Location", textvariable=self.location
        )
        self.search_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    def get_search_text(self):
        return self.location.get()

class WeatherDisplay:
    def __init__(self, app):
        self.app = app
        self.create_display_labels()

    def create_display_labels(self):
        # Temperature Label
        self.temp_label = customtkinter.CTkLabel(self.app, text="60° F", font=("Roboto", 40))
        self.temp_label.grid(row=3, column=2, padx=0, pady=10, sticky="nsew")

        # Weather Condition Label
        self.weather_label = customtkinter.CTkLabel(self.app, text="Cloudy", font=("Roboto", 30))
        self.weather_label.grid(row=3, column=3, padx=0, pady=10, sticky="nsew")

    def update_weather(self, temperature, condition):
        self.temp_label.configure(text=f"{temperature}° F")
        self.weather_label.configure(text=condition)

class Forecast:
    def __init__(self, app):
        self.app = app
        self.create_forecast_buttons()

    def create_forecast_buttons(self):
        self.hourly_button = customtkinter.CTkButton(
            self.app, text="Hourly", command=lambda: self.select_forecast("hourly"),
            text_color="black", border_width=1
        )
        self.hourly_button.grid(row=5, column=2, padx=0, pady=10)

        self.daily_button = customtkinter.CTkButton(
            self.app, text="Daily", command=lambda: self.select_forecast("daily"),
            text_color="black"
        )
        self.daily_button.grid(row=5, column=3, padx=0, pady=10)

    def select_forecast(self, forecast_type):
        # Logic to switch between hourly and daily forecasts
        pass

class DataLoader:
    def __init__(self):
        pass

    def load_data(self):
        # Implement data loading logic
        pass


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
        self.forecast_canvas.bind('<Configure>', lambda e: self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all")))

        self.forecast_frame = customtkinter.CTkFrame(self.forecast_canvas)
        self.forecast_canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")


class WeatherApp:
    def __init__(self):
        # Initialize the main window
        self.app = customtkinter.CTk()
        self.settings = Settings(self.app)
        self.setup_window()

        self.configure_layout()
        self.title = customtkinter.CTkLabel(self.app, text="The Weather App")
        self.title.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        self.navigation = Navigation(self.app)
        self.search = Search(self.app)
        self.weather_display = WeatherDisplay(self.app)
        self.forecast = Forecast(self.app)
        self.data_loader = DataLoader()
        self.scrollable_area = ScrollableArea(self.app)

    def setup_window(self):
        self.app.title("The Weather App")
        self.app.geometry("720x480")
        self.settings.set_appearance_mode("System")  # Set appearance mode
        self.settings.set_theme("blue")  # Set color theme

    def configure_layout(self):
        for i in range(6):
            self.app.grid_columnconfigure(i, weight=1)
        self.app.grid_rowconfigure(6, weight=1)
        

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    weather_app = WeatherApp()
    weather_app.run()