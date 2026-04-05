from src.earnings_automation.ebay.populate_reader import read_lines
from typing import List 

def price_extract(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    prices: List[str] = []
    for row in reader:
        price = (row.get("Item price") or "").strip()
        # Keep 1:1 row alignment with the source CSV (don't drop rows).
        prices.append("" if price == "--" else price)
    
    return prices 
