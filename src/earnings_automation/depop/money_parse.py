# Drop this into a utils file (or paste it at the top of each extractor)
# This is intentionally "over-safe" for Depop exports.

def parse_money(raw) -> float:
    """
    Converts Depop CSV money fields into float safely.
    Handles: '$1.23', 'N/A', '', '-', '=""-""', '"-"' and other Excel-safe dash formats.
    """
    s = "" if raw is None else str(raw)
    s = s.strip()

    # Depop/Excel "dash" formats
    # ex: =""-""  or  " - " or ="-" or "-".
    s = s.replace('=""-""', '-')
    if s.startswith("="):
        s = s.lstrip("=").strip()
    s = s.strip('"').strip()

    if s in {"", "N/A", "-", "–", "—"}:
        return 0.0

    # remove currency formatting
    s = s.replace("$", "").replace(",", "").strip()

    if s in {"", "N/A", "-"}:
        return 0.0

    return float(s)
