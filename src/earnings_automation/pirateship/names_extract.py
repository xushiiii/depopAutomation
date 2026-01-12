import csv

def extract_names(csv_path: str):
    names = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            desc = (row.get("Description", "") or "").strip()
            if not desc:
                continue

            if desc.startswith("PayPal Payment"):
                continue

            if ":" in desc:
                name = desc.split(":", 1)[0].strip()
                names.append(name)

    return names