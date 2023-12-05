import tkinter
import customtkinter as ctk

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
