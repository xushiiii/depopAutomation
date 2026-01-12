import re 

def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", " ", title) 
    title = re.sub(r"\s+", " ", title).strip()
    return title 
