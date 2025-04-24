from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .google_sheets import write_to_sheets
from selenium.webdriver.edge.options import Options
from . import options


def find_measurement_input(driver, measurement_name):
    """Find a specific measurement input field by its label name."""
    print(f"Looking for {measurement_name} measurement input field...")
    measurement_xpath = f"//p[contains(@class, 'MeasurementInput-module__displayName___wXItr') and text()='{measurement_name}']/ancestor::div[contains(@class, 'MeasurementInput-module__measurement___iAr4s')]//input"
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, measurement_xpath))
    )
    print(f"Found {measurement_name} measurement input field")
    return input_field


def automate_grailed_listing(selected_buttons, text_input):
    print("Starting automation process...")
    # Extract text input
        # Extract text inputs
    title = text_input.get("Title", "")
    description = text_input.get("Description", "")
    brand = text_input.get("Brand", "")
    size = text_input.get("Size", "")
    price = text_input.get("Bought For Price", "")
    listing_price = text_input.get("Listing Price", "")
    pit2pit = text_input.get("Pit-to-pit", "")
    top2bot = text_input.get("Top-to-bottom", "")
    pit2sleeve = text_input.get("Pit-to-sleeve", "")
    waist = text_input.get("Waist", "")
    leg_opening = text_input.get("Leg Opening", "")
    inseam = text_input.get("Inseam", "")
    hashtags = text_input.get("Hashtags", "")
    size_text = text_input.get("Size_text", "")

    # Extract selected button values
    condition = selected_buttons.get("Condition", "")
    color = selected_buttons.get("Color", [])
    gender = selected_buttons.get("Gender", "")
    category = selected_buttons.get("Category", "")
    subcategory = selected_buttons.get("Subcategory", "")
    item_type = selected_buttons.get("Type", [])
    source = selected_buttons.get("Source", "")
    material = selected_buttons.get("Material", [])
    age = selected_buttons.get("Age", "")
    style = selected_buttons.get("Style", [])
    fit_options = selected_buttons.get("Fit", [])
    occasion_options = selected_buttons.get("Occasion", [])
    package_size = selected_buttons.get("Package Size", [])
    edge_options = Options()
    edge_options.use_chromium = True

    #LAPTOP EDGE OPTIONS
    #edge_options.add_argument(r"--user-data-dir=C:\Users\taylo\AppData\Local\Microsoft\Edge\User Data")
    #edge_options.add_argument(r"--profile-directory=Default")

    #PC EDGE OPTIONS:
    edge_options.add_argument("user-data-dir=C:\\Users\\Taylor Xu\\AppData\\Local\\Microsoft\\Edge\\User Data")
    edge_options.add_argument("profile-directory=Default")
    print("Setting up Edge driver...")
    driver = webdriver.Edge(options=edge_options)
    print("Navigating to Grailed sell page...")
    driver.get("https://www.grailed.com/sell/new") 

    time.sleep(5)
    print("Waiting for page to load...")
    
    # Wait for the department input to be present
    print("Looking for department input field...")
    department_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.SellFormInput.CustomDropDown-module__input___Z6Qbq"))
    )
    print("Found department input field")

    # Click the input to open the department dropdown
    print("Clicking department input to open dropdown...")
    department_input.click()
    print("Department dropdown opened")
    
    
    # Find the Menswear option using its specific attributes
    if gender == "Male":
        print("Looking for Menswear option...")
        menswear_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='department-option' and contains(text(), 'Menswear')]"))
        )
        print("Found Menswear option, clicking...")
        menswear_option.click()
        print("Selected Menswear")
    else:
        print("Looking for Womenswear option...")
        womenswear_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='department-option' and contains(text(), 'Womenswear')]"))
        )
        print("Found Womenswear option, clicking...")
        womenswear_option.click()
        print("Selected Womenswear")
    
    # Add a delay after selecting Menswear to allow the subcategory options to appear
    print("Waiting for subcategory options to appear...")
    time.sleep(1)
    
    if category == "Tops":
    # Find the Tops option using its specific attributes
        print("Looking for Tops option...")
        tops_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='category-option']//div[contains(text(), 'Tops')]"))
        )
        print("Found Tops option, clicking...")
        tops_option.click()
        print("Selected Tops")
        
        if subcategory == "T-shirts":
            print("Looking for T-shirts option...")
            t_shirts_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Short Sleeve T-Shirts')]"))
            )
            print("Found T-shirts option, clicking...")
            t_shirts_option.click()
            print("Selected T-shirts")

        elif subcategory == "Shirts":
            print("Looking for Long Sleeve T-Shirts option...")
            long_sleeve_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Long Sleeve T-Shirts')]"))
            )
            print("Found Long Sleeve T-Shirts option, clicking...")
            long_sleeve_option.click()
            print("Selected Long Sleeve T-Shirts")

        elif subcategory == "Hoodies" or subcategory == "Sweatshirts":
            print("Looking for Hoodies or Sweatshirts option...")
            hoodies_or_sweatshirts_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Sweatshirts & Hoodies')]"))
            )   
            print("Found Hoodies or Sweatshirts option, clicking...")
            hoodies_or_sweatshirts_option.click()
            print("Selected Hoodies or Sweatshirts")

        elif subcategory == "Sweaters" or subcategory == "Cardigans":
            print("Looking for Sweaters or Cardigans option...")
            sweaters_or_cardigans_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Sweaters & Knitwear')]"))
            )
            print("Found Sweaters or Cardigans option, clicking...")
            sweaters_or_cardigans_option.click()
            print("Selected Sweaters or Cardigans")
            
        elif subcategory == "Other":
            print("Looking for Other option...")
            other_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Jerseys')]"))
            )   
            print("Found Other option, clicking...")
            other_option.click()
            print("Selected Other")
        else:
            print("Error, subcategory in menswear tops not found")

    elif category == "Bottoms":
        print("Looking for Bottoms option...")
        bottoms_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='category-option']//div[contains(text(), 'Bottoms')]"))
        )
        print("Found Bottoms option, clicking...")
        bottoms_option.click()
        print("Selected Bottoms")

        if subcategory == "Pants":
            print("Looking for Pants option...")
            pants_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Casual Pants')]"))
            )
            print("Found Pants option, clicking...")
            pants_option.click()
            print("Selected Pants") 

        elif subcategory == "Jeans":    
            print("Looking for Jeans option...")
            jeans_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Denim')]"))
            )
            print("Found Jeans option, clicking...")
            jeans_option.click()
            print("Selected Jeans")

        elif subcategory == "Shorts":
            print("Looking for Shorts option...")
            shorts_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Shorts')]"))
            )
            print("Found Shorts option, clicking...")
            shorts_option.click()
            print("Selected Shorts")

        elif subcategory == "Sweatpants":
            print("Looking for Sweatpants option...")
            sweatpants_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='subcategory-option' and contains(text(), 'Sweatpants & Joggers')]"))
            )
            print("Found Sweatpants option, clicking...")
            sweatpants_option.click()
            print("Selected Sweatpants")    
            
        else:
            print("Error, subcategory in menswear bottoms not found")

    elif category == "Coats and Jackets":
        print("Looking for Coats and Jackets option...")
        coats_and_jackets_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='category-option']//div[contains(text(), 'Outerwear')]"))
        )
        print("Found Coats and Jackets option, clicking...")
        coats_and_jackets_option.click()
    
    elif category == "Footwear": 
        print("Looking for Footwear option...")
        footwear_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@role='menuitem' and @data-cy='category-option']//div[contains(text(), 'Footwear')]"))
        )
        print("Found Footwear option, clicking...")
        footwear_option.click()
        print("Selected Footwear")

    else:
        print("Error, category not found")
    
    # Add a delay after selecting Tops to allow the subcategory options to appear
    print("Waiting for subcategory options to appear...")
    time.sleep(2)
    
    # Find and type into the designer input field
    print("Looking for designer input field...")
    designer_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "designer-autocomplete"))
    )
    print("Found designer input field, typing Nike...")
    designer_input.send_keys(brand)
    print("Typed Nike into designer field")
    
    # Wait for the autocomplete dropdown to appear and select the first Nike option
    print("Waiting for autocomplete dropdown to appear...")
    time.sleep(2)
    print("Looking for first brand option in dropdown...")
    brand_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//li[@data-cy='menu-item' and @role='menuitem' and contains(text(), '{brand}')]"))
    )
    print(f"Found {brand} option, clicking...")
    brand_option.click()
    print(f"Selected {brand} from dropdown")
    
    # Add a delay after selecting Nike
    print("Waiting for size dropdown to appear...")
    time.sleep(2)
    
    # Find and select the XXS size option
    if size == "XXS":
        print("Looking for XXS size option...")
        size_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='xxs' and contains(text(), 'US XXS / EU 40')]"))
        )
        print("Found XXS size option, clicking...")
        size_option.click()
        print("Selected XXS size")

    elif size == "XS":
        print("Looking for XS size option...")
        size_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='xs' and contains(text(), 'US XS / EU 42 / 0')]"))
        )
        print("Found XS size option, clicking...")
        size_option.click()
        print("Selected XS size")

    elif size == "S":
        print("Looking for S size option...")   
        size_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='s' and contains(text(), 'US S / EU 44-46 / 1')]"))
        )
        print("Found S size option, clicking...")
        size_option.click()
        print("Selected S size")

    elif size == "M":
        print("Looking for M size option...")
        size_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='m' and contains(text(), 'US M / EU 48-50 / 2')]"))
        )
        print("Found M size option, clicking...")
        size_option.click()
        print("Selected M size")

    elif size == "L":
        print("Looking for L size option...")   
        size_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='l' and contains(text(), 'US L / EU 52-54 / 3')]"))
        )
        print("Found L size option, clicking...")
        size_option.click()
        print("Selected L size")        
        
    elif size == "XL":
        print("Looking for XL size option...")
        size_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='xl' and contains(text(), 'US XL / EU 56-58 / 4')]"))
        )
        print("Found XL size option, clicking...")
        size_option.click()
        print("Selected XL size")

    elif size == "XXL":
        print("Looking for XXL size option...")
        size_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='xxl' and contains(text(), 'US XXL / EU 58-60 / 5')]"))
        )
        print("Found XXL size option, clicking...")
        size_option.click()
        print("Selected XXL size")  
        
    else:
        print("Error, size not found")

    # Add a delay after selecting size
    print("Waiting for item name input to appear...")
    time.sleep(2)
    
    # Find and type into the item name input field
    print("Looking for item name input field...")
    title_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )
    print(f"Found item name input field, typing {title}...")
    title_input.send_keys(title)
    print(f"Typed {title} into item name field")
    
    # Add a delay after typing item name
    print("Waiting for color input to appear...")
    time.sleep(2)
    
    # Find and type into the color input field
    print("Looking for color input field...")
    color_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "color-autocomplete"))
    )
    first_color = color[0] if color else "Unknown"
    print(f"Found color input field, typing {first_color}...")
    color_input.send_keys(first_color)
    print(f"Typed {first_color} into color field")
    
    # Add a delay after typing color
    print("Waiting for condition dropdown to appear...")
    time.sleep(2)
    
    # Find and select the New/Never Worn condition option
    if condition == "Brand New":
        print("Looking for New/Never Worn condition option...")
        condition_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='is_new' and contains(text(), 'New/Never Worn')]"))
        )
        print("Found New/Never Worn condition option, clicking...")
        condition_option.click()
        print("Selected New/Never Worn condition")

    elif condition == "Like New":
        print("Looking for Like New condition option...")
        condition_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='is_new' and contains(text(), 'Gently Used')]"))
        )
        print("Found Like New condition option, clicking...")   
        condition_option.click()
        print("Selected Like New condition")

    elif condition == "Used - Excellent" or condition == "Used - Good":
        print("Looking for Used - Excellent condition option...")
        condition_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='is_new' and contains(text(), 'Used')]"))
        )
        print("Found Used - Excellent condition option, clicking...")
        condition_option.click()
        print("Selected Used - Excellent condition")
        
    elif condition == "Used - Fair":
        print("Looking for Used - Fair condition option...")
        condition_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[@value='is_new' and contains(text(), 'Very Worn ')]"))
        )
        print("Found Used - Fair condition option, clicking...")
        condition_option.click()
        print("Selected Used - Fair condition")

    else:
        print("Error, condition not found")
        
    # Add a delay after selecting condition
    print("Waiting for description textarea to appear...")
    time.sleep(2)
    
    # Find the description container and then the textarea within it
    print("Looking for description container...")
    description_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.description-container"))
    )
    print("Found description container, looking for textarea...")
    description_textarea = description_container.find_element(By.TAG_NAME, "textarea")
    print("Found description textarea, clicking to focus...")
    driver.execute_script("arguments[0].click();", description_textarea)
    time.sleep(1)  # Wait for focus
    print(f"Setting description: {description}")
    driver.execute_script(f"arguments[0].value = '{description}';", description_textarea)
    print("Typed description into textarea")
    
    # Measurements section
    print("Starting measurements input...")
    time.sleep(2)  # Wait for measurements section to be fully loaded
    
    try:
        # Chest measurement
        if pit2pit:
            chest_input = find_measurement_input(driver, "Chest")
            chest_input.send_keys(pit2pit)
            print(f"Entered chest measurement: {pit2pit}")

        # Length measurement
        if top2bot:
            length_input = find_measurement_input(driver, "Length")
            length_input.send_keys(top2bot)
            print(f"Entered length measurement: {top2bot}")

        # Shoulders measurement (if you have this measurement in your data)
        shoulders_measurement = text_input.get("Shoulders", "")  # Add this to your text inputs if not already present
        if shoulders_measurement:
            shoulders_input = find_measurement_input(driver, "Shoulders")
            shoulders_input.send_keys(shoulders_measurement)
            print(f"Entered shoulders measurement: {shoulders_measurement}")

        # Sleeve Length measurement
        if pit2sleeve:
            sleeve_input = find_measurement_input(driver, "Sleeve Length")
            sleeve_input.send_keys(pit2sleeve)
            print(f"Entered sleeve length measurement: {pit2sleeve}")

        # Hem measurement (if you have this measurement in your data)
        hem_measurement = text_input.get("Hem", "")  # Add this to your text inputs if not already present
        if hem_measurement:
            hem_input = find_measurement_input(driver, "Hem")
            hem_input.send_keys(hem_measurement)
            print(f"Entered hem measurement: {hem_measurement}")

    except Exception as e:
        print(f"Error inputting measurements: {e}")
        
    # Add a delay after typing measurements
    print("Waiting after entering measurements...")
    time.sleep(2)
    
    # Add a delay after typing measurement
    print("Waiting for hashtag input to appear...")
    time.sleep(2)
    
    # Find and type into the hashtag input field
    print("Looking for hashtag input field...")
    hashtag_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.-hashtag-input"))
    )
    print("Found hashtag input field, typing test and pressing enter...")
    hashtag_input.send_keys("test")
    hashtag_input.send_keys(Keys.RETURN)
    print("Typed test into hashtag input and pressed enter")
    
    # Add a delay after typing hashtag
    print("Waiting for country of origin input to appear...")
    time.sleep(2)
    
    # Find and type into the country of origin input field
    print("Looking for country of origin input field...")
    country_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "countryOfOrigin"))
    )
    print("Found country of origin input field, typing United States...")
    country_input.send_keys("United States")
    print("Typed United States into country of origin field")
    
    # Add a delay after typing country
    print("Waiting for price input to appear...")
    time.sleep(2)
    
    # Find and type into the price input field
    print("Looking for price input field...")
    price_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "price"))
    )
    print("Found price input field, typing 1...")
    price_input.send_keys("1")
    print("Typed 1 into price input field")
    
    # Add a delay after typing price
    print("Waiting for smart pricing checkbox to appear...")
    time.sleep(2)
    
    # Find and uncheck the smart pricing checkbox
    print("Looking for smart pricing checkbox...")
    try:
        # First try: Find by name and class
        smart_pricing_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='smartPricing.enabled'].Checkbox-module__checkbox___OVQLf"))
        )
        print("Found smart pricing checkbox, unchecking...")
        if smart_pricing_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", smart_pricing_checkbox)
        print("Unchecked smart pricing checkbox")
    except:
        print("First attempt failed, trying alternative approach...")
        try:
            # Second try: Find by data attribute
            smart_pricing_checkbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-gtm-form-interact-field-id='21']"))
            )
            print("Found smart pricing checkbox using alternative method, unchecking...")
            if smart_pricing_checkbox.is_selected():
                driver.execute_script("arguments[0].click();", smart_pricing_checkbox)
            print("Unchecked smart pricing checkbox")
        except:
            print("Could not find or interact with smart pricing checkbox, continuing...")
    
    # Add a delay after unchecking smart pricing
    print("Waiting for shipping checkboxes to appear...")
    time.sleep(2)
    
    # Find and uncheck all shipping checkboxes
    shipping_checkboxes = [
        ("shipping.ca.enabled", "15"),
        ("shipping.uk.enabled", "16"),
        ("shipping.eu.enabled", "17"),
        ("shipping.asia.enabled", "18"),
        ("shipping.au.enabled", "19"),
        ("shipping.other.enabled", "20")
    ]
    
    for name, field_id in shipping_checkboxes:
        print(f"Looking for {name} checkbox...")
        try:
            # First try: Find by name and class
            checkbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"input[name='{name}'].Checkbox-module__checkbox___OVQLf"))
            )
            print(f"Found {name} checkbox, unchecking...")
            if checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
            print(f"Unchecked {name} checkbox")
        except:
            print(f"First attempt failed for {name}, trying alternative approach...")
            try:
                # Second try: Find by data attribute
                checkbox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"input[data-gtm-form-interact-field-id='{field_id}']"))
                )
                print(f"Found {name} checkbox using alternative method, unchecking...")
                if checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", checkbox)
                print(f"Unchecked {name} checkbox")
            except:
                print(f"Could not find or interact with {name} checkbox, continuing...")
    
    # Add a delay after unchecking shipping checkboxes
    print("Waiting for Save as Draft button to appear...")
    time.sleep(2)
    
    # Find and click the Save as Draft button
    print("Looking for Save as Draft button...")
    try:
        save_draft_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.Button-module__button___gha04.Button-module__large___DWRNc.Button-module__secondary___PTcqW"))
        )
        print("Found Save as Draft button, clicking...")
        driver.execute_script("arguments[0].click();", save_draft_button)
        print("Clicked Save as Draft button")
    except:
        print("Could not find or interact with Save as Draft button, continuing...")
    
    print("Automation complete. Keeping window open for 60 seconds...")
    time.sleep(60)  # Keep window open for 60 seconds
    print("Closing browser window...")
    driver.quit()


