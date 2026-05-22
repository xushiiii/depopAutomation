from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import subprocess
import threading
import time

from src.depop_automation.driver import get_driver
from src.depop_automation.category_select import select_category
from src.depop_automation.open_edge import open_create_page
from src.depop_automation.subcategory_select import select_subcategory
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
from src.depop_automation.type_select import select_type
from src.depop_automation.fit_select import select_fit
from src.depop_automation.human_pause import (
    pause_between_sections,
    pause_between_steps,
    pause_long,
    pause_medium,
)

# One WebDriver session; concurrent threads would interleave navigations and clicks.
_draft_lock = threading.Lock()


def create_depop_draft(selected_buttons, text_input):
    shipping = selected_buttons.get("Shipping", "")
    gender = selected_buttons.get("Gender", "")
    category = selected_buttons.get("Category", "")
    subcategory = selected_buttons.get("Subcategory", "")
    type = selected_buttons.get("Type", [])
    fit = selected_buttons.get("Fit", [])
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

    with _draft_lock:
        driver = get_driver()

        try:
            open_create_page(driver)
            pause_medium()

            write_description(driver, text_input, selected_buttons)
            pause_between_sections()

            select_category(driver, gender, category, subcategory)
            pause_between_sections()

            close_dropdowns(driver)
            pause_between_steps()

            if category == "Bottoms":
                if type:
                    select_type(driver, type)
                    pause_between_steps()
                close_dropdowns(driver)
                pause_between_steps()
                if fit:
                    select_fit(driver, fit)
                    pause_between_steps()

            close_dropdowns(driver)
            pause_between_steps()

            select_occasion(driver, occasion)
            pause_between_steps()

            close_dropdowns(driver)
            pause_between_steps()

            select_material(driver, material)
            pause_between_steps()

            close_dropdowns(driver)
            pause_between_steps()

            select_brand(driver, brand, type_delay=0.09)
            pause_between_steps()

            close_dropdowns(driver)
            pause_between_steps()

            select_condition(driver, condition)
            pause_between_steps()

            select_size(driver, size)
            pause_between_steps()

            select_colors(driver, color)
            pause_between_steps()

            close_dropdowns(driver)
            pause_between_steps()

            select_source(driver, source)
            pause_between_steps()

            close_dropdowns(driver)
            pause_between_steps()

            select_age(driver, age)
            pause_between_steps()

            close_dropdowns(driver)
            pause_between_steps()

            select_styles(driver, style)
            pause_between_sections()

            close_dropdowns(driver)
            pause_between_steps()

            select_price(driver, price)
            pause_between_sections()

            select_shipping(driver, shipping, category, subcategory)
            pause_long()

            click_save_draft(driver)
            pause_long()

        finally:
            # Browser stays open; get_driver() reuses the same session on the next submit.
            pass

if __name__ == "__main__":
    create_depop_draft({}, {})
