def normalize_name(s: str) -> str:
    return " ".join((s or "").strip().lower().split())