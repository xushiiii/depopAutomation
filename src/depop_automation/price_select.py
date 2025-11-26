# price_select.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_price(driver, amount, timeout: int = 15):
    """
    Sets the Item price (number). Accepts int/float/str.
    """
    wait = WebDriverWait(driver, timeout)
    price = wait.until(EC.element_to_be_clickable((By.ID, "priceAmount__input")))
    price.click()
    price.send_keys(Keys.CONTROL, "a")
    price.send_keys(Keys.DELETE)
    price.send_keys(str(amount))

    # verify
    val = wait.until(EC.visibility_of_element_located((By.ID, "priceAmount__input"))).get_attribute("value") or ""
    assert val != "" and float(val) >= 0, f"Price not set. Got '{val}'"
