import tkinter as tk 

options = {
    "Category": ["Tops", "Bottoms", "Coats and Jackets", "Footwear", "Dresses"], 
    "Occasion": ["Casual", "Festival", "Going Out", "Outdoors", "Party", "Relaxation", "School", "Summer", "Winter", "Work", "Workout"],
    "Material": ["Acrylic", "Canvas", "Cotton", "Polyester", "Leather", "Nylon", "Silk", "Wool"],
    "Condition": ["Brand New", "Like New", "Used - Excellent", "Used - Good", "Used - Fair"],
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

button_fields = set(options.keys())
selected_options = {}

root = tk.Tk()
root.title("Depop Item Form")

submit_button = tk.Button(root, text="Submit", font=("Arial", 12), padx=10, pady=5)
submit_button.pack(side="bottom", pady=20)
root.mainloop()