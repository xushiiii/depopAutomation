import tkinter as tk
from helpers.tab_nav import focus_next_widget
from automation import automate_depop_listing
import tkinter as tk 
from options import options, text_input, subcategory_options, common_bottom_fit, common_bottom_types, type_options, fit_options
import state 

def on_text_change(event, label_name, textbox):
    state.text_inputs_data[label_name] = textbox.get("1.0", "end-1c").strip()
    print(f"Updated {label_name}: {state.text_inputs_data[label_name]}")  

def on_button_click(category, value):
    if category == "Category":
        previous_category = state.selected_buttons.get("Category", "")

        if previous_category and previous_category != value:
            state.selected_styles.clear()  
            state.selected_types.clear()  
            print(f"Cleared styles and types when switching from {previous_category} to {value}")

        state.selected_buttons["Category"] = value
        state.selected_buttons.pop("Subcategory", None)  
        state.selected_buttons.pop("Type", None)  
    elif category == "Style":
        if value in state.selected_styles:
            state.selected_styles.remove(value)
        elif len(state.selected_styles) < 3:
            state.selected_styles.add(value)
        else:
            return 
        state.selected_buttons[category] = list(state.selected_styles)

    elif category == "Fit":
        if value in state.selected_fit:
            state.selected_fit.remove(value)
        elif len(state.selected_fit) < 2:
            state.selected_fit.add(value)
        else:
            return 
        state.selected_buttons[category] = list(state.selected_fit)

    elif category == "Occasion":
        if value in state.selected_occasion:
            state.selected_occasion.remove(value)
        elif len(state.selected_occasion) < 3:
            state.selected_occasion.add(value)
        else:
            return 
        state.selected_buttons[category] = list(state.selected_occasion)

    elif category == "Color":
        if value in state.selected_color:
            state.selected_color.remove(value)
        elif len(state.selected_color) < 2:
            state.selected_color.add(value)
        else:
            return
        state.selected_buttons[category] = list(state.selected_color)

        
    elif category == "Material":
        if value in state.selected_materials:
            state.selected_materials.remove(value)
        elif len(state.selected_materials) < 3:
            state.selected_materials.add(value)
        else:
            return 
        state.selected_buttons[category] = list(state.selected_materials)

    elif category == "Type":
        selected_cat = state.selected_buttons.get("Category")    
        type_limit = 1
        if selected_cat == "Bottoms":
            type_limit = 3
        elif selected_cat == "Coats and Jackets":
            type_limit = 1
        else:
            type_limit = 2

        if value in state.selected_types:
            state.selected_types.remove(value)
        elif len(state.selected_types) < type_limit:
            state.selected_types.add(value)
        else:
            return 
        state.selected_buttons["Type"] = list(state.selected_types)

    elif category == "Subcategory":  
        if state.selected_buttons.get("Subcategory") == value:
            del state.selected_buttons["Subcategory"]
        else:
            state.selected_buttons["Subcategory"] = value
    else:
        if state.selected_buttons.get(category) == value:
            del state.selected_buttons[category]
        else:
            state.selected_buttons[category] = value

    print(f"Selected {category}: {value}")  
    update_all_buttons()
    check_subcategories() 


def update_all_buttons():
    for btn, (category, value) in list(state.all_buttons.items()):  
        if btn.winfo_exists():
            if (category == "Style" and value in state.selected_styles) or \
               (category == "Color" and value in state.selected_color) or \
               (category == "Type" and value in state.selected_types) or \
               (category == "Fit" and value in state.selected_fit) or \
               (category == "Occasion" and value in state.selected_occasion) or \
               (category == "Material" and value in state.selected_materials) or \
               (category == "Subcategory" and state.selected_buttons.get("Subcategory") == value) or \
               (state.selected_buttons.get(category) == value):
                btn.config(bg="lightblue", relief="sunken")  
            else:
                btn.config(bg="white", relief="raised")  
        else:
            del state.all_buttons[btn]  


def create_button(parent_frame, j, i, category, button_text):
    input_button = tk.Button(
        parent_frame, 
        text=button_text, 
        font=("Arial", 12, "bold"),
        command=lambda c=category, v=button_text: on_button_click(c, v)  # ✅ Pass variables explicitly
    )
    input_button.grid(row = j, column = i, padx=10, pady=5, stick="w")
    state.all_buttons[input_button] = (category, button_text)
    return input_button

root = tk.Tk()
root.title("Depop Item Form")
root.geometry("1000x500")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

root.bind_all("<MouseWheel>", _on_mouse_wheel)  
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

    state.text_inputs_data[title] = ""  
    state.textbox_dict[title] = textbox  # ✅ Store textbox in dictionary

    print(f"Creating text field for {title}")  # Debugging

    textbox.bind("<KeyRelease>", lambda event: on_text_change(event, title, textbox))
    textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(state.textbox_dict, event, tb))  # ✅ Bind Tab key

    state.labels.append(text_label)
    state.textboxs.append(textbox)
    label_exists = True


for i in range(len(text_input)):
    text_label = tk.Label(text_frame, text=text_input[i], font=("Arial", 15, "bold"))
    text_label.grid(row = i, column=0, sticky="w", padx=10)

    textbox = tk.Text(text_frame, height = 3, width = 30, font=("Arial", 10), wrap="word", bd = 1, relief="solid")
    textbox.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
    text_frame.columnconfigure(1, weight=1)
    state.text_inputs_data[text_input[i]] = ""
    state.textbox_dict[text_input[i]] = textbox  # ✅ Stores textbox widgets

    textbox.bind("<KeyRelease>", lambda event, name=text_input[i], tb=textbox: on_text_change(event, name, tb))
    textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(state.textbox_dict, event, tb))  # ✅ Bind Tab key

    print(f"Textbox count: {len(state.textboxs)}")  # Debugging

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
    global row_index
    for btn in state.subcategory_buttons:
        btn.destroy()
        if btn in state.all_buttons:
            del state.all_buttons[btn]
    for lbl in state.labels:
        lbl.destroy()
    for txt in state.textboxs:
        txt.destroy()
    state.labels.clear()
    state.textboxs.clear()
    state.subcategory_buttons.clear()  

    if state.selected_buttons.get("Category") == "Tops":
        create_subcategory("Tops")
        if state.selected_buttons.get("Subcategory") != "T-shirts":
            create_label("Top-to-bottom")
            create_label("Pit-to-pit")
            create_label("Pit-to-sleeve")            
        else:
            create_label("Top-to-bottom")
            create_label("Pit-to-pit")
    if state.selected_buttons.get("Category") == "Bottoms":
        create_subcategory("Bottoms")
        create_label("Waist")
        create_label("Inseam")
        create_label("Leg Opening")
        if state.selected_buttons.get("Subcategory"):
            create_type(state.selected_buttons.get("Subcategory"))
            create_fit(state.selected_buttons.get("Subcategory"))
    
    if state.selected_buttons.get("Category") == "Coats and Jackets":
        create_subcategory("Coats and Jackets")    
        create_label("Top-to-bottom")
        create_label("Pit-to-pit")
        create_label("Pit-to-sleeve")   
        if state.selected_buttons.get("Subcategory") == "Coats":
            create_type("Coats")
        if state.selected_buttons.get("Subcategory") == "Jackets":
            create_type("Jackets")
    
    if state.selected_buttons.get("Category") == "Footwear":
        create_subcategory("Footwear")
        print("Creating Size_text field")  # Debugging: Ensure this runs

        create_label("Size_text")
        if state.selected_buttons.get("Subcategory") == "Boots":
            create_type("Boots")
        if state.selected_buttons.get("Subcategory") == "Sneakers":
            create_type("Sneakers")


def create_subcategory(clothing_category):
    global row_index
    col_index = 1
    row_index += 1
    for subcategory in subcategory_options[clothing_category]:
        btn = create_button(button_frame, row_index, col_index, "Subcategory", subcategory)
        state.subcategory_buttons.append(btn)
        state.all_buttons[btn] = ("Subcategory", subcategory)  # ✅ Ensure tracking in state.all_buttons
        col_index += 1
    update_all_buttons()  # ✅ Refresh button colors after creation


def create_type(clothing_type):
    global row_index
    col_index = 1
    row_index += 1
    for type in type_options[clothing_type]:
        btn = create_button(button_frame, row_index, col_index, "Type", type)
        state.subcategory_buttons.append(btn)
        state.all_buttons[btn] = ("Type", type)  # ✅ Ensure tracking in state.all_buttons
        col_index += 1
    update_all_buttons()  # ✅ Refresh button colors after creation

def create_fit(clothing_type):
    global row_index
    col_index = 1
    row_index += 1
    for fit in fit_options[clothing_type]:
        btn = create_button(button_frame, row_index, col_index, "Fit", fit)
        state.subcategory_buttons.append(btn)
        state.all_buttons[btn] = ("Fit", fit)  # ✅ Ensure tracking in state.all_buttons
        col_index += 1
    update_all_buttons()  # ✅ Refresh button colors after creation

def on_submit():
    print("Submitted")
    automate_depop_listing(state.selected_buttons, state.text_inputs_data)
    state.text_inputs_data.clear()
    print("text_input cleared")
    # Clear selected options
    state.clear_state()

    for name, textbox in state.textbox_dict.items():
        textbox.delete("1.0", "end")
    print("Cleared all textboxes")
    update_all_buttons()

    check_subcategories()

submit_button = tk.Button(root, text="Submit", font=("Arial", 12), padx=10, pady=5, command=on_submit)
submit_button.pack(side="bottom", pady=20)
root.mainloop()

