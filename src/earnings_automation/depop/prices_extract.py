
import csv
from src.earnings_automation.depop.money_parse import parse_money

def extract_price(csv_path: str):
    prices = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices.append(parse_money(row.get("Item price", "")))
    return prices