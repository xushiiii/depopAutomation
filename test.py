from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import subprocess
import time

# ----------- CONFIG -----------
# Pick the subcategory you want to test:
TEST_SUBCATEGORY = "T-shirts"   # e.g., "T-shirts", "Hoodies", "Sweatshirts", etc.

# Use your existing Edge user-data so you stay logged in:
EDGE_USER_DATA_DIR = r"C:\Users\Taylor Xu\AppData\Local\Microsoft\Edge\User Data"
EDGE_PROFILE_DIR   = "Default"

# Path to your local msedgedriver (keeps it simple; no webdriver-manager dependency)
EDGE_DRIVER_PATH   = r"C:\Users\Taylor Xu\Downloads\edgedriver_win64\msedgedriver.exe"
# --------------------------------


def get_driver():
    # Kill any running Edge/EdgeDriver so we start clean (same as your main)
    subprocess.run('taskkill /F /IM msedge.exe', shell=True)
    subprocess.run('taskkill /F /IM msedgedriver.exe', shell=True)

    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument(f"user-data-dir={EDGE_USER_DATA_DIR}")
    edge_options.add_argument(f"profile-directory={EDGE_PROFILE_DIR}")

    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.maximize_window()
    return driver


def open_create_page(driver):
    driver.get("https://www.depop.com/products/create")
    # Wait for any key element to ensure the app loaded (description or category input)
    WebDriverWait(driver, 20).until(
        EC.any_of(
            EC.presence_of_element_located((By.ID, "description")),
            EC.presence_of_element_located((By.ID, "group-input"))
        )
    )


def pick_category_men_tops(driver):
    """
    Opens the Category dropdown and selects 'Men - Tops' (group-item-0).
    This mirrors your current approach and keeps the test isolated.
    """
    wait = WebDriverWait(driver, 15)

    # Open category dropdown
    toggle = wait.until(EC.element_to_be_clickable((By.ID, "group-toggle-button")))
    toggle.click()
    # Wait for it to be open
    wait.until(lambda d: d.find_element(By.ID, "group-toggle-button").get_attribute("aria-expanded") == "true")
    wait.until(EC.visibility_of_element_located((By.ID, "group-menu")))

    # Click Men - Tops (id: group-item-0 in your markup)
    option = wait.until(EC.element_to_be_clickable((By.ID, "group-item-0")))
    option.click()

    # Verify Category input shows Men - Tops
    val = wait.until(EC.visibility_of_element_located((By.ID, "group-input"))).get_attribute("value") or ""
    assert val.strip() == "Men - Tops", f"Category not set correctly. Got '{val}'"
    print("[OK] Category selected: Men - Tops")


def pick_subcategory_by_click(driver, label: str):
    """
    Open Subcategory dropdown and click the exact option by text.
    """
    wait = WebDriverWait(driver, 15)

    # Open subcategory dropdown
    wait.until(EC.element_to_be_clickable((By.ID, "productType-toggle-button"))).click()
    # Wait for open + visible
    wait.until(lambda d: d.find_element(By.ID, "productType-toggle-button").get_attribute("aria-expanded") == "true")
    wait.until(EC.visibility_of_element_located((By.ID, "productType-menu")))

    # Click the option by visible <p> text
    opt_xpath = f"//ul[@id='productType-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
    wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath))).click()

    # Verify
    val = wait.until(EC.visibility_of_element_located((By.ID, "productType-input"))).get_attribute("value") or ""
    assert val.strip() == label, f"Subcategory not set correctly. Expected '{label}', got '{val}'"
    print(f"[OK] Subcategory selected: {label}")


def pick_subcategory_by_typing(driver, label: str):
    """
    Type into the Subcategory combobox and press Enter.
    Use this if you prefer keyboard-only.
    """
    wait = WebDriverWait(driver, 15)
    inp = wait.until(EC.element_to_be_clickable((By.ID, "productType-input")))
    inp.click()
    inp.send_keys(Keys.CONTROL, "a")
    inp.send_keys(Keys.DELETE)
    inp.send_keys(label)
    inp.send_keys(Keys.ENTER)

    # Verify
    val = wait.until(EC.visibility_of_element_located((By.ID, "productType-input"))).get_attribute("value") or ""
    assert val.strip() == label, f"Subcategory not set correctly. Expected '{label}', got '{val}'"
    print(f"[OK] Subcategory selected (typed): {label}")


def main():
    driver = get_driver()
    try:
        open_create_page(driver)

        # Ensure Category is set to Men - Tops first (so the subcategory list matches your HTML)
        pick_category_men_tops(driver)

        # --- Choose ONE of the following two helpers ---

        # 1) Click the option in the dropdown (recommended)
        pick_subcategory_by_click(driver, TEST_SUBCATEGORY)

        # 2) Or: type and press Enter (keyboard-only)
        #pick_subcategory_by_typing(driver, TEST_SUBCATEGORY)

        # Pause briefly so you can see the result before the window closes
        time.sleep(3)

    finally:
        # Comment this out if you want to keep the browser open
        driver.quit()


if __name__ == "__main__":
    main()
