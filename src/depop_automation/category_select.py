# src/depop_automation/category_select.py

import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import your UI config so we can optionally sanity-check combos
from src.options import subcategory_options


def _group_menu_is_open(driver) -> bool:
    try:
        menu = driver.find_element(By.ID, "group-menu")
        return menu.is_displayed()
    except (NoSuchElementException, StaleElementReferenceException):
        return False


def _category_dropdown_expanded(driver) -> bool:
    """Prefer aria-expanded on the combobox toggle (reliable across SPA re-renders)."""
    try:
        toggle = driver.find_element(By.ID, "group-toggle-button")
        ae = toggle.get_attribute("aria-expanded")
        if ae is not None:
            return ae == "true"
    except (NoSuchElementException, StaleElementReferenceException):
        pass
    return _group_menu_is_open(driver)


def _click_toggle(driver, toggle) -> None:
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
        toggle,
    )
    try:
        toggle.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", toggle)


def _ensure_category_dropdown_open(driver, wait: WebDriverWait) -> None:
    """
    Reused Edge sessions often leave the category panel out of sync with is_displayed()
    (e.g. focus still in description, or menu stuck half-open). Blur/dismiss, then close-if-open
    and open fresh so option rows are actually in the tree and clickable.
    """
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ESCAPE)
    time.sleep(0.08)

    toggle = wait.until(EC.element_to_be_clickable((By.ID, "group-toggle-button")))
    if _category_dropdown_expanded(driver):
        _click_toggle(driver, toggle)
        # Wait until Depop actually collapses the menu (avoid toggling twice = still closed).
        for _ in range(50):
            if not _category_dropdown_expanded(driver):
                break
            time.sleep(0.1)
        else:
            _click_toggle(driver, toggle)
            time.sleep(0.2)

    if not _category_dropdown_expanded(driver):
        _click_toggle(driver, toggle)
        time.sleep(0.2)

    # Menu content can paint after the toggle flips; avoids flaky timeouts on 2nd+ submit.
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#group-menu li[role='option']")
            )
        )
    except TimeoutException:
        pass


def select_category(
    driver,
    gender: str,
    category: str,
    subcategory: str,
    timeout: int = 15
) -> None:
    """
    Selects the Depop 'Category' value, which now effectively combines:
      - gender      (e.g. 'Male', 'Female')
      - category    (e.g. 'Tops', 'Bottoms', 'Coats and jackets', 'Footwear')
      - subcategory (e.g. 'Jumpers', 'T-shirts', 'Jeans', 'Jackets')

    It targets markup like:

      <ul id="group-menu">
        <div>
          <p>Women > Tops</p>              # section header
          <li role="option"><p>Jumpers</p></li>
          <li role="option"><p>T-shirts</p></li>
          ...
        </div>
      </ul>

    We no longer rely on 'group-item-*' ids. Instead we:
      1) Find the section header "Women > Tops" (derived from gender + category)
      2) Click the <li> whose <p> text is the subcategory (e.g. 'Jumpers')
    
    Raises:
        ValueError: If required parameters are missing or selection fails
    """

    gender = (gender or "").strip()
    category = (category or "").strip()
    subcategory = (subcategory or "").strip()

    if not gender or not category or not subcategory:
        raise ValueError(
            f"Missing required parameters for category selection – "
            f"gender='{gender}', category='{category}', subcategory='{subcategory}'"
        )

    # Optional sanity check using your subcategory_options
    if category not in subcategory_options:
        print(f"[DEBUG] Unknown category '{category}' – not in subcategory_options, continuing anyway.")
    elif subcategory not in subcategory_options[category]:
        print(
            f"[DEBUG] Subcategory '{subcategory}' not listed for category '{category}' "
            f"in subcategory_options, continuing anyway."
        )

    wait = WebDriverWait(driver, timeout)

    # Map your UI gender to Depop's section header prefix
    gender_map = {
        "Male": "Men",
        "Female": "Women",
        "Men": "Men",
        "Women": "Women",
        "Kids": "Kids",
    }
    gender_label = gender_map.get(gender, gender)

    # Your 'Category' options already match Depop headers:
    #   "Tops", "Bottoms", "Coats and jackets", "Footwear"
    # so we can use category directly.
    section_text = f"{gender_label} > {category}"

    # Escape single quotes in XPath string literals by doubling them
    # XPath: use single quotes for the string, so escape single quotes by doubling them
    def escape_xpath_string(s: str) -> str:
        """Escape single quotes for use in XPath string literal (using single quotes)."""
        return s.replace("'", "''")

    escaped_section = escape_xpath_string(section_text)
    escaped_subcategory = escape_xpath_string(subcategory)

    # Prefer the list wrapper when present; fall back if Depop drops id="group-menu"
    # or the <ul> fails Selenium's visibility check while options are still interactable.
    option_xpath_primary = (
        "//ul[@id='group-menu']"
        f"//div[.//p[normalize-space()='{escaped_section}']]"
        f"//li[@role='option'][.//p[normalize-space()='{escaped_subcategory}']]"
    )
    option_xpath_fallback = (
        f"//div[.//p[normalize-space()='{escaped_section}']]"
        f"//li[@role='option'][.//p[normalize-space()='{escaped_subcategory}']]"
    )

    def _wait_option_clickable(xpath: str):
        try:
            return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            # Present but not "clickable" (overlay, animation): still scroll + click below.
            el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                el,
            )
            return el

    try:
        # 1) Reset and open — reused sessions often mis-detect "already open" and skip the toggle.
        _ensure_category_dropdown_open(driver, wait)

        # 2) Wait for the target row directly (more reliable than #group-menu visibility alone).
        try:
            option_el = _wait_option_clickable(option_xpath_primary)
        except TimeoutException:
            option_el = _wait_option_clickable(option_xpath_fallback)
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            option_el,
        )
        try:
            option_el.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", option_el)

        # 3) Debug: what does the input show now?
        value = (
            wait.until(EC.visibility_of_element_located((By.ID, "group-input")))
            .get_attribute("value")
            or ""
        )
        print(
            f"[DEBUG] Category selected – header='{section_text}', "
            f"subcategory='{subcategory}', group-input='{value}'"
        )

    except Exception as e:
        error_msg = (
            f"Category selection failed for "
            f"gender='{gender}', category='{category}', subcategory='{subcategory}': {e}"
        )
        print(f"[ERROR] {error_msg}")
        raise ValueError(error_msg) from e
