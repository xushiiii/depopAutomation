# src/earnings_automation/extract_buyer_name.py

import csv

def extract_buyer_name(csv_path: str):
    buyers = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            buyers.append((row.get("Name", "") or "").strip())

    return buyers
