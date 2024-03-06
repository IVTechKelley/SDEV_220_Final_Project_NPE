import sqlite3
import os

def initialize_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the products table with the category column
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

    # Insert sample data with categories
    sample_data = [
        ("PlayStation 5 Slim", "Next-gen gaming console", 499.99, "images/ps5.jpg", "Consoles"),
        ("Xbox Series XS", "Powerful gaming and entertainment system", 499.99, "images/xbox.jpg", "Consoles"),
        ("MacBook Pro 11", "Sleek and powerful laptop", 2499.99, "images/macbook.jpg", "Laptops"),
        ("Dell XPS", "High-performance laptop for professionals", 999.99, "images/dell_xps.jpg", "Laptops"),
        ("Samsung Refrigerator", "Energy-efficient refrigerator", 1399.99, "images/samsung_refrigerator.jpg", "Appliances"),
        ("LG Bundle Washer & Dryer", "Front-loading washing machine and efficient drying machine", 499.99, "images/lg_washer_dryer.jpg", "Appliances")
    ]

    for product in sample_data:
        cursor.execute("INSERT INTO products (name, description, price, image_path, category) VALUES (?, ?, ?, ?, ?)", product)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_file = "products.db"
    
    # Create the "images" folder if it doesn't exist
    os.makedirs("images", exist_ok=True)
    
    initialize_database(db_file)
    print("Database initialized successfully.")
