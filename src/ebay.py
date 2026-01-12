from __future__ import annotations

from pathlib import Path
import csv
from typing import Dict, Any
import ebay_options as ebay_options
INFO_LINES = [
    "#INFO,Version=0.0.2,Template= eBay-draft-listings-template_US,,,,,,,,",
    "#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html,,,,,,,,,,",
    "\"#INFO After you've successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.com/sh/lst/drafts\",,,,,,,,,,",
    "#INFO,,,,,,,,,,",
]

def create_ebay_drafts(selected_buttons, text_input):
    folder_path = Path(r"C:\Users\taylo\Downloads\ebay_listings")
    out_dir.mkdir(parents=True, exist_ok=True)
    file_path = out_dir / "listing.csv"
    with file_path.open("w", newline="", encoding="utf-8-sig") as f:
        foreach line in ebay_options.INFO_LINES:
            

    subcategory = selected_buttons.get("Subcategory", "")
    if subcategory == "T-shirts":

    else if subcategory == "Hoodies" OR subcategory == "Sweatshirts":   
    
    else if subcategory == "Jumpers":
