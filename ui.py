import tkinter as tk
from functools import partial

import tkinter as tk 
text_input = ["Description", "Material", "Brand", "Condition", "Size", "Colour"]
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

subcategory_buttons = []  # Track generated buttons to avoid duplicates

selected_buttons = {}
def on_button_click(category, value):
    selected_buttons[category] = value
    print(f"Selected {category}: {value}")  # Debugging output
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

if "Category" in selected_buttons and selected_buttons["Category"] == "Tops":
    col_index = 1
    for subcategory in subcategory_options["Tops"]:
        create_button(button_frame, row_index, col_index, "Subcategory", subcategory)
        col_index += 1
        
def check_subcategories():
    """Continuously checks if 'Tops' is selected and updates UI dynamically."""
    global subcategory_buttons  # Keep track of buttons to remove later

    # Remove previous buttons if they exist
    for btn in subcategory_buttons:
        btn.destroy()
    subcategory_buttons.clear()  # Reset list

    if selected_buttons.get("Category") == "Tops":
        col_index = 1

        # Create new buttons for subcategories
        for subcategory in subcategory_options["Tops"]:
            btn = create_button(button_frame, row_index, col_index, "Subcategory", subcategory)
            subcategory_buttons.append(btn)  # Track created buttons
            col_index += 1  # Move buttons to the right
        row_index += 1


submit_button = tk.Button(root, text="Submit", font=("Arial", 12), padx=10, pady=5)
submit_button.pack(side="bottom", pady=20)
root.mainloop()

