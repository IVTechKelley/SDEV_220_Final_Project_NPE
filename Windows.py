import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests

# Sample data: three product categories, each with two products, price, and short description
products = {
    "Consoles": {
        "PlayStation 5 Slim": {
            "price": "$499.99",
            "description": "Next-gen gaming console",
            "image_url": "https://th.bing.com/th/id/OIP.LWbmXV4fL2RuIcgdbQUavQHaK4?rs=1&pid=ImgDetMain"
        },
        "Xbox Series XS": {
            "price": "$499.99",
            "description": "Powerful gaming and entertainment system",
            "image_url": "https://th.bing.com/th/id/OIP.ffc9A_ZPTJPNtDUJTmdJOAAAAA?rs=1&pid=ImgDetMain"
        }
    },
    "Laptops": {
        "MacBook Pro 11": {
            "price": "$2499.99",
            "description": "Sleek and powerful laptop",
            "image_url": "https://th.bing.com/th/id/R.701e6935b4f20a70c26685c8e89041ce?rik=8HGBRtOf2gJZRg&pid=ImgRaw&r=0"
        },
        "Dell XPS": {
            "price": "$999.99",
            "description": "High-performance laptop for professionals",
            "image_url": "https://th.bing.com/th/id/R.c247eaeccf7b4ebf2ae354f60627d220?rik=OdmoioAZMEjy4A&pid=ImgRaw&r=0"
        }
    },
    "Appliances": {
        "Samsung Refrigerator": {
            "price": "$1399.99",
            "description": "Energy-efficient refrigerator",
            "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6323/6323227cv29d.jpg"
        },
        "LG Bundle Washer & Dryer": {
            "price": "$499.99",
            "description": "Front-loading washing machine and efficient drying machine",
            "image_url": "https://th.bing.com/th/id/OIP.vbHbe_80k1UthIEeLsChrwHaFW?rs=1&pid=ImgDetMain"
        }
    }
}

def load_image_from_url(url, size=(100, 100)):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    img = Image.open(img_data)
    img = img.resize(size, resample=Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def update_listbox(category, search_query=None):
    text_widget.delete("1.0", tk.END)  # Clear previous items

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
        image_url = info.get("image_url", "")  # Get image URL if available
        if image_url:
            img = load_image_from_url(image_url)
            text_widget.image_create(tk.END, image=img)
        text_widget.insert(tk.END, f"{category}: {item} - {info['price']} - {info['description']}\n")

def on_search():
    search_query = entry_search.get()
    selected_category = category_var.get()
    update_listbox(selected_category, search_query)
    filter_btn.config(state=tk.NORMAL)  # Enable the filter button

# Create the main window
window = tk.Tk()
window.title("Great Purchases")  # Set the title of the window

# Create and place widgets in the window
label_title = tk.Label(window, text="Great Purchases", font=("Arial", 24, "bold"), fg="#007BFF")  # Blue color
label_title.pack(pady=10)

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

# Create a Text widget for displaying products
text_widget = tk.Text(window, height=20, width=200, font=("Calibri", 12), wrap=tk.WORD)
text_widget.pack(pady=10)

# Add to Cart button
add_to_cart_button = tk.Button(window, text="Add to Cart", bg="#4CAF50", fg="white", font=("Helvetica", 12))
add_to_cart_button.place_forget()

# Filter buttons
filter_frame = tk.Frame(window)
filter_frame.place_forget()

filter_btn = tk.Button(window, text="Filter", command=lambda: filter_frame.place(x=window.winfo_width()-100, y=0, anchor=tk.NE), bg="#008CBA", fg="white", font=("Helvetica", 12), state=tk.DISABLED)
filter_btn.place(x=window.winfo_width()-100, y=0, anchor=tk.NE)

for category in ["Consoles", "Laptops", "Appliances"]:
    filter_category_button = tk.Button(filter_frame, text=category, command=lambda cat=category: filter_category(cat), bg="#008CBA", fg="white", font=("Helvetica", 10))
    filter_category_button.pack(side=tk.LEFT)

window.bind("<Button-1>", lambda event: filter_frame.place_forget())

update_listbox(category_var.get())

window.mainloop()











