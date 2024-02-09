import tkinter as tk
from PIL import Image, ImageTk


class Product:
    def __init__(self, product_id, name, price, description, image_path):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.image_path = image_path


class ProductDatabase:
    def __init__(self):
        self.products = {}

    def add_product(self, product_id, name, price, description, image_path):
        # Store product information in the database
        self.products[product_id] = {
            'name': name,
            'price': price,
            'description': description,
            'image_path': image_path
        }

    def get_product_info(self, product_id):
        # Retrieve product information from the database
        return self.products.get(product_id)


class Controller:
    def __init__(self, root, product_database):
        self.root = root
        self.product_database = product_database
        self.current_window = None

    def show_shopping_window(self):
        self.close_current_window()
        shopping_window = create_shopping_window(self.root, self.show_cart_window)
        self.current_window = shopping_window

    def show_cart_window(self):
        self.close_current_window()
        cart_window = create_cart_window(self.root, self.show_shopping_window, self.show_checkout_window)
        self.current_window = cart_window

    def show_checkout_window(self):
        self.close_current_window()
        checkout_window = create_checkout_window(self.root, self.show_shopping_window, self.show_cart_window)
        self.current_window = checkout_window

    def close_current_window(self):
        if self.current_window:
            self.current_window.destroy()


def create_shopping_window(root, on_cart_button_click):
    shopping_window = tk.Toplevel(root)
    shopping_window.title("Shopping Window")

    cart_button = tk.Button(shopping_window, text="Go to Shopping Cart", command=on_cart_button_click)
    cart_button.pack()

    # Additional window design code can be added here

    return shopping_window


def create_cart_window(root, on_shopping_button_click, on_checkout_button_click):
    cart_window = tk.Toplevel(root)
    cart_window.title("Shopping Cart Window")

    back_to_shopping_button = tk.Button(cart_window, text="Back to Shopping", command=on_shopping_button_click)
    back_to_shopping_button.pack()

    checkout_button = tk.Button(cart_window, text="Go to Checkout", command=on_checkout_button_click)
    checkout_button.pack()

    # Additional window design code can be added here

    return cart_window


def create_checkout_window(root, on_shopping_button_click, on_cart_button_click):
    checkout_window = tk.Toplevel(root)
    checkout_window.title("Checkout Window")

    back_to_shopping_button = tk.Button(checkout_window, text="Back to Shopping", command=on_shopping_button_click)
    back_to_shopping_button.pack()

    back_to_cart_button = tk.Button(checkout_window, text="Back to Shopping Cart", command=on_cart_button_click)
    back_to_cart_button.pack()

    # Additional window design code can be added here

    return checkout_window


# Create a product database for development
development_database = ProductDatabase()
development_database.add_product(1, "Sample Product", 20.99, "Sample Description", "path/to/image.jpg")
development_database.add_product(2, "Sample Product", 12.99, "Sample Description", "path/to/image.jpg")
development_database.add_product(3, "Sample Product", 8.99, "Sample Description", "path/to/image.jpg")

# Create the main application window (root)
root = tk.Tk()
root.withdraw()  # Hide the main application window initially

# Create a controller instance
controller = Controller(root, development_database)

# Show the shopping window on startup
controller.show_shopping_window()

if __name__ == "__main__":
    root.mainloop()
