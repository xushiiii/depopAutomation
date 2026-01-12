from typing import Optional 

def format_money(value: str) -> Optional[float]:
    if value is None:
        return None 
    
    formatted_money = value.strip()
    if formatted_money == "" or formatted_money == "--":
        return None
    formatted_money = formatted_money.replace("$", "").replace(",", "")
    return float(formatted_money)