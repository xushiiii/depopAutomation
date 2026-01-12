from pathlib import Path 
from datetime import datetime 

LOG_DIR = Path(r"C:\Users\taylo\OneDrive\Desktop\pirateship_earnings")

def start_log(csv_path: str) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    csv_stem = Path(csv_path).stem 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"{csv_stem}_processed_{timestamp}.log.txt"

    with log_path.open("w", encoding="utf-8") as f:
        f.write(f"[START] Processing CSV: {csv_path}\n")
        f.write("-" * 80 + "\n")
    
    return log_path

def write_log(
    log_path: Path, 
    *, 
    status: str, 
    sheet_name: str,
    csv_name: str,
    price
) -> None: 
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            f"[{status}] | "
            f"Sheet name = {sheet_name} | "
            f"CSV name = {csv_name} | "
            f"Price = {price}\n"
        )
