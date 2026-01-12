import csv 
from pathlib import Path 
from typing import List 

def read_lines(csv_path: str) -> List[dict[str, str]]:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found at: {csv_path}")
        
    lines = path.read_text(encoding="utf-8-sig").splitlines()

    header_idx = None
    for i, line in enumerate(lines):
        cols = next(csv.reader([line]), [])
        if "Item title" in cols and "Item price" in cols:
                header_idx = i 
                break

    if header_idx is None:
        raise ValueError("Could not find header index")
    
    reader = csv.DictReader(lines[header_idx:])
    return reader 