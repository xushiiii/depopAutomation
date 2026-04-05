from pathlib import Path 
from datetime import date, datetime 

LOG_DIR = Path(r"C:\Users\taylo\OneDrive\Desktop\ebay_earnings")

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
    matched_title: str | None, 
    score: int | float | None, 
    sold_date,
    buyer_name=None,
    item_price, 
    shipping_paid, 
    shipping_actual, 
    fee
) -> None: 
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            f"[{status}] score={score} | "
            f"CSV title = {csv_title} | "
            f"Matched title = {matched_title} | "
            f"date=  {sold_date} | "
            f"buyer_name = {buyer_name} | "
            f"price = {item_price} | "
            f"shipping_paid = {shipping_paid} | "
            f"shipping_actual = {shipping_actual} | "
            f"fee = {fee}\n"
        )
