import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os

def initialize_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_path TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

class DatabaseEditor:
    def __init__(self, root, db_file):
        self.root = root
        self.db_file = db_file

        self.root.title("Database Editor")

        self.initialize_database()

        self.tree = ttk.Treeview(self.root, columns=("Name", "Description", "Price", "Image Path", "Category"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Image Path", text="Image Path")
        self.tree.heading("Category", text="Category")
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

        self.populate_tree()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.add_button = tk.Button(self.button_frame, text="Add Product", command=self.add_product)
        self.add_button.pack(side=tk.LEFT)

        self.remove_button = tk.Button(self.button_frame, text="Remove Product", command=self.remove_product)
        self.remove_button.pack(side=tk.LEFT)

    def initialize_database(self):
        if not os.path.exists(self.db_file):
            initialize_database(self.db_file)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))

        conn.close()

    def add_product(self):
        AddProductWindow(self.root, self.db_file, self.populate_tree)

    def remove_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to remove.")
            return

        product_id = self.tree.item(selected_item, "text")

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()

        conn.close()

        self.populate_tree()

class AddProductWindow:
    def __init__(self, root, db_file, callback):
        self.root = root
        self.db_file = db_file
        self.callback = callback

        self.top = tk.Toplevel(self.root)
        self.top.title("Add Product")

        self.name_label = tk.Label(self.top, text="Name:")
        self.name_label.grid(row=0, column=0)

        self.name_entry = tk.Entry(self.top)
        self.name_entry.grid(row=0, column=1)

        self.description_label = tk.Label(self.top, text="Description:")
        self.description_label.grid(row=1, column=0)

        self.description_entry = tk.Entry(self.top)
        self.description_entry.grid(row=1, column=1)

        self.price_label = tk.Label(self.top, text="Price:")
        self.price_label.grid(row=2, column=0)

        self.price_entry = tk.Entry(self.top)
        self.price_entry.grid(row=2, column=1)

        self.image_path_label = tk.Label(self.top, text="Image Path:")
        self.image_path_label.grid(row=3, column=0)

        self.image_path_entry = tk.Entry(self.top)
        self.image_path_entry.grid(row=3, column=1)

        self.category_label = tk.Label(self.top, text="Category:")
        self.category_label.grid(row=4, column=0)

        self.category_entry = tk.Entry(self.top)
        self.category_entry.grid(row=4, column=1)

        self.add_button = tk.Button(self.top, text="Add", command=self.add_product)
        self.add_button.grid(row=5, columnspan=2)

    def add_product(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        image_path = self.image_path_entry.get()
        category = self.category_entry.get()

        if not name or not description or not price or not image_path or not category:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number.")
            return

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO products (name, description, price, image_path, category) VALUES (?, ?, ?, ?, ?)", (name, description, price, image_path, category))
        conn.commit()

        conn.close()

        self.callback()
        self.top.destroy()

if __name__ == "__main__":
    db_file = "products.db"

    root = tk.Tk()
    DatabaseEditor(root, db_file)
    root.mainloop()
