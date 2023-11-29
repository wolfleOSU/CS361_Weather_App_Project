import tkinter
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk

class Settings:
    def __init__(self, frame, data_loader):
        self.c_clicked = False
        self.f_clicked = True
        self.w_clicked = False
        self.co_clicked = True

        self.data_loader = data_loader

        self.celsius_btn = ctk.CTkButton(frame, text="Celsius", command=self.celsius_clicked, corner_radius=10)
        self.celsius_btn.grid(row=0,column=0, padx=5, pady=5)

        self.fahrenheit_btn = ctk.CTkButton(frame, text="Fahrenheit", command=self.fahrenheit_clicked, corner_radius=10)
        self.fahrenheit_btn.grid(row=0,column=0, padx=5, pady=5)

        self.warm_btn = ctk.CTkButton(frame, text="Warm", command=self.warm_clicked, corner_radius=10)
        self.warm_btn.grid(row=1,column=0, padx=5, pady=5)

        self.cool_btn = ctk.CTkButton(frame, text="Cool", command=self.cool_clicked, corner_radius=10)
        self.cool_btn.grid(row=1,column=0, padx=5, pady=5)

        self.toggle_button(self.celsius_btn, self.c_clicked)
        self.toggle_button(self.fahrenheit_btn, self.f_clicked)
        self.toggle_button(self.warm_btn, self.w_clicked)
        self.toggle_button(self.cool_btn, self.co_clicked)


    def toggle_button(self, button, is_clicked):
        if not is_clicked:
            button.grid()
        else:
            button.grid_remove()

    def celsius_clicked(self):
        self.c_clicked = not self.c_clicked
        self.f_clicked = not self.f_clicked
        self.data_loader.unit = "C"
        self.data_loader.update_current()
        self.toggle_button(self.celsius_btn, self.c_clicked)
        self.toggle_button(self.fahrenheit_btn, self.f_clicked)

    def fahrenheit_clicked(self):
        self.f_clicked = not self.f_clicked
        self.c_clicked = not self.c_clicked
        self.data_loader.unit = "F"
        self.data_loader.update_current()
        self.toggle_button(self.fahrenheit_btn, self.f_clicked)
        self.toggle_button(self.celsius_btn, self.c_clicked)

    def warm_clicked(self):
        self.w_clicked = not self.w_clicked
        self.co_clicked = not self.w_clicked
        ctk.set_appearance_mode("light")
        self.toggle_button(self.warm_btn, self.w_clicked)
        self.toggle_button(self.cool_btn, self.co_clicked)
        

    def cool_clicked(self):
        self.co_clicked = not self.co_clicked
        self.w_clicked = not self.co_clicked
        ctk.set_appearance_mode("dark")
        self.toggle_button(self.cool_btn, self.co_clicked)
        self.toggle_button(self.warm_btn, self.w_clicked)
        
