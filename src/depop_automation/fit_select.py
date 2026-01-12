from src.depop_automation.dropdown_helper import _pick_from_dropdown

def select_fit(driver, labels, timeout: int = 15):
    """Fit: up to 2 (e.g. ['Bootcut', 'Flare'])."""
    _pick_from_dropdown(driver, base_id="attributes.bottom-style", labels=labels, max_select=2, timeout=timeout)
