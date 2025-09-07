import tkinter as tk
from .helpers.tab_nav import focus_next_widget
from .automation import automate_depop_listing
from .options import options, subcategory_options, common_bottom_fit, common_bottom_types, type_options, fit_options, text_input_grailed, text_input_default, text_input_ebay
from . import state
from .grailedAutomation import automate_grailed_listing
from src.google_sheets import write_to_sheets

# Style Configuration
BG_COLOR = "#f0f0f0"  # Light gray background
ACCENT_COLOR = "#4a7abc"  # Blue accent color
TEXT_COLOR = "#333333"  # Dark gray text
BUTTON_COLOR = "#ffffff"  # White button background
SELECTED_BUTTON_COLOR = "#e1e8f0"  # Light blue for selected buttons
FONT_FAMILY = "Segoe UI"  # Modern font

# Configure root window style
root = tk.Tk()
root.title("Depop Item Form")
root.geometry("1200x700")  # Slightly larger window
root.configure(bg=BG_COLOR)
i = 0
label_exists = False

grailed_enabled = tk.BooleanVar(value=False)
ebay_enabled = tk.BooleanVar(value=True)
sheets_enabled = tk.BooleanVar(value=True)

def on_text_change(event, label_name, textbox):
    state.text_inputs_data[label_name] = textbox.get("1.0", "end-1c").strip()

def on_button_click(category, value):
    if category == "Category":
        previous_category = state.selected_buttons.get("Category", "")

        if previous_category and previous_category != value:
            state.selected_styles.clear()  
            state.selected_types.clear()  
            #print(f"Cleared styles and types when switching from {previous_category} to {value}")

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

    #print(f"Selected {category}: {value}")  
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

def create_label(title):
    global row_index, label_exists
    row_index += 1

    col_index = 0
    text_label = tk.Label(
        button_frame, 
        text=title, 
        font=(FONT_FAMILY, 14, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    text_label.grid(row=row_index, column=col_index, sticky="w", padx=15, pady=8)

    textbox = tk.Text(
        button_frame, 
        height=1, 
        width=15, 
        font=(FONT_FAMILY, 11),
        wrap="word", 
        bd=1, 
        relief="solid",
        bg="white"
    )
    textbox.grid(row=row_index, column=1, sticky="ew", padx=15, pady=8)
    button_frame.columnconfigure(1, weight=1)

    state.text_inputs_data[title] = ""
    state.textbox_dict[title] = textbox

    textbox.bind("<KeyRelease>", lambda event: on_text_change(event, title, textbox))
    textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(state.textbox_dict, event, tb))

    state.labels.append(text_label)
    state.textboxs.append(textbox)
    label_exists = True

def create_button(parent_frame, j, i, category, button_text):
    input_button = tk.Button(
        parent_frame, 
        text=button_text, 
        font=(FONT_FAMILY, 11),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        relief="flat",
        padx=10,
        pady=5,
        command=lambda c=category, v=button_text: on_button_click(c, v)
    )
    input_button.grid(row=j, column=i, padx=8, pady=6, sticky="w")
    state.all_buttons[input_button] = (category, button_text)
    return input_button

def build_text_inputs():
    # Remove existing widgets
    for widget in text_frame.grid_slaves():
        if int(widget.grid_info()["row"]) > 0:  # Keep the checkboxes in row 0
            widget.destroy()
    state.text_inputs_data.clear()
    state.textbox_dict.clear()

    # Choose which fields to show
    if grailed_enabled.get():
        fields = text_input_grailed
    else:
        fields = text_input_default

    for i, label in enumerate(fields):
        text_label = tk.Label(text_frame, text=label, font=("Arial", 15, "bold"))
        text_label.grid(row=i+1, column=0, sticky="w", padx=10)
        textbox = tk.Text(text_frame, height=3, width=30, font=("Arial", 10), wrap="word", bd=1, relief="solid")
        textbox.grid(row=i+1, column=1, sticky="ew", padx=10, pady=5)
        text_frame.columnconfigure(1, weight=1)
        state.text_inputs_data[label] = ""
        state.textbox_dict[label] = textbox
        textbox.bind("<KeyRelease>", lambda event, name=label, tb=textbox: on_text_change(event, name, tb))
        textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(state.textbox_dict, event, tb))

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
        create_label("Rise")
        if state.selected_buttons.get("Subcategory") in ["Jeans", "Sweatpants", "Pants", "Leggings"]:
            create_type("Jeans")
            create_fit("Jeans")
    
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
        state.all_buttons[btn] = ("Subcategory", subcategory)
        col_index += 1
    update_all_buttons()

def create_type(clothing_type):
    global row_index
    col_index = 1
    row_index += 1
    for type in type_options[clothing_type]:
        btn = create_button(button_frame, row_index, col_index, "Type", type)
        state.subcategory_buttons.append(btn)
        state.all_buttons[btn] = ("Type", type)
        col_index += 1
    update_all_buttons()

def create_fit(clothing_type):
    global row_index
    col_index = 1
    row_index += 1
    for fit in fit_options[clothing_type]:
        btn = create_button(button_frame, row_index, col_index, "Fit", fit)
        state.subcategory_buttons.append(btn)
        state.all_buttons[btn] = ("Fit", fit)
        col_index += 1
    update_all_buttons()  

def on_submit():
    if sheets_enabled.get() == True:
        write_to_sheets(
            state.text_inputs_data.get("Bought For Price"),  # price
            state.text_inputs_data.get("Title"),             # description
            state.text_inputs_data.get("Location"),          # location  
            state.selected_buttons.get("Category"),        # category
            state.selected_buttons.get("Subcategory")      # subcategory
        )    
    automate_depop_listing(state.selected_buttons, state.text_inputs_data)

    if grailed_enabled.get() == True:
        automate_grailed_listing(state.selected_buttons, state.text_inputs_data)

    # Reset all button states
    for btn, (category, value) in list(state.all_buttons.items()):
        if btn.winfo_exists():
            btn.config(bg=BUTTON_COLOR, relief="raised")  # Reset to default button appearance
    
    # Clear all selected values
    state.selected_buttons.clear()
    state.selected_styles.clear()
    state.selected_types.clear()
    state.selected_fit.clear()
    state.selected_occasion.clear()
    state.selected_color.clear()
    state.selected_materials.clear()
    
    # Clear all text inputs
    for textbox in state.textbox_dict.values():
        if textbox.winfo_exists():
            textbox.delete("1.0", "end")
    
    # Update button states and check subcategories
    update_all_buttons()
    check_subcategories()
    
    print("Form reset complete")

# Create main container with padding
main_container = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_container.pack(fill="both", expand=True)

# Create canvas and scrollbar
canvas = tk.Canvas(main_container, bg=BG_COLOR, highlightthickness=0)
scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_COLOR, padx=20, pady=20)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack scrollbar and canvas
scrollbar.pack(side="right", fill="y", padx=5)
canvas.pack(side="left", fill="both", expand=True)

def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

root.bind_all("<MouseWheel>", _on_mouse_wheel)

# Create main content frame
main_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
main_frame.pack(fill="x", pady=10)

# Create section frames with visual separation
text_frame = tk.LabelFrame(main_frame, text="Item Details", font=(FONT_FAMILY, 12, "bold"), 
                          bg=BG_COLOR, fg=TEXT_COLOR, padx=15, pady=15)
text_frame.pack(fill="x", padx=10, pady=10)

button_frame = tk.LabelFrame(main_frame, text="Item Attributes", font=(FONT_FAMILY, 12, "bold"),
                           bg=BG_COLOR, fg=TEXT_COLOR, padx=15, pady=15)
button_frame.pack(fill="x", padx=10, pady=10)

ebay_checkbox = tk.Checkbutton(
    text_frame,
    text="Draft on Ebay?",
    variable=ebay_enabled,
    font=(FONT_FAMILY, 15, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    selectcolor=BG_COLOR,
    activebackground=BG_COLOR,
    activeforeground=TEXT_COLOR,
    command=build_text_inputs
)

grailed_checkbox = tk.Checkbutton(
    text_frame,
    text="Draft on Grailed?",
    variable=grailed_enabled,
    font=(FONT_FAMILY, 15, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    selectcolor=BG_COLOR,
    activebackground=BG_COLOR,
    activeforeground=TEXT_COLOR,
    command=build_text_inputs
)

sheets_checkbox = tk.Checkbutton(
    text_frame,
    text="Track Expenses in Sheets?",
    variable=sheets_enabled,
    font=(FONT_FAMILY, 15, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    selectcolor=BG_COLOR,
    activebackground=BG_COLOR,
    activeforeground=TEXT_COLOR
)

sheets_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
grailed_checkbox.grid(row=0, column=1, sticky="w", padx=10, pady=(0, 5))
ebay_checkbox.grid(row = 0, column=2, stick="w", padx=10, pady=(0, 5))

if grailed_enabled.get() == True:
    text_input = text_input_grailed
else:
    text_input = text_input_default
if ebay_enabled.get() == True:
    text_input = text_input_ebay
else:
    text_input = text_input_default
    
for i in range(len(text_input)):
    text_label = tk.Label(text_frame, text=text_input[i], font=("Arial", 15, "bold"))
    text_label.grid(row = i+1, column=0, sticky="w", padx=10)

    textbox = tk.Text(text_frame, height = 3, width = 30, font=("Arial", 10), wrap="word", bd = 1, relief="solid")
    textbox.grid(row=i+1, column=1, sticky="ew", padx=10, pady=5)
    text_frame.columnconfigure(1, weight=1)
    state.text_inputs_data[text_input[i]] = ""
    state.textbox_dict[text_input[i]] = textbox  # ✅ Stores textbox widgets

    textbox.bind("<KeyRelease>", lambda event, name=text_input[i], tb=textbox: on_text_change(event, name, tb))
    textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(state.textbox_dict, event, tb))  # ✅ Bind Tab key

row_index = len(text_input) + 1  # Update row_index to account for the extra row

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

# Create submit button frame
submit_frame = tk.Frame(main_frame, bg=BG_COLOR)
submit_frame.pack(fill="x", padx=10, pady=20)

submit_button = tk.Button(
    submit_frame,
    text="Create Listing",
    font=(FONT_FAMILY, 12, "bold"),
    bg=ACCENT_COLOR,
    fg="white",
    padx=20,
    pady=10,
    relief="flat",
    command=on_submit
)
submit_button.pack(pady=10)

build_text_inputs()

root.mainloop()

