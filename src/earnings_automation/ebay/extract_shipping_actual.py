from typing import List 
from src.earnings_automation.ebay.populate_reader import read_lines 

def extract_shipping_actual_prices(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    shipping: List[str] = []
    for row in reader:
        price = (row.get("Shipping labels") or "").strip()
        # Keep 1:1 row alignment with the source CSV (don't drop rows).
        shipping.append("" if price == "--" else price)
    
    return shipping