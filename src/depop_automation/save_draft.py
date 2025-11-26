# draft_click.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_save_draft(driver, timeout: int = 15):
    """
    Clicks the 'Save as a draft' button.
    """
    wait = WebDriverWait(driver, timeout)
    btn = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[@type='submit'][.//span[normalize-space()='Save as a draft']]"
    )))
    btn.click()
