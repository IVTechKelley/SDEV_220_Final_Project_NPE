import tkinter as tk
from PIL import Image, ImageTk

# Sample data: three product categories, each with two products, price, and short description
products = {
    "Consoles": {
        "PlayStation": {"price": "$299.99", "description": "Next-gen gaming console", "image_path": "ps4.jpg"},
        "Xbox": {"price": "$349.99", "description": "Powerful gaming and entertainment system", "image_path": "xbox.jpg"}
    },
    "Laptops": {
        "MacBook": {"price": "$1299.99", "description": "Sleek and powerful laptop", "image_path": "macbook.jpg"},
        "Dell XPS": {"price": "$999.99", "description": "High-performance laptop for professionals", "image_path": "dell.jpg"}
    },
    "Appliances": {
        "Refrigerator": {"price": "$799.99", "description": "Energy-efficient refrigerator", "image_path": "fridge.jpg"},
        "Washing Machine": {"price": "$499.99", "description": "Front-loading washing machine", "image_path": "washing_machine.jpg"}
    }
}

def load_images():
    loaded_images = {}
    for category, products_dict in products.items():
        for product, info in products_dict.items():
            image_path = info.get("image_path")
            if image_path:
                img = Image.open(image_path)
                img = img.resize((50, 50), Image.ANTIALIAS)  # Resize the image to fit in the listbox
                loaded_images[product] = ImageTk.PhotoImage(img)
    return loaded_images

def update_listbox(category, search_query=None):
    listbox.delete(0, tk.END)  # Clear previous items

    loaded_images = load_images()

    if search_query:
        # Filter products based on the search query
        filtered_products = {
            product: info for product, info in products[category].items()
            if search_query.lower() in product.lower() or search_query.lower() in info["description"].lower()
        }
    else:
        # If no search query, display all products in the category
        filtered_products = products[category]

    for item, info in filtered_products.items():
        img = loaded_images.get(item)
        listbox.insert(tk.END, {"text": f"{category}: {item} - {info['price']} - {info['description']}", "image": img, "info": info})

def on_search():
    search_query = entry_search.get()
    selected_category = category_var.get()
    update_listbox(selected_category, search_query)

def show_add_to_cart_button(event):
    # Get the selected item from the listbox
    selected_item = listbox.get(listbox.curselection())

    # Display the "Add to Cart" button dynamically
    add_to_cart_button.place(x=event.x, y=event.y, anchor=tk.NW)
    add_to_cart_button.config(command=lambda: on_add_to_cart(selected_item))

def hide_add_to_cart_button(event):
    # Hide the "Add to Cart" button when not hovering over the listbox
    add_to_cart_button.place_forget()

def on_add_to_cart(selected_item):
    cart_listbox.insert(tk.END, selected_item)

def filter_category(category):
    category_var.set(category)
    update_listbox(category)

def open_shopping_cart():
    cart_window = tk.Toplevel(window)
    cart_window.title("Shopping Cart")

    cart_label = tk.Label(cart_window, text="Shopping Cart")
    cart_label.pack(pady=10)

    cart_listbox = tk.Listbox(cart_window, height=10, width=80)
    cart_listbox.pack(pady=10)

    remove_button = tk.Button(cart_window, text="Remove Item", command=lambda: remove_item(cart_listbox))
    remove_button.pack(pady=10)

    checkout_button = tk.Button(cart_window, text="Checkout", command=checkout)
    checkout_button.pack(pady=10)

    continue_shopping_button = tk.Button(cart_window, text="Continue Shopping", command=cart_window.destroy)
    continue_shopping_button.pack(pady=10)

def remove_item(cart_listbox):
    selected_index = cart_listbox.curselection()
    if selected_index:
        cart_listbox.delete(selected_index)

def checkout():
    # Placeholder function for checkout logic
    print("Checkout logic goes here")

# Create the main window
window = tk.Tk()
window.title("Shopping Window")

# Create and place widgets in the window
label_search = tk.Label(window, text="Search:")
label_search.pack(pady=10)

entry_search = tk.Entry(window)
entry_search.pack(pady=10)

category_var = tk.StringVar()
category_var.set("Consoles")  # Default category

category_menu = tk.OptionMenu(window, category_var, "Consoles", "Laptops", "Appliances")
category_menu.pack(pady=10)

button_search = tk.Button(window, text="Search", command=on_search)
button_search.pack(pady=10)

listbox = tk.Listbox(window, height=10, width=80)
listbox.pack(pady=10)

# Add to Cart button
add_to_cart_button = tk.Button(window, text="Add to Cart")
add_to_cart_button.place_forget()  # Initially hide the button

# Filter buttons
filter_frame = tk.Frame(window)
filter_frame.place_forget()  # Initially hide the filter frame

filter_btn = tk.Button(window, text="Filter", command=lambda: filter_frame.place(x=window.winfo_width()-100, y=0, anchor=tk.NE))
filter_btn.place(x=window.winfo_width()-100, y=0, anchor=tk.NE)

for category in ["Consoles", "Laptops", "Appliances"]:
    filter_category_button = tk.Button(filter_frame, text=category, command=lambda cat=category: filter_category(cat))
    filter_category_button.pack(side=tk.LEFT)

# Event binding to hide filter frame when clicked outside
window.bind("<Button-1>", lambda event: filter_frame.place_forget())

# Initialize listbox with default category
update_listbox(category_var.get())

# Set the initial text for the filter button
filter_btn["text"] = "Filter"

# Shopping Cart button
cart_button = tk.Button(window, text="Shopping Cart", command=open_shopping_cart)
cart_button.pack(pady=10)

# Start the GUI event loop
window.mainloop()




