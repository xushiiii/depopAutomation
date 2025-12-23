import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

# LAPTOP Use your existing Edge user-data so you stay logged in:
EDGE_USER_DATA_DIR = r"C:\Users\taylo\AppData\Local\Microsoft\Edge\User Data"
EDGE_PROFILE_DIR   = "Default"

# LAPTOP Path to your local msedgedriver (manual installation)
EDGE_DRIVER_PATH   = r"C:\Users\taylo\Downloads\edgedriver_win64 (1)\msedgedriver.exe"

def get_driver():
    subprocess.run('taskkill /F /IM msedge.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('taskkill /F /IM msedgedriver.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    edge_options = Options()

    edge_options.add_argument(f"user-data-dir={EDGE_USER_DATA_DIR}")
    edge_options.add_argument(f"profile-directory={EDGE_PROFILE_DIR}")

    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    # ✅ Reduce Chromium / DevTools noise
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # ✅ Silence msedgedriver logs (Selenium version dependent)
    try:
        service = Service(EDGE_DRIVER_PATH, log_output=os.devnull)
    except TypeError:
        service = Service(EDGE_DRIVER_PATH, log_path=os.devnull)

    driver = webdriver.Edge(service=service, options=edge_options)

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver
