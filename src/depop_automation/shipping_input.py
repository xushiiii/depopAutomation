from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def _select_small_package_size(driver, wait: WebDriverWait, type_delay: float = 0.07):
    """
    Package size combobox (#shippingMethods-input). Type "Small" slowly so keystrokes
    aren't dropped (same idea as brand_select). Depop will adjust after photos anyway.
    """
    inp = wait.until(EC.element_to_be_clickable((By.ID, "shippingMethods-input")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'})", inp)
    inp.click()
    time.sleep(0.08)

    inp.send_keys(Keys.CONTROL, "a")
    inp.send_keys(Keys.DELETE)
    time.sleep(0.06)

    for ch in "Small":
        inp.send_keys(ch)
        time.sleep(type_delay)

    time.sleep(0.35)

    try:
        wait.until(EC.visibility_of_element_located((By.ID, "shippingMethods-menu")))
    except Exception:
        pass

    time.sleep(0.08)
    inp.send_keys(Keys.ARROW_DOWN)
    inp.send_keys(Keys.ARROW_DOWN)
    inp.send_keys(Keys.ARROW_DOWN)
    inp.send_keys(Keys.ENTER)

    try:
        inp.send_keys(Keys.ESCAPE)
    except Exception:
        pass
    try:
        driver.execute_script("document.activeElement && document.activeElement.blur();")
    except Exception:
        pass


def select_shipping(driver, shipping, category, subcategory, timeout=15):
    wait = WebDriverWait(driver, timeout)

    # Close any open menus that might intercept clicks
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.05)
    except Exception:
        pass

    if shipping == "Depop":
        depop_radio = wait.until(EC.presence_of_element_located((By.ID, "usps__shipping")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", depop_radio)
        driver.execute_script("arguments[0].click()", depop_radio)
        if not depop_radio.is_selected():
            label = driver.find_element(By.ID, "usps__shipping__label")
            driver.execute_script("arguments[0].click()", label)
        wait.until(EC.presence_of_element_located((By.ID, "shippingMethods-input")))
        time.sleep(0.12)
        _select_small_package_size(driver, wait)
        return

    if category == "Tops":
        if subcategory == "T-shirts":
            price = 6.5
        else:
            price = 7.5
    elif category == "Bottoms":
        if subcategory == "Shorts":
            price = 6.5
        else:
            price = 7.5
    elif category == "Coats and jackets":
        price = 8.5
    elif category == "Footwear":
        price = 9.0
    else:
        price = 12.0

    manual_radio = wait.until(EC.presence_of_element_located((By.ID, "manual__shipping")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'})", manual_radio)
    driver.execute_script("arguments[0].click()", manual_radio)

    if not manual_radio.is_selected():
        label = driver.find_element(By.ID, "manual__shipping__label")
        driver.execute_script("arguments[0].click()", label)

    cost = wait.until(EC.element_to_be_clickable((By.ID, "nationalShippingCost__input")))
    cost.click()
    cost.send_keys(Keys.CONTROL, "a")
    cost.send_keys(Keys.DELETE)
    cost.send_keys(str(price))
