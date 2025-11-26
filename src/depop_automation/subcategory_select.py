from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import subprocess
import time

def select_subcategory(driver, label: str):
    """
    Open Subcategory dropdown and click the exact option by text.
    """
    wait = WebDriverWait(driver, 15)

    # Open subcategory dropdown
    wait.until(EC.element_to_be_clickable((By.ID, "productType-toggle-button"))).click()
    # Wait for open + visible
    wait.until(lambda d: d.find_element(By.ID, "productType-toggle-button").get_attribute("aria-expanded") == "true")
    wait.until(EC.visibility_of_element_located((By.ID, "productType-menu")))

    # Click the option by visible <p> text
    opt_xpath = f"//ul[@id='productType-menu']//li[@role='option'][.//p[normalize-space()='{label}']]"
    wait.until(EC.element_to_be_clickable((By.XPATH, opt_xpath))).click()

    # Verify
    val = wait.until(EC.visibility_of_element_located((By.ID, "productType-input"))).get_attribute("value") or ""
    assert val.strip() == label, f"Subcategory not set correctly. Expected '{label}', got '{val}'"
    print(f"[OK] Subcategory selected: {label}")