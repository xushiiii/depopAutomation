import tkinter as tk 
from tkinter import filedialog, messagebox 
from src.earnings_automation.ebay.sheets import report_earnings 
from src.earnings_automation.depop.sheets import report_depop_earnings
from src.earnings_automation.pirateship.sheets import track_pirateship
class EarningsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.ebay_path = None
        self.depop_path = None
        self.pirateship_path = None
        top = tk.Frame(self)
        top.pack(fill="x")

        tk.Button(
            top, 
            text= "Back", 
            command=lambda: controller.show("HomeScreen")
        ).pack(side="left", padx=10, pady=10)

        tk.Label(
            self, 
            text = "Upload eBay Earnings Report",
            font = ("Segoe UI", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            self,
            text = "Choose CSV",
            width=20, 
            command=self.choose_ebay_csv 
        ).pack(pady=10)
        
        self.ebay_path_label = tk.Label(
            self,
            text="No file selected",
            fg="gray",
            font=("Segoe UI", 9)
        )
        self.ebay_path_label.pack(pady=(0, 10))
        
        tk.Button(
            self,
            text="Process / Upload",
            width=20,
            command=self.process_ebay_report
        ).pack(pady=10)


        tk.Label(
            self, 
            text = "Upload Depop Earnings Report",
            font = ("Segoe UI", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            self,
            text = "Choose CSV",
            width=20, 
            command=self.choose_depop_csv 
        ).pack(pady=10)

        self.depop_path_label = tk.Label(
            self,
            text="No file selected",
            fg="gray",
            font=("Segoe UI", 9)
        )
        self.depop_path_label.pack(pady=(0, 10))

        tk.Button(
            self,
            text="Process / Upload",
            width=20,
            command=self.process_depop_report
        ).pack(pady=10)

        tk.Label(
            self, 
            text = "Upload PirateShip Shipping Report",
            font = ("Segoe UI", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            self,
            text = "Choose CSV",
            width=20, 
            command=self.choose_pirateship_csv 
        ).pack(pady=10)

        self.pirateship_path_label = tk.Label(
            self,
            text="No file selected",
            fg="gray",
            font=("Segoe UI", 9)
        )
        self.pirateship_path_label.pack(pady=(0, 10))

        tk.Button(
            self,
            text="Process / Upload",
            width=20,
            command=self.process_pirateship_report
        ).pack(pady=10)

    def choose_ebay_csv(self):
        path = filedialog.askopenfilename(
            title = "Select eBay earnings CSV", 
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return 
        self.ebay_path = path 
        self.ebay_path_label.config(text=path, fg="black")
        print(f"Selected eBay path: {path}")

    def choose_depop_csv(self):
        path = filedialog.askopenfilename(
            title = "Select Depop earnings CSV", 
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return 
        self.depop_path = path 
        self.depop_path_label.config(text=path, fg="black")
        print(f"Selected Depop path: {path}")

    def choose_pirateship_csv(self):
        path = filedialog.askopenfilename(
            title = "Select PirateShip shipping CSV", 
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return 
        self.pirateship_path = path 
        self.pirateship_path_label.config(text=path, fg="black")
        print(f"Selected PirateShip path: {path}")

    def process_ebay_report(self):
        if not self.ebay_path:
            messagebox.showwarning("No file selected", "Please choose an eBay CSV file first.")
            return

        try:
            report_earnings(self.ebay_path)
            messagebox.showinfo("Done", "eBay earnings report processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process eBay report:\n{e}")

    def process_depop_report(self):
        if not self.depop_path:
            messagebox.showwarning("No file selected", "Please choose a Depop CSV file first.")
            return

        try:
            report_depop_earnings(self.depop_path)
            messagebox.showinfo("Done", "Depop earnings report processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process Depop report:\n{e}")

    def process_pirateship_report(self):
        if not self.pirateship_path:
            messagebox.showwarning("No file selected", "Please choose a PirateShip CSV file first.")
            return
        try:
            track_pirateship(self.pirateship_path)
            messagebox.showinfo("Done", "PirateShip shipping report processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process PirateShip report:\n{e}")
