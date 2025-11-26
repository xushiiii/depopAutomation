from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import subprocess
import time

def open_create_page(driver):
    driver.get("https://www.depop.com/products/create")
    # Wait for any key element to ensure the app loaded (description or category input)
    WebDriverWait(driver, 20).until(
        EC.any_of(
            EC.presence_of_element_located((By.ID, "description")),
            EC.presence_of_element_located((By.ID, "group-input"))
        )
    )