'''
    Consumer Retail Electronics Shopping Platform

    Authors: Patrick Kelley, Nathaniel Johnson, Evan Kupec

    Description: This program serves as a demonstration for a shopping platform. The user can navigate through 
                 the shopping, cart, and checkout windows by using appropriately labeled buttons. Products can
                 be searched and filtered, and they can be added to the user's cart with a button. In the cart
                 window, users can increase or decrease the quantity of items in their cart before checking out.
                 The checkout window prompts users to enter necessary details and displays pricing totals. When
                 finished, the submit button will generate a summary/report of the user's sale.
'''


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Products:
    def __init__(self):
        """Initialize the Products class with an empty dictionary to store product information."""
        self.products = {}

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
products = Products()
products.add_product(1, "Consoles", "PlayStation 5", 469.99, "Immerse yourself in cutting-edge graphics and innovative features.", "images/ps5.jpg")
products.add_product(2, "Consoles", "Xbox Series X", 449.99, "Experience top-notch performance and a vast gaming library.", "images/xbox_series_x.jpg")
products.add_product(3, "Consoles", "Nintendo Switch", 299.99, "Seamlessly switch between TV and handheld modes for an unparalleled gaming adventure.", "images/nintendo_switch.jpg")
products.add_product(4, "Consoles", "PlayStation 4 Pro", 349.99, "Immerse yourself in stunning 4K graphics and enhanced gaming features.", "images/ps4_pro.jpg")
products.add_product(5, "Consoles", "Xbox One S", 279.99, "Enjoy a vast world of entertainment with this stylish gaming console.", "images/xbox_one_s.jpg")
products.add_product(6, "Laptops", "MacBook", 1299.99, "This sleek and powerful laptop is designed for optimal performance and efficiency.", "images/macbook.jpg")
products.add_product(7, "Laptops", "Dell XPS", 999.99, "This high-performance laptop combines power and style for seamless productivity.", "images/dell.jpg")
products.add_product(8, "Laptops", "HP Spectre x360", 1199.99, "This convertible laptop boasts a sleek design and versatile functionality.", "images/hp_spectre.jpg")
products.add_product(9, "Laptops", "Lenovo ThinkPad", 899.99, "This business-grade laptop offers robust features and reliability.", "images/lenovo_thinkpad.jpg")
products.add_product(10, "Laptops", "Asus ROG Zephyrus", 1499.99, "This high-end gaming laptop delivers unparalleled performance and cutting-edge specifications.", "images/asus_rog.jpg")
products.add_product(11, "Appliances", "Refrigerator", 799.99, "Keep your food fresh and organized while minimizing environmental impact.", "images/fridge.jpg")
products.add_product(12, "Appliances", "Washing Machine", 499.99, "Enjoy efficiency and advanced features for hassle-free cleaning.", "images/washing_machine.jpg")
products.add_product(13, "Appliances", "Dishwasher", 349.99, "Experience hassle-free cleaning and enjoy more time for the things you love.", "images/dishwasher.jpg")
products.add_product(14, "Appliances", "Microwave Oven", 129.99, "Perfect for quick and easy meals, it's a must-have in any modern kitchen.", "images/microwave.jpg")
products.add_product(15, "Appliances", "Air Purifier", 199.99, "Enhance your home environment and prioritize your well-being with this essential appliance.", "images/air_purifier.jpg")
    

class WindowController:
    DEFAULT_WIDTH = 450
    DEFAULT_HEIGHT = 450

    def __init__(self, root, products, shopping_cart):
        """
        Initialize the WindowController class. Controls window navigation, opening and closing.

        Args:
            root: The root Tkinter window.
            products (Products): An instance of the Products class containing product information.
            shopping_cart (dict): The shopping cart dictionary to keep track of selected items.
        """
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
        """
        Initialize the ShoppingWindow class.

        Args:
            root: The root Tkinter window.
            controller (WindowController): The window controller for handling window navigation.
            products (Products): An instance of the Products class containing product information.
            shopping_cart (dict): The shopping cart dictionary to keep track of selected items.
        """
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

        self.category_var = tk.StringVar()
        self.category_var.set("All")
        categories = ["All", "Consoles", "Laptops", "Appliances"]
        self.category_menu = tk.OptionMenu(self, self.category_var, "All", "Consoles", "Laptops", "Appliances", command=self.on_search)
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

        for category in categories[1:]:
            filter_category_button = tk.Button(self.filter_frame, text=category, command=lambda cat=category: self.on_search(cat))
            filter_category_button.pack(side=tk.LEFT)

        cart_button = tk.Button(self, text="Shopping Cart", command=self.controller.show_cart_window)
        cart_button.pack(pady=10)

        self.on_search()

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
        """
        Handle the search action triggered by the user.

        Args:
            *args: Additional arguments.
        """
        selected_category = self.category_var.get()
        search_query = self.entry_search.get()
        self.update_list(selected_category, search_query)
    
    def add_to_cart(self):
        """
        Add the selected product to the shopping cart.

        Retrieves the selected product from the list and updates the shopping cart accordingly.
        """
        selected_item = self.tree.focus()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            product_name = item_values[0]
            product_price = float(item_values[1][1:])
            if product_name:
                if product_name not in self.shopping_cart:
                    self.shopping_cart[product_name] = {
                        'name': product_name,
                        'price': product_price,
                        'quantity': 1
                    }
                else:
                    self.shopping_cart[product_name]['quantity'] += 1
    
    def show_selected_item(self, event):
        """
        Display detailed information about the selected product.

        Args:
            event: The event triggering the action (not used).
        """
        selected_item = self.tree.focus()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            product_name = item_values[0]
            product_info = self.products.get_product_by_name(product_name)
            description = product_info['description']
            image_path = product_info['image_path']
            
            original_image = Image.open(image_path)
            original_width = original_image.size[0]
            new_size = (int(original_width), 150)
            resized_image = original_image.resize(new_size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            self.item_image_label.config(image=photo)
            self.item_image_label.image = photo
            self.item_image_label.config(width=new_size[0], height=150, anchor="n")
            self.item_description_label.config(text=description)


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