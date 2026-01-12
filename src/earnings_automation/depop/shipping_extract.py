import csv
from src.earnings_automation.depop.money_parse import parse_money

def extract_shipping_cost(csv_path: str):
    shipping_costs = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            shipping_costs.append(parse_money(row.get("Buyer shipping cost", "")))
    return shipping_costs
