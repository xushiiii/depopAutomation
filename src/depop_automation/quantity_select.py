from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_quantity(driver, qty: int, timeout: int = 15):
    """
    Sets the numeric Quantity field next to Size.
    """
    wait = WebDriverWait(driver, timeout)
    qty_inp = wait.until(EC.element_to_be_clickable((By.ID, "quantity__input")))
    qty_inp.clear()
    qty_inp.send_keys(str(qty))