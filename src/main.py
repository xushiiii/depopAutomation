from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import subprocess
import time

from src.depop_automation.driver import get_driver
from src.depop_automation.category_select import select_category
from src.depop_automation.open_edge import open_create_page
from src.depop_automation.subcategory_select import select_subcategory
from src.depop_automation.type_select import select_type_from_user_choices
from src.depop_automation.occasion_select import select_occasion 
from src.depop_automation.material_select import select_material
from src.depop_automation.brand_select import select_brand
from src.depop_automation.condition_select import select_condition
from src.depop_automation.size_condition import select_size
from src.depop_automation.quantity_select import select_quantity
from src.depop_automation.color_select import select_colors
from src.depop_automation.source_select import select_source
from src.depop_automation.age_select import select_age
from src.depop_automation.styles_select import select_styles
from src.depop_automation.shipping_input import select_shipping
from src.depop_automation.price_select import select_price
from src.depop_automation.save_draft import click_save_draft
from src.depop_automation.close_downdown import close_dropdowns
from src.depop_automation.description_writer import write_description

# Keep a reference to the driver to prevent garbage collection
# This prevents Edge from closing when the function completes
_current_driver = None

def create_depop_draft(selected_buttons, text_input):
    gender = selected_buttons.get("Gender", "")
    category = selected_buttons.get("Category", "")
    subcategory = selected_buttons.get("Subcategory", "")
    type = selected_buttons.get("Type", [])
    occasion = selected_buttons.get("Occasion", [])
    material = selected_buttons.get("Material", [])
    brand = text_input.get("Brand", "")
    condition = selected_buttons.get("Condition", "")
    size = text_input.get("Size", "")
    color = selected_buttons.get("Color", [])
    source = selected_buttons.get("Source", [])
    age = selected_buttons.get("Age", "")
    style = selected_buttons.get("Style", [])
    price = text_input.get("Listing Price", "")

    global _current_driver
    driver = get_driver()
    _current_driver = driver  

    try:
        open_create_page(driver)

        write_description(driver,text_input, selected_buttons)

        select_category(driver, gender, category, subcategory)

        #select_subcategory(driver, subcategory)

        close_dropdowns(driver)
        #select_type_from_user_choices(driver, gender, category, subcategory, type)

        close_dropdowns(driver)
        select_occasion(driver, occasion)

        close_dropdowns(driver)
        select_material(driver, material)
        
        close_dropdowns(driver)
        select_brand(driver, brand)

        close_dropdowns(driver)
        select_condition(driver, condition)

        select_size(driver, size)

        #select_quantity(driver, 1)

        select_colors(driver, color)

        close_dropdowns(driver)
        select_source(driver, source)

        close_dropdowns(driver)
        select_age(driver, age)

        close_dropdowns(driver)
        select_styles(driver, style)

        close_dropdowns(driver)

        select_price(driver, price)

        select_shipping(driver, category, subcategory)
        
        click_save_draft(driver)


        time.sleep(3)

    finally:
        # Keep browser open after listing completes
        # Edge will be terminated when a new listing begins (in get_driver())
        pass

if __name__ == "__main__":
    # Only for CLI/manual testing; UI will import and call run_depop_listing
    run_depop_listing({}, {})
