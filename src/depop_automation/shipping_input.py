from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def select_shipping(driver, category, subcategory, timeout=15):
    wait = WebDriverWait(driver, timeout)
    if category == "Tops":
        if subcategory == "T-shirts":
            price = 6.5
        price = 7.5
    elif category == "Bottoms":
        if subcategory == "Shorts":
            price = 6.5
        price = 7.5
    elif category == "Coats and jackets":
        price = 8.5
    elif category == "Footwear":
        price = 9.0
    else:
        price = 12.0
    # 1) Close any open menus that might intercept clicks
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.05)
    except Exception:
        pass

    # 2) Select "Other" (manual) shipping
    manual_radio = wait.until(EC.presence_of_element_located((By.ID, "manual__shipping")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'})", manual_radio)
    driver.execute_script("arguments[0].click()", manual_radio)

    # Fallback: click the label if needed
    if not manual_radio.is_selected():
        label = driver.find_element(By.ID, "manual__shipping__label")
        driver.execute_script("arguments[0].click()", label)

    # 3) Fill the price field (appears after selecting manual)
    cost = wait.until(EC.element_to_be_clickable((By.ID, "nationalShippingCost__input")))
    cost.click()
    cost.send_keys(Keys.CONTROL, "a")
    cost.send_keys(Keys.DELETE)
    cost.send_keys(str(price))