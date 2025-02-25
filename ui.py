import tkinter as tk
import sys
import os
from helpers.tab_nav import focus_next_widget

from functools import partial
from test import automate_depop_listing
import tkinter as tk 

text_input = ["Description", "Hashtags", "Bought For Price", "Listing Price", "Brand", "Size"]
options = {
    "Occasion": ["Casual", "Festival", "Going Out", "Outdoors", "Party", "Relaxation", "School", "Summer", "Winter", "Work", "Workout"],
    "Material": ["Acrylic", "Canvas", "Cotton", "Polyester", "Leather", "Nylon", "Silk", "Wool"],
    "Condition": ["Brand New", "Like New", "Used - Excellent", "Used - Good", "Used - Fair"],
    "Gender": ["Male", "Female"],
    "Source": ["Vintage", "Preloved", "Deadstock"],
    "Age": ["Modern", "90s", "80s", "70s"],
    "Style": ["Streetwear", "Sportswear", "Goth", "Retro", "Boho", "Western", "Indie", "Skater", "Grunge", "Minimalist", "Preppy", "Casual", "Utility", "Cottage", "Y2K", "Biker", "Gorpcore", "Coquette"],
    "Category": ["Tops", "Bottoms", "Coats and Jackets", "Footwear"]
}

subcategory_options = {
    "Tops": ["T-shirts", "Hoodies", "Sweatshirts", "Sweaters", "Cardigans", "Shirts", "Other"],
    "Bottoms":["Jeans", "Sweatpants", "Pants", "Shorts", "Leggings"],
    "Coats and Jackets": ["Coats", "Jackets"],
    "Footwear": ["Sneakers", "Boots"]
}
common_bottom_types = ["Cargo", "Distressed", "Faded", "Embroidered", "Ripped"]
common_bottom_fit = ["Bootcut", "Flare", "High waisted", "Low rise", "Straight leg", "Wide leg"]
type_options = {
    "Jeans": common_bottom_types,
    "Sweatpants": common_bottom_types,
    "Pants": common_bottom_types,
    "Coats": ["Overcoat", "Puffer", "Raincoat"],
    "Jackets": ["Bomber", "Lightweight", "Shacket", "Varsity", "Windbreaker"],
    "Sneakers": ["Basketball", "Gym", "Lifestyle", "Running", "Skateboarding", "Tennis"],
    "Boots": ["Ankle", "Chelsea", "Biker", "Military", "Platform"]
}
fit_options = {
    "Jeans": common_bottom_fit,
    "Sweatpants": common_bottom_fit,
    "Pants": common_bottom_fit
}
selected_styles = set()
selected_types = set()
selected_materials = set()
selected_fit = set()
selected_occasion = set()
subcategory_buttons = []  
labels = []
textboxs = []
selected_buttons = {}
text_inputs_data = {}
textbox_dict = {}
all_buttons = {}
def on_text_change(event, label_name, textbox):
    text_inputs_data[label_name] = textbox.get("1.0", "end-1c").strip()
    print(f"Updated {label_name}: {text_inputs_data[label_name]}")  

def on_button_click(category, value):
    global selected_styles, selected_types, selected_fit
    if category == "Category":
        previous_category = selected_buttons.get("Category", "")

        if previous_category and previous_category != value:
            selected_styles.clear()  
            selected_types.clear()  
            print(f"Cleared styles and types when switching from {previous_category} to {value}")

        selected_buttons["Category"] = value
        selected_buttons.pop("Subcategory", None)  
        selected_buttons.pop("Type", None)  
    elif category == "Style":
        if value in selected_styles:
            selected_styles.remove(value)
        elif len(selected_styles) < 3:
            selected_styles.add(value)
        else:
            return 
        selected_buttons[category] = list(selected_styles)
    elif category == "Fit":
        if value in selected_fit:
            selected_fit.remove(value)
        elif len(selected_fit) < 2:
            selected_fit.add(value)
        else:
            return 
        selected_buttons[category] = list(selected_fit)

    elif category == "Occasion":
        if value in selected_occasion:
            selected_occasion.remove(value)
        elif len(selected_occasion) < 3:
            selected_occasion.add(value)
        else:
            return 
        selected_buttons[category] = list(selected_occasion)

    elif category == "Material":
        if value in selected_materials:
            selected_materials.remove(value)
        elif len(selected_materials) < 3:
            selected_materials.add(value)
        else:
            return 
        selected_buttons[category] = list(selected_materials)

    elif category == "Type":
        selected_cat = selected_buttons.get("Category")    
        type_limit = 1
        if selected_cat == "Bottoms":
            type_limit = 3
        elif selected_cat == "Coats and Jackets":
            type_limit = 1
        else:
            type_limit = 2

        if value in selected_types:
            selected_types.remove(value)
        elif len(selected_types) < type_limit:
            selected_types.add(value)
        else:
            return 
        selected_buttons["Type"] = list(selected_types)

    elif category == "Subcategory":  # ✅ Ensure subcategory selection is properly updated
        if selected_buttons.get("Subcategory") == value:
            del selected_buttons["Subcategory"]
        else:
            selected_buttons["Subcategory"] = value
    else:
        if selected_buttons.get(category) == value:
            del selected_buttons[category]
        else:
            selected_buttons[category] = value

    print(f"Selected {category}: {value}")  # ✅ Debugging
    update_all_buttons()
    check_subcategories()  # ✅ Ensure new selections trigger subcategory updates


def update_all_buttons():
    for btn, (category, value) in list(all_buttons.items()):  # ✅ Iterate through all tracked buttons
        if btn.winfo_exists():
            if (category == "Style" and value in selected_styles) or \
               (category == "Type" and value in selected_types) or \
               (category == "Fit" and value in selected_fit) or \
               (category == "Occasion" and value in selected_occasion) or \
               (category == "Material" and value in selected_materials) or \
               (category == "Subcategory" and selected_buttons.get("Subcategory") == value) or \
               (selected_buttons.get(category) == value):
                btn.config(bg="lightblue", relief="sunken")  # ✅ Mark selected buttons
            else:
                btn.config(bg="white", relief="raised")  # ✅ Reset unselected buttons
        else:
            del all_buttons[btn]  # ✅ Remove destroyed button references


def create_button(parent_frame, j, i, category, button_text):
    input_button = tk.Button(
        parent_frame, 
        text=button_text, 
        font=("Arial", 12, "bold"),
        command=lambda c=category, v=button_text: on_button_click(c, v)  # ✅ Pass variables explicitly
    )
    input_button.grid(row = j, column = i, padx=10, pady=5, stick="w")
    all_buttons[input_button] = (category, button_text)
    return input_button

root = tk.Tk()
root.title("Depop Item Form")
root.geometry("1000x500")

# Create a canvas and a scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure the scrollbar to scroll when the frame size changes
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Add the scrollable frame inside the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack scrollbar and canvas
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

root.bind_all("<MouseWheel>", _on_mouse_wheel)  # Windows/macOS
# Main frame inside scrollable frame
main_frame = tk.Frame(scrollable_frame)
main_frame.pack(fill="x", padx=20, pady=20)


text_frame = tk.Frame(main_frame)
text_frame.pack(fill="x", padx=10, pady=10)

button_frame = tk.Frame(main_frame)
button_frame.pack(fill="x", padx=10, pady=10)
i = 0
label_exists = False

def create_label(title):
    global row_index, label_exists
    row_index += 1

    col_index = 0
    text_label = tk.Label(button_frame, text=title, font=("Arial", 15, "bold"))
    text_label.grid(row = row_index, column = col_index, stick="w", padx=10)

    textbox = tk.Text(button_frame, height = 1, width = 10, font=("Arial", 10), wrap="word", bd = 1, relief="solid")
    textbox.grid(row=row_index, column=1, sticky="ew", padx=10, pady=5)
    button_frame.columnconfigure(1, weight=1)

    text_inputs_data[title] = ""  
    textbox_dict[title] = textbox  # ✅ Store textbox in dictionary

    print(f"Creating text field for {title}")  # Debugging

    textbox.bind("<KeyRelease>", lambda event: on_text_change(event, title, textbox))
    textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(textbox_dict, event, tb))  # ✅ Bind Tab key

    labels.append(text_label)
    textboxs.append(textbox)
    label_exists = True


for i in range(len(text_input)):
    text_label = tk.Label(text_frame, text=text_input[i], font=("Arial", 15, "bold"))
    text_label.grid(row = i, column=0, sticky="w", padx=10)

    textbox = tk.Text(text_frame, height = 3, width = 30, font=("Arial", 10), wrap="word", bd = 1, relief="solid")
    textbox.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
    text_frame.columnconfigure(1, weight=1)
    text_inputs_data[text_input[i]] = ""
    textbox_dict[text_input[i]] = textbox  # ✅ Stores textbox widgets

    textbox.bind("<KeyRelease>", lambda event, name=text_input[i], tb=textbox: on_text_change(event, name, tb))
    textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(textbox_dict, event, tb))  # ✅ Bind Tab key

    print(f"Textbox count: {len(textboxs)}")  # Debugging

row_index = len(text_input)  
print(row_index)
for key, values in options.items():
    col_index = 1
    input_label = tk.Label(button_frame, text=key, font=("Arial", 15, "bold"))
    input_label.grid(row = row_index, column=0, sticky="w", padx=10, pady=5)
    for value in options[key]:
        create_button(button_frame, row_index, col_index, key, value)
        if col_index >= 5:
            col_index = 1
            row_index += 1
        else:
            col_index += 1
    row_index += 1

        
def check_subcategories():
    global subcategory_buttons  
    global row_index
    for btn in subcategory_buttons:
        btn.destroy()
        if btn in all_buttons:
            del all_buttons[btn]
    for lbl in labels:
        lbl.destroy()
    for txt in textboxs:
        txt.destroy()
    labels.clear()
    textboxs.clear()
    subcategory_buttons.clear()  

    if selected_buttons.get("Category") == "Tops":
        create_subcategory("Tops")
        if selected_buttons.get("Subcategory") != "T-shirts":
            create_label("Top-to-bottom")
            create_label("Pit-to-pit")
            create_label("Pit-to-sleeve")            
        else:
            create_label("Top-to-bottom")
            create_label("Pit-to-pit")
    if selected_buttons.get("Category") == "Bottoms":
        create_subcategory("Bottoms")
        create_label("Waist")
        create_label("Inseam")
        create_label("Leg Opening")
        if selected_buttons.get("Subcategory"):
            create_type(selected_buttons.get("Subcategory"))
            create_fit(selected_buttons.get("Subcategory"))
    
    if selected_buttons.get("Category") == "Coats and Jackets":
        create_subcategory("Coats and Jackets")    
        create_label("Top-to-bottom")
        create_label("Pit-to-pit")
        create_label("Pit-to-sleeve")   
        if selected_buttons.get("Subcategory") == "Coats":
            create_type("Coats")
        if selected_buttons.get("Subcategory") == "Jackets":
            create_type("Jackets")
    
    if selected_buttons.get("Category") == "Footwear":
        create_subcategory("Footwear")
        print("Creating Size_text field")  # Debugging: Ensure this runs

        create_label("Size_text")
        if selected_buttons.get("Subcategory") == "Boots":
            create_type("Boots")
        if selected_buttons.get("Subcategory") == "Sneakers":
            create_type("Sneakers")


def create_subcategory(clothing_category):
    global row_index
    col_index = 1
    row_index += 1
    for subcategory in subcategory_options[clothing_category]:
        btn = create_button(button_frame, row_index, col_index, "Subcategory", subcategory)
        subcategory_buttons.append(btn)
        all_buttons[btn] = ("Subcategory", subcategory)  # ✅ Ensure tracking in all_buttons
        col_index += 1
    update_all_buttons()  # ✅ Refresh button colors after creation


def create_type(clothing_type):
    global row_index
    col_index = 1
    row_index += 1
    for type in type_options[clothing_type]:
        btn = create_button(button_frame, row_index, col_index, "Type", type)
        subcategory_buttons.append(btn)
        all_buttons[btn] = ("Type", type)  # ✅ Ensure tracking in all_buttons
        col_index += 1
    update_all_buttons()  # ✅ Refresh button colors after creation

def create_fit(clothing_type):
    global row_index
    col_index = 1
    row_index += 1
    for fit in fit_options[clothing_type]:
        btn = create_button(button_frame, row_index, col_index, "Fit", fit)
        subcategory_buttons.append(btn)
        all_buttons[btn] = ("Fit", fit)  # ✅ Ensure tracking in all_buttons
        col_index += 1
    update_all_buttons()  # ✅ Refresh button colors after creation

def on_submit():
    print("Submitted")
    automate_depop_listing(selected_buttons, text_inputs_data)
    text_inputs_data.clear()
    print("text_input cleared")
    # Clear selected options
    selected_buttons.clear()
    print("cleared")
    selected_styles.clear()
    print("clear 1")
    selected_types.clear()
    print("clear 2")
    selected_materials.clear()
    print("clear 3")
    selected_fit.clear()
    print("clear 4")
    selected_occasion.clear()
    print("clear 5")
    print(f"Textbox count: {len(textboxs)}")  # Debugging

    # Clear textboxes in the UI
    for name, textbox in textbox_dict.items():
        textbox.delete("1.0", "end")
    print("Cleared all textboxes")
    # Update button states
    update_all_buttons()

    # Remove subcategory fields and labels
    check_subcategories()

submit_button = tk.Button(root, text="Submit", font=("Arial", 12), padx=10, pady=5, command=on_submit)
submit_button.pack(side="bottom", pady=20)
root.mainloop()

