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

    # Find all options and match by exact text
    all_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='productType-menu']//li[@role='option']")))
    
    print(f"[DEBUG] Looking for subcategory: '{label}'")
    print(f"[DEBUG] Found {len(all_options)} options in dropdown")
    
    found_option = None
    for i, opt in enumerate(all_options):
        try:
            # Try to find text in <p> tag first
            try:
                p_elem = opt.find_element(By.XPATH, ".//p")
                opt_text = p_elem.text.strip()
            except:
                # If no <p> tag, try getting text directly from the li
                opt_text = opt.text.strip()
            
            print(f"[DEBUG] Option {i}: text='{opt_text}', looking for '{label}'")
            
            # Also print the HTML structure for the first few options to debug
            if i < 3:
                print(f"[DEBUG] Option {i} HTML: {opt.get_attribute('outerHTML')[:200]}")
            
            if opt_text == label:
                print(f"[DEBUG] Match found! Clicking '{opt_text}'")
                found_option = opt
                break
        except Exception as e:
            print(f"[DEBUG] Error reading option {i}: {e}")
            continue
    
    if found_option is None:
        raise ValueError(f"Could not find subcategory option with text '{label}'")
    
    # Scroll into view and click
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", found_option)
    time.sleep(0.1)
    found_option.click()

    # Verify
    val = wait.until(EC.visibility_of_element_located((By.ID, "productType-input"))).get_attribute("value") or ""
    print(f"[DEBUG] After click, input value is: '{val}'")
    if val.strip() != label:
        raise ValueError(f"Subcategory not set correctly. Expected '{label}', got '{val}'")
    print(f"[OK] Subcategory selected: {label}")