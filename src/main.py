from src.app import run_app
from src.depop_automation.create_draft import create_depop_draft  # kept for fallback
from src.depop_automation.csv_upload import append_depop_csv_row
from src.earnings_automation.ebay.extract_title import extract_item_titles
from src.earnings_automation.ebay.earnings import match_title_in_sheet
from src.earnings_automation.ebay.extract_date import extract_dates
from src.earnings_automation.ebay.extract_price import price_extract 
from src.earnings_automation.ebay.extract_shipping_paid import extract_shipping_paid_prices
from src.earnings_automation.ebay.extract_shipping_actual import extract_shipping_actual_prices
from src.earnings_automation.ebay.extract_fee import extract_fee_values 
from src.earnings_automation.ebay.sheets import report_earnings

# Switch to Selenium draft flow by setting `create_depop_draft=create_depop_draft` below.
if __name__ == "__main__":
    run_app(create_depop_draft = append_depop_csv_row, upload_earnings = report_earnings)
