from src.depop_automation.dropdown_helper import _pick_from_dropdown

def select_type(driver, labels, timeout: int = 15):
    """Type: up to 3 (e.g. ['Cargo', 'Distressed', 'Faded'])."""
    _pick_from_dropdown(driver, base_id="attributes.bottom-fit", labels=labels, max_select=3, timeout=timeout)
