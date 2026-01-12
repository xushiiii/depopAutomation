from typing import List 
from src.earnings_automation.ebay.populate_reader import read_lines 
from src.helpers.date_format import format_date 

def extract_dates(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)
    dates: List[str] = []
    for row in reader:
        date = (row.get("Order creation date") or "--").strip()
        if date and date != "--":
            date = format_date(date)
            dates.append(date)

    return dates 