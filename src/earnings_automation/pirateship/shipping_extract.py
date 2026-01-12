import csv

def extract_shipping(csv_path: str):
    values = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            desc = (row.get("Description", "") or "").strip()
            if not desc or desc.startswith("PayPal Payment"):
                continue

            total = (row.get("Total", "") or "").strip()
            if not total:
                continue

            values.append(float(total))

    return values