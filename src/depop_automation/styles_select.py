from src.depop_automation.dropdown_helper import _pick_from_dropdown

def select_styles(driver, labels, timeout: int = 15):
    """Style: up to 3 (e.g. ['Streetwear','Y2K','Retro'])."""
    _pick_from_dropdown(driver, base_id="style", labels=labels, max_select=3, timeout=timeout)