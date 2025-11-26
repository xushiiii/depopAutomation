from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def select_brand(driver, brand_name: str, timeout: int = 15, type_delay: float = 0.06):
    wait = WebDriverWait(driver, timeout)
    base = "brand"

    # focus + clear
    inp = wait.until(EC.element_to_be_clickable((By.ID, f"{base}-input")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'})", inp)
    inp.click()
    inp.send_keys(Keys.CONTROL, "a")
    inp.send_keys(Keys.DELETE)

    # type slowly to avoid dropped keystrokes (e.g., "Nike" becoming "ie")
    for ch in brand_name:
        inp.send_keys(ch)
        time.sleep(type_delay)

    # make sure the suggestions menu is open
    try:
        wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))
    except Exception:
        try:
            driver.find_element(By.ID, f"{base}-toggle-button").click()
            wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))
        except Exception:
            pass  # if the menu still doesn't show, ArrowDown may still select first item if available

    # always choose the first suggestion with ArrowDown + Enter
    inp.send_keys(Keys.ARROW_DOWN)
    inp.send_keys(Keys.ENTER)

    # close the menu and blur so focus leaves the Brand field
    try:
        inp.send_keys(Keys.ESCAPE)
    except Exception:
        pass
    try:
        toggle = driver.find_element(By.ID, f"{base}-toggle-button")
        if toggle.get_attribute("aria-expanded") == "true":
            toggle.click()
    except Exception:
        pass
    # hard blur to prevent subsequent keys going into Brand
    try:
        driver.execute_script("document.activeElement && document.activeElement.blur();")
    except Exception:
        pass
