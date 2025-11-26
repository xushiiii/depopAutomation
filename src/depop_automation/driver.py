from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import subprocess
from selenium import webdriver
import time
# Use your existing Edge user-data so you stay logged in:
EDGE_USER_DATA_DIR = r"C:\Users\Taylor Xu\AppData\Local\Microsoft\Edge\User Data"
EDGE_PROFILE_DIR   = "Default"

# Path to your local msedgedriver (manual installation)
EDGE_DRIVER_PATH   = r"C:\Users\Taylor Xu\Downloads\edgedriver_win64 (1)\msedgedriver.exe"
# --------------------------------
def get_driver():
    # Terminate any existing Edge/EdgeDriver instances when starting a new listing
    # This ensures a clean state for each new listing session
    subprocess.run('taskkill /F /IM msedge.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('taskkill /F /IM msedgedriver.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for processes to fully terminate before starting new session
    time.sleep(2)

    edge_options = Options()
    # Remove deprecated use_chromium - Edge is Chromium by default now
    edge_options.add_argument(f"user-data-dir={EDGE_USER_DATA_DIR}")
    edge_options.add_argument(f"profile-directory={EDGE_PROFILE_DIR}")
    # Add options to prevent hanging and improve stability
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=edge_options)
    # Set timeouts to prevent indefinite hanging
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver
