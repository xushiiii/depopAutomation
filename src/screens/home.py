# src/screens/home.py

import tkinter as tk 
from tkinter import filedialog 

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):

        super().__init__(parent)
        self.controller = controller 

        tk.Label(
            self, 
            text="Home",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(60, 20))

        tk.Button(
            self, 
            text = "Create a Listing",
            font=("Segoe UI", 12),
            width = 26, 
            command = lambda:controller.show("ListingScreen")
        ).pack(pady=10)

        tk.Button(
            self, 
            text = "Upload Earnings Report",
            font = ("Segoe UI", 12), 
            width = 26,
            command = lambda:controller.show("EarningsScreen")
        ).pack(pady=10)