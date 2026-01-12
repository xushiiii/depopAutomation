from src.google_sheets import _get_sheet
from src.earnings_automation.ebay.earnings import match_title_in_sheet
from src.earnings_automation.ebay.extract_title import extract_item_titles
from src.earnings_automation.ebay.extract_date import extract_dates
from src.earnings_automation.ebay.extract_price import price_extract 
from src.earnings_automation.ebay.extract_shipping_paid import extract_shipping_paid_prices
from src.earnings_automation.ebay.extract_shipping_actual import extract_shipping_actual_prices
from src.earnings_automation.ebay.extract_fee import extract_fee_values 
from src.earnings_automation.ebay.log import write_log 
from src.earnings_automation.ebay.log import start_log
def report_earnings(csv_path: str):
    ebay_title_col = 1
    header_rows = 1
    sheet = _get_sheet()
    col_vals = sheet.col_values(ebay_title_col)
    titles = col_vals[header_rows:]

    item_titles = extract_item_titles(csv_path)
    date = extract_dates(csv_path)
    item_price = price_extract(csv_path)
    shipping_paid = extract_shipping_paid_prices(csv_path)
    shipping_actual = extract_shipping_actual_prices(csv_path)
    fee = extract_fee_values(csv_path)

    log_path = start_log(csv_path)

    lengths = [len(item_titles), len(date), len(item_price), len(shipping_paid), len(shipping_actual), len(fee)]
    if len(set(lengths)) != 1:
        print("[WARN] Extracted lists have different lengths:", lengths)

    # Collect all updates to batch them
    updates = []

    for i in range(len(item_titles)):
        query_title = item_titles[i]

        result = match_title_in_sheet(
            titles,
            query=query_title,
            title_col=ebay_title_col,      # title column
            header_rows=header_rows,    # header
            min_score=80
        )

        if result is None:
            write_log(
                log_path,
                status="NO MATCH",
                csv_title=query_title,
                matched_title=None,
                score=None,
                sold_date=date[i],
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
            item_price=item_price[i],
            shipping_paid=shipping_paid[i],
            shipping_actual=shipping_actual[i],
            fee=fee[i],
        )

        values = [[
            "Ebay",                 # E = SITE
            float(item_price[i]),         # F = SOLD FOR
            abs(float(fee[i])),                # G = SITE FEE
            float(shipping_paid[i]),       # H = SHIPPING PAID
            abs(float(shipping_actual[i])),     # I = SHIPPING ACTUAL
            (date[i]),               # J = SOLD DATE
        ]]

        updates.extend([
            {"range": f"D{row}", "values": [["SOLD"]]},
            {"range": f"E{row}:J{row}", "values": values},
        ])
        
        print(f"[UPDATED] row={row} score={score} title={matched}")
    
    # Batch update all changes at once
    if updates:
        sheet.batch_update(updates, value_input_option="USER_ENTERED")

