from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def automate_depop_listing():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:\\Users\\Taylor Xu\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument("profile-directory=Default")
    chrome_options.add_experimental_option("detach", True)

    # Launch Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.depop.com/products/create")  # Replace with the actual URL

    try:
        # Description
        description_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "description"))
        )
        description_box.send_keys("This is a sample description for the item.")
        
        # Category
        category_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingCategories__category__select"))
        )
        category_input.send_keys("Tops")
        time.sleep(2)
        category_input.send_keys(Keys.ARROW_DOWN)
        category_input.send_keys(Keys.ENTER)

        # Subcategory
        subcategory_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingCategories__subcategory__select"))
        )
        subcategory_input.send_keys("TShirt")
        time.sleep(1)
        subcategory_input.send_keys(Keys.ENTER)

        # Occasion
        occasion_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "occasion-attribute__select"))
        )
        occasion_input.send_keys("Casual")
        occasion_input.send_keys(Keys.ENTER)
        time.sleep(1)
        occasion_input.send_keys("Party")
        occasion_input.send_keys(Keys.ENTER)

        # Brand
        brand_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingBrands__select"))
        )
        brand_input.send_keys("Polo Ralph Lauren")
        brand_input.send_keys(Keys.ENTER)

        # Material
        material_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "material-attribute__select"))
        )
        material_input.send_keys("Cotton")
        material_input.send_keys(Keys.ENTER)

        # Condition
        condition_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__listing__condition__select"))
        )
        condition_input.send_keys("Good")
        condition_input.send_keys(Keys.ENTER)

        # Size
        size_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "createProductSizes__sizeRow0__size__select"))
        )
        size_input.send_keys("L")
        size_input.send_keys(Keys.ENTER)

        # Colour
        colour_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__listing__colour__select"))
        )
        colour_input.send_keys("Black")
        colour_input.send_keys(Keys.ENTER)

        # Source
        source_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__source__select"))
        )
        source_input.send_keys("Vintage")
        source_input.send_keys(Keys.ENTER)

        # Age
        age_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__age__select"))
        )
        age_input.send_keys("Modern")
        age_input.send_keys(Keys.ENTER)

        # Style
        style_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listingSelect__style__select"))
        )
        style_input.send_keys("Streetwear")
        style_input.send_keys(Keys.ENTER)

        # Parcel Size
        parcel_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "shipping__parcelSize__select"))
        )
        parcel_input.send_keys("M")
        parcel_input.send_keys(Keys.ARROW_DOWN)
        parcel_input.send_keys(Keys.ENTER)
        
        print("Successfully filled out the Depop listing form!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Keep the browser open for review
        time.sleep(5)
        driver.quit()

# Call the function
