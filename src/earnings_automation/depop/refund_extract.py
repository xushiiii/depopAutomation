# src/earnings_automation/extract_refund.py

import csv

def extract_refund(csv_path: str):
    refunds = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            raw = (row.get("Refunded to buyer amount", "") or "").strip()

            if not raw or raw in {"N/A", '=""-""', '=""'}:
                refunds.append(0.0)
            else:
                refunds.append(float(raw.replace("$", "").replace(",", "")))

    return refunds
