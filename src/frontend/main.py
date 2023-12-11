import tkinter
import re
from CTkListbox import *
from tkinter import END
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk

#from ..backend.weatherApp_API_Testing import WeatherDataFetcher
from ..backend.API import initialize
from ..backend.API import current_Location


class Settings:
    def __init__(self, frame, data_loader):
        #true=fahrenheit
        self.t_clicked = True
        #true=dark
        self.c_clicked = True

        self.temps = ["Celsius", "Fahrenheit"]
        self.colors = ["Light", "Dark"]

        self.data_loader = data_loader

        self.temp_btn = ctk.CTkButton(frame, text="Celsius", command=self.temp_clicked, corner_radius=10)
        self.temp_btn.grid(row=0,column=0, padx=5, pady=5)

        self.color_btn = ctk.CTkButton(frame, text="Light", command=self.color_clicked, corner_radius=10)
        self.color_btn.grid(row=1,column=0, padx=5, pady=5)



    def temp_clicked(self):
        self.t_clicked = not self.t_clicked
        self.data_loader.unit = self.temps[self.t_clicked][0]
        self.data_loader.update_current()
        self.temp_btn.configure(text = self.temps[not self.t_clicked])

    def color_clicked(self):
        self.c_clicked = not self.c_clicked
        self.color_btn.configure(text = self.colors[not self.c_clicked])
        ctk.set_appearance_mode(self.colors[self.c_clicked].lower())

"""
Sets up 3 icons: the left and right buttons to select different saved locations as well
as the gear icon that opens the settings menu.
"""
class Navigation:
    def __init__(self, app, data_loader):
        self.app = app
        self.data_loader = data_loader
        self.create_navigation_buttons()
        self.settings_clicked = False
        self.heart_clicked = False
        self.favorites_list = FavoriteList(self.data_loader)
        

    def create_navigation_buttons(self):
        # Settings gear button
        gear_image = Image.open("src/frontend/assets/gear.png").resize((30, 30), Image.BICUBIC)
        gear_icon = ctk.CTkImage(gear_image)
        self.settings_button = ctk.CTkButton(self.app, image=gear_icon, width=30, height=30, command=self.on_settings_click, text="")
        self.settings_button.grid(row=1, column=5, padx=10, pady=5, sticky="e")

        # Create and hide settings panel
        self.settingsframe = tkinter.Frame(self.app)
        self.settingsframe.grid(row=2, column=5, padx=10, pady=5)
        self.settings_box = Settings(self.settingsframe, self.data_loader)
        self.settingsframe.grid_remove()

        # Favorite Location Button
        heart_image = Image.open("src/frontend/assets/heart.png").resize((30, 30), Image.BICUBIC)
        heart_icon = ctk.CTkImage(heart_image)
        self.settings_button = ctk.CTkButton(self.app, image=heart_icon, width=30, height=30, command=self.on_favorite_click, text="")
        self.settings_button.grid(row=2, column=3, padx=10, pady=5, sticky="e")

        # Left arrow button
        left_image = Image.open("src/frontend/assets/left.png").resize((20, 20), Image.BICUBIC)
        left_icon = ctk.CTkImage(left_image)
        self.left_button = ctk.CTkButton(self.app, image=left_icon, width=20, height=20, command=self.on_left_click, text="")
        self.left_button.grid(row=2, column=1, padx=10, pady=10)

        # Right arrow button
        right_image = Image.open("src/frontend/assets/right.png").resize((20, 20), Image.BICUBIC)
        right_icon = ctk.CTkImage(right_image)
        self.right_button = ctk.CTkButton(self.app, image=right_icon, width=20, height=20, command=self.on_right_click, text="")
        self.right_button.grid(row=2, column=4, padx=10, pady=10)

        # Location Display Box
        self.location_box = ctk.CTkLabel(self.app, text="Corvallis", fg_color="#4da6ff", font=("Verdana", 35),
            corner_radius=7, text_color="black")
        self.location_box.grid(row=2, column=2, columnspan = 2, padx=5, pady=(50, 15))

    def on_settings_click(self):
        if self.settings_clicked:
            self.settingsframe.grid_remove()
        else:
            self.settingsframe.grid()
        self.settings_clicked = not self.settings_clicked
        
    def change_city(self, location):
        self.location_box.configure(text=location)

    def on_favorite_click(self):
        # I'm leaving all this commented for the time being, but based one what it's doing,
        #you're probably going to want to do it in the favoriteList. The code that did work here
        #so far was simplified

        #Is the heart icon going to change at all depending on weather it is pressed or not?
        #if not most all of this isn't going to be useful

        city = self.location_box.cget("text")
        if not self.favorites_list.isNotEmpty():
            self.heart_clicked = False
        else: 
            if not self.favorites_list.matchCurrent(city):
                self.heart_clicked = False
        self.heart_clicked = not self.heart_clicked
        self.favorites_list.buttonClick(self.heart_clicked, city)

    def on_left_click(self):
        if self.favorites_list.isNotEmpty():
            self.favorites_list.shiftLeft()
            self.change_city(self.favorites_list.fetchHead())
            self.heart_clicked = True

    def on_right_click(self):
        if self.favorites_list.isNotEmpty():
            self.favorites_list.shiftRight()
            self.change_city(self.favorites_list.fetchHead())
            self.heart_clicked = True

"""
Sets up the search bar.
"""

class Search:
    def __init__(self, app, weather_app):
        self.app = app
        self.weather_app = weather_app
        self.location = ctk.StringVar()
        self.font1 = ('Times', 24, 'bold')

        self.create_search_entry()
        self.create_list_box()
        self.cities = open("src/frontend/output_file.txt").read().split("\n")

        self.search_entry.bind('<KeyRelease>', self.get_data)


    def create_list_box(self):
        self.l1 = CTkListbox(self.app, height=3, font=self.font1, multiple_selection=False, text_color='gray', command=self.on_click)
        self.l1.grid(row=2, column=2, columnspan=2, padx=10, pady=5, sticky="ew")
        self.l1.grid_remove()


    def on_click(self, event=None):
        original = self.search_entry.cget("border_color")
        self.search_entry.configure(border_color="light green")
        clickLocation = self.l1.get(self.l1.curselection())
        print(f'Clicked Location: {clickLocation}')
        self.l1.deactivate(self.l1.curselection())
        self.l1.delete('all')
        self.l1.grid_remove()
        self.weather_app.navigation.location_box.grid()
        self.weather_app.update_city(clickLocation)
        self.location.set("")
        self.app.after(200, lambda: self.search_entry.configure(border_color=original))

    def create_search_entry(self):
        self.search_entry = ctk.CTkEntry(
            self.app, width=120, height=40, corner_radius=8, border_width=2,
            placeholder_text="Search for a Location", textvariable=self.location
        )

        self.search_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")
        self.search_entry.bind("<Return>", lambda event=None: self.on_search_submit())

    def get_search_text(self):
        print("Location Searched: ", self.location.get())
        return self.location.get()

    def on_search_submit(self, event=None):
        city = self.get_search_text()
        match_found = False  # Flag to check if any match is found
        self.weather_app.navigation.heart_clicked = False

        for element in self.cities:
            if re.fullmatch(city, element, re.IGNORECASE):
                original = self.search_entry.cget("border_color")
                self.search_entry.configure(border_color="light green")
                self.weather_app.update_city(city)
                self.location.set("")
                self.app.after(200, lambda: self.search_entry.configure(border_color=original))
                self.weather_app.navigation.location_box.grid()
                self.l1.grid_remove()
                print('trying to search for location')
                match_found = True
                break  # Break out of the loop once a match is found
        if not match_found:
            print('no match in system')
            original = self.search_entry.cget("border_color")
            self.search_entry.configure(border_color="red")
            self.app.after(500, lambda: self.search_entry.configure(border_color=original)) 



    def get_data(self, *args):  # populate the Listbox with matching options
        search_str = self.location.get()  # user entered string
        self.l1.delete('all')  # Delete all elements of Listbox

        if search_str and len(search_str) >= 3:
            self.l1.grid()
            for element in self.cities:
                if re.match(search_str, element, re.IGNORECASE):
                    self.l1.insert('END', element)  # add matching options to Listbox
        elif search_str: 
            self.l1.grid()
            self.weather_app.navigation.location_box.grid_remove()
        else:
            self.weather_app.navigation.location_box.grid()
            self.l1.delete("all")
            self.l1.grid_remove()
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
        self.temp_label = ctk.CTkLabel(self.app, text="Loading...", font=("Tahoma", 55), fg_color="grey", height=175, corner_radius=15)
        self.temp_label.grid(row=3, column=2, padx=5, pady=(15,25), sticky="nsew")

        # Weather Condition Label
        self.weather_label = ctk.CTkLabel(self.app, text="Loading...", font=("Tahoma", 40), fg_color="grey", height=175, corner_radius=15)
        self.weather_label.grid(row=3, column=3, padx=5, pady=(15,25), sticky="nsew")

    def update_weather(self, temperature, condition, unit):
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
        self.create_forecast_buttons(data_loader.unit)
        self.buttonColors = ["grey", "#4da6ff"]


    def create_forecast_buttons(self, unit):
        self.hourly_button = ctk.CTkButton(
            self.app, text="Hourly", command=lambda: self.select_forecast(1, unit),
            text_color="black", border_width=1, font=("Verdana", 18), fg_color="grey"
        )
        self.hourly_button.grid(row=5, column=2, padx=0, pady=10)

        self.daily_button = ctk.CTkButton(
            self.app, text="Daily", command=lambda: self.select_forecast(0, unit),
            text_color="black", border_width=0, font=("Verdana", 18)
        )
        self.daily_button.grid(row=5, column=3, padx=0, pady=10)
    
    #hourly = 1; daily = 0
    def select_forecast(self, forecast_type, unit):
        self.hourly_button.configure(fg_color=self.buttonColors[not forecast_type])
        self.hourly_button.configure(border_width= not forecast_type)
        self.daily_button.configure(fg_color=self.buttonColors[forecast_type])
        self.daily_button.configure(border_width=forecast_type)
        self.data_loader.forecast_type = forecast_type
        self.data_loader.update_current()


"""
Main frontend method to receive the API data from the backend and then put it into the correct area.
"""
class DataLoader:
    def __init__(self, weather_display, scrollable_area, city, forecast_type, unit):
        self.city = city
        self.weather_fetcher = initialize(self.city)
        self.weather_display = weather_display
        self.scrollable_area = scrollable_area
        #[daily, hourly]
        self.forecasts = [None, None]
        self.current = None
        self.unit = unit
        self.forecast_type = forecast_type

    def update_city(self, new_city):
        self.city = new_city
        self.weather_fetcher = initialize(self.city)

    def load_data(self):
        self.current = self.weather_fetcher.current
        print("Loading Current")

        self.forecasts[0] = self.weather_fetcher.daily
        self.forecasts[1] = self.weather_fetcher.hourly
        
    def update_current(self):
        if self.current:
            self.weather_display.update_weather(self.current['Temperature'], self.current['Condition'], self.unit) 
            if self.forecasts[0] and self.forecasts[1]:
                self.scrollable_area.update_area(self.forecasts[self.forecast_type], self.forecast_type, self.unit)
            print("Updating current")

"""
Sets up the main box that holds the forecast info. Updates to take the API data and display it.
"""
class ScrollableArea:
    def __init__(self, app):
        self.app = app
        self.create_scrollable_area()

    def create_scrollable_area(self):
        self.forecast_container = ctk.CTkFrame(self.app, corner_radius=10, bg_color="grey")
        self.forecast_container.grid(row=6, column=1, columnspan=4, padx=0, pady=10, sticky="nsew")

        self.forecast_canvas = ctk.CTkCanvas(self.forecast_container)
        self.forecast_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.forecast_container, command=self.forecast_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.forecast_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.forecast_canvas.bind('<Configure>', self.adjust_frame_width)

        # Create the forecast_frame within the canvas
        self.forecast_frame = ctk.CTkFrame(self.forecast_canvas, bg_color="grey")
        self.canvas_window = self.forecast_canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")

        # Bind the <Configure> event of the forecast_frame to adjust the scrollregion of the canvas
        self.forecast_frame.bind('<Configure>', lambda e: self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all")))


    def adjust_canvas_scrollregion(self, event):
        # Update the scrollregion of the canvas
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

    def adjust_frame_width(self, event):
        canvas_width = event.width
        self.forecast_canvas.itemconfig(self.canvas_window, width=canvas_width)
        # Update the scrollregion of the canvas
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

    def update_area(self, forecast, type, unit):
        # Clear existing forecast widgets
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()
            # Iterate over the indices of the forecast lists
        self.forecast_frame.grid_columnconfigure((0, 1, 2, 3), weight=2)
        for i in range(len(forecast['Time'])):
            time = forecast['Time'][i]
            temp = forecast['Temperature'][i]
            condition = forecast['Conditions'][i]
            wind_speed = forecast['Wind Speed'][i]
            wind_dir = forecast['Wind Direction'][i]
            if unit == "C":
                temp = (temp - 32) * 5 / 9
                wind_speed = (wind_speed * 1.609344)
            condition = forecast['Conditions'][i]
            #humidity = forecast['Humidity'][i]
            #dew_point = forecast['Dew Point'][i]

            time_label = ctk.CTkLabel(self.forecast_frame, text=time)
            temp_label = ctk.CTkLabel(self.forecast_frame, text=f"{round(temp, 2)}°{unit}")
            condition_label = ctk.CTkLabel(self.forecast_frame, text=condition)
            wind_label = ctk.CTkLabel(self.forecast_frame, text=f"Wind: {wind_speed} mph {wind_dir}")
            if unit == "F":
                wind_label = ctk.CTkLabel(self.forecast_frame, text=f"Wind: {wind_speed} mph {wind_dir}")
            else:
                wind_label = ctk.CTkLabel(self.forecast_frame, text=f"Wind: {wind_speed} kph {wind_dir}")
            #humidity_label = ctk.CTkLabel(self.forecast_frame, text=f"Humidity: {humidity}%")
            #dew_point_label = ctk.CTkLabel(self.forecast_frame, text=f"Dew Point: {dew_point}° F")

            # Grid these labels
            time_label.grid(row=i, column=0, sticky="ew")
            temp_label.grid(row=i, column=1, sticky="ew")
            condition_label.grid(row=i, column=2, sticky="ew")
            wind_label.grid(row=i, column=3, sticky="ew")
            #humidity_label.grid(row=i, column=4, sticky="ew")
            #dew_point_label.grid(row=i, column=5, sticky="ew")
        # Update the frame and canvas configurations
        self.forecast_frame.update_idletasks()
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

"""
Class for circularly linked list of favorite city data
"""
class FavoriteList:
    #   if you start out by making the head the current weather that'll simplify a lot of this code
    #   that was already the idea lol
    
    def __init__(self, data_loader):
        self.head = None
        self.data_loader = data_loader

    def isNotEmpty(self):
        if not self.head:
            return False
        else:
            return True
        
    def matchCurrent(self, city):
        if self.head.city == city:
            return True
        else:
            return False

    #Add favorited location
    def append(self, city): 
        if not self.head: #No head node yet, create first entry in list
            self.head = FavoriteNode(city)
            self.head.next = self.head
            self.head.prev = self.head
        else: #Adds new node previous to head node and sets it to be the new head
            newNode = FavoriteNode(city)
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            cur.next = newNode
            newNode.next = self.head
            newNode.prev = cur
            self.head.prev = newNode
            self.head = newNode

    #Remove current favorite function
    def removeHead(self):
        if self.head == self.head.next:
            self.head = None
        else:
            next = self.head.next
            prev = self.head.prev
            prev.next = next
            next.prev = prev
            self.head = next

    #For arrow keys, shift right or left in list and [pull data from head node] AFTER CALLING
    def shiftRight(self):
        self.head = self.head.next
        self.data_loader.update_city(self.head.city)
        self.data_loader.load_data()
        self.data_loader.update_current()

    def shiftLeft(self):
        self.head = self.head.prev
        self.data_loader.update_city(self.head.city)
        self.data_loader.load_data()
        self.data_loader.update_current()

    def fetchHead(self):
        return self.head.city
    
    def buttonClick(self, on, city):
        if on:
            self.append(city)
        else:
            self.removeHead()

"""
Class for favorite location node in list
"""
class FavoriteNode:
    def __init__(self, city):
        self.city = city
        self.next = None
        self.prev = None

"""
The main class, holds the other classes and holds the actually functionality to launch the window.
"""
class WeatherApp:
    def __init__(self):
        # Initialize the main window
        self.app = ctk.CTk()
        self.setup_window()

        self.configure_layout()
        self.title = ctk.CTkLabel(self.app, text="The Weather App")
        self.title.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        
        self.search = Search(self.app, self)
        self.weather_display = WeatherDisplay(self.app)
        self.scrollable_area = ScrollableArea(self.app)
        current = current_Location()
        self.current_city = current.location
        self.default_city = "Corvallis, Oregon"
        self.data_loader = DataLoader(self.weather_display, self.scrollable_area, self.default_city, 1, "F")
        self.forecast = Forecast(self.app, self.data_loader, self.scrollable_area)
        self.navigation = Navigation(self.app, self.data_loader)
    
    def update_city(self, city):
        self.data_loader.update_city(city)
        self.data_loader.load_data()
        self.data_loader.update_current()
        self.navigation.change_city(city)


    def setup_window(self):
        self.app.title("The Weather App")
        self.app.geometry("720x480")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

    def configure_layout(self):
        for i in range(6):
            self.app.grid_columnconfigure(i, weight=1)
        self.app.grid_rowconfigure(6, weight=1)
        

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    weather_app = WeatherApp()
    if weather_app.current_city == None:
        weather_app.update_city(weather_app.default_city)
    else:
        weather_app.update_city(weather_app.current_city)
    weather_app.run()
