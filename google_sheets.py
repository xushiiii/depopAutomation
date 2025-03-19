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
SERVICE_ACCOUNT_FILE = "C:\\Users\\taylo\\source\\depopAutomation\\resellingautomation-9c38ccc65a6d.json"

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open("Reselling").sheet1  
def write_to_sheets(price, description):
    price_float = float(price)
    col_values = sheet.col_values(1)
    next_row = len(col_values) + 1
    sheet.update(range_name=f"A{next_row}:B{next_row}", values=[[description, price_float]])
