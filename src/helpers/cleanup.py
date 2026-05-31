import gspread 
import re 
from google.oauth2.service_account import Credentials

from selenium.webdriver.edge.options import Options

WORDS = {
    "Outerwear": {"coat","jacket","windbreaker","puffer","parka","anorak","shell","trench","raincoat","overcoat"},
    "Shoes": {"shoe","shoes","sneaker","sneakers","boot","boots","sandal","sandals",
              "loafer","loafers","clog","clogs","mule","mules","cleats"},
    "Midlayer": {"hoodie","sweatshirt","crewneck","pullover","cardigan","fleece","sweater","zip-up","zip","1/4","quarter","full"},
    "Bottoms": {"pants","jean","jeans","chino","chinos","trouser","trousers","jogger","joggers","leggings","cargo"},
    "Shorts": {"shorts","jorts"},
    "Tops": {"shirt","tee","polo","henley","blouse","button","button-up","buttonup","t", "shirt", "t-shirt", "tshirt", "tee"},
}

edge_options = Options()
edge_options.use_chromium = True  

from src.machine_paths import get_paths

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]

credentials = Credentials.from_service_account_file(
    get_paths().service_account_file, scopes=SCOPES
)
client = gspread.authorize(credentials)
sheet = client.open("Reselling").sheet1  

# Define the regex pattern for tokenizing words
#TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[''/-][A-Za-z0-9]+)*")  # keeps hyphen/slash/apostrophes inside tokens

# Get all data at once to avoid multiple API calls
print("Reading sheet data...")
all_data = sheet.get_all_values()
print(f"Total rows in sheet: {len(all_data)}")

# Collect all updates to batch them
updates = []
uncategorized_count = 0
last_processed_items = []  # Keep track of last few processed items

# Process each row (skip header row)
for row_idx, row_data in enumerate(all_data[1:], start=2):
    if not row_data or not row_data[0]:  # Skip empty rows
        continue
        
    text = row_data[0]  # First column
    words = text.lower().split()
    tokens = set(words)

    # Show progress every 1000 rows
    if row_idx % 1000 == 0:
        print(f"Processing row {row_idx}...")

    category = None
    if WORDS["Outerwear"] & tokens:
        category = "Outerwear"
    elif WORDS["Shoes"] & tokens:
        category = "Shoes"
    elif WORDS["Midlayer"] & tokens:
        category = "Midlayer"
    elif WORDS["Bottoms"] & tokens:
        category = "Bottoms"
    elif WORDS["Tops"] & tokens:
        category = "Tops"
    elif WORDS["Shorts"] & tokens:
        category = "Shorts"
    else:
        category = "Uncategorized"
    
    # Add to updates if category found
    if category:
        updates.append([row_idx, category])
        # Keep track of last few categorized items
        last_processed_items.append(f"Row {row_idx}: '{text[:50]}...' → {category}")
        if len(last_processed_items) > 10:  # Keep only last 10
            last_processed_items.pop(0)
    else:
        uncategorized_count += 1
        if uncategorized_count <= 10:  # Only show first 10 uncategorized items
            print(f"Row {row_idx}: No category found for: {text[:50]}...")

print(f"\nFound {len(updates)} categorized items and {uncategorized_count} uncategorized items")

# Show the last few items that were processed
if last_processed_items:
    print(f"\n📝 Last {len(last_processed_items)} categorized items:")
    for item in last_processed_items:
        print(f"  {item}")

# Show some statistics
print(f"\n📊 Processing Summary:")
print(f"  Total rows processed: {len(all_data) - 1}")
print(f"  Successfully categorized: {len(updates)}")
print(f"  Uncategorized: {uncategorized_count}")
print(f"  Success rate: {(len(updates) / (len(all_data) - 1) * 100):.1f}%")

# Batch update all changes at once (much faster and avoids rate limits)
if updates:
    print(f"\n🔄 Updating {len(updates)} rows with categories...")
    
    # Prepare the data for batch update
    batch_data = []
    for row_idx, category in updates:
        batch_data.append([category])  # Just the category value for column B
    
    # Get the row numbers for the range
    row_numbers = [row_idx for row_idx, _ in updates]
    min_row = min(row_numbers)
    max_row = max(row_numbers)
    
    # Update the entire range at once - Fixed deprecation warning
    range_name = f"B{min_row}:B{max_row}"
    print(f"📝 Updating range: {range_name}")
    
    try:
        sheet.update(values=batch_data, range_name=range_name)  # Correct argument order
        print(f"✅ Successfully updated {len(updates)} rows in range {range_name}")
    except Exception as e:
        print(f"❌ Error updating sheet: {e}")
        # Fallback: update in smaller batches
        print("🔄 Trying smaller batch updates...")
        batch_size = 100
        for i in range(0, len(updates), batch_size):
            batch = updates[i:i+batch_size]
            batch_data_small = [[cat] for _, cat in batch]
            start_row = batch[0][0]
            end_row = batch[-1][0]
            range_small = f"B{start_row}:B{end_row}"
            try:
                sheet.update(values=batch_data_small, range_name=range_small)
                print(f"✅ Updated batch {i//batch_size + 1}: rows {start_row}-{end_row}")
            except Exception as e2:
                print(f"❌ Error in batch {i//batch_size + 1}: {e2}")
else:
    print("No categories to update")

print("\n🎉 Word processing complete!")
