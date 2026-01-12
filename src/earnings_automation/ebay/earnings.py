from src.google_sheets import _get_sheet
from src.earnings_automation.ebay.title_match import match_title 
def match_title_in_sheet(titles, query: str, *, title_col: int = 1, header_rows: int = 1, min_score: int = 70):

    best_title, score, idx = match_title(query, titles, min_score=min_score)
    if best_title is None:
        return None

    row_number = header_rows + 1 + idx
    return best_title, score, row_number