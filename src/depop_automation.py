import csv
import os
from . import headerOptions
from datetime import datetime

csv_file = 'depop_listings.csv'

file_exists = os.path.exists(csv_file)
FIELDNAMES = headerOptions.options["depop"]

INFO_LINES = [
    'Template version: 5,,,,,,,,,,,,,,,,,,,,,,,,',
    'Description,Category,Price,Brand,Condition,Size,Color 1,Color 2,Source 1,Source 2,Age,Style 1,Style 2,Style 3,Location,Picture Hero url,Picture 2 url,Picture 3 url,Picture 4 url,Picture 5 url,Picture 6 url,Picture 7 url,Picture 8 url,Domestic Shipping price,International Shipping price',
    '"Must be no more than 1,000 characters. Max. 5 hashtags.",Select a category from the dropdown menu. You can type to search as well.,Occasion,Enter a price without a currency symbol. We''ll use the currency you usually list in.,Select a brand from the dropdown menu,Select a condition from the dropdown menu,Select a size from the dropdown menu,Select a color from the dropdown menu,Select a color from the dropdown menu,Select a source from the dropdown menu,Select a source from the dropdown menu,Select an age from the dropdown menu,Select a style from the dropdown menu,Select a style from the dropdown menu,Select a style from the dropdown menu,Select the location you''re shipping from,Enter the url for the picture that will appear first,Enter the url for the picture that will appear second,Enter the url for the picture that will appear third,Enter the url for the picture that will appear fourth,Enter the url for the picture that will appear fifth,Enter the url for the picture that will appear sixth,Enter the url for the picture that will appear seventh,Enter the url for the picture that will appear eighth,Enter a shipping price without a currency symbol,Enter a shipping price without a currency symbol'
]
def add(val, list, places = 2):
    if val is None:
        list.append("")
    elif isinstance(v, float):
        list.append(f"{val:.{places}f}")
    else:
        parts.append(str(val))

def write_header(path: str):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        with open(path, "a", newline="", encoding="utf-8") as f:
            for line in INFO_LINES:
                f.write(line + "\n")

def write_to_csv(selected_buttons, text_input):
    write_header(csv_file)
    headerLength = len(headerOptions.options["depop"])
    parts = []
    # Get the basic description and hashtags
    description = text_input.get("Description", "")
    hashtags = text_input.get("Hashtags", "")

    # Get measurements
    pit2pit = text_input.get("Pit-to-pit", "")
    top2bot = text_input.get("Top-to-bottom", "")
    pit2sleeve = text_input.get("Pit-to-sleeve", "")
    waist = text_input.get("Waist", "")
    inseam = text_input.get("Inseam", "")
    rise = text_input.get("Rise", "")

    # Get category and subcategory for conditional formatting
    category = selected_buttons.get("Category", "")
    subcategory = selected_buttons.get("Subcategory", "")

    # Build the structured description based on category
    if subcategory == "T-shirts":
        regular_description = (
            f"Pit-to-pit: {pit2pit}\n"
            f"Top-to-bottom: {top2bot}\n\n"
            "Please message me if shipping costs seem off.\n"
            "Open to serious offers!\n\n"
            "All sales are final\n\n"
            f"{hashtags}"
        )
    elif category == "Bottoms":
        regular_description = (
            f"Waist: {waist}\n"
            f"Inseam: {inseam}\n"
            f"Rise: {rise}\n\n"
            "Please message me if shipping costs seem off.\n\n"
            "Open to serious offers!\n\n"
            "All sales are final\n\n"
            f"{hashtags}"
        )
    elif category == "Footwear":
        regular_description = (
            "Please message me if shipping costs seem off.\n\n"
            "Open to serious offers!\n\n"
            "All sales are final\n\n"
            f"{hashtags}"
        )
    else:
        regular_description = (
            f"Pit-to-pit: {pit2pit}\n"
            f"Top-to-bottom: {top2bot}\n"
            f"Pit-to-sleeve: {pit2sleeve}\n\n"
            "Please message me if shipping costs seem off.\n"
            "Open to serious offers!\n\n"
            "All sales are final\n\n"
            f"{hashtags}"
        )

    # Combine title, description, and structured text
    title = text_input.get("Title", "")
    if description:
        fulldesc = f"{title}\n\n{description}\n\n{regular_description}"
    else:
        fulldesc = f"{title}\n\n{regular_description}"

    # Clean up trailing newlines and escape commas for CSV
    fulldesc = fulldesc.rstrip("\n")
    # Escape commas so they're treated as content, not field separators
    fulldesc_escaped = fulldesc.replace(',', '\\,')
    parts.append(fulldesc_escaped)

    if selected_buttons.get("Gender") == "Male":
        match selected_buttons.get("Category"):
            case "Tops":
                match selected_buttons.get("Subcategory"):
                    case "T-shirts":
                        parts.append('"Men >> Tops >> T-shirts (menswear, tops, tshirts)"')
                    case "Shirts":
                        parts.append('"Men >> Tops >> Shirts (menswear, tops, shirts)"')
                    case "Hoodies":
                        parts.append('"Men >> Tops >> Hoodies (menswear, tops, hoodies)"')
                    case "Sweatshirts":
                        parts.append('"Men >> Tops >> Sweatshirts (menswear, tops, sweatshirts)"')
                    case "Sweaters":
                        parts.append('"Men >> Tops >> Sweaters (menswear, tops, jumpers)"')
                    case "Cardigans":
                        parts.append('"Men >> Tops >> Cardigans (menswear, tops, cardigans)"')
                    case "Other":
                        parts.append('"Men >> Tops >> Other (menswear, tops, other-tops)"')
                    case "Polo Shirts":
                        parts.append('"Men >> Tops >> Polo Shirts (menswear, tops, polo-shirts)"')
                    case _:
                        parts.append("")
            case "Bottoms":
                match selected_buttons.get("Subcategory"):
                    case "Jeans":
                        parts.append('"Men >> Bottoms >> Jeans (menswear, bottoms, jeans)"')
                    case "Sweatpants":
                        parts.append('"Men >> Bottoms >> Sweatpants (menswear, bottoms, joggers-tracksuits)"')
                    case "Pants":
                        parts.append('"Men >> Bottoms >> Pants (menswear, bottoms, trousers)"')
                    case "Shorts":
                        parts.append('"Men >> Bottoms >> Shorts (menswear, bottoms, shorts)"')
                    case "Leggings":
                        parts.append('"Men >> Bottoms >> Leggings (menswear, bottoms, leggings)"')
                    case _:
                        parts.append("")
            case "Coats and Jackets":
                match selected_buttons.get("Subcategory"):
                    case "Coats":
                        parts.append('"Men >> Coats and Jackets >> Coats (menswear, coats-and-jackets, coats)"')
                    case "Jackets":
                        parts.append('"Men >> Coats and Jackets >> Jackets (menswear, coats-and-jackets, jackets)"')
                    case _:
                        parts.append("")
            case "Footwear":
                match selected_buttons.get("Subcategory"):
                    case "Sneakers":
                        parts.append('"Men >> Footwear >> Sneakers (menswear, footwear, trainers)"')
                    case "Boots":
                        parts.append('"Men >> Footwear >> Boots (menswear, footwear, boots)"')
                    case "Other":
                        parts.append('"Men >> Footwear >> Other (menswear, footwear, other-footwear)"')
                    case _:
                        parts.append("")
            case _:
                parts.append("")

    if selected_buttons.get("Gender") == "Female":
        match selected_buttons.get("Category"):
            case "Tops":
                match selected_buttons.get("Subcategory"):
                    case "T-shirts":
                        parts.append('"Women >> Tops >> T-shirts (womenswear, tops, tshirts)"')
                    case "Shirts":
                        parts.append('"Women >> Tops >> Shirts (womenswear, tops, shirts)"')
                    case "Hoodies":
                        parts.append('"Women >> Tops >> Hoodies (womenswear, tops, hoodies)"')
                    case "Sweatshirts":
                        parts.append('"Women >> Tops >> Sweatshirts (womenswear, tops, sweatshirts)"')
                    case "Sweaters":
                        parts.append('"Women >> Tops >> Sweaters (womenswear, tops, jumpers)"')
                    case "Cardigans":
                        parts.append('"Women >> Tops >> Cardigans (womenswear, tops, cardigans)"')
                    case "Other":
                        parts.append('"Women >> Tops >> Other (womenswear, tops, other-tops)"')
                    case "Polo Shirts":
                        parts.append('"Women >> Tops >> Polo Shirts (womenswear, tops, polo-shirts)"')
                    case _:
                        parts.append("")
            case "Bottoms":
                match selected_buttons.get("Subcategory"):
                    case "Jeans":
                        parts.append('"Women >> Bottoms >> Jeans (womenswear, bottoms, jeans)"')
                    case "Sweatpants":
                        parts.append('"Women >> Bottoms >> Sweatpants (womenswear, bottoms, joggers-tracksuits)"')
                    case "Pants":
                        parts.append('"Women >> Bottoms >> Pants (womenswear, bottoms, trousers)"')
                    case "Shorts":
                        parts.append('"Women >> Bottoms >> Shorts (womenswear, bottoms, shorts)"')
                    case "Leggings":
                        parts.append('"Women >> Bottoms >> Leggings (womenswear, bottoms, leggings)"')
                    case _:
                        parts.append("")
            case "Coats and Jackets":
                match selected_buttons.get("Subcategory"):
                    case "Coats":
                        parts.append('"Women >> Coats and Jackets >> Coats (womenswear, coats-and-jackets, coats)"')
                    case "Jackets":
                        parts.append('"Women >> Coats and Jackets >> Jackets (womenswear, coats-and-jackets, jackets)"')
                    case _:
                        parts.append("")
            case "Footwear":
                match selected_buttons.get("Subcategory"):
                    case "Sneakers":
                        parts.append('"Women >> Footwear >> Sneakers (womenswear, footwear, trainers)"')
                    case "Boots":
                        parts.append('"Women >> Footwear >> Boots (womenswear, footwear, boots)"')
                    case "Other":
                        parts.append('"Women >> Footwear >> Other (womenswear, footwear, other-footwear)"')
                    case _:
                        parts.append("")
            case _:
                parts.append("")

    price = text_input.get("Listing Price", "")
    parts.append(price)
    
    brand = text_input.get("Brand", "")
    if brand:
        if brand == "Other":
            formatted_brand = f"{brand} (unbranded)"
            parts.append(formatted_brand)
        else:
            formatted_brand = brand.lower().replace(" ", "-")
            formatted_brand = f"{brand} ({formatted_brand})"
            parts.append(formatted_brand)
    else:
        parts.append("")

    condition = selected_buttons.get("Condition", "")
    if condition:
        match condition:
            case "Brand New":
                parts.append("Brand New (brand_new)")
            case "Like New":
                parts.append("Like New (used_like_new)")
            case "Used - Excellent":
                parts.append("Used - Excellent (used_excellent)")
            case "Used - Fair":
                parts.append("Used - Fair (used_fair)")
            case "Used - Good":
                parts.append("Used - Good (used_good)")
            case _:
                parts.append("")
    else:
        parts.append("")

    parts.append(text_input.get("Size", ""))

    i = 0
    colors = selected_buttons.get("Color", [])
    for color in colors:
        formatted_color = f"{color} ({color.lower()})"
        parts.append(formatted_color)
        i += 1
    if i < 2:
        parts.append("")
    
    i = 0 
    sources = selected_buttons.get("Source", [])
    # Handle case where Source might be a string instead of list
    if isinstance(sources, str):
        sources = [sources]
    for source in sources:
        formatted_source = f"{source} ({source.lower()})"
        parts.append(formatted_source)
        i += 1
    if i < 2:
        parts.append("")
    
    age = selected_buttons.get("Age", "")
    if age == "00s":
        parts.append("00s (y2k)")
    elif age == "Modern":
        parts.append("Modern (modern)")
    elif age:
        parts.append(f"{age} ({age})")
    else:
        parts.append("")

    styles = selected_buttons.get("Style", [])
    i = 0
    for style in styles:
        formatted_style = style.replace(" ", "_")
        formatted_style = f"{style} ({formatted_style.lower()})"
        parts.append(formatted_style)
        i += 1
    if i < 3:
        parts.append("")

    parts.append('"Minneapolis, United States"')

    parts.append("")
    parts.append("")
    parts.append("")
    parts.append("")
    parts.append("")
    parts.append("")
    parts.append("")
    parts.append("")
    parts.append("7.5")
    parts.append("0")
    csv_line = ",".join(parts)

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        f.write(csv_line + "\n")
        

# Example usage function
def automate_depop_listing(selected_buttons, text_input):
    """
    Main function to handle eBay listing automation
    For now, just writes to CSV
    """
    print("Starting Depop automation...")
    write_to_csv(selected_buttons, text_input)
    print("Depop automation complete!")

def main(buttons, input):
    # Test with empty data
    automate_depop_listing(buttons, input)

# Test data for testing the automation
def test_depop_automation():
    """Test function with sample data"""
    
    # Test Data 1 - Male T-shirt
    selected_buttons_1 = {
        "Gender": "Male",
        "Category": "Tops",
        "Subcategory": "T-shirts",
        "Condition": "Good",
        "Color": ["Blue", "White"],
        "Source": ["Vintage"],
        "Age": "90s",
        "Style": ["Casual", "Streetwear"]
    }

    text_input_1 = {
        "Description": "Vintage blue Nike t-shirt in great condition. Perfect for casual wear.",
        "Price": "25.00",
        "Brand": "Nike",
        "Size": "M",
        "Location": "United States"
    }

    # Test Data 2 - Female Hoodie
    selected_buttons_2 = {
        "Gender": "Female",
        "Category": "Tops",
        "Subcategory": "Hoodies",
        "Condition": "Excellent",
        "Color": ["Black"],
        "Source": ["Designer", "Vintage"],
        "Age": "00s",
        "Style": ["Streetwear", "Minimalist", "Casual"]
    }

    text_input_2 = {
        "Description": "Black designer hoodie from the early 2000s. Soft and comfortable.",
        "Price": "45.00",
        "Brand": "Alo Yoga",
        "Size": "S",
        "Location": "United States"
    }

    # Test Data 3 - Male Sneakers
    selected_buttons_3 = {
        "Gender": "Male",
        "Category": "Footwear",
        "Subcategory": "Sneakers",
        "Condition": "Fair",
        "Color": ["White", "Black"],
        "Source": ["Designer"],
        "Age": "10s",
        "Style": ["Athletic"]
    }

    text_input_3 = {
        "Description": "Classic white sneakers with black accents. Some wear but still stylish.",
        "Price": "80.00",
        "Brand": "Adidas Originals",
        "Size": "10",
        "Location": "United States"
    }

    # Test Data 4 - Edge Cases
    selected_buttons_4 = {
        "Gender": "Female",
        "Category": "Bottoms",
        "Subcategory": "Jeans",
        "Condition": "Good",
        "Color": ["Blue"],  # Only one color
        "Source": ["Vintage"],  # Only one source
        "Age": "80s",
        "Style": ["Vintage"]  # Only one style
    }

    text_input_4 = {
        "Description": "Classic blue vintage jeans",
        "Price": "35.00",
        "Brand": "Levi's",
        "Size": "28",
        "Location": "United States"
    }

    # Run tests
    print("Testing Depop automation with sample data...")
    print("\n--- Test 1: Male T-shirt ---")
    automate_depop_listing(selected_buttons_1, text_input_1)
    
    print("\n--- Test 2: Female Hoodie ---")
    automate_depop_listing(selected_buttons_2, text_input_2)
    
    print("\n--- Test 3: Male Sneakers ---")
    automate_depop_listing(selected_buttons_3, text_input_3)
    
    print("\n--- Test 4: Edge Cases ---")
    automate_depop_listing(selected_buttons_4, text_input_4)
    
    print("\nAll tests completed! Check depop_listings.csv for results.")

if __name__ == "__main__":
    test_depop_automation()

