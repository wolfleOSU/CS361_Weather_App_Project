import tkinter as tk

def get_weather():
    # Dummy weather fetching function
    weather_label.config(text="Sunny\n25°C", font=("Helvetica", 20))

# Main application window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

# Set the grid weight for the columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


# Title label with background color
title_label = tk.Label(root, text="Weather App", font=("Helvetica", 24), bg="blue", fg="white")
title_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Entry for location - expanded and centered
location_entry = tk.Entry(root, font=("Helvetica", 16), width=20)
location_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

# Button to fetch weather - made larger
fetch_weather_button = tk.Button(root, text="Get Weather", font=("Helvetica", 16), command=get_weather, width=10)
fetch_weather_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# Label to display weather - font size increased for future updates
weather_label = tk.Label(root, text="Please enter a location to see the weather.", font=("Helvetica", 16))
weather_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

# Make the window's grid expandable
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(1, weight=1)

# Status bar at the bottom of the page - made to fill the width
status_label = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.grid(row=5, column=0, columnspan=2, sticky="we", padx=10)

root.mainloop()
