from src.google_sheets import _get_sheet
from src.earnings_automation.depop.title_extract import extract_title
from src.earnings_automation.depop.date_extract import extract_date 
from src.earnings_automation.depop.prices_extract import extract_price
from src.earnings_automation.depop.shipping_extract import extract_shipping_cost 
from src.earnings_automation.depop.boosting_fee_extract import extract_boosting_fee 
from src.earnings_automation.depop.payment_fee_extract import extract_payment_fee
from src.earnings_automation.depop.name_extract import extract_buyer_name
from src.earnings_automation.depop.refund_extract import extract_refund
from src.earnings_automation.depop.title_match import match_title
from src.earnings_automation.depop.log import start_log, write_log


def match_title_in_sheets(titles, query: str, *, title_col: int = 1, header_rows: int = 1, min_score: int = 70):
    """Wrapper function to match title and return row number (similar to ebay's match_title_in_sheet)"""
    best_title, score, idx = match_title(query, titles, min_score=min_score)
    if best_title is None:
        return None
    
    row_number = header_rows + 1 + idx
    return best_title, score, row_number 


def report_depop_earnings(csv_path: str):
    depop_title_col = 1
    header_rows = 1
    sheet = _get_sheet()
    col_vals = sheet.col_values(depop_title_col)
    titles = col_vals[header_rows:]

    item_titles = extract_title(csv_path)
    dates = extract_date(csv_path)
    prices = extract_price(csv_path)
    shipping_fees = extract_shipping_cost(csv_path)
    boosting_fees = extract_boosting_fee(csv_path)
    payment_fees = extract_payment_fee(csv_path)
    buyer_names = extract_buyer_name(csv_path)
    refund_fees = extract_refund(csv_path)
    fee_index = 0
    skip_index = []
    i = 0

    log_path = start_log(csv_path)

    if refund_fees:
        for fee_index in range(len(refund_fees)):
            if refund_fees[fee_index] > 0:
                skip_index.append(fee_index)
    
    # Collect all updates to batch them
    updates = []
            
    for i in range(len(item_titles)):
        if i in skip_index:
            continue
        else:
            query_title = item_titles[i]
            
            result = match_title_in_sheets(
                titles, 
                query = query_title, 
                title_col = depop_title_col, 
                header_rows = header_rows, 
                min_score = 90
            )

            if result is None:
                write_log(
                    log_path, 
                    status="NO MATCH", 
                    csv_title = query_title, 
                    sold_date = dates[i],
                    buyer_name = buyer_names[i], 
                    price = prices[i], 
                    shipping_fee = shipping_fees[i], 
                    boosting_fee = boosting_fees[i], 
                    selling_fee = payment_fees[i]
                )
                continue

            matched, score, row = result 

            write_log(
                log_path, 
                status = "UPDATED", 
                csv_title = query_title, 
                matched_title = matched, 
                score = score, 
                sold_date = dates[i], 
                buyer_name = buyer_names[i], 
                price = prices[i],
                shipping_fee = shipping_fees[i],
                site_fee = payment_fees[i], 
                boosting_fee = boosting_fees[i]
            )

            sheet_values = [[
                # Your sheet header layout:
                # A Depop Item Title | B Ebay Item Title | C Category | D Location | E Site | F Sold Date |
                # G Buyer Name | H Bought For | I Sold For: | J Site Fee | K Exposure Fee | L Shipping Paid |
                # M Shipping Actual | …
                "Depop",
                dates[i],
                buyer_names[i],
            ]]

            sheet_values_fees = [[
                prices[i],
                abs(payment_fees[i]),
                abs(boosting_fees[i]),
                # For now: write Buyer shipping cost into both Shipping Paid and Shipping Actual
                abs(shipping_fees[i]),
                abs(shipping_fees[i]),
            ]]

            updates.extend([
                {"range": f"E{row}:G{row}", "values": sheet_values},
                {"range": f"I{row}:M{row}", "values": sheet_values_fees},
            ])
    
    # Batch update all changes at once
    if updates:
        sheet.batch_update(updates, value_input_option="USER_ENTERED")




            