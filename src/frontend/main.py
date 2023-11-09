import tkinter as tk

def get_weather():
    # Dummy weather fetching function
    weather_label.config(text="Sunny, 25°C")

# Main application window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

# Title label
title_label = tk.Label(root, text="Weather App", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Entry for location
location_entry = tk.Entry(root)
location_entry.grid(row=1, column=0, padx=10, pady=10)

# Button to fetch weather
fetch_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
fetch_weather_button.grid(row=1, column=1, padx=10)

# Label to display weather
weather_label = tk.Label(root, text="Please enter a location to see the weather.")
weather_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Status bar
status_label = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E)

# Run the application
root.mainloop()
