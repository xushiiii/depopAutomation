from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

def write_description(driver, text_input: dict, selected_buttons: dict, timeout=15):
    """
    Fill the Description <textarea id="description"> with a composed message.
    text_input: dict with keys like Title, Description, Hashtags, measurements...
    selected_buttons: dict with Category/Subcategory etc. (used for which template to use)
    """

    # Safe getters
    g = lambda k: (text_input.get(k) or "").strip()
    title       = g("Title")
    body        = g("Description")
    pit2pit     = g("Pit-to-pit")
    top2bot     = g("Top-to-bottom")
    pit2sleeve  = g("Pit-to-sleeve")
    waist       = g("Waist")
    inseam      = g("Inseam")
    rise        = g("Rise")
    hashtags    = g("Hashtags")

    category    = (selected_buttons.get("Category") or "").strip()
    subcategory = (selected_buttons.get("Subcategory") or "").strip()

    # Simple templates
    if subcategory == "T-shirts":
        details = (
            (f"Pit-to-pit: {pit2pit}\n" if pit2pit else "") +
            (f"Top-to-bottom: {top2bot}\n" if top2bot else "")
        ).strip()
    elif category == "Bottoms":
        details = (
            (f"Waist: {waist}\n" if waist else "") +
            (f"Inseam: {inseam}\n" if inseam else "") +
            (f"Rise: {rise}\n" if rise else "")
        ).strip()
    elif category == "Footwear":
        details = ""  # no standard measurements
    else:
        details = (
            (f"Pit-to-pit: {pit2pit}\n" if pit2pit else "") +
            (f"Top-to-bottom: {top2bot}\n" if top2bot else "") +
            (f"Pit-to-sleeve: {pit2sleeve}\n" if pit2sleeve else "")
        ).strip()

    tail = "Open to serious offers!\n\nAll sales are final"
    if hashtags:
        tail = f"{tail}\n\n{hashtags}"

    parts = []
    if title: parts.append(title)
    if body:  parts.append(body)
    if details: parts.append(details)
    parts.append(tail)

    fulldesc = "\n\n".join(p for p in parts if p).strip()

    # Now enforce the 1000-char limit at the END
    fulldesc = fulldesc[:1000]

    wait = WebDriverWait(driver, timeout)
    ta = wait.until(EC.element_to_be_clickable((By.ID, "description")))
    ta.click()
    ta.send_keys(Keys.CONTROL, "a")
    ta.send_keys(Keys.DELETE)
    ta.send_keys(fulldesc)

    # (Optional) soft check (avoid strict equality due to whitespace normalization)
    current = ta.get_attribute("value") or ""
    if not current:
        raise RuntimeError("Description field is still empty after typing.")
