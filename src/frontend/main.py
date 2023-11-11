import tkinter
import customtkinter
from customtkinter import CTkImage
from PIL import Image, ImageTk


#Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("The Weather App")

# Grid layout
for i in range(6):
    app.grid_columnconfigure(i, weight=1)


# Add UI
title = customtkinter.CTkLabel(app, text="The Weather App")
title.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="ew")

location = tkinter.StringVar()
search = customtkinter.CTkEntry(app, width=120, height=40, corner_radius=2, border_width=2,placeholder_text="Search for a Location", textvariable=location)
search.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

#Settings gear
gear_image = Image.open("assets\gear.png")
gear_image = gear_image.resize((30,30), Image.Resampling.LANCZOS)
gear_icon = CTkImage(gear_image)

settings_button = customtkinter.CTkButton(app, image=gear_icon, width=30, height=30, command=lambda: print("settings"), text="")
settings_button.grid(row=1, column=5, padx=10, pady=5, sticky="e")

# Weather Information Label and arrows
# Left Arrow Button
left_image = Image.open("assets/left.png")
left_image = left_image.resize((20, 20), Image.Resampling.LANCZOS)  # Resize to match button size
left_icon = CTkImage(left_image)

left_button = customtkinter.CTkButton(app, image=left_icon, width=20, height=20, command=lambda: print("left"), text="")
left_button.grid(row=2, column=1, padx=10, pady=10)  # Adjust row and column for proper placement

# Weather Location Label
currentlocation = tkinter.StringVar()
weather_loc_label = customtkinter.CTkLabel(app, text="Current Location")
weather_loc_label.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="ew")  # Centered in the middle columns

# Right Arrow Button
right_image = Image.open("assets/right.png")
right_image = right_image.resize((20, 20), Image.Resampling.LANCZOS)
right_icon = CTkImage(right_image)

right_button = customtkinter.CTkButton(app, image=right_icon, width=20, height=20, command=lambda: print("right"), text="")
right_button.grid(row=2, column=4, padx=10, pady=10)  # Adjust row and column for proper placement


# Main Display for the large version of Temp and Weather condition
# Temperature Frame
temp_frame = customtkinter.CTkFrame(app, corner_radius=10)
temp_frame.grid(row=3, column=2, padx=0, pady=10, sticky="nsew")

# Temperature Label
temp_label = customtkinter.CTkLabel(temp_frame, text="60° F", font=("Roboto", 40))
temp_label.pack(padx=30, pady=40)  # Adjust padding as needed

# Weather Condition Frame
weather_frame = customtkinter.CTkFrame(app, corner_radius=10)
weather_frame.grid(row=3, column=3, padx=0, pady=10, sticky="nsew")

# Weather Condition Label
weather_label = customtkinter.CTkLabel(weather_frame, text="Cloudy", font=("Roboto", 30))
weather_label.pack(padx=30, pady=40)  # Adjust padding as needed (this is controlling the size of boxes)

# Forecast Select Label
forecast_select_label = customtkinter.CTkLabel(app, text="Forecast Select", font=("Roboto", 14))
forecast_select_label.grid(row=4, column=0, columnspan=6, pady=10, sticky="ew")

# Function to handle button click
def select_forecast(forecast_type):
    if forecast_type == "hourly":
        hourly_button.configure(fg_color="#4da6ff")  # Highlighted color
        daily_button.configure(fg_color="#F0F0F0")   # Default color
    elif forecast_type == "daily":
        daily_button.configure(fg_color="#4da6ff")   # Highlighted color
        hourly_button.configure(fg_color="#F0F0F0")  # Default color

# Hourly Button
hourly_button = customtkinter.CTkButton(app, text="Hourly", command=lambda: select_forecast("hourly"), text_color="black", border_width=1)
hourly_button.grid(row=5, column=2, padx=0, pady=10)

# Daily Button
daily_button = customtkinter.CTkButton(app, text="Daily", command=lambda: select_forecast("daily"), text_color="black")
daily_button.grid(row=5, column=3, padx=0, pady=10)

# Initially select 'Hourly'
select_forecast("hourly")


# MAIN DATA DISPLAY
forecast_container = customtkinter.CTkFrame(app, corner_radius=10)
forecast_container.grid(row=6, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

# Configure the grid to allow the container to expand
app.grid_rowconfigure(6, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(4, weight=1)

# Canvas for the Scrollable Area
forecast_canvas = tkinter.Canvas(forecast_container)
forecast_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

# Scrollbar
scrollbar = tkinter.Scrollbar(forecast_container, orient="vertical", command=forecast_canvas.yview)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# Configure the canvas to work with the scrollbar
forecast_canvas.configure(yscrollcommand=scrollbar.set)
forecast_canvas.bind('<Configure>', lambda e: forecast_canvas.configure(scrollregion=forecast_canvas.bbox("all")))

# Canvas and Scrollbar setup
forecast_canvas = tkinter.Canvas(forecast_container)
forecast_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

scrollbar = tkinter.Scrollbar(forecast_container, orient="vertical", command=forecast_canvas.yview)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

forecast_canvas.configure(yscrollcommand=scrollbar.set)
forecast_canvas.bind('<Configure>', lambda e: forecast_canvas.configure(scrollregion=forecast_canvas.bbox("all")))

# Inner frame for displaying data
forecast_frame = tkinter.Frame(forecast_canvas)
forecast_canvas.create_window((0, 0), window=forecast_frame, anchor="nw")

# Functions to load data
def load_hourly_data():
    # Clear current data
    for widget in forecast_frame.winfo_children():
        widget.destroy()

    # Sample hourly data
    for hour in range(24):
        time_label = tkinter.Label(forecast_frame, text=f"{hour}:00")
        time_label.grid(row=hour, column=0, sticky='w', padx=(10, 0))

        temp_label = tkinter.Label(forecast_frame, text=f"{60 + hour}°F")
        temp_label.grid(row=hour, column=1, padx=5)

        condition_label = tkinter.Label(forecast_frame, text="Cloudy")
        condition_label.grid(row=hour, column=2, padx=5)

        rain_chance_label = tkinter.Label(forecast_frame, text=f"{hour}%")
        rain_chance_label.grid(row=hour, column=3, padx=5)

def load_daily_data():
    # Clear current data
    for widget in forecast_frame.winfo_children():
        widget.destroy()

    # Sample daily data
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        day_label = tkinter.Label(forecast_frame, text=day)
        day_label.grid(row=i, column=0, sticky='w', padx=(10, 0))

        temp_label = tkinter.Label(forecast_frame, text=f"{70 + i}°F")
        temp_label.grid(row=i, column=1, padx=5)

        condition_label = tkinter.Label(forecast_frame, text="Sunny")
        condition_label.grid(row=i, column=2, padx=5)

        rain_chance_label = tkinter.Label(forecast_frame, text=f"{10 * i}%")
        rain_chance_label.grid(row=i, column=3, padx=5)


# Modify the select_forecast function
def select_forecast(forecast_type):
    if forecast_type == "hourly":
        hourly_button.configure(fg_color="#4da6ff")  # Highlighted color for the selected button
        daily_button.configure(fg_color="#F0F0F0")   # Default color for the unselected button
        load_hourly_data()  # Load and display hourly data
    elif forecast_type == "daily":
        daily_button.configure(fg_color="#4da6ff")   # Highlighted color for the selected button
        hourly_button.configure(fg_color="#F0F0F0")  # Default color for the unselected button
        load_daily_data()   # Load and display daily data

# Initially select 'Hourly' forecast
select_forecast("hourly")


# Run as loop to stay open
app.mainloop()