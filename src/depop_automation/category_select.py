# src/depop_automation/category_select.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import your UI config so we can optionally sanity-check combos
from src.options import subcategory_options


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

    try:
        # 1) Open the Category dropdown
        toggle = wait.until(EC.element_to_be_clickable((By.ID, "group-toggle-button")))
        toggle.click()

        # Wait for it to actually open
        wait.until(
            lambda d: d.find_element(By.ID, "group-toggle-button")
            .get_attribute("aria-expanded")
            == "true"
        )
        wait.until(EC.visibility_of_element_located((By.ID, "group-menu")))

        # 2) Inside the section whose header matches "Women > Tops",
        #    click the li whose p text is the given subcategory.
        # Escape quotes in case section_text or subcategory contains them
        escaped_section = escape_xpath_string(section_text)
        escaped_subcategory = escape_xpath_string(subcategory)
        
        option_xpath = (
            "//ul[@id='group-menu']"
            f"//div[.//p[normalize-space()='{escaped_section}']]"
            f"//li[@role='option'][.//p[normalize-space()='{escaped_subcategory}']]"
        )

        option_el = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option_el.click()

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
