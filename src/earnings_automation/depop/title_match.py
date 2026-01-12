from src.earnings_automation.ebay.cleanup import normalize_title 
from rapidfuzz import process, fuzz 

def match_title(query: str, candidates: list[str], *, min_score: int = 70):
    filtered = [(i, c) for i, c in enumerate(candidates) if c and c.strip()]
    if not filtered: 
        return None, 0, None 
    
    idx_map, text = zip(*filtered)

    result = process.extractOne(
        query,
        list(text),
        scorer=fuzz.token_set_ratio,
        processor=normalize_title
    )

    if not result:
        return None, 0, None

    best_text, score, local_idx = result
    if score < min_score:
        return None, score, None

    original_idx = idx_map[local_idx]
    return best_text, score, original_idx