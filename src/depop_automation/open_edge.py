from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CREATE_URL = "https://www.depop.com/products/create"
CREATE_PATH = "/products/create"


def switch_to_depop_window(driver, prefer_create: bool = False) -> None:
    """
    When attaching to an existing Edge session, WebDriver may be focused on a
    tab the user is not using. Prefer a Depop tab, and the create page if open.
    """
    handles = driver.window_handles
    depop_handle = None
    create_handle = None

    for handle in handles:
        driver.switch_to.window(handle)
        url = driver.current_url or ""
        if "depop.com" not in url:
            continue
        depop_handle = handle
        if CREATE_PATH in url:
            create_handle = handle

    if prefer_create and create_handle:
        driver.switch_to.window(create_handle)
    elif depop_handle:
        driver.switch_to.window(depop_handle)
    elif handles:
        driver.switch_to.window(handles[-1])


def _create_form_ready(driver) -> bool:
    try:
        if driver.find_element(By.ID, "description").is_displayed():
            return True
    except Exception:
        pass
    try:
        if driver.find_element(By.ID, "group-input").is_displayed():
            return True
    except Exception:
        pass
    return False


def _description_usable(driver) -> bool:
    try:
        el = driver.find_element(By.ID, "description")
        return el.is_displayed()
    except Exception:
        return False


def _maybe_refresh_stale_form(driver, wait: WebDriverWait) -> None:
    if not _description_usable(driver):
        return
    el = driver.find_element(By.ID, "description")
    if (el.get_attribute("value") or "").strip():
        driver.refresh()
        wait.until(lambda d: CREATE_PATH in (d.current_url or ""))
        wait.until(_create_form_ready)


def _wait_for_create_page(driver, timeout: int = 45) -> None:
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: CREATE_PATH in (d.current_url or ""))
    wait.until(
        EC.any_of(
            EC.presence_of_element_located((By.ID, "description")),
            EC.presence_of_element_located((By.ID, "group-input")),
        )
    )
    wait.until(_create_form_ready)


def open_create_page(driver):
    switch_to_depop_window(driver)
    # Navigate in this tab — do not switch to another "create" tab afterward (stale SPA).
    nav_handle = driver.current_window_handle
    last_url = ""

    for attempt in range(3):
        try:
            driver.switch_to.window(nav_handle)
        except Exception:
            switch_to_depop_window(driver)
            nav_handle = driver.current_window_handle

        try:
            driver.get(CREATE_URL)
        except TimeoutException:
            pass

        try:
            _wait_for_create_page(driver, timeout=45)
            wait = WebDriverWait(driver, 15)
            _maybe_refresh_stale_form(driver, wait)
            if not _description_usable(driver):
                # Form shell loaded but description not visible yet.
                time.sleep(2)
                _wait_for_create_page(driver, timeout=30)
            return
        except TimeoutException:
            last_url = driver.current_url or ""
            if attempt < 2:
                time.sleep(2)
                try:
                    driver.refresh()
                except Exception:
                    pass
                continue

    raise TimeoutException(
        f"Could not load the Depop create listing page (last url: {last_url!r}). "
        "In Edge, check for login, CAPTCHA, or a bot-block page, then open "
        f"{CREATE_URL} manually and try again."
    )
