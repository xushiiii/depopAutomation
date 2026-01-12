import csv
from src.earnings_automation.depop.money_parse import parse_money

def extract_boosting_fee(csv_path: str):
    fees = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fees.append(parse_money(row.get("Boosting fee", "")))
    return fees