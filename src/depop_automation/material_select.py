from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def select_material(driver, labels, timeout=15):
    base = "attributes.material"
    wait = WebDriverWait(driver, timeout)

    # Scroll the button into view and click using JavaScript to avoid header overlap
    button = wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'smooth'})", button)
    time.sleep(0.3)  # Brief pause after scroll to ensure page has settled
    driver.execute_script("arguments[0].click()", button)
    wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))

    for label in labels[:4]:
        xpath = f"//ul[@id='{base}-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
        opt = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", opt)
        driver.execute_script("arguments[0].click()", opt)

        # keep menu open for next pick
        try:
            wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))
        except Exception:
            button = wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button")))
            driver.execute_script("arguments[0].click()", button)
            wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))
