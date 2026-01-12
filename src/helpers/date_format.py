from datetime import datetime 

def format_date(date: str) -> str:
    formatted_date = datetime.strptime(date.strip(), "%b %d, %Y")
    return formatted_date.strftime("%m/%d/%Y")