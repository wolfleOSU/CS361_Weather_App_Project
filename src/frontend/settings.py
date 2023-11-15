import tkinter
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk

class settings:
    def __init__(self):
        #initialize settings
        #fill in default settings
        #create display boxes for settings

        self.celsius_btn = ctk.CTkButton(self, text="Celsius", command=self.celsius_clicked, corner_radius=10)
        self.celsius_btn.pack()

        self.fahrenheit_btn = ctk.CTkButton(self, text="Fahrenheit", command=self.fahrenheit_clicked, corner_radius=10)
        self.fahrenheit_btn.pack()

        self.warm_btn = ctk.CTkButton(self, text="Warm", command=self.warm_clicked, corner_radius=10)
        self.warm_btn.pack()

        self.cool_btn = ctk.CTkButton(self, text="Cool", command=self.cool_clicked, corner_radius=10)
        self.cool_btn.pack()


    def celsius_clicked(self, isclicked):
        #function for when celsius button is clicked
        #runs when button is clicked and should change values to celsius
        1+1
    
    def fahrenheit_clicked(self, isclicked):
        #function for when fahrenheit button is clicked
        #runs when button is clicked and should change values to fahrenheit
        1+1
    
    def warm_clicked(self, isclicked):
        #function for when warm setting is clicked
        #runs when button is clicked and should change the theme to warm
        1+1
    
    def cool_clicked(self, isclicked):
        #functions for when cool setting is clicked
        #runs when button is clicked and should change the theme to cool
        1+1


app = ctk.CTk()
app.geometry("720x480")
app.title("The Weather App")

test = settings()