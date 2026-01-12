from typing import List 
from src.earnings_automation.ebay.populate_reader import read_lines 

def extract_shipping_paid_prices(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    shipping: List[str] = []
    for row in reader:
        price = row.get("Shipping and handling") or "".strip()
        if price and price != "--":
            shipping.append(price)
    
    return shipping