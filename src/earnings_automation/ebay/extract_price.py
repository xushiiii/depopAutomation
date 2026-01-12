from src.earnings_automation.ebay.populate_reader import read_lines
from typing import List 

def price_extract(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    prices: List[str] = []
    for row in reader:
        price = (row.get("Item price") or "").strip()
        if price and price != "--":
            prices.append(price)
    
    return prices 
