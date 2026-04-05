import csv

from src.earnings_automation.depop.money_parse import parse_money


def extract_usps_cost(csv_path: str):
    costs = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            costs.append(parse_money(row.get("USPS Cost", "")))
    return costs

