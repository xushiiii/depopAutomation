from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import subprocess
import time

# ---------- PC CONFIG (commented out) ----------
# TEST is for "Women > Jumpers"
# EDGE_USER_DATA_DIR = r"C:\Users\Taylor Xu\AppData\Local\Microsoft\Edge\User Data"
# EDGE_PROFILE_DIR   = "Default"
# EDGE_DRIVER_PATH   = r"C:\Users\Taylor Xu\Downloads\edgedriver_win64\msedgedriver.exe"
# ------------------------------------------------

# ---------- LAPTOP CONFIG ----------
EDGE_USER_DATA_DIR = r"C:\Users\taylo\AppData\Local\Microsoft\Edge\User Data"
EDGE_PROFILE_DIR   = "Default"
EDGE_DRIVER_PATH   = r"C:\Users\taylo\Downloads\edgedriver_win64 (1)\msedgedriver.exe"
# ----------------------------------


def get_driver():
    # Start clean - suppress errors if processes don't exist
    subprocess.run('taskkill /F /IM msedge.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('taskkill /F /IM msedgedriver.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for processes to fully terminate before starting new session
    time.sleep(2)

    edge_options = Options()
    # Edge is Chromium by default, no need for use_chromium
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


def open_create_page(driver):
    driver.get("https://www.depop.com/products/create")
    # Wait for description OR category input so we know the page is ready
    WebDriverWait(driver, 20).until(
        EC.any_of(
            EC.presence_of_element_located((By.ID, "description")),
            EC.presence_of_element_located((By.ID, "group-input")),
        )
    )


def select_women_jumpers(driver):
    """
    Open the 'Category' combobox and select the 'Women > Jumpers' option.

    Assumptions:
    - The HTML structure matches what you pasted (section headers like 'Women > ...').
    - The visible option text for the item is exactly 'Jumpers'.
      If Depop uses something like 'Jumpers & cardigans', change the label below.
    """
    wait = WebDriverWait(driver, 15)

    # Open the Category dropdown
    toggle = wait.until(EC.element_to_be_clickable((By.ID, "group-toggle-button")))
    toggle.click()

    # Wait until it's really open
    wait.until(
        lambda d: d.find_element(By.ID, "group-toggle-button")
        .get_attribute("aria-expanded")
        == "true"
    )
    wait.until(EC.visibility_of_element_located((By.ID, "group-menu")))

    # ---- XPATH logic ----
    # We:
    # 1. Find a <div> block under <ul id="group-menu"> whose section header contains "Women"
    # 2. Inside that block, click the <li> whose <p> text is exactly "Jumpers"
    #
    # If the option label is "Jumpers & cardigans" or similar, update 'Jumpers' below.
    WOMEN_JUMPERS_LABEL = "Jumpers"

    women_jumpers_xpath = (
        "//ul[@id='group-menu']"
        "//div[.//p[contains(normalize-space(), 'Women')]]"
        "//li[@role='option'][.//p[normalize-space()='{label}']]"
    ).format(label=WOMEN_JUMPERS_LABEL)

    option_el = wait.until(EC.element_to_be_clickable((By.XPATH, women_jumpers_xpath)))
    option_el.click()

    # Check what the input now thinks is selected
    value = (
        wait.until(EC.visibility_of_element_located((By.ID, "group-input")))
        .get_attribute("value")
        or ""
    )
    print(f"[DEBUG] group-input value after selection: '{value}'")


def main():
    driver = get_driver()
    try:
        open_create_page(driver)
        select_women_jumpers(driver)

        # Just to see it before the script ends
        time.sleep(4)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
