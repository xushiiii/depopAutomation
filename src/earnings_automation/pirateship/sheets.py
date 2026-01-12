from src.google_sheets import _get_sheet
from src.earnings_automation.pirateship.name_normalize import normalize_name
from src.earnings_automation.pirateship.shipping_extract import extract_shipping
from src.earnings_automation.pirateship.names_extract import extract_names
from src.earnings_automation.pirateship.log import start_log, write_log 

def track_pirateship(csv_path: str):
    buyer_name_col = 7  # column number in gspread (1-based)
    header_rows = 1
    sheet = _get_sheet()

    buyer_names_csv = extract_names(csv_path)
    shipping_prices_csv = extract_shipping(csv_path)

    # Read buyer names column once instead of calling find() multiple times
    col_vals = sheet.col_values(buyer_name_col)
    buyer_names_sheet = col_vals[header_rows:]  # sheet data rows only

    log_path = start_log(csv_path)

    updates = []

    for i in range(min(len(buyer_names_csv), len(shipping_prices_csv))):
        csv_name = buyer_names_csv[i]
        current_price = shipping_prices_csv[i]

        # Search locally in the already-loaded column
        try:
            sheet_idx = buyer_names_sheet.index(csv_name)
            row = header_rows + 1 + sheet_idx  # Convert to actual row number
            
            write_log(log_path, status="MATCH", sheet_name=csv_name, csv_name=csv_name, price=current_price)
            updates.append({"range": f"M{row}", "values": [[abs(float(current_price))]]})
        except ValueError:
            # Name not found in sheet
            write_log(log_path, status="NO MATCH", sheet_name=None, csv_name=csv_name, price=current_price)

    # Batch update all changes at once
    if updates:
        sheet.batch_update(updates, value_input_option="USER_ENTERED")