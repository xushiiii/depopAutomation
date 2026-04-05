import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

# False: kill Edge, launch a new window with your profile (original behavior).
# True: attach to Edge you already started — see EDGE_REMOTE_DEBUG_PORT below.
ATTACH_TO_EXISTING_EDGE = False

# When ATTACH_TO_EXISTING_EDGE is True, start Edge yourself with remote debugging, e.g.:
#   "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222
# (Or create a desktop shortcut with that flag in Target.) Then run the script.
# Normal “open Edge from taskbar” does not expose this port; the script cannot attach without it.
EDGE_REMOTE_DEBUG_PORT = 9222

# LAPTOP Use your existing Edge user-data so you stay logged in:
EDGE_USER_DATA_DIR = r"C:\Users\taylo\AppData\Local\Microsoft\Edge\User Data"
EDGE_PROFILE_DIR   = "Default"

#EDGE_USER_DATA_DIR = r"C:\Users\Taylor Xu\AppData\Local\Microsoft\Edge\User Data"
#EDGE_PROFILE_DIR   = "Default"

# DESKTOP Path to your local msedgedriver (manual installation)
#EDGE_DRIVER_PATH   = r"C:\Users\Taylor Xu\Downloads\edgedriver_win64 (2)\msedgedriver.exe"

# LAPTOP Path to your local msedgedriver (manual installation)
EDGE_DRIVER_PATH   = r"C:\Users\taylo\Downloads\edgedriver_win64 (1)\msedgedriver.exe"

def get_driver():
    if not ATTACH_TO_EXISTING_EDGE:
        subprocess.run('taskkill /F /IM msedge.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run('taskkill /F /IM msedgedriver.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Profile + Edge processes need a moment; too short → next launch can sit on loading
        time.sleep(4)

    edge_options = Options()
    # Depop is a heavy SPA; default "normal" waits for full load and can hit
    # "Timed out receiving message from renderer". We wait for real elements in open_create_page.
    edge_options.page_load_strategy = "none"

    if ATTACH_TO_EXISTING_EDGE:
        edge_options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{EDGE_REMOTE_DEBUG_PORT}"
        )
    else:
        edge_options.add_argument(f"user-data-dir={EDGE_USER_DATA_DIR}")
        edge_options.add_argument(f"profile-directory={EDGE_PROFILE_DIR}")

        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")

        # Reduce Chromium / DevTools noise
        edge_options.add_argument("--log-level=3")
        edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Silence msedgedriver logs (Selenium version dependent)
    try:
        service = Service(EDGE_DRIVER_PATH, log_output=os.devnull)
    except TypeError:
        service = Service(EDGE_DRIVER_PATH, log_path=os.devnull)

    driver = webdriver.Edge(service=service, options=edge_options)

    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)
    if not ATTACH_TO_EXISTING_EDGE:
        driver.maximize_window()
    return driver
