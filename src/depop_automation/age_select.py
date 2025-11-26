from src.depop_automation.dropdown_helper import _pick_from_dropdown

def select_age(driver, label: str, timeout: int = 15):
    """Age: single value (e.g. '90s', 'Modern', 'Antique')."""
    _pick_from_dropdown(driver, base_id="age", labels=[label], max_select=1, timeout=timeout)

