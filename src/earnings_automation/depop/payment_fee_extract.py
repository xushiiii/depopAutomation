# src/earnings_automation/extract_payment_fee.py

import csv
from src.earnings_automation.depop.money_parse import parse_money

def extract_payment_fee(csv_path: str):
    fees = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            fees.append(parse_money(row.get("Depop Payments fee")))
    return fees
