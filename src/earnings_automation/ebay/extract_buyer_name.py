from typing import List

from src.earnings_automation.ebay.populate_reader import read_lines


def extract_buyer_names(csv_path: str) -> List[str]:
    reader = read_lines(csv_path)

    names: List[str] = []
    for row in reader:
        name = (row.get("Buyer name") or "").strip()
        # Keep 1:1 row alignment with the source CSV (don't drop rows).
        names.append("" if name == "--" else name)

    return names

