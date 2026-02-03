import sqlite3

conn = sqlite3.connect("promo_sales.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER
);

CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);
""")

cursor.executescript("""
INSERT INTO customers VALUES (1, 21), (2, 23), (3, 35);
INSERT INTO items VALUES (1, 'x'), (2, 'y'), (3, 'z');
INSERT INTO sales VALUES
(1, 1, 1, 5),
(2, 1, 1, 5),
(3, 2, 1, 1),
(4, 2, 2, 1),
(5, 2, 3, 1),
(6, 3, 3, 1),
(7, 3, 3, 1);
""")

conn.commit()
conn.close()

print("✅ Database created successfully.")
