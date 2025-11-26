from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from src.google_sheets import write_to_sheets
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

import src.options as options
import subprocess

#TODO: Jacket Type getting stuck 

def automate_depop_listing(selected_buttons, text_input):
    # Kill any running Edge and EdgeDriver processes
    subprocess.run('taskkill /F /IM msedge.exe', shell=True)
    subprocess.run('taskkill /F /IM msedgedriver.exe', shell=True)

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
    location = selected_buttons.get("Location", "")
    
    # Debug print statements
    print("=== DEBUG VALUES ===")
    print(f"condition: {condition}")
    print(f"color: {color}")
    print(f"gender: {gender}")
    print(f"category: {category}")
    print(f"subcategory: {subcategory}")
    print(f"item_type: {item_type}")
    print(f"source: {source}")
    print(f"material: {material}")
    print(f"age: {age}")
    print(f"style: {style}")
    print(f"fit_options: {fit_options}")
    print(f"occasion_options: {occasion_options}")
    print(f"package_size: {package_size}")
    print(f"location: {location}")
    print("===================")

    #write_to_sheets(price, title, location, category, subcategory)

    edge_options = Options()
    edge_options.use_chromium = True

    #LAPTOP EDGE OPTIONS
    #edge_options.add_argument(r"--user-data-dir=C:\Users\taylo\AppData\Local\Microsoft\Edge\User Data")
    #edge_options.add_argument(r"--profile-directory=Default")

    #PC EDGE OPTIONS:
    edge_options.add_argument("user-data-dir=C:\\Users\\Taylor Xu\\AppData\\Local\\Microsoft\\Edge\\User Data")
    edge_options.add_argument("profile-directory=Default")
    # Try WebDriver Manager first, fallback to manual if it fails
    try:
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
    except Exception as e:
        print(f"WebDriver Manager failed: {e}")
        print("Falling back to manual WebDriver path...")
        service = Service(r"C:\Users\Taylor Xu\Downloads\edgedriver_win64\msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.get("https://www.depop.com/products/create")

    try:
        description_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "description"))
        )
        if subcategory == "T-shirts":
            regular_description = (
                f"Pit-to-pit: {pit2pit}\n"
                f"Top-to-bottom: {top2bot}\n\n"
                "Please message me if shipping costs seem off.\n"
                "Open to serious offers!\n\n"
                "All sales are final\n\n"
                f"{hashtags}"
            )
        elif category == "Bottoms":
            regular_description = (
                f"Waist: {waist}\n"
                f"Inseam: {inseam}\n"
                f"Rise: {rise}\n\n"
                "Please message me if shipping costs seem off.\n\n"
                "Open to serious offers!\n\n"
                "All sales are final\n\n"
                f"{hashtags}"
            )
        elif category == "Footwear":
            regular_description = (
                "Please message me if shipping costs seem off.\n\n"
                "Open to serious offers!\n\n"
                "All sales are final\n\n"
                f"{hashtags}"
            )
        else:
            regular_description = (
                f"Pit-to-pit: {pit2pit}\n"
                f"Top-to-bottom: {top2bot}\n"
                f"Pit-to-sleeve: {pit2sleeve}\n\n"
                "Open to serious offers!\n\n"
                "All sales are final\n\n"
                f"{hashtags}"
            )
        if description:
            fulldesc = f"{title}\n\n{description}\n\n{regular_description}"
            
        else:
            fulldesc = f"{title}\n\n{regular_description}"

        fulldesc = fulldesc.rstrip("\n")
        description_box.clear()
        lines = fulldesc.split("\n")
        for i, line in enumerate(lines):
            description_box.send_keys(line)
            if i < len(lines) - 1:
                description_box.send_keys(Keys.ENTER)
        
        print("Description box found successfully!")

    except Exception as e:
        print(f"Failed to find description box: {e}")
    
    try:
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "group-toggle-button"))
        )
        dropdown_button.click()
        if gender == "Male":
            match category:
                case "Tops":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-0"))  
                    )
                case "Bottoms":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-1"))  
                    )
                case "Coats and Jackets":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-2"))  
                    )
                case "Footwear":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-5"))  
                    )
                case _:
                    print("[DEBUG] Error, category not recognized")
        elif gender == "Female":
            match category:
                case "Tops":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-11"))  
                    )
                case "Bottoms":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-12"))  
                    )
                case "Coats and Jackets":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-14"))  
                    )
                case "Footwear":
                    option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "group-item-17"))  
                    )
                case _:
                    print("[DEBUG] Error, category not recognized")
        option.click()

    except Exception as e:
        print(f"Category submission error: {e}")
    
    try: 
        # Subcategory
        subcategory_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "productType-input"))
        )
        subcategory_input.click()
        subcategory_input.clear()
        subcategory_input.send_keys("TEST")

        if subcategory in options.subcategory_options.get(category, []):
            subcategory_input.send_keys(subcategory)
            if subcategory == "Pants":
                subcategory_input.send_keys(Keys.ARROW_DOWN)

            elif subcategory == "Shirts":
                subcategory_input.send_keys(Keys.ARROW_DOWN)
                subcategory_input.send_keys(Keys.ARROW_DOWN)

            subcategory_input.send_keys(Keys.ENTER)
        else:
            print("[DEBUG] Error, subcategory not recognized")
    except Exception as e:
        print(f"Subcategory submission error: {e}")

    try: 
        #All tops don't have a "type" options, everything else does. 
        if category != "Tops":
            print("[DEBUG] category is not 'Tops', proceeding with type options logic.")           
            #Type Jeans/Sweatpants/Pants/Leggings (If Applicable)
            if subcategory in ["Jeans", "Sweatpants", "Trousers", "Leggings"]:
                print("[DEBUG] subcategory is in ['Jeans', 'Sweatpants', 'Pants', 'Leggings'], proceeding with type options logic.")
                type_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "bottom-fit-attribute__select"))  
                )
                for item in item_type:
                    type_input.send_keys(item)
                    type_input.send_keys(Keys.ENTER)
                
                print("[DEBUG] fit_options:", fit_options)
                print("[DEBUG] options.common_bottom_fit:", options.common_bottom_fit)
                if any(fit in options.common_bottom_fit for fit in fit_options):
                    print("[DEBUG] At least one fit_option is in options.common_bottom_fit")
                    fit_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "bottom-style-attribute__select"))
                    )
                    for item in fit_options:
                        fit_input.send_keys(item)
                        fit_input.send_keys(Keys.ENTER)
                else:
                    print("[DEBUG] No fit_option is in options.common_bottom_fit")
            else:
                print("[DEBUG] subcategory is not in ['Jeans', 'Sweatpants', 'Pants', 'Leggings'], skipping type options logic.")
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
            if subcategory == "Sneakers":
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
        else:
            print("[DEBUG] category is 'Tops', skipping type options logic.")   
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
            #size_input.send_keys('"')
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

    # Parcel Size
    time.sleep(1)  # Small delay before parcel size interaction
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "manual__shipping"))
        ).click()

        manual_shipping_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nationalShippingCost__input"))
        )
        manual_shipping_box.click()
        manual_shipping_box.send_keys(Keys.CONTROL, "a")
        manual_shipping_box.send_keys(Keys.DELETE)
        manual_shipping_box.send_keys("12")


    except Exception as e:
        print(f"Parcel submission error: {e}")

    #Price 
    time.sleep(1)  # Small delay before price interaction
    try:
        price_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "price__input")) 
        )
        price_input.click()
        time.sleep(0.3)  # Brief pause after click
        price_input.send_keys(Keys.CONTROL, "a")
        price_input.send_keys(Keys.DELETE)
        price_input.send_keys(listing_price)
        #price_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Price selection error: {e}")
    #Draft Submit 
    time.sleep(1)  # Small delay before draft submit
    try:
        draft_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > form > div.styles__SubmitButtonsContainer-sc-2b412d69-0.hMVIOz > button"))
        )
        draft_button.click()
    except Exception as e:
        print(f"Draft submit error: {e}")
    finally:
        time.sleep(5)
