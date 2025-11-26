# size_quantity.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_size(driver, label: str, timeout: int = 15):
    """
    Selects a size by its visible text (e.g., 'M', 'XL', 'One size', 'Other').
    """
    base = "variants"
    wait = WebDriverWait(driver, timeout)

    # open dropdown
    wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))

    # click the option
    opt_xpath = f"//ul[@id='{base}-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
    opt = wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'})", opt)
    driver.execute_script("arguments[0].click()", opt)

    # verify the input shows the selected value
    val = (wait.until(EC.visibility_of_element_located((By.ID, f"{base}-input")))
              .get_attribute("value") or "").strip()
    assert val == label, f"Size not set. Expected '{label}', got '{val}'"
