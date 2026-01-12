from typing import List 
from src.earnings_automation.ebay.populate_reader import read_lines 

def extract_fee_values(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    prices: List[str] = []
    for row in reader:
        fee = row.get("Final Value Fee - variable") or "".strip()
        if fee and fee != "--":
            prices.append(fee)
    
    return prices