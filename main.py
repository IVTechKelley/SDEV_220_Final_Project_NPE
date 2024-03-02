import tkinter as tk
from PIL import Image, ImageTk


class Products:
    def __init__(self):
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
    
    def get_products_by_name(self, name):
        return [product_info for product_info in self.products.values() if product_info['name'] == name]

    
# Product database
products = Products()
products.add_product(1, "Consoles", "Playstation 5", 469.99, "Latest Sony Gaming System", "images/ps5.jpg")
products.add_product(2, "Consoles", "Xbox Series X", 449.99, "Latest Microsoft Gaming System", "images/xbox_series_x.jpg")
products.add_product(3, "Laptops", "MacBook", 1299.99, "Sleek and powerful laptop", "images/macbook.jpg")
products.add_product(4, "Laptops", "Dell XPS", 999.99, "High-performance laptop for professionals", "images/dell.jpg")
products.add_product(5, "Appliances", "Refrigerator", 799.99, "Energy-efficient refrigerator", "images/fridge.jpg")
products.add_product(6, "Appliances", "Washing Mahine", 499.99, "Front-loading washing machine", "images/washing_machine.jpg")
    

class WindowController:
    def __init__(self, root, products, shopping_cart):
        self.root = root
        self.products = products
        self.current_window = None
        self.shopping_cart = shopping_cart

    def show_shopping_window(self):
        self.close_current_window()
        shopping_window = ShoppingWindow(self.root, self, products, shopping_cart)
        self.current_window = shopping_window

    def show_cart_window(self):
        self.close_current_window()
        cart_window = CartWindow(self.root, self, products, shopping_cart)
        self.current_window = cart_window

    def show_checkout_window(self):
        self.close_current_window()
        checkout_window = CheckoutWindow(self.root, self)
        self.current_window = checkout_window

    def close_current_window(self):
        if self.current_window:
            self.current_window.destroy()


class ShoppingWindow(tk.Toplevel):
    def __init__(self, root, controller, products, shopping_cart):
        super().__init__(root)
        self.title("Shopping")
        self.controller = controller
        self.products = products
        self.shopping_cart = shopping_cart

        self.label_search = tk.Label(self, text="Search:")
        self.label_search.pack(pady=10)
        self.entry_search = tk.Entry(self)
        self.entry_search.pack(pady=10)

        self.category_var = tk.StringVar()
        self.category_var.set("All")
        categories = ["All", "Consoles", "Laptops", "Appliances"]
        self.category_menu = tk.OptionMenu(self, self.category_var, "All", "Consoles", "Laptops", "Appliances", command=self.on_search)
        self.category_menu.pack(pady=10)

        self.button_search = tk.Button(self, text="Search", command=self.on_search)
        self.button_search.pack(pady=10)
        self.listbox = tk.Listbox(self, height=10, width=80)
        self.listbox.pack(pady=10)

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

    def update_listbox(self, category, search_query=None):
        self.listbox.delete(0, tk.END)
        if category == "All":
            products = products = list(self.products.products.values())
        else:
            products = self.products.get_products_by_category(category)

        if search_query:
            products = [product for product in products if search_query.lower() in product['name'].lower()]
        
        for product in products:
            product_info = f"{product['name']} - ${product['price']:.2f}"
            self.listbox.insert(tk.END, product_info)

    def on_search(self, *args):
        selected_category = self.category_var.get()
        search_query = self.entry_search.get()
        self.update_listbox(selected_category, search_query)
    
    def add_to_cart(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            product_id = list(self.products.products.keys())[selected_index[0]]
            product_info = self.products.get_product_info(product_id)

            if product_id not in self.shopping_cart:
                self.shopping_cart[product_id] = {
                    'name': product_info['name'],
                    'price': product_info['price'],
                    'quantity': 1
                }
            else:
                self.shopping_cart[product_id]['quantity'] += 1


class CartWindow(tk.Toplevel):
    def __init__(self, root, controller, products, shopping_cart):
        super().__init__(root)
        self.title("Shopping Cart")
        self.controller = controller
        self.products = products
        self.shopping_cart = shopping_cart

        self.cart_label = tk.Label(self, text="Shopping Cart")
        self.cart_label.pack(pady=10)
        self.cart_listbox = tk.Listbox(self, height=10, width=80)
        self.cart_listbox.pack(pady=10)

        self.remove_button = tk.Button(self, text="Remove Item", command=self.remove_item)
        self.remove_button.pack(pady=10)

        self.checkout_button = tk.Button(self, text="Checkout", command=self.controller.show_checkout_window)
        self.checkout_button.pack(pady=10)
        self.back_to_shopping_button = tk.Button(self, text="Continue Shopping", command=self.controller.show_shopping_window)
        self.back_to_shopping_button.pack(pady=10)

        self.update_listbox()

    def add_to_cart(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            product_id = list(self.products.products.keys())[selected_index[0]]
            product_info = self.products.get_product_info(product_id)
            self.shopping_cart[product_id]['quantity'] += 1

    def remove_item(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            product_id = list(self.shopping_cart.keys())[selected_index[0]]
            if self.shopping_cart[product_id]['quantity'] > 1:
                self.shopping_cart[product_id]['quantity'] -= 1
            else:
                del self.shopping_cart[product_id]
        self.update_listbox()

    def update_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        for product_id, item in self.shopping_cart.items():
            product_info = f"{item['name']} - ${item['price']:.2f} x {item['quantity']}"
            self.cart_listbox.insert(tk.END, product_info)


class CheckoutWindow(tk.Toplevel):
    def __init__(self, root, controller):
        super().__init__(root)
        self.title("Checkout")
        self.controller = controller

        back_to_shopping_button = tk.Button(self, text="Back to Shopping", command=self.controller.show_shopping_window)
        back_to_shopping_button.pack()
        back_to_cart_button = tk.Button(self, text="Back to Shopping Cart", command=self.controller.show_cart_window)
        back_to_cart_button.pack()


root = tk.Tk()
root.withdraw()
shopping_cart = {}
controller = WindowController(root, products, shopping_cart)
controller.show_shopping_window()

if __name__ == "__main__":
    root.mainloop()