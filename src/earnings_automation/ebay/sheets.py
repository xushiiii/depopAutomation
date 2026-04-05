from src.google_sheets import _get_sheet
from src.earnings_automation.ebay.earnings import match_title_in_sheet
from src.earnings_automation.ebay.extract_title import extract_item_titles
from src.earnings_automation.ebay.extract_date import extract_dates
from src.earnings_automation.ebay.extract_price import price_extract 
from src.earnings_automation.ebay.extract_buyer_name import extract_buyer_names
from src.earnings_automation.ebay.extract_shipping_paid import extract_shipping_paid_prices
from src.earnings_automation.ebay.extract_shipping_actual import extract_shipping_actual_prices
from src.earnings_automation.ebay.extract_fee import extract_fee_values 
from src.earnings_automation.ebay.log import write_log 
from src.earnings_automation.ebay.log import start_log

# Sheet columns (row 1 headers):
# A Depop Item Title | B Ebay Item Title | C Category | D Location | E Site | F Sold Date |
# G Buyer Name | H Bought For | I Sold For: | J Site Fee | K Exposure Fee | L Shipping Paid |
# M Shipping Actual | …
def _as_float_or_blank(value: str):
    s = (value or "").strip()
    if not s or s == "--":
        return ""
    try:
        return float(s)
    except ValueError:
        # If the CSV contains currency formatting (e.g. "$19.99"), try stripping it.
        s2 = s.replace("$", "").replace(",", "")
        return float(s2) if s2 else ""

def report_earnings(csv_path: str):
    depop_title_col = 1
    ebay_title_col = 2
    header_rows = 1
    sheet = _get_sheet()
    ebay_titles = sheet.col_values(ebay_title_col)[header_rows:]
    depop_titles = sheet.col_values(depop_title_col)[header_rows:]

    item_titles = extract_item_titles(csv_path)
    date = extract_dates(csv_path)
    buyer_names = extract_buyer_names(csv_path)
    item_price = price_extract(csv_path)
    shipping_paid = extract_shipping_paid_prices(csv_path)
    shipping_actual = extract_shipping_actual_prices(csv_path)
    fee = extract_fee_values(csv_path)

    log_path = start_log(csv_path)

    lengths = [
        len(item_titles),
        len(date),
        len(buyer_names),
        len(item_price),
        len(shipping_paid),
        len(shipping_actual),
        len(fee),
    ]
    if len(set(lengths)) != 1:
        print("[WARN] Extracted lists have different lengths:", lengths)

    # Collect all updates to batch them
    updates = []

    for i in range(len(item_titles)):
        query_title = item_titles[i]
        if not query_title:
            continue

        # Prefer matching against the Ebay Item Title column (B). If not found,
        # fall back to Depop Item Title (A) to still locate the correct row.
        result = match_title_in_sheet(
            ebay_titles,
            query=query_title,
            title_col=ebay_title_col,
            header_rows=header_rows,
            min_score=80,
        )

        matched_from = "EBAY_TITLE"
        if result is None:
            result = match_title_in_sheet(
                depop_titles,
                query=query_title,
                title_col=depop_title_col,
                header_rows=header_rows,
                min_score=80,
            )
            matched_from = "DEPOP_TITLE"

        if result is None:
            write_log(
                log_path,
                status="NO MATCH",
                csv_title=query_title,
                matched_title=None,
                score=None,
                sold_date=date[i],
                buyer_name=buyer_names[i] if i < len(buyer_names) else None,
                item_price=item_price[i],
                shipping_paid=shipping_paid[i],
                shipping_actual=shipping_actual[i],
                fee=fee[i],
            )
            print(f"[SKIP] No match for: {query_title}")
            continue 

        matched, score, row = result

        write_log(
            log_path,
            status="UPDATED",
            csv_title=query_title,
            matched_title=matched,
            score=score,
            sold_date=date[i],
            buyer_name=buyer_names[i] if i < len(buyer_names) else None,
            item_price=item_price[i],
            shipping_paid=shipping_paid[i],
            shipping_actual=shipping_actual[i],
            fee=fee[i],
        )

        updates.extend([
            {"range": f"E{row}", "values": [["Ebay"]]},
            {"range": f"F{row}", "values": [[date[i]]]},
            {"range": f"G{row}", "values": [[buyer_names[i]]] if i < len(buyer_names) else [[""]]},
            {"range": f"I{row}", "values": [[_as_float_or_blank(item_price[i])]]},
            {"range": f"J{row}", "values": [[abs(_as_float_or_blank(fee[i]))] if _as_float_or_blank(fee[i]) != "" else [""]]},
            {"range": f"L{row}", "values": [[_as_float_or_blank(shipping_paid[i])]]},
            {"range": f"M{row}", "values": [[abs(_as_float_or_blank(shipping_actual[i]))] if _as_float_or_blank(shipping_actual[i]) != "" else [""]]},
        ])
        
        print(f"[UPDATED] row={row} score={score} matched_from={matched_from} title={matched}")
    
    # Batch update all changes at once
    if updates:
        sheet.batch_update(updates, value_input_option="USER_ENTERED")

