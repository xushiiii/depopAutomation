from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:\\Users\\Taylor Xu\\AppData\\Local\\Google\\Chrome\\User Data")  # Path to your Chrome profile
chrome_options.add_argument("profile-directory=Default")  # Use your existing profile
chrome_options.add_experimental_option("detach", True)  # Keep the browser open

# Launch Chrome
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.depop.com/products/create")  # Replace with the actual URL
try:
    description_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "description"))
    )
    description_box.send_keys("This is a sample description for the item.")
    print("Successfully typed in the description box!")
except Exception as e:
    print(f"An error occurred while typing into the description box: {e}")
# Wait for the category textbox
category_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingCategories__category__select"))
)

# Type a category name
category_input.send_keys("Tops")

# Pause to allow the dropdown to load
time.sleep(2)

# Navigate options using ARROW_DOWN and select with RETURN
category_input.send_keys(Keys.ARROW_DOWN)  # Highlight the first option
time.sleep(1)
category_input.send_keys(Keys.ENTER)  # Select the highlighted option

subcategory_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingCategories__subcategory__select"))
)

subcategory_input.send_keys("TShirt")
time.sleep(1)
subcategory_input.send_keys(Keys.ENTER)


occasion_input1 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "occasion-attribute__select"))
)
occasion_input1.send_keys("Casual")
occasion_input1.send_keys(Keys.ENTER)
time.sleep(1)
occasion_input2 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "occasion-attribute__select"))
)
occasion_input2.send_keys("Party")
occasion_input2.send_keys(Keys.ENTER)
brand_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingBrands__select"))
)
material1_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "material-attribute__select"))
)
material1_input.send_keys("Cotton")
material1_input.send_keys(Keys.ENTER)
brand_input.send_keys("Polo Ralph Lauren")
brand_input.send_keys(Keys.ENTER)

condition_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingSelect__listing__condition__select"))
)
condition_input.send_keys("Good")
condition_input.send_keys(Keys.ENTER)

size_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "createProductSizes__sizeRow0__size__select"))
)

size_input.send_keys("L")
size_input.send_keys(Keys.ENTER)

colour_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingSelect__listing__colour__select"))
)
colour_input.send_keys("Black")
colour_input.send_keys(Keys.ENTER)

source_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingSelect__source__select"))
)
source_input.send_keys("Vintage")
source_input.send_keys(Keys.ENTER)

age_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingSelect__age__select"))
)
age_input.send_keys("Modern")
age_input.send_keys(Keys.ENTER)

style_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "listingSelect__style__select"))
)
style_input.send_keys("Streetwear")
style_input.send_keys(Keys.ENTER)

parcel_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "shipping__parcelSize__select"))
)
parcel_input.send_keys("M")
parcel_input.send_keys(Keys.ARROW_DOWN)
parcel_input.send_keys(Keys.ENTER)  
#listingSelect__listing__colour__select-label
time.sleep(5)
#createProductSizes__sizeRow0__size__select-label 
# Close the browser
driver.quit()