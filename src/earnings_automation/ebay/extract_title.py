from typing import List 
from src.earnings_automation.ebay.populate_reader import read_lines 

def extract_item_titles(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    titles: List[str] = []
    for row in reader:
        title = (row.get("Item title") or "").strip()
        if title and title != "--":
            titles.append(title)
    
    return titles 
