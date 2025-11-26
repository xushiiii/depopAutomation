from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_category(driver, gender, category):
    wait = WebDriverWait(driver, 15)

    # map (gender, category) -> group-item-N
    ids = {
        ("Male",   "Tops"):              0,
        ("Male",   "Bottoms"):           1,
        ("Male",   "Coats and jackets"): 2,
        ("Male",   "Footwear"):          5,
        ("Female", "Tops"):              11,
        ("Female", "Bottoms"):           12,
        ("Female", "Coats and jackets"): 14,
        ("Female", "Footwear"):          17,
    }

    item_id = ids[(gender, category)]  # keep it simple; will KeyError if wrong

    # open dropdown
    toggle = wait.until(EC.element_to_be_clickable((By.ID, "group-toggle-button")))
    toggle.click()
    wait.until(lambda d: d.find_element(By.ID, "group-toggle-button").get_attribute("aria-expanded") == "true")
    wait.until(EC.visibility_of_element_located((By.ID, "group-menu")))

    # click option
    option = wait.until(EC.element_to_be_clickable((By.ID, f"group-item-{item_id}")))
    option.click()

    # verify
    val = wait.until(EC.visibility_of_element_located((By.ID, "group-input"))).get_attribute("value") or ""
    expected = f"{'Men' if gender=='Male' else 'Women'} - {category}"
    assert val.strip() == expected, f"Category not set correctly. Got '{val}'"
    print(f"[OK] Category selected: {val}")
