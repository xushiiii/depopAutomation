# src/screens/listing.py
import tkinter as tk
import threading

from src.helpers.tab_nav import focus_next_widget
from src.options import (
    options,
    subcategory_options,
    type_options,
    fit_options,
)
from src import state


class ListingScreen(tk.Frame):
    DEPOP_FORM_ORDER = [
        "button", "Category",
        "button", "Subcategory",
        "text", "Title",
        "text", "Description",
        "text", "Hashtags",
        "text", "Bought For Price",
        "text", "Listing Price",
        "text", "Location",
        "measurement", "Measurement",
        "text", "Size", 
        "text", "Brand",
        "button", "Gender",
        "button", "Condition",
        "button", "Color",
        "button", "Occasion",
        "button", "Material",
        "button", "Source",
        "button", "Age",
        "button", "Style",
    ]
    MEASUREMENTS = {
        "Tops": ["Pit-to-pit", "Top-to-bottom", "Pit-to-sleeve"], 
        "Bottoms": ["Leg Opening", "Inseam", "Rise", "Waist"], 
        "Coats and jackets" : ["Pit-to-pit", "Top-to-bottom", "Pit-to-sleeve"]
    }

    BG_COLOR = "#f0f0f0"
    ACCENT_COLOR = "#4a7abc"
    TEXT_COLOR = "#333333"
    BUTTON_COLOR = "#ffffff"
    SELECTED_BUTTON_COLOR = "#dbeafe"  # nicer light blue
    FONT_FAMILY = "Segoe UI"

    def __init__(self, parent, controller):
        super().__init__(parent, bg=self.BG_COLOR)
        self.controller = controller

        self.grailed_enabled = tk.BooleanVar(master=controller, value=False)
        self.ebay_enabled = tk.BooleanVar(master=controller, value=False)
        self.sheets_enabled = tk.BooleanVar(master=controller, value=True)

        self.row_index = 0
        self._build_ui()

    def _build_ui(self):
        top = tk.Frame(self, bg=self.BG_COLOR)
        top.pack(fill="x")

        tk.Button(
            top,
            text="← Back",
            command=lambda: self.controller.show("HomeScreen"),
            bd=1,
            relief="solid",
        ).pack(side="left", padx=10, pady=10)

        tk.Label(
            top,
            text="User Input Form",
            font=(self.FONT_FAMILY, 16, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        ).pack(side="left", padx=10)

        self.main_container = tk.Frame(self, bg=self.BG_COLOR, padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)

        # Canvas + scrollbar
        self.canvas = tk.Canvas(self.main_container, bg=self.BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y", padx=5)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BG_COLOR, padx=20, pady=20)
        self._canvas_window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # keep scrollregion updated
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # prevent horizontal clipping: match inner frame width to canvas width
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel
        self.controller.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.main_frame = tk.Frame(self.scrollable_frame, bg=self.BG_COLOR)
        self.main_frame.pack(fill="x", pady=10)

        self.form_frame = tk.LabelFrame(
            self.main_frame,
            text="Item Details",
            font=(self.FONT_FAMILY, 12, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            padx=15,
            pady=15,
        )
        self.form_frame.pack(fill="x", padx=10, pady=10)

        # Make "controls" column expand
        self.form_frame.grid_columnconfigure(0, weight=0)
        self.form_frame.grid_columnconfigure(1, weight=1)

        # Checkboxes row (row 0)
        self.sheets_checkbox = tk.Checkbutton(
            self.form_frame,
            text="Track Expenses in Sheets?",
            variable=self.sheets_enabled,
            font=(self.FONT_FAMILY, 12, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            selectcolor=self.BG_COLOR,
            activebackground=self.BG_COLOR,
            activeforeground=self.TEXT_COLOR,
        )
        self.grailed_checkbox = tk.Checkbutton(
            self.form_frame,
            text="Draft on Grailed?",
            variable=self.grailed_enabled,
            font=(self.FONT_FAMILY, 12, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            selectcolor=self.BG_COLOR,
            activebackground=self.BG_COLOR,
            activeforeground=self.TEXT_COLOR,
            command=self.build_form,
        )
        self.ebay_checkbox = tk.Checkbutton(
            self.form_frame,
            text="Draft on Ebay?",
            variable=self.ebay_enabled,
            font=(self.FONT_FAMILY, 12, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            selectcolor=self.BG_COLOR,
            activebackground=self.BG_COLOR,
            activeforeground=self.TEXT_COLOR,
            command=self.build_form,
        )

        self.sheets_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 8))
        self.grailed_checkbox.grid(row=0, column=1, sticky="w", padx=10, pady=(0, 8))
        self.ebay_checkbox.grid(row=0, column=2, sticky="w", padx=10, pady=(0, 8))

        self.build_form()

        submit_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        submit_frame.pack(fill="x", padx=10, pady=20)

        tk.Button(
            submit_frame,
            text="Create Listing",
            font=(self.FONT_FAMILY, 12, "bold"),
            bg=self.ACCENT_COLOR,
            fg="white",
            padx=18,
            pady=10,
            bd=0,
            relief="flat",
            command=self.on_submit,
        ).pack(pady=10)

    # ----------------------------
    # EVENT HANDLERS / HELPERS
    # ----------------------------
    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self._canvas_window_id, width=event.width)

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_text_change(self, label_name: str, textbox: tk.Text):
        state.text_inputs_data[label_name] = textbox.get("1.0", "end-1c").strip()

    def create_button(self, parent_frame, row, col, category, button_text):
        btn = tk.Button(
            parent_frame,
            text=button_text,
            font=(self.FONT_FAMILY, 11),
            bg=self.BUTTON_COLOR,
            fg=self.TEXT_COLOR,
            relief="solid",
            bd=1,
            padx=12,
            pady=6,
            width=12,
            command=lambda c=category, v=button_text: self.on_button_click(c, v),
        )
        btn.grid(row=row, column=col, padx=6, pady=6, sticky="w")
        state.all_buttons[btn] = (category, button_text)
        return btn

    def _set_button_selected(self, btn: tk.Button, selected: bool):
        if selected:
            btn.config(bg=self.SELECTED_BUTTON_COLOR, relief="solid", bd=1)
        else:
            btn.config(bg=self.BUTTON_COLOR, relief="solid", bd=1)

    def update_all_buttons(self):
        for btn, (category, value) in list(state.all_buttons.items()):
            if not btn.winfo_exists():
                del state.all_buttons[btn]
                continue

            selected = (
                (category == "Style" and value in state.selected_styles) or
                (category == "Color" and value in state.selected_color) or
                (category == "Type" and value in state.selected_types) or
                (category == "Fit" and value in state.selected_fit) or
                (category == "Occasion" and value in state.selected_occasion) or
                (category == "Material" and value in state.selected_materials) or
                (category == "Subcategory" and state.selected_buttons.get("Subcategory") == value) or
                (state.selected_buttons.get(category) == value)
            )
            self._set_button_selected(btn, selected)

    def on_button_click(self, category, value):
        if category == "Category":
            previous_category = state.selected_buttons.get("Category", "")
            if previous_category and previous_category != value:
                state.selected_styles.clear()
                state.selected_types.clear()

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
            if selected_cat == "Bottoms":
                type_limit = 3
            elif selected_cat == "Coats and jackets":
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

        self.update_all_buttons()

        # Rebuild form if category/subcategory changes to prevent overlapping widgets
        if category in ("Category", "Subcategory"):
            self.build_form()
            self.update_all_buttons()

    # ----------------------------
    # FORM BUILDING
    # ----------------------------
    def build_form(self):
        # Remove widgets beyond row 0
        for widget in self.form_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        # Keep selections, but remove old button refs
        for btn in list(state.all_buttons.keys()):
            if not btn.winfo_exists():
                del state.all_buttons[btn]

        # Preserve text
        preserved_text_values = dict(state.text_inputs_data)

        # Clear text state
        state.text_inputs_data.clear()
        state.textbox_dict.clear()

        self._preserved_text_values = preserved_text_values
        self.row_index = 1

        i = 0
        while i < len(self.DEPOP_FORM_ORDER):
            item_type = self.DEPOP_FORM_ORDER[i]
            item_name = self.DEPOP_FORM_ORDER[i + 1]

            if item_type == "text":
                self.create_text_input(self.form_frame, item_name)

            elif item_type == "button":
                if item_name in ("Subcategory", "Type", "Fit"):
                    self._insert_dynamic_buttons_if_needed(item_name)
                elif item_name in options:
                    self._create_button_group(self.form_frame, item_name)

            elif item_type == "measurement":
                self.add_measurements()
            i += 2

        # Restore text values
        for key, value in self._preserved_text_values.items():
            if key in state.textbox_dict and state.textbox_dict[key].winfo_exists():
                state.textbox_dict[key].delete("1.0", "end")
                state.textbox_dict[key].insert("1.0", value)
                state.text_inputs_data[key] = value

        delattr(self, "_preserved_text_values")

    def _insert_dynamic_buttons_if_needed(self, button_type):
        cat = state.selected_buttons.get("Category")
        subcat = state.selected_buttons.get("Subcategory")

        if button_type == "Subcategory" and cat:
            if cat in subcategory_options:
                self.create_subcategory(cat)

        elif button_type == "Type" and cat and subcat:
            # Bottoms: use the subcategory itself
            if cat == "Bottoms" and subcat in ("Jeans", "Sweatpants", "Trousers", "Leggings"):
                self.create_type(subcat)
            elif cat == "Coats and jackets" and subcat in ("Coats", "Jackets"):
                self.create_type(subcat)
            elif cat == "Footwear" and subcat in ("Boots", "Trainers", "Loafers"):
                self.create_type(subcat)

        elif button_type == "Fit" and cat and subcat:
            if cat == "Bottoms" and subcat in ("Jeans", "Sweatpants", "Trousers", "Leggings"):
                self.create_fit(subcat)

    def create_text_input(self, parent, label):
        text_label = tk.Label(
            parent,
            text=label,
            font=(self.FONT_FAMILY, 13, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        text_label.grid(row=self.row_index, column=0, sticky="nw", padx=10, pady=6)
        
        labels = {"Top-to-bottom", "Pit-to-pit", "Pit-to-sleeve", "Leg opening", "Inseam", "Rise", "Waist"}
        is_measurement = label in labels
        if is_measurement:
            textbox = tk.Text(
                parent,
                height=2,
                width=5,
                font=(self.FONT_FAMILY, 11),
                wrap="word",
                bd=1,
                relief="solid",
            )
            # For measurements, don't expand - use fixed width
            textbox.grid(row=self.row_index, column=1, sticky="w", padx=10, pady=6)
        else:
            textbox = tk.Text(
                parent,
                height=2,
                font=(self.FONT_FAMILY, 11),
                wrap="word",
                bd=1,
                relief="solid",
            )
            # For regular inputs, expand to fill available space
            textbox.grid(row=self.row_index, column=1, sticky="ew", padx=10, pady=6)
            parent.grid_columnconfigure(1, weight=1)

        state.text_inputs_data.setdefault(label, "")
        state.textbox_dict[label] = textbox

        textbox.bind("<KeyRelease>", lambda event, name=label, tb=textbox: self.on_text_change(name, tb))
        textbox.bind("<Tab>", lambda event, tb=textbox: focus_next_widget(state.textbox_dict, event, tb))

        self.row_index += 1

    def _create_button_group(self, parent, category):
        if category not in options:
            return

        label = tk.Label(
            parent,
            text=category,
            font=(self.FONT_FAMILY, 13, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        label.grid(row=self.row_index, column=0, sticky="nw", padx=10, pady=6)

        btn_frame = tk.Frame(parent, bg=self.BG_COLOR)
        btn_frame.grid(row=self.row_index, column=1, sticky="w", padx=10, pady=6)
        parent.grid_columnconfigure(1, weight=1)

        values = options[category]
        buttons_per_row = 4
        r = 0
        c = 0

        for value in values:
            btn = self.create_button(btn_frame, r, c, category, value)
            c += 1
            if c >= buttons_per_row:
                c = 0
                r += 1

        self.row_index += 1

    def create_subcategory(self, clothing_category):
        values = subcategory_options.get(clothing_category, [])
        if not values:
            return

        label = tk.Label(
            self.form_frame,
            text="Subcategory",
            font=(self.FONT_FAMILY, 13, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        label.grid(row=self.row_index, column=0, sticky="nw", padx=10, pady=6)

        btn_frame = tk.Frame(self.form_frame, bg=self.BG_COLOR)
        btn_frame.grid(row=self.row_index, column=1, sticky="w", padx=10, pady=6)

        buttons_per_row = 4
        r = 0
        c = 0

        for subcat in values:
            btn = self.create_button(btn_frame, r, c, "Subcategory", subcat)
            state.all_buttons[btn] = ("Subcategory", subcat)

            c += 1
            if c >= buttons_per_row:
                c = 0
                r += 1

        self.row_index += 1

    def create_type(self, clothing_type):
        values = type_options.get(clothing_type, [])
        if not values:
            return

        label = tk.Label(
            self.form_frame,
            text="Type",
            font=(self.FONT_FAMILY, 13, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        label.grid(row=self.row_index, column=0, sticky="nw", padx=10, pady=6)

        btn_frame = tk.Frame(self.form_frame, bg=self.BG_COLOR)
        btn_frame.grid(row=self.row_index, column=1, sticky="w", padx=10, pady=6)

        buttons_per_row = 5
        r = 0
        c = 0

        for t in values:
            btn = self.create_button(btn_frame, r, c, "Type", t)
            state.all_buttons[btn] = ("Type", t)

            c += 1
            if c >= buttons_per_row:
                c = 0
                r += 1

        self.row_index += 1

    def create_fit(self, clothing_type):
        values = fit_options.get(clothing_type, [])
        if not values:
            return

        label = tk.Label(
            self.form_frame,
            text="Fit",
            font=(self.FONT_FAMILY, 13, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        label.grid(row=self.row_index, column=0, sticky="nw", padx=10, pady=6)

        btn_frame = tk.Frame(self.form_frame, bg=self.BG_COLOR)
        btn_frame.grid(row=self.row_index, column=1, sticky="w", padx=10, pady=6)

        buttons_per_row = 4
        r = 0
        c = 0

        for fit in values:
            btn = self.create_button(btn_frame, r, c, "Fit", fit)
            state.all_buttons[btn] = ("Fit", fit)

            c += 1
            if c >= buttons_per_row:
                c = 0
                r += 1

        self.row_index += 1

    # ----------------------------
    # SUBMIT / RESET
    # ----------------------------
    def on_submit(self):
        if self.sheets_enabled.get():
            try:
                from src.google_sheets import write_to_sheets
                write_to_sheets(
                    state.text_inputs_data.get("Bought For Price"),
                    state.text_inputs_data.get("Title"),
                    state.text_inputs_data.get("Location"),
                    state.selected_buttons.get("Category"),
                    state.selected_buttons.get("Subcategory"),
                )
            except Exception as e:
                print(f"[Sheets] Error: {e}")
                import traceback
                traceback.print_exc()

        threading.Thread(
            target=self.controller.create_depop_draft,
            args=(state.selected_buttons.copy(), state.text_inputs_data.copy()),
            daemon=True,
        ).start()

        self.reset_form()

    def reset_form(self):
        for btn in list(state.all_buttons.keys()):
            if btn.winfo_exists():
                self._set_button_selected(btn, False)

        state.selected_buttons.clear()
        state.selected_styles.clear()
        state.selected_types.clear()
        state.selected_fit.clear()
        state.selected_occasion.clear()
        state.selected_color.clear()
        state.selected_materials.clear()

        state.text_inputs_data.clear()

        for textbox in list(state.textbox_dict.values()):
            if textbox.winfo_exists():
                textbox.delete("1.0", "end")

        self.update_all_buttons()
        self.build_form()
        print("Form reset complete")

    def add_measurements(self):
        cat = state.selected_buttons.get("Category")
        fields = self.MEASUREMENTS.get(cat, [])
        for field in fields:
            self.create_text_input(self.form_frame, field)