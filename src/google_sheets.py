import gspread 
from google.oauth2.service_account import Credentials

from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.use_chromium = True  

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
#DESKTOP
#SERVICE_ACCOUNT_FILE = "C:\\Users\\Taylor Xu\\Downloads\\resellingautomation-1044349da8d8.json"  

#LAPTOP
SERVICE_ACCOUNT_FILE = r"C:\Users\taylo\Downloads\resellingautomation-7a1c1c833f65.json"

# Lazy initialization to avoid import-time errors
_client = None
_sheet = None

def _get_sheet():
    """Lazy initialization of Google Sheets client and sheet."""
    global _client, _sheet
    if _sheet is None:
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        _client = gspread.authorize(credentials)
        _sheet = _client.open("Reselling").sheet1
    return _sheet

def write_to_sheets(price, description, location, category, subcategory):
    try:
        # Validate inputs
        if not price or not description:
            print("[Sheets] Missing required fields (price or description)")
            return
        
        sheet = _get_sheet()
        price_float = float(price)
        col_values = sheet.col_values(1)
        next_row = len(col_values) + 1
        
        # Handle category mapping
        if category == "Footwear":
            category = "Shoes"
        if category == "Tops":
            if subcategory != "T-shirts" and subcategory != "Other":
                category = "Midlayer"
        
        # Ensure all values are strings/numbers (handle None)
        description = description or ""
        category = category or ""
        location = location or ""
        
        sheet.update(range_name=f"A{next_row}:D{next_row}", values=[[description, category, location, price_float]])
        print(f"[Sheets] Successfully wrote row {next_row} to Google Sheets")
    except Exception as e:
        print(f"[Sheets] Error writing to Google Sheets: {e}")
        raise
