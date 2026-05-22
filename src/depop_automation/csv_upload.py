"""
Append one row per UI submission to a Depop bulk-upload CSV in Downloads.

Format matches Depop's "Template version: 6" CSV. Each submit just appends
another row; upload the file on Depop when you're ready to publish.

This replaces the Selenium draft flow without removing it. To switch back,
re-import and pass `create_depop_draft` in `src/main.py`.
"""
import csv
import threading
from pathlib import Path


CSV_FILENAME = "depop_drafts.csv"
CSV_PATH = Path.home() / "Downloads" / CSV_FILENAME

TEMPLATE_VERSION_ROW = ["Template version: 6"] + [""] * 25

HEADER_ROW = [
    "Description",
    "Category",
    "Price",
    "Brand",
    "Condition",
    "Size",
    "Color 1",
    "Color 2",
    "Source 1",
    "Source 2",
    "Age",
    "Style 1",
    "Style 2",
    "Style 3",
    "Location",
    "Picture Hero url",
    "Picture 2 url",
    "Picture 3 url",
    "Picture 4 url",
    "Picture 5 url",
    "Picture 6 url",
    "Picture 7 url",
    "Picture 8 url",
    "Domestic Shipping price",
    "International Shipping price",
    "SKU",
]

HELP_ROW = [
    "Must be no more than 1,000 characters. Max. 5 hashtags.",
    "Select a category from the dropdown menu. You can type to search as well.",
    "Enter a price without a currency symbol. We'll use the currency you usually list in.",
    "Select a brand from the dropdown menu",
    "Select a condition from the dropdown menu",
    "Select a size from the dropdown menu",
    "Select a color from the dropdown menu",
    "Select a color from the dropdown menu",
    "Select a source from the dropdown menu",
    "Select a source from the dropdown menu",
    "Select an age from the dropdown menu",
    "Select a style from the dropdown menu",
    "Select a style from the dropdown menu",
    "Select a style from the dropdown menu",
    "Select the location you're shipping from",
    "Enter the url for the picture that will appear first",
    "Enter the url for the picture that will appear second",
    "Enter the url for the picture that will appear third",
    "Enter the url for the picture that will appear fourth",
    "Enter the url for the picture that will appear fifth",
    "Enter the url for the picture that will appear sixth",
    "Enter the url for the picture that will appear seventh",
    "Enter the url for the picture that will appear eighth",
    "Enter a shipping price without a currency symbol",
    "Enter a shipping price without a currency symbol",
    "Enter the SKU",
]

CONDITION_MAP = {
    "Brand new": "brand_new",
    "Like new": "used_like_new",
    "Used - Excellent": "used_excellent",
    "Used - Fair": "used_fair",
    "Used - Good": "used_good",
}

# Maps form Gender -> Depop CSV gender slug.
GENDER_SLUG_MAP = {
    "Male": "menswear",
    "Female": "womenswear",
    "Men": "menswear",
    "Women": "womenswear",
    "Kids": "kids",
}

# Maps form Gender -> Depop's display label used in the category path.
GENDER_LABEL_MAP = {
    "Male": "Men",
    "Female": "Women",
    "Men": "Men",
    "Women": "Women",
    "Kids": "Kids",
}

# Codes whose label != naive slug. Add overrides here as you discover them.
AGE_CODE_OVERRIDES = {
    "00s": "y2k",
}

# Subcategory slug overrides (Depop uses non-obvious codes for some).
SUBCATEGORY_SLUG_OVERRIDES = {
    "T-shirts": "tshirts",
}

STYLE_CODE_OVERRIDES = {
    "Y2K": "y2_k",
}

LOCATION = "Minneapolis, United States"

_write_lock = threading.Lock()


def _norm_code(value) -> str:
    """Lowercase, trim, spaces -> underscores. Matches Depop's CSV codes."""
    if not value:
        return ""
    return str(value).strip().lower().replace(" ", "_")


def _slugify(value) -> str:
    """Lowercase, trim, spaces -> hyphens. Matches Depop's category slug format."""
    if not value:
        return ""
    return str(value).strip().lower().replace(" ", "-")


def _sentence_case(text: str) -> str:
    """'Polo Shirts' -> 'Polo shirts', 'T-shirts' -> 'T-shirts'."""
    if not text:
        return ""
    text = str(text).strip()
    if not text:
        return ""
    return text[0].upper() + text[1:].lower()


def _build_category_path(selected_buttons: dict) -> str:
    """
    Build Depop's CSV 'Category' value, e.g.
        Male / Tops / Polo Shirts ->
            'Men >> Tops >> Polo shirts (menswear, tops, polo-shirts)'
        Female / Coats and jackets / Jackets ->
            'Women >> Coats and jackets >> Jackets (womenswear, coats-and-jackets, jackets)'
    """
    gender_form = (selected_buttons.get("Gender") or "").strip()
    category = (selected_buttons.get("Category") or "").strip()
    subcategory = (selected_buttons.get("Subcategory") or "").strip()

    if not (gender_form and category and subcategory):
        return ""

    gender_label = GENDER_LABEL_MAP.get(gender_form, gender_form)
    subcategory_label = _sentence_case(subcategory)

    gender_slug = GENDER_SLUG_MAP.get(gender_form, _slugify(gender_form))
    category_slug = _slugify(category)
    subcategory_slug = SUBCATEGORY_SLUG_OVERRIDES.get(subcategory) or _slugify(subcategory)

    label_path = f"{gender_label} >> {category} >> {subcategory_label}"
    code_path = f"{gender_slug}, {category_slug}, {subcategory_slug}"
    return f"{label_path} ({code_path})"


def _norm_list(values, n: int):
    """Return exactly n normalized codes (padded with empty strings)."""
    if values is None:
        items = []
    elif isinstance(values, str):
        items = [values]
    else:
        items = list(values)
    out = [_norm_code(v) for v in items if v]
    out += [""] * (n - len(out))
    return out[:n]


def _label_code(value, code_overrides: dict | None = None) -> str:
    """Format a single value as 'Label (code)', e.g. 'Blue (blue)'."""
    if not value:
        return ""
    label = str(value).strip()
    if not label:
        return ""
    overrides = code_overrides or {}
    code = overrides.get(label) or _norm_code(label)
    if not code:
        return ""
    return f"{label} ({code})"


def _label_code_list(values, n: int, code_overrides: dict | None = None):
    """Return exactly n 'Label (code)' strings (padded with empty strings)."""
    if values is None:
        items = []
    elif isinstance(values, str):
        items = [values]
    else:
        items = list(values)
    out = [_label_code(v, code_overrides) for v in items if v]
    out += [""] * (n - len(out))
    return out[:n]


def _format_price(value) -> str:
    """11 -> '11.00', '11.5' -> '11.50'. Leaves unparseable values untouched."""
    if value is None:
        return ""
    raw = str(value).strip()
    if not raw:
        return ""
    cleaned = raw.replace("$", "").replace(",", "").strip()
    try:
        return f"{float(cleaned):.2f}"
    except ValueError:
        return raw


def _build_description(text_input: dict, selected_buttons: dict) -> str:
    """Same composition as description_writer.write_description, returned as text."""
    g = lambda k: (text_input.get(k) or "").strip()
    title = g("Title")
    body = g("Description")
    pit2pit = g("Pit-to-pit")
    top2bot = g("Top-to-bottom")
    pit2sleeve = g("Pit-to-sleeve")
    waist = g("Waist")
    inseam = g("Inseam")
    rise = g("Rise")
    leg_opening = g("Leg Opening")
    hashtags = g("Hashtags")

    category = (selected_buttons.get("Category") or "").strip()
    subcategory = (selected_buttons.get("Subcategory") or "").strip()

    if subcategory == "T-shirts":
        details = (
            (f"Pit-to-pit: {pit2pit}\n" if pit2pit else "")
            + (f"Top-to-bottom: {top2bot}\n" if top2bot else "")
        ).strip()
    elif category == "Bottoms":
        details = (
            (f"Waist: {waist}\n" if waist else "")
            + (f"Inseam: {inseam}\n" if inseam else "")
            + (f"Rise: {rise}\n" if rise else "")
            + (f"Leg Opening: {leg_opening}\n" if leg_opening else "")
        ).strip()
    elif category == "Footwear":
        details = ""
    else:
        details = (
            (f"Pit-to-pit: {pit2pit}\n" if pit2pit else "")
            + (f"Top-to-bottom: {top2bot}\n" if top2bot else "")
            + (f"Pit-to-sleeve: {pit2sleeve}\n" if pit2sleeve else "")
        ).strip()

    tail = (
        "All orders shipped next day.\n"
        "Priority shipping upgrade available prior to purchase.\n"
        "Please message me with any questions!"
    )
    if hashtags:
        tail = f"{tail}\n\n{hashtags}"

    parts = []
    if title:
        parts.append(title)
    if body:
        parts.append(body)
    if details:
        parts.append(details)
    parts.append(tail)

    fulldesc = "\n\n".join(p for p in parts if p).strip()
    return fulldesc[:1000]


def _ensure_csv_exists() -> None:
    if CSV_PATH.exists():
        return
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(TEMPLATE_VERSION_ROW)
        writer.writerow(HEADER_ROW)
        writer.writerow(HELP_ROW)


def _build_row(selected_buttons: dict, text_input: dict) -> list:
    description = _build_description(text_input, selected_buttons)
    category = _build_category_path(selected_buttons)
    price = _format_price(text_input.get("Listing Price"))
    brand = ""  # Depop CSV: leave Brand empty (set manually after import).
    size = (text_input.get("Size") or "").strip()
    sku = (text_input.get("Location") or "").strip()

    condition_label = (selected_buttons.get("Condition") or "").strip()
    condition_code = CONDITION_MAP.get(condition_label, "")
    condition = (
        f"{condition_label} ({condition_code})"
        if condition_label and condition_code
        else ""
    )

    color_1, color_2 = _label_code_list(selected_buttons.get("Color"), 2)
    source_1, source_2 = _label_code_list(selected_buttons.get("Source"), 2)
    style_1, style_2, style_3 = _label_code_list(
        selected_buttons.get("Style"), 3, STYLE_CODE_OVERRIDES
    )

    age_label = (selected_buttons.get("Age") or "").strip()
    if age_label:
        age_code = AGE_CODE_OVERRIDES.get(age_label) or _norm_code(age_label)
        age = f"{age_label} ({age_code})"
    else:
        age = ""

    return [
        description,
        category,
        price,
        brand,
        condition,
        size,
        color_1,
        color_2,
        source_1,
        source_2,
        age,
        style_1,
        style_2,
        style_3,
        LOCATION,
        "", "", "", "", "", "", "", "",
        "", "",
        sku,
    ]


def append_depop_csv_row(selected_buttons: dict, text_input: dict) -> None:
    """Drop-in replacement for create_depop_draft: writes a CSV row instead."""
    with _write_lock:
        _ensure_csv_exists()
        row = _build_row(selected_buttons, text_input)
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)
    print(f"[Depop CSV] Appended row -> {CSV_PATH}")
