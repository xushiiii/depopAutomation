from pathlib import Path 
from datetime import datetime 

LOG_DIR = Path(r"C:\Users\taylo\OneDrive\Desktop\depop_earnings")

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
    csv_title: str, 
    matched_title: str | None = None,
    score: int | float | None = None, 
    sold_date = None,
    buyer_name = None, 
    price = None, 
    shipping_fee = None, 
    boosting_fee = None, 
    selling_fee = None,
    site_fee = None
) -> None: 
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            f"[{status}] score={score} | "
            f"CSV title = {csv_title} | "
            f"Matched title = {matched_title} | "
            f"date = {sold_date} | "
            f"buyer_name = {buyer_name} | "
            f"price = {price} | "
            f"shipping_fee = {shipping_fee} | "
            f"boosting_fee = {boosting_fee} | "
            f"fee = {selling_fee or site_fee}\n"
        )
