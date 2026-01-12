import csv

def extract_title(csv_path: str):
    titles = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            description = row.get("Description", "")

            # normalize newlines and split
            lines = description.replace("\r", "").split("\n")

            # first non-empty line = title
            title = ""
            for line in lines:
                line = line.strip()
                if line:
                    title = line
                    break

            titles.append(title)

    return titles