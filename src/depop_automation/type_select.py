from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Map (Category Label in UI, Subcategory) -> base id used by the "Type" combobox
TYPE_BASES = {
    # Bottoms: same control across subcategories
    ("Men - Bottoms",   None): "attributes.bottom-fit",
    ("Women - Bottoms", None): "attributes.bottom-fit",

    # Coats & Jackets (note: "Other" has no Type control)
    ("Men - Coats and jackets",   "Coats"):   "attributes.coat-type",
    ("Men - Coats and jackets",   "Jackets"): "attributes.jacket-type",
    ("Women - Coats and jackets", "Coats"):   "attributes.coat-type",
    ("Women - Coats and jackets", "Jackets"): "attributes.jacket-type",

    # Footwear
    ("Men - Footwear",   "Sneakers"): "attributes.trainers-type",
    ("Women - Footwear", "Sneakers"): "attributes.trainers-type",
    ("Men - Footwear",   "Boots"):    "attributes.boot-type",
    ("Women - Footwear", "Boots"):    "attributes.boot-type",
    ("Men - Footwear",   "Loafers"):  "attributes.shoe-type",
    ("Women - Footwear", "Loafers"):  "attributes.shoe-type",
}


def build_category_label(gender: str, category: str) -> str:
    """
    Convert user choices to Depop UI label:
      ("Male", "Bottoms") -> "Men - Bottoms"
      ("Female", "Coats and jackets") -> "Women - Coats and jackets"
    """
    g = (gender or "").strip().lower()
    gender_map = {"male": "Men", "men": "Men", "female": "Women", "women": "Women"}
    ui_gender = gender_map.get(g)
    if not ui_gender:
        raise ValueError(f"Unknown gender: {gender!r}")
    return f"{ui_gender} - {category.strip()}"


def select_type(driver, category_label: str, subcategory: str | None, labels, timeout: int = 15):
    """
    Clicks Type options for the given category/subcategory.
      - category_label: e.g. "Men - Bottoms", "Men - Coats and jackets", "Men - Footwear"
      - subcategory:    e.g. "Jeans", "Coats", "Jackets", "Sneakers", "Boots", "Loafers" (or None for Bottoms)
      - labels:         list of visible option texts to select (handles single or multi-select)
    Keeps it simple: if we don't have a mapping, we silently return.
    """
    # Coats & Jackets → 'Other' has no Type control
    if category_label in ("Men - Coats and jackets", "Women - Coats and jackets") and subcategory == "Other":
        return

    base = TYPE_BASES.get((category_label, subcategory)) or TYPE_BASES.get((category_label, None))
    if not base:
        return  # nothing to do if unmapped

    wait = WebDriverWait(driver, timeout)

    # Open dropdown
    wait.until(EC.element_to_be_clickable((By.ID, f"{base}-toggle-button"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, f"{base}-menu")))

    # Pick up to 3 options
    for label in (labels or [])[:3]:
        xp = f"//ul[@id='{base}-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
        opt = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
        # JS click avoids overlay/interception
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", opt)
        driver.execute_script("arguments[0].click()", opt)

    # Close the menu so it doesn't block other controls
    try:
        driver.find_element(By.ID, f"{base}-input").send_keys(Keys.ESCAPE)
    except Exception:
        pass


def select_type_from_user_choices(driver, gender: str, category: str, subcategory: str | None, labels, timeout: int = 15):
    """
    Tiny wrapper so callers can pass 'Male'/'Female' and 'Bottoms'/'Coats and jackets'/etc.
    """
    category_label = build_category_label(gender, category)
    return select_type(driver, category_label, subcategory, labels, timeout=timeout)