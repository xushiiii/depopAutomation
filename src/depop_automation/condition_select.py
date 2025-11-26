from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def select_condition(driver, label="Brand new", timeout=15):
    wait = WebDriverWait(driver, timeout)

    # clear any open overlays
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.05)
    except Exception:
        pass

    # open dropdown
    wait.until(EC.element_to_be_clickable((By.ID, "condition-toggle-button"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "condition-menu")))

    # click the option (case-insensitive)
    target = label.strip().lower()
    xpath = (
        "//ul[@id='condition-menu']"
        "//li[@role='option'][.//p[translate(normalize-space(.),"
        " 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')="
        f"'{target}']]"
    )
    opt = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'})", opt)
    driver.execute_script("arguments[0].click()", opt)

    # collapse so it doesn't block the next fields
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    except Exception:
        pass
