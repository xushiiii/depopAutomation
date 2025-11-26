from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_occasion(driver, labels, timeout=15):
    """
    Select up to 3 occasions by visible text, e.g. ["Casual","Work","Winter"].
    """
    base = "attributes.occasion"
    wait = WebDriverWait(driver, timeout)

    # open dropdown
    wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))

    for label in labels[:3]:
        opt_xpath = f"//ul[@id='{base}-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
        opt = wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", opt)
        driver.execute_script("arguments[0].click()", opt)

        # keep menu open if it closes between picks
        try:
            wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))
        except Exception:
            wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))

    # optional: close
    try:
        driver.find_element(By.ID, f"{base}-toggle-button").click()
    except Exception:
        pass
