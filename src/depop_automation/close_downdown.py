# utils/menus.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def close_dropdowns(driver, presses: int = 2, delay: float = 0.05):
    """Close any open menus by sending ESC to the page body."""
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(presses):
        body.send_keys(Keys.ESCAPE)
        if delay:
            time.sleep(delay)
