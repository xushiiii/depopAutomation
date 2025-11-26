# attributes_select.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def _pick_from_dropdown(driver, base_id: str, labels, max_select: int, timeout: int = 15):
    """
    Generic picker for these Depop selects.
    base_id is the prefix (e.g. 'source', 'age', 'style').
    """
    wait = WebDriverWait(driver, timeout)

    # open dropdown
    wait.until(EC.element_to_be_clickable((By.ID, f"{base_id}-toggle-button"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, f"{base_id}-menu")))

    for label in labels[:max_select]:
        opt_xpath = f"//ul[@id='{base_id}-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
        opt = wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", opt)
        driver.execute_script("arguments[0].click()", opt)

        # keep the menu visible between picks (some UIs close after each click)
        try:
            wait.until(EC.visibility_of_element_located((By.ID, f"{base_id}-menu")))
        except Exception:
            wait.until(EC.element_to_be_clickable((By.ID, f"{base_id}-toggle-button"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, f"{base_id}-menu")))

    # optional: close dropdown (safe to ignore failures)
    try:
        driver.find_element(By.ID, f"{base_id}-toggle-button").click()
    except Exception:
        pass
