# ============================================================
# PROJECT: Supermarket Sales Analysis
# FILE   : DatabaseLoad.py
# DESC   : Load cleaned CSV into PostgreSQL (NO SQLAlchemy)
# ============================================================

import pandas as pd
import psycopg2


# ============================================================
# 1. LOAD CLEAN DATA
# ============================================================

df = pd.read_csv("../Data/SuperMarket_Clean.csv")
print("✅ Data loaded:", df.shape)


# ============================================================
# 2. CONNECT TO POSTGRESQL
# ============================================================

try:
    conn = psycopg2.connect(
        host="localhost",
        database="supermarket",
        user="postgres",   # <-- change if needed
        password=""
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL")

except Exception as e:
    print("❌ Connection error:", e)
    exit()


# ============================================================
# 3. CREATE TABLE
# ============================================================

create_table_query = """
DROP TABLE IF EXISTS supermarket_sales;

CREATE TABLE supermarket_sales (
    invoice_id TEXT,
    branch TEXT,
    city TEXT,
    customer_type TEXT,
    gender TEXT,
    product_line TEXT,
    unit_price FLOAT,
    quantity INT,
    sales FLOAT,
    cogs FLOAT,
    tax_5percent FLOAT,
    gross_income FLOAT,
    rating FLOAT,
    payment TEXT,
    date DATE,
    time TIME,
    hour INT,
    day_name TEXT,
    month INT,
    week INT
);
"""

cursor.execute(create_table_query)
conn.commit()
print("✅ Table created")


# ============================================================
# 4. INSERT DATA (SAFE + CONTROLLED)
# ============================================================

insert_query = """
INSERT INTO supermarket_sales (
    invoice_id, branch, city, customer_type, gender,
    product_line, unit_price, quantity, sales, cogs,
    tax_5percent, gross_income, rating, payment,
    date, time, hour, day_name, month, week
) VALUES (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""

for _, row in df.iterrows():

    values = [
        row["invoice_id"],
        row["branch"],
        row["city"],
        row["customer_type"],
        row["gender"],
        row["product_line"],
        float(row["unit_price"]),
        int(row["quantity"]),
        float(row["sales"]),
        float(row["cogs"]),
        float(row["tax_5percent"]),
        float(row["gross_income"]),
        float(row["rating"]),
        row["payment"],
        row["date"],
        row["time"],
        int(row["hour"]),
        row["day_name"],
        int(row["month"]),
        int(row["week"])
    ]

    cursor.execute(insert_query, values)


conn.commit()
print("🎉 Data inserted successfully")


# ============================================================
# 5. CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()

print("🔒 Connection closed")
