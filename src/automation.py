from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.google_sheets import write_to_sheets
from selenium.webdriver.edge.options import Options
import src.options as options

#TODO: Jacket Type getting stuck 

def automate_depop_listing(selected_buttons, text_input):
    print("Starting Depop automation...")

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
    rise = text_input.get("Rise", "")
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
    write_to_sheets(price, title)
    edge_options = Options()
    edge_options.use_chromium = True

    #LAPTOP EDGE OPTIONS
    #edge_options.add_argument(r"--user-data-dir=C:\Users\taylo\AppData\Local\Microsoft\Edge\User Data")
    #edge_options.add_argument(r"--profile-directory=Default")

    #PC EDGE OPTIONS:
    edge_options.add_argument("user-data-dir=C:\\Users\\Taylor Xu\\AppData\\Local\\Microsoft\\Edge\\User Data")
    edge_options.add_argument("profile-directory=Default")
    driver = webdriver.Edge(options=edge_options)
    driver.get("https://www.depop.com/products/create")

    try:
        description_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "description"))
        )
        if subcategory == "T-shirts":
            regular_description = "\nPit-to-pit: " + str(pit2pit) + "\nTop-to-bottom: " + str(top2bot) + "\nOpen to serious offers!\nAll sales are final\n" + "\n" + str(hashtags)
        elif category == "Bottoms":
            regular_description = "Waist: " + str(waist) + "\nInseam: " + str(inseam) + "\nRise: " + str(rise) + "\nOpen to serious offers!\nAll sales are final\n" + "\n" + str(hashtags)
        elif category == "Footwear":
            regular_description = "Size: " + str(size_text) + "\nOpen to serious offers!\nAll sales are final\n" + "\n" + str(hashtags)
        else:
            regular_description = "\nPit-to-pit: " + str(pit2pit) + "\nTop-to-bottom: " + str(top2bot) + "\nPit-to-sleeve: " + str(pit2sleeve) + "\nOpen to serious offers!\nAll sales are final\n" + "\n" + str(hashtags)
        if description:
            fulldesc = title + "\n" + description + "\n" + regular_description
        else:
            fulldesc = title + "\n" + regular_description
        description_box.send_keys(fulldesc)
        print("Description box found successfully!")

    except Exception as e:
        print(f"Failed to find description box: {e}")
    
    try:
        # Category
        category_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingCategories__category__select"))
        )
        # Input the selected category
        category_input.send_keys(category)

        # If the item is for women 
        if gender == "Female":
            category_input.send_keys(Keys.ARROW_DOWN)

        # Else: Male, no keys will default to Male 
        category_input.send_keys(Keys.ENTER)

    except Exception as e:
        print(f"Category submission error: {e}")
    
    try: 
        # Subcategory
        subcategory_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingCategories__subcategory__select"))
        )
        if subcategory in options.subcategory_options.get(category, []):
            subcategory_input.send_keys(subcategory)
            subcategory_input.send_keys(Keys.ENTER)
        else:
            print("Error, subcategory not recognized")
    except Exception as e:
        print(f"Subcategory submission error: {e}")

    try: 
        #All tops don't have a "type" options, everything else does. 
        if category != "Tops":
            #Type Jeans/Sweatpants/Pants/Leggings (If Applicable)
            if subcategory in ["Jeans", "Sweatpants", "Pants", "Leggings"]:
                type_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "bottom-fit-attribute__select"))  
                )
                for item in item_type:
                    type_input.send_keys(item)
                    type_input.send_keys(Keys.ENTER)
                
                if fit_options in options.fit_options:
                    fit_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "bottom-style-attribute__select"))
                    )
                    for item in fit_options:
                        fit_input.send_keys(item)
                        fit_input.send_keys(Keys.ENTER)
            
            #Type Jacket and Coats (If Applicable)
            if subcategory == "Coats":
            # Process coat-type input
                type_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "coat-type-attribute__select"))
                )
                for item in item_type:
                    type_input.send_keys(item)
                    type_input.send_keys(Keys.ENTER)
                
            if subcategory == "Jackets":
                type_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "jacket-type-attribute__select"))
                )
                for item in item_type:
                    type_input.send_keys(item)
                    type_input.send_keys(Keys.ENTER)
            
            #Type Trainer (Sneaker) (If Applicable)
            if subcategory == "Sneaker":
                type_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "trainers-type-attribute__select"))  
                )
                for item in item_type:
                    type_input.send_keys(item)
                    type_input.send_keys(Keys.ENTER)
            
            #Type Boots (If Applicable)
            if subcategory == "Boots":
                type_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "boots-type-attribute__select"))  
                )
                for item in item_type:
                    type_input.send_keys(item)
                    type_input.send_keys(Keys.ENTER)
                    
    except Exception as e:
        print(f"Subcategory submission error: {e}")

    # Occasion
    try:
        occasion_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "occasion-attribute__select"))
        )
        for occasion in occasion_options:
            occasion_input.send_keys(occasion)
            occasion_input.send_keys(Keys.ENTER)

    except Exception as e:
        print(f"Occasion submission error: {e}")

    # Material
    try:
        material_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "material-attribute__select"))
        )
        for item in material:    
            material_input.send_keys(item)
            material_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Material submission error: {e}")

    # Brand
    try:
        brand_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingBrands__select"))
        )
        brand_input.send_keys(brand)
        brand_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Brand submission error: {e}")

    # Condition
    try:
        condition_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__listing__condition__select"))
        )
        condition_input.send_keys(condition)
        condition_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Condition submission error: {e}")

    # Size
    try:
        size_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "createProductSizes__sizeRow0__size__select"))
        )
        if size == "3XS":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ENTER)
        elif size == "XXS":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ENTER)
        elif size == "XS":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ARROW_DOWN)
            size_input.send_keys(Keys.ARROW_DOWN)
            size_input.send_keys(Keys.ENTER)
        elif size == "S":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ARROW_DOWN)
            size_input.send_keys(Keys.ARROW_DOWN)
            size_input.send_keys(Keys.ARROW_DOWN)
            size_input.send_keys(Keys.ARROW_DOWN)
            size_input.send_keys(Keys.ENTER)
        elif size == "M":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ENTER)
        elif size == "L":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ENTER)
        elif size == "XL":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ENTER)
        elif size == "XXL":
            size_input.send_keys(size)
            size_input.send_keys(Keys.ENTER)
        else:
            size_input.send_keys(size)
            size_input.send_keys('"')
            size_input.send_keys(Keys.ENTER)         
    except Exception as e:
        print(f"Size submission error: {e}")

    #Color
    try:
        color_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__listing__colour__select"))
        )
        for item in color:
            color_input.send_keys(item)
            color_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Color submission error: {e}")
    
    # Source
    try:
        source_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__source__select"))
        )
        source_input.send_keys(source)
        source_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Source submission error: {e}")

    # Age
    try:
        age_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__age__select"))
        )
        age_input.send_keys(age)
        age_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Age submission error: {e}")

    # Style
    try:
        style_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__style__select"))
        )
        for item in style:
            style_input.send_keys(item)
            style_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Style submission error: {e}")
            
    price_x_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main > form > div.styles__PriceSection-sc-e8abcf0-3.hlTBwK > div > div > div > svg"))
    )
    price_x_element.click()

    #Price 
    try:
        price_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "price__input")) 
        )
        price_input.send_keys(listing_price)
    except Exception as e:
        print(f"Price selection error: {e}")

    # Parcel Size
    try:
        parcel_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "shipping__parcelSize__select"))
        )
        if package_size == "XXS":
            parcel_input.send_keys("XXS")
            parcel_input.send_keys(Keys.ENTER)
        elif package_size == "XS":
            parcel_input.send_keys("XS")
            parcel_input.send_keys(Keys.ARROW_DOWN)
            parcel_input.send_keys(Keys.ENTER)
        elif package_size == "S":
            parcel_input.send_keys("S")
            parcel_input.send_keys(Keys.ARROW_DOWN)
            parcel_input.send_keys(Keys.ARROW_DOWN)
            parcel_input.send_keys(Keys.ENTER)  
        elif package_size == "M":
            parcel_input.send_keys("M")
            parcel_input.send_keys(Keys.ENTER)      
        elif package_size == "L":
            parcel_input.send_keys("L")
            parcel_input.send_keys(Keys.ARROW_DOWN)
            parcel_input.send_keys(Keys.ARROW_DOWN)
            parcel_input.send_keys(Keys.ENTER)    
        elif package_size == "XL":
            parcel_input.send_keys("XL")
            parcel_input.send_keys(Keys.ENTER)
        else:
            print("Package size was not recognized.")
    except Exception as e:
        print(f"Parcel submission error: {e}")

    #Draft Submit 
    try:
        draft_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > form > div.styles__SubmitButtonsContainer-sc-2b412d69-0.hMVIOz > button"))
        )
        draft_button.click()
    except Exception as e:
        print(f"Draft submit error: {e}")
    finally:
        time.sleep(5)
