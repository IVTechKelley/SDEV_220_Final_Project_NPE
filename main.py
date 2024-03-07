'''
    Consumer Retail Electronics Shopping Platform

    Authors: Patrick Kelley, Nathaniel Johnson, Evan Kupec

    Description: This program serves as a demonstration for a shopping platform. The user can navigate through 
                 the shopping cart and checkout windows by using appropriately labeled buttons. Products can
                 be searched, filtered, and added to the user's cart with a button. In the cart window
                 users can increase or decrease the quantity of items in their cart before checking out.
                 The checkout window prompts users to enter necessary details and displays pricing totals.
                 When finished, the submit button generates a summary report of the user's sale.
'''

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

class Products:
    def __init__(self, db_file):
        self.products = {}
        self.load_products(db_file)

    def load_products(self, db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        for row in rows:
            product_id, name, description, price, image_path, category = row
            self.add_product(product_id, category, name, price, description, image_path)

        conn.close()

    def add_product(self, product_id, category, name, price, description, image_path):
        self.products[product_id] = {
            'category': category,
            'name': name,
            'price': price,
            'description': description,
            'image_path': image_path
        }

    def get_product_info(self, product_id):
        return self.products.get(product_id)

    def get_products_by_category(self, category):
        return [product_info for product_info in self.products.values() if product_info['category'] == category]

    def get_product_by_name(self, name):
        for product_id, product_info in self.products.items():
            if product_info['name'] == name:
                return product_info
        return None

# Product database
db_file = "products.db"
products = Products(db_file)

class WindowController:
    DEFAULT_WIDTH = 450
    DEFAULT_HEIGHT = 450

    def __init__(self, root, products, shopping_cart):
        self.root = root
        self.products = products
        self.current_window = None
        self.shopping_cart = shopping_cart

    def create_window(self, window_class, *args, **kwargs):
        window = window_class(self.root, self, self.products, self.shopping_cart, *args, **kwargs)
        window.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}+{self.center_x()}+{self.center_y()}")
        self.current_window = window

    def show_shopping_window(self):
        self.close_current_window()
        self.create_window(ShoppingWindow)

    def show_cart_window(self):
        self.close_current_window()
        self.create_window(CartWindow)

    def show_checkout_window(self):
        self.close_current_window()
        self.create_window(CheckoutWindow)

    def close_current_window(self):
        if self.current_window:
            self.current_window.destroy()

    def center_x(self):
        return (self.root.winfo_screenwidth() - self.DEFAULT_WIDTH) // 2

    def center_y(self):
        return (self.root.winfo_screenheight() - self.DEFAULT_HEIGHT) // 2

class ShoppingWindow(tk.Toplevel):
    def __init__(self, root, controller, products, shopping_cart):

        super().__init__(root)
        self.title("Shopping")
        self.controller = controller
        self.products = products
        self.shopping_cart = shopping_cart

        self.search_frame = tk.Frame(self)
        self.entry_search = tk.Entry(self.search_frame)
        self.entry_search.pack(side=tk.LEFT, pady=10)
        
        self.button_search = tk.Button(self.search_frame, text="Search", command=self.on_search)
        self.button_search.pack(side=tk.LEFT, padx=5) 
        self.search_frame.pack(pady=10)

        # Get unique categories from the database
        categories = self.get_unique_categories()

        self.category_var = tk.StringVar()
        self.category_var.set("All")
        self.category_menu = tk.OptionMenu(self, self.category_var, *categories, command=self.on_search)
        self.category_menu.pack(pady=10)

        self.listbox_frame = tk.Frame(self)
        self.tree = ttk.Treeview(self.listbox_frame, columns=("Name", "Price"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.column("Name", width=120)
        self.tree.column("Price", width=70, anchor=tk.E)
        self.tree.pack(side=tk.LEFT)
        self.tree.bind("<ButtonRelease-1>", self.show_selected_item)

        self.item_display_frame = tk.Frame(self.listbox_frame, padx=10)
        self.item_image_label = tk.Label(self.item_display_frame, text="")
        self.item_image_label.pack(pady=5)

        self.item_description_label = tk.Label(self.item_display_frame, text="", width=55, height=3, wraplength=220)
        self.item_description_label.pack()

        self.item_display_frame.pack(side=tk.LEFT, padx=10)
        self.listbox_frame.pack(pady=10)

        self.add_to_cart_button = tk.Button(self, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.pack(pady=10)
        self.filter_frame = tk.Frame(self)
        self.filter_btn = tk.Button(self, text="Filter", command=lambda: self.filter_frame.place(x=self.winfo_width()-100, y=0, anchor=tk.NE))
        self.filter_btn.place(x=self.winfo_width()-100, y=0, anchor=tk.NE)

        for category in categories:
            filter_category_button = tk.Button(self.filter_frame, text=category, command=lambda cat=category: self.on_search(cat))
            filter_category_button.pack(side=tk.LEFT)

        self.cart_button = tk.Button(self, text="Shopping Cart", command=self.controller.show_cart_window)
        self.cart_button.pack(pady=10)

        self.on_search()

    def get_unique_categories(self):
        """
        Retrieve unique categories from the database.
        """
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ["All"] + categories

    def update_list(self, category, search_query=None):
        """
        Update the displayed product list based on the selected category and search query.
        Args:
        category (str): The selected category for filtering products.
        search_query (str, optional): The search query for filtering products by name. Defaults to None.
        """
        self.tree.delete(*self.tree.get_children())
        if category == "All":
            products = list(self.products.products.values())
        else:
            products = self.products.get_products_by_category(category)
        if search_query:
            products = [product for product in products if search_query.lower() in product['name'].lower()]
        for product in products:
            self.tree.insert("", "end", values=(product['name'], "${:.2f}".format(product['price'])))

    def on_search(self, *args):
        selected_category = self.category_var.get()
        search_query = self.entry_search.get()
        self.update_list(selected_category, search_query)

    def add_to_cart(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            product_name = item_values[0]
            product_info = self.products.get_product_by_name(product_name)

            if product_info:
                product_id = list(self.products.products.keys())[list(self.products.products.values()).index(product_info)]
                if product_name not in self.shopping_cart:
                    self.shopping_cart[product_name] = {
                        'id': product_id,
                        'name': product_name,
                        'price': product_info['price'],
                        'quantity': 1
                    }

                    # Change the button text temporarily
                    self.add_to_cart_button.config(text="Item Added")
                    self.after(2000, lambda: self.add_to_cart_button.config(text="Add to Cart"))  # Change back after 2000 milliseconds

                else:
                    self.shopping_cart[product_name]['quantity'] += 1

                    # Change the button text temporarily
                    self.add_to_cart_button.config(text="Quantity Increased")
                    self.after(2000, lambda: self.add_to_cart_button.config(text="Add to Cart"))  # Change back after 2000 milliseconds

                self.update_listbox()

    def show_selected_item(self, event):
        """
        Display detailed information about the selected product.
        Args:
        event: The event triggering the action (not used).
        """
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            product_name = item_values[0] if item_values else None
            product_info = self.products.get_product_by_name(product_name)
            description = product_info['description']
            image_path = product_info['image_path']

            try:
                # Assuming 'images/' is the directory where your images are stored
                original_image = Image.open(image_path)
                original_width = original_image.size[0]
                new_size = (int(original_width), 150)
                resized_image = original_image.resize(new_size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)
                self.item_image_label.config(image=photo)
                self.item_image_label.image = photo
                self.item_image_label.config(width=new_size[0], height=150, anchor="n")
                self.item_description_label.config(text=description)
            except FileNotFoundError:
                print(f"Image file not found: {image_path}")
                # Handle the missing image file gracefully, e.g., show a default image.

    def update_listbox(self):
        """
        Update the displayed list of items in the shopping window.
        This implementation clears the existing listbox and shows product names and prices.
        You may need to adjust this based on your application's logic.
        """
        self.tree.delete(*self.tree.get_children())
        selected_category = self.category_var.get()
        search_query = self.entry_search.get()

        if selected_category == "All":
            products = list(self.products.products.values())
        else:
            products = self.products.get_products_by_category(selected_category)

        if search_query:
            products = [product for product in products if search_query.lower() in product['name'].lower()]

        for product in products:
            product_name = product['name']
            product_price = "${:.2f}".format(product['price'])
            self.tree.insert("", "end", values=(product_name, product_price))

class CartWindow(tk.Toplevel):
    def __init__(self, root, controller, products, shopping_cart):
        """
        Initialize the CartWindow class.

        Args:
            root: The root Tkinter window.
            controller (WindowController): The window controller for handling window navigation.
            products (Products): An instance of the Products class containing product information.
            shopping_cart (dict): The shopping cart dictionary to keep track of selected items.
        """
        super().__init__(root)
        self.title("Shopping Cart")
        self.controller = controller
        self.products = products
        self.shopping_cart = shopping_cart

        self.cart_label = tk.Label(self, text="Shopping Cart")
        self.cart_label.pack(pady=10)

        self.cart_listbox = tk.Listbox(self, height=10, width=80)
        self.cart_listbox.pack(pady=10)

        self.total_label = tk.Label(self, text="Total: $0.00")
        self.total_label.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.remove_button = tk.Button(button_frame, text="Remove Item", command=self.remove_item)
        self.remove_button.pack(side=tk.LEFT, padx=5)
        self.add_button = tk.Button(button_frame, text="Add Item", command=self.add_to_cart)
        self.add_button.pack(side=tk.LEFT, padx=5)
        self.checkout_button = tk.Button(button_frame, text="Checkout", command=self.controller.show_checkout_window)
        self.checkout_button.pack(side=tk.RIGHT, padx=5)
        self.back_to_shopping_button = tk.Button(button_frame, text="Continue Shopping", command=self.controller.show_shopping_window)
        self.back_to_shopping_button.pack(side=tk.RIGHT, padx=5)

        self.update_listbox()

    def add_to_cart(self):
        """
        Increase the quantity of the selected item in the shopping cart.
        """
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            product_id = list(self.shopping_cart.keys())[selected_index[0]]
            self.shopping_cart[product_id]['quantity'] += 1
        self.update_listbox()

    def remove_item(self):
        """
        Decrease the quantity of the selected item in the shopping cart.
        Remove the item if the quantity becomes zero.
        """
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            product_id = list(self.shopping_cart.keys())[selected_index[0]]
            if self.shopping_cart[product_id]['quantity'] > 1:
                self.shopping_cart[product_id]['quantity'] -= 1
            else:
                del self.shopping_cart[product_id]
        self.update_listbox()

    def update_listbox(self):
        """
        Update the displayed list of items in the shopping cart.
        """
        self.cart_listbox.delete(0, tk.END)
        total_price = 0.0
        for product_id, item in self.shopping_cart.items():
            product_info = f"{item['name']} - ${item['price']:.2f} x {item['quantity']}"
            total_price += item['price'] * item['quantity']
            self.cart_listbox.insert(tk.END, product_info)
        self.total_label.config(text=f"Total: ${total_price:.2f}")


class CheckoutWindow(tk.Toplevel):
    def __init__(self, root, controller, products, shopping_cart):
        """
        Initialize the CheckoutWindow class.

        Args:
            root: The root Tkinter window.
            controller (WindowController): The window controller for handling window navigation.
            products (Products): An instance of the Products class containing product information.
            shopping_cart (dict): The shopping cart dictionary to keep track of selected items.
        """
        super().__init__(root)
        self.title("Checkout")
        self.controller = controller
        self.products = products
        self.shopping_cart = shopping_cart

        self.configure(padx=30)

        tk.Label(self, text="Payment Information").grid(row=0, column=1, pady=10, sticky=tk.W + tk.E)
        tk.Label(self, text="Cardholder Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cardholder_name_entry = tk.Entry(self)
        self.cardholder_name_entry.grid(row=1, column=1, pady=5)

        tk.Label(self, text="Card Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.card_number_entry = tk.Entry(self)
        self.card_number_entry.grid(row=2, column=1, pady=5)

        tk.Label(self, text="Expiration Date: (MM/YY)").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.expiration_date_entry = tk.Entry(self)
        self.expiration_date_entry.grid(row=3, column=1, pady=5)

        tk.Label(self, text="CVV:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.cvv_entry = tk.Entry(self)
        self.cvv_entry.grid(row=4, column=1, pady=5)

        tk.Label(self, text="Shipping Information").grid(row=5, column=1, pady=10, sticky=tk.W + tk.E)
        tk.Label(self, text="Street Address:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.address_entry = tk.Entry(self)
        self.address_entry.grid(row=6, column=1, pady=5)

        tk.Label(self, text="City:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.city_entry = tk.Entry(self)
        self.city_entry.grid(row=7, column=1, pady=5)

        tk.Label(self, text="State:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.state_entry = tk.Entry(self)
        self.state_entry.grid(row=8, column=1, pady=5)

        tk.Label(self, text="Zip Code:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.zip_code_entry = tk.Entry(self)
        self.zip_code_entry.grid(row=9, column=1, pady=5)

        self.base_price_label = tk.Label(self, text="Subtotal: $0.00")
        self.base_price_label.grid(row=7, column=2, pady=5, sticky=tk.E)

        self.taxes_label = tk.Label(self, text="Tax: $0.00")
        self.taxes_label.grid(row=8, column=2, pady=5, sticky=tk.E)

        self.final_price_label = tk.Label(self, text="Total: $0.00")
        self.final_price_label.grid(row=9, column=2, pady=5, sticky=tk.E)

        confirm_button = tk.Button(self, text="Place Order", command=self.confirm_checkout)
        confirm_button.grid(row=11, column=1, pady=10)
        back_to_shopping_button = tk.Button(self, text="Back to Shopping", command=self.controller.show_shopping_window)
        back_to_shopping_button.grid(row=12, column=0, pady=5, sticky=tk.W)
        back_to_cart_button = tk.Button(self, text="Back to Cart", command=self.controller.show_cart_window)
        back_to_cart_button.grid(row=12, column=2, pady=5, sticky=tk.E)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.update_totals()

    def update_totals(self):
        """
        Update the displayed subtotal, tax, and total amounts based on the items in the shopping cart.
        """
        base_price = sum(item['price'] * item['quantity'] for item in self.controller.shopping_cart.values())
        tax_rate = 0.07
        taxes = base_price * tax_rate
        final_price = base_price + taxes
        self.base_price_label.config(text=f"Subtotal: ${base_price:.2f}")
        self.taxes_label.config(text=f"Tax: ${taxes:.2f}")
        self.final_price_label.config(text=f"Total: ${final_price:.2f}")

    def confirm_checkout(self):
        """
        Update the displayed subtotal, tax, and total amounts based on the items in the shopping cart.
        """
        cardholder_name = self.cardholder_name_entry.get()
        card_number = self.card_number_entry.get()
        expiration_date = self.expiration_date_entry.get()
        cvv = self.cvv_entry.get()
        address = self.address_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zip_code = self.zip_code_entry.get()
        if any(not field for field in [cardholder_name, card_number, expiration_date, cvv, address, city, state, zip_code]):
            for entry in [self.cardholder_name_entry, self.card_number_entry, self.expiration_date_entry,
                        self.cvv_entry, self.address_entry, self.city_entry, self.state_entry, self.zip_code_entry]:
                if not entry.get():
                    entry.insert(0, "Field cannot be empty")
            return
        
        receipt_text = f"Payment Information:\n\nCardholder Name: {cardholder_name}\n\nCard Number: {card_number}\n\nExpiration Date: {expiration_date}\n\n\nShipping Information:\n\nStreet Address: {address}\n\nCity: {city}\n\nState: {state}\n\nZip Code: {zip_code}"
        receipt_text += f"\n\nOrder Summary:\n\n{self.base_price_label.cget('text')}\n{self.taxes_label.cget('text')}\n{self.final_price_label.cget('text')}"
        self.controller.shopping_cart.clear()
        ReceiptWindow(self, self.controller, receipt_text)


class ReceiptWindow(tk.Toplevel):
    def __init__(self, root, controller, receipt_text):
        """
        Initialize the ReceiptWindow class.

        Args:
            root: The root Tkinter window.
            controller (WindowController): The window controller for handling window navigation.
            receipt_text (str): The text to be displayed in the receipt.
        """
        super().__init__(root)
        self.title("Receipt")
        self.controller = controller 
        self.geometry(f"{controller.DEFAULT_WIDTH}x{controller.DEFAULT_HEIGHT}+{controller.center_x()}+{controller.center_y()}")
        tk.Label(self, text=receipt_text, justify=tk.LEFT).pack(padx=20, pady=20)
        ok_button = tk.Button(self, text="OK", command=self.controller.show_shopping_window)
        ok_button.pack(pady=10)

root = tk.Tk()
root.withdraw()
shopping_cart = {}
controller = WindowController(root, products, shopping_cart)
controller.show_shopping_window()

if __name__ == "__main__":
    root.mainloop()
