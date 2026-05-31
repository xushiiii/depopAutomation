import gspread 
from google.oauth2.service_account import Credentials

from selenium.webdriver.edge.options import Options

from src.machine_paths import get_paths

edge_options = Options()
edge_options.use_chromium = True  

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]

# Lazy initialization to avoid import-time errors
_client = None
_sheet = None
_cached_machine = None


def reset_sheets_client() -> None:
    """Clear cached client when desktop/laptop selection changes."""
    global _client, _sheet, _cached_machine
    _client = None
    _sheet = None
    _cached_machine = None


def _get_sheet():
    """Lazy initialization of Google Sheets client and sheet."""
    global _client, _sheet, _cached_machine
    from src.machine_paths import get_machine

    machine = get_machine()
    if _sheet is None or _cached_machine != machine:
        service_account_file = get_paths().service_account_file
        credentials = Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
        _client = gspread.authorize(credentials)
        _sheet = _client.open("Reselling").sheet1
        _cached_machine = machine
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
        
        sheet.batch_update([
            {"range": f"A{next_row}", "values": [[description]]},
            {"range": f"C{next_row}", "values": [[category]]},
            {"range": f"D{next_row}", "values": [[location]]},
            {"range": f"H{next_row}", "values": [[price_float]]},
        ])


        print(f"[Sheets] Successfully wrote row {next_row} to Google Sheets")
    except Exception as e:
        print(f"[Sheets] Error writing to Google Sheets: {e}")
        raise
