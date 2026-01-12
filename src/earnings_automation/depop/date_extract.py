import csv

def extract_date(csv_path: str):
    dates = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            date = row.get("Date of sale", "").strip()
            dates.append(date)

    return dates