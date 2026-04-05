from typing import List 
from src.earnings_automation.ebay.populate_reader import read_lines 

def extract_fee_values(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    prices: List[str] = []
    for row in reader:
        fee = (row.get("Final Value Fee - variable") or "").strip()
        # Keep 1:1 row alignment with the source CSV (don't drop rows).
        prices.append("" if fee == "--" else fee)
    
    return prices