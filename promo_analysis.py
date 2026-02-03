import sqlite3
import pandas as pd

DB_PATH = "promo_sales.db"   
OUTPUT_SQL = "promo_result_sql.csv"
OUTPUT_PANDAS = "promo_result_pandas.csv"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

sql_query = """
SELECT 
    c.customer_id AS Customer,
    c.age AS Age,
    i.item_name AS Item,
    SUM(s.quantity) AS Quantity
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
JOIN items i ON s.item_id = i.item_id
WHERE c.age BETWEEN 18 AND 35
  AND s.quantity IS NOT NULL
GROUP BY c.customer_id, c.age, i.item_name
HAVING SUM(s.quantity) > 0
ORDER BY c.customer_id, i.item_name;
"""

df_sql = pd.read_sql_query(sql_query, conn)
df_sql.to_csv(OUTPUT_SQL, sep=';', index=False)
print(f"✅ SQL solution saved to {OUTPUT_SQL}")

customers = pd.read_sql_query("SELECT * FROM customers;", conn)
sales = pd.read_sql_query("SELECT * FROM sales;", conn)
items = pd.read_sql_query("SELECT * FROM items;", conn)

merged = (
    sales.merge(customers, on='customer_id')
         .merge(items, on='item_id')
)

filtered = merged[(merged['age'].between(18, 35)) & (merged['quantity'].notnull())]

result = (
    filtered.groupby(['customer_id', 'age', 'item_name'], as_index=False)
            .agg({'quantity': 'sum'})
)

result = result[result['quantity'] > 0]

result.rename(columns={
    'customer_id': 'Customer',
    'age': 'Age',
    'item_name': 'Item',
    'quantity': 'Quantity'
}, inplace=True)

result.to_csv(OUTPUT_PANDAS, sep=';', index=False)
print(f"✅ Pandas solution saved to {OUTPUT_PANDAS}")

conn.close()
