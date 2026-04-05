from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CREATE_URL = "https://www.depop.com/products/create"


def open_create_page(driver):
    # First navigation after a fresh Edge+profile launch sometimes times out; one retry usually clears it.
    for attempt in range(2):
        try:
            driver.get(CREATE_URL)
            break
        except TimeoutException:
            if attempt == 0:
                time.sleep(2)
                continue
            raise
    # Wait for any key element to ensure the app loaded (description or category input)
    WebDriverWait(driver, 60).until(
        EC.any_of(
            EC.presence_of_element_located((By.ID, "description")),
            EC.presence_of_element_located((By.ID, "group-input"))
        )
    )
