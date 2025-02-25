from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import gspread 
from google.oauth2.service_account import Credentials

from selenium.webdriver.edge.options import Options
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]

SERVICE_ACCOUNT_FILE = "C:\\Users\\Taylor Xu\\Downloads\\resellingautomation-1044349da8d8.json"  

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open("Reselling").sheet1  
def write_to_sheets(price, description):
    price_int = int(price)
    col_values = sheet.col_values(1)
    next_row = len(col_values) + 1
    sheet.update(range_name=f"A{next_row}:B{next_row}", values=[[description, price_int]])

def automate_depop_listing(selected_buttons, text_input):

    description = text_input.get("Description")
    brand = text_input.get("Brand")
    size = text_input.get("Size")
    price = text_input.get("Bought For Price")
    listing_price = text_input.get("Listing Price")
    pit2pit = text_input.get("Pit-to-pit")
    top2bot = text_input.get("Top-to-bottom")
    pit2sleeve = text_input.get("Pit-to-sleeve")
    waist = text_input.get("Waist")
    leg_opening = text_input.get("Leg Opening")
    inseam = text_input.get("Inseam")
    hashtags = text_input.get("Hashtags")
    condition = selected_buttons.get("Condition")
    size_text = text_input.get("Size_text")
    gender = selected_buttons.get("Gender")
    category = selected_buttons.get("Category")
    subcategory = selected_buttons.get("Subcategory")
    item_type = selected_buttons.get("Type")
    source = selected_buttons.get("Source")
    material = selected_buttons.get("Material")
    age = selected_buttons.get("Age")
    style = selected_buttons.get("Style")
    edge_options = Options()
    edge_options.use_chromium = True  
    fit_options = selected_buttons.get("Fit")
    occasion_options = selected_buttons.get("Occasion")
    write_to_sheets(price, description)


    edge_options.add_argument("user-data-dir=C:\\Users\\Taylor Xu\\AppData\\Local\\Microsoft\\Edge\\User Data")
    edge_options.add_argument("profile-directory=Default")  # Change if using a different Edge profile

    # Launch Edge
    driver = webdriver.Edge(options=edge_options)
    driver.get("https://www.depop.com/products/create")
    time.sleep(1)
    for item in occasion_options:
        print(item)
    try:
        # Description
        description_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "description"))
        )
        if subcategory == "T-shirts":
            regular_description = "Size: " + str(size) + "\nPit-to-pit: " + str(pit2pit) + "\nTop-to-bottom: " + str(top2bot) + "\nCondition: " + str(condition) + "\nOpen to serious offers!\nPlease message me if you have any questions!\nAll sales are final\n" + "\n" + str(hashtags)
        elif category == "Bottoms":
            regular_description = "Waist: " + str(waist) + "\nInseam: " + str(inseam) + "\nLeg Opening: " + str(leg_opening) + "\nCondition: " + str(condition) + "\nOpen to serious offers!\nPlease message me if you have any questions!\nAll sales are final\n" + "\n" + str(hashtags)
        elif category == "Footwear":
            regular_description = "Size: " + str(size_text) + "\nOpen to serious offers!\nPlease message me if you have any questions!\nAll sales are final\n" + "\n" + str(hashtags)
        else:
            regular_description = "Size: " + str(size) + "\nPit-to-pit: " + str(pit2pit) + "\nTop-to-bottom: " + str(top2bot) + "\nPit-to-sleeve: " + str(pit2sleeve) + "\nCondition: " + str(condition) + "\nOpen to serious offers!\nPlease message me if you have any questions!\nAll sales are final\n" + "\n" + str(hashtags)
        fulldesc = f"{description}\n\n{regular_description}"
        description_box.send_keys(fulldesc)

    
        category_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingCategories__category__select"))
        )

        category_input.send_keys(category)
        if gender == "Female":
            category_input.send_keys(Keys.ARROW_DOWN)
        category_input.send_keys(Keys.ENTER)

        # Subcategory Selection (Optimized with Dictionary)
        subcategory_mapping = {
            "T-shirts": "TShirt",
            "Hoodies": "Hoodie",
            "Sweatshirts": "Sweatshirt",
            "Sweaters": "Sweater",
            "Cardigans": "Cardigan",
            "Shirts": "Shirt",
            "Other": "Other"
        }

        subcategory_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingCategories__subcategory__select"))
        )

        if subcategory in subcategory_mapping:
            subcategory_input.send_keys(subcategory_mapping[subcategory])
            subcategory_input.send_keys(Keys.ENTER)
        else:
            subcategory_input.send_keys(subcategory)
            subcategory_input.send_keys(Keys.ENTER)

        # Type Selection for Bottoms, Coats & Jackets, Footwear
        type_options = {
            "Jeans": ["Cargo", "Distressed", "Faded", "Embroidered", "Ripped"],
            "Sweatpants": ["Cargo", "Distressed", "Faded", "Embroidered", "Ripped"],
            "Pants": ["Cargo", "Distressed", "Faded", "Embroidered", "Ripped"],
            "Coats": ["Overcoat", "Puffer", "Raincoat"],
            "Jackets": ["Bomber", "Lightweight", "Shacket", "Varsity", "Windbreaker"],
            "Sneakers": ["Basketball", "Gym", "Lifestyle", "Running", "Skateboarding", "Tennis"],
            "Boots": ["Ankle", "Chelsea", "Biker", "Military", "Platform"]
        }

        if subcategory in type_options and category != "Footwear":
            type_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "bottom-fit-attribute__select"))  
            )
            for item in item_type:
                type_input.send_keys(item)
                type_input.send_keys(Keys.ENTER)

        if category == "Bottoms":  
            fit_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "bottom-style-attribute__select"))  
            )
            for fit in fit_options:
                fit_input.send_keys(fit)
                fit_input.send_keys(Keys.ENTER)

        if category == "Footwear":
            shoes_type_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "trainers-type-attribute__select"))  
            )
            for item in item_type:
                shoes_type_input.send_keys(item)
                shoes_type_input.send_keys(Keys.ENTER)
            
        # Occasion
        occasion_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "occasion-attribute__select"))
        )
        for occasion in occasion_options:
            occasion_input.send_keys(occasion)
            occasion_input.send_keys(Keys.ENTER)

        # Brand
        brand_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingBrands__select"))
        )
        brand_input.send_keys(brand)
        brand_input.send_keys(Keys.ENTER)

        # Material
        material_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "material-attribute__select"))
        )
        for item in material:    
            material_input.send_keys(item)
            material_input.send_keys(Keys.ENTER)

        # Condition
        condition_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__listing__condition__select"))
        )
        condition_input.send_keys(condition)
        condition_input.send_keys(Keys.ENTER)

        # Size
        size_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "createProductSizes__sizeRow0__size__select"))
        )
        size_input.send_keys(size)
        size_input.send_keys(Keys.ENTER)

        # Source
        source_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__source__select"))
        )
        source_input.send_keys(source)
        source_input.send_keys(Keys.ENTER)

        # Age
        age_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__age__select"))
        )
        age_input.send_keys(age)
        age_input.send_keys(Keys.ENTER)

        # Style
        style_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__style__select"))
        )
        for item in style:
            style_input.send_keys(item)
            style_input.send_keys(Keys.ENTER)

        # Parcel Size
        parcel_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "shipping__parcelSize__select"))
        )
        parcel_input.send_keys("M")
        parcel_input.send_keys(Keys.ARROW_DOWN)
        parcel_input.send_keys(Keys.ENTER)
                
        price_x_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main > form > div.styles__PriceSection-sc-e8abcf0-3.hlTBwK > div > div > div > svg"))
        )
        price_x_element.click()

        price_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "price__input")) 
        )
        price_input.send_keys(listing_price)
    
        draft_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#main > form > div.styles__SubmitButtonsContainer-sc-2b412d69-0.hMVIOz > button"))
        )
        draft_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(5)
