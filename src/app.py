import tkinter as tk 

from src.screens.home import HomeScreen 
from src.screens.listing import ListingScreen
from src.screens.earnings import EarningsScreen 

class App(tk.Tk):

    def __init__(self, *, create_depop_draft, upload_earnings):

        super().__init__()
        self.create_depop_draft = create_depop_draft
        self.upload_earnings = upload_earnings 

        self.title("Reselling Automation")
        self.geometry("1200x700")

        container = tk.Frame(self)
        container.pack(fill="both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight=1)
        self.screens = {}

        for Scrn in (HomeScreen, ListingScreen, EarningsScreen):
            screen = Scrn(parent = container, controller=self) 
            screen.grid(row = 0, column = 0, sticky="nsew")
            self.screens[Scrn.__name__] = screen 

        self.show("HomeScreen")

    def show(self, screen_name: str):
        screen = self.screens[screen_name]
        screen.tkraise()

        if hasattr(screen, "on_show"):
            screen.on_show()
    
def run_app(*, create_depop_draft, upload_earnings):
    app = App(create_depop_draft = create_depop_draft, upload_earnings = upload_earnings)
    app.mainloop()

