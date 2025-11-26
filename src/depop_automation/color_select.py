# color_select.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_colors(driver, labels, timeout: int = 15, max_select: int = 2):
    """
    Select up to `max_select` colors by visible text: e.g. ["Black", "Blue"].
    Default max is 2 (matches the UI note). Set to 3 if your form allows three.
    """
    base = "colour"
    wait = WebDriverWait(driver, timeout)

    # open dropdown
    wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))

    for label in labels[:max_select]:
        opt_xpath = f"//ul[@id='{base}-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
        opt = wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", opt)
        driver.execute_script("arguments[0].click()", opt)

        # keep the menu open between picks (reopen if it closes)
        try:
            wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))
        except Exception:
            wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))

    # optional: close dropdown
    try:
        driver.find_element(By.ID, f"{base}-toggle-button").click()
    except Exception:
        pass
