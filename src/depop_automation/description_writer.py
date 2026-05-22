from selenium.common.exceptions import ElementClickInterceptedException
from src.depop_automation.human_pause import pause_medium, pause_short
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _textarea_content(element) -> str:
    return (element.get_attribute("value") or element.text or "").strip()


def _fill_textarea(driver, element, text: str) -> None:
    driver.execute_script(
        """
        const el = arguments[0];
        const value = arguments[1];
        el.focus();
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 'value'
        ).set;
        setter.call(el, value);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        element,
        text,
    )
    if _textarea_content(element):
        return
    element.click()
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.DELETE)
    element.send_keys(text)


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
    leg_opening = g("Leg Opening")
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
            (f"Rise: {rise}\n" if rise else "") +
            (f"Leg Opening: {leg_opening}\n" if leg_opening else "")
        ).strip()
    elif category == "Footwear":
        details = ""  # no standard measurements
    else:
        details = (
            (f"Pit-to-pit: {pit2pit}\n" if pit2pit else "") +
            (f"Top-to-bottom: {top2bot}\n" if top2bot else "") +
            (f"Pit-to-sleeve: {pit2sleeve}\n" if pit2sleeve else "")
        ).strip()

    tail = "All orders shipped next day.\nPriority shipping upgrade available prior to purchase.\nPlease message me with any questions!"
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
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
        ta,
    )
    pause_short()
    try:
        ta.click()
    except ElementClickInterceptedException:
        # Photo thumbnails (e.g. styles_thumbnailContainer) can sit over the textarea hit target.
        driver.execute_script("arguments[0].focus();", ta)
    pause_short()
    _fill_textarea(driver, ta, fulldesc)
    pause_medium()

    if not _textarea_content(ta):
        raise RuntimeError("Description field is still empty after typing.")
