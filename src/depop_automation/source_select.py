# src/depop_automation/source_select.py
from typing import Iterable, Union
from src.depop_automation.dropdown_helper import _pick_from_dropdown

_ALLOWED = {
    "vintage":  "Vintage",
    "preloved": "Preloved",
    "deadstock":"Deadstock",
}

def select_source(driver, labels: Union[str, Iterable[str], None], timeout: int = 15):
    """
    Source: up to 2 (valid: Vintage, Preloved, Deadstock).
    Accepts a single string or an iterable of strings.
    """
    # Normalize to a list
    if labels is None:
        items = []
    elif isinstance(labels, str):
        items = [labels]
    else:
        items = list(labels)

    normalized = []
    for lbl in items:
        key = (lbl or "").strip().lower()
        if key in _ALLOWED:
            normalized.append(_ALLOWED[key])

    # de-dupe and cap at 2
    normalized = list(dict.fromkeys(normalized))[:2]
    if not normalized:
        return

    _pick_from_dropdown(driver, base_id="source", labels=normalized, max_select=2, timeout=timeout)
