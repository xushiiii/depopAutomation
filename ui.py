import tkinter as tk
from functools import partial
from test import automate_depop_listing
import tkinter as tk 
text_input = ["Description", "Bought for Price", "Material", "Brand", "Condition", "Size"]
options = {
    "Occasion": ["Casual", "Festival", "Going Out", "Outdoors", "Party", "Relaxation", "School", "Summer", "Winter", "Work", "Workout"],
    "Material": ["Acrylic", "Canvas", "Cotton", "Polyester", "Leather", "Nylon", "Silk", "Wool"],
    "Condition": ["Brand New", "Like New", "Used - Excellent", "Used - Good", "Used - Fair"],
    "Category": ["Tops", "Bottoms", "Coats and Jackets", "Footwear"]
}

subcategory_options = {
    "Tops": ["T-shirts", "Hoodies", "Sweatshirts", "Sweaters", "Cardigans", "Shirts", "Other"],
    "Bottoms":["Jeans", "Sweatpants", "Pants", "Shorts", "Leggings"],
    "Coats and Jackets": ["Coats", "Jackets"],
    "Footwear": ["Sneakers", "Boots"]
}
type_options = {
    "Jeans": ["Cargo", "Distressed", "Faded", "Embroidered", "Ripped"],
    "Sweatpants": ["Cargo", "Distressed", "Faded", "Embroidered", "Ripped"],
    "Pants": ["Cargo", "Distressed", "Faded", "Embroidered", "Ripped"],
    "Coats": ["Overcoat", "Puffer", "Raincoat"],
    "Jackets": ["Bomber", "Lightweight", "Shacket", "Varsity", "Windbreaker"],
    "Sneakers": ["Basketball", "Gym", "Lifestyle", "Running", "Skateboarding", "Tennis"],
    "Boots": ["Ankle", "Chelsea", "Biker", "Military", "Platform"]
}

subcategory_buttons = []  
labels = []
textboxs = []
selected_buttons = {}
def on_button_click(category, value):
    selected_buttons[category] = value
    print(f"Selected {category}: {value}")  
    check_subcategories()


def create_button(parent_frame, j, i, category, button_text):
    input_button = tk.Button(
        parent_frame, 
        text=button_text, 
        font=("Arial", 12, "bold"),
        command=lambda: on_button_click(category, button_text)
    )
    input_button.grid(row = j, column = i, padx=10, pady=5, stick="w")
    return input_button

root = tk.Tk()
root.title("Depop Item Form")
root.geometry("")

main_frame = tk.Frame(root)
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
    labels.append(text_label)
    textboxs.append(textbox)
    label_exists = True


for i in range(len(text_input)):
    text_label = tk.Label(text_frame, text=text_input[i], font=("Arial", 15, "bold"))
    text_label.grid(row = i, column=0, sticky="w", padx=10)

    textbox = tk.Text(text_frame, height = 3, width = 30, font=("Arial", 10), wrap="word", bd = 1, relief="solid")
    textbox.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
    text_frame.columnconfigure(1, weight=1)

row_index = len(text_input)  
print(row_index)
for key, values in options.items():
    col_index = 1
    input_label = tk.Label(button_frame, text=key, font=("Arial", 15, "bold"))
    input_label.grid(row = row_index, column=0, sticky="w", padx=10, pady=5)
    for value in options[key]:
        create_button(button_frame, row_index, col_index, key, value)
        col_index += 1
    row_index += 1

        
def check_subcategories():
    global subcategory_buttons  
    global row_index
    for btn in subcategory_buttons:
        btn.destroy()
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
            create_type("Jeans")
    
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
        create_label("Size")
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
        col_index += 1

def create_type(clothing_type):
    global row_index
    col_index = 1
    row_index += 1
    for type in type_options[clothing_type]:
        btn = create_button(button_frame, row_index, col_index, "Type", type)
        subcategory_buttons.append(btn)
        col_index += 1

def on_submit():
    print("Submitted")
    automate_depop_listing()

submit_button = tk.Button(root, text="Submit", font=("Arial", 12), padx=10, pady=5, command=on_submit)
submit_button.pack(side="bottom", pady=20)
root.mainloop()

