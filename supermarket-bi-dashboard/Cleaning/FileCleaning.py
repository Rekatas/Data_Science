# ============================================================
# PROJECT: Supermarket Sales Analysis
# FILE   : FileCleaning.py
# DESC   : Expert ETL cleaning pipeline (GitHub-ready)
# ============================================================

import os
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATH (portable for GitHub)
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

DATA_PATH = os.path.join(PROJECT_ROOT, "Data", "SuperMarket Analysis.csv")

print("📂 Loading file from:")
print(DATA_PATH)


# ============================================================
# 2. SAFE LOAD (ERROR HANDLING)
# ============================================================

try:
    df = pd.read_csv(DATA_PATH)
    print("\n✅ Dataset loaded successfully")

except FileNotFoundError:
    print("\n❌ File not found. Check Data folder or filename.")
    exit()

except Exception as e:
    print("\n❌ Unexpected error:", e)
    exit()


data = df.copy()


# ============================================================
# 3. DATA OVERVIEW
# ============================================================

print("\n=== DATA OVERVIEW ===")
print(data.head())
print("\nShape:", data.shape)
print("\nColumns:")
print(list(data.columns))


# ============================================================
# 4. CLEAN COLUMN NAMES
# ============================================================

data.columns = (
    data.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("%", "percent")
)

print("\n✅ Columns standardized")


# ============================================================
# 5. MISSING VALUES
# ============================================================

print("\n=== NULL VALUES ===")
print(data.isnull().sum())

data = data.fillna({
    "customer_type": "unknown",
    "gender": "unknown",
    "product_line": "unknown"
})

print("\n✅ Missing values handled")


# ============================================================
# 6. DUPLICATES
# ============================================================

before = len(data)
data = data.drop_duplicates()
after = len(data)

print(f"\n🧹 Duplicates removed: {before - after}")


# ============================================================
# 7. DATE + TIME FIX (AM/PM FORMAT FIXED)
# ============================================================

# DATE
data["date"] = pd.to_datetime(data["date"], errors="coerce")

# TIME (12-hour format with AM/PM)
data["time"] = pd.to_datetime(
    data["time"],
    format="%I:%M:%S %p",
    errors="coerce"
)

# extract hour safely
data["hour"] = data["time"].dt.hour

print("\n✅ Date & Time converted correctly")


# ============================================================
# 8. TEXT STANDARDIZATION
# ============================================================

for col in ["gender", "customer_type", "product_line", "payment"]:
    data[col] = data[col].str.strip().str.title()

print("✅ Text standardized")


# ============================================================
# 9. BUSINESS RULE CLEANING
# ============================================================

data = data[
    (data["quantity"] > 0) &
    (data["unit_price"] > 0) &
    (data["sales"] > 0)
]

print("✅ Invalid rows removed")


# ============================================================
# 10. FEATURE ENGINEERING
# ============================================================

data["day_name"] = data["date"].dt.day_name()
data["month"] = data["date"].dt.month
data["week"] = data["date"].dt.isocalendar().week

print("✅ Time features created (hour, day, month, week)")


# ============================================================
# 11. FINANCIAL VALIDATION
# ============================================================

data["profit_check"] = data["sales"] - data["cogs"] - data["tax_5percent"]

print("\n=== PROFIT CHECK ===")
print(data["profit_check"].describe())


# ============================================================
# 12. FINAL QUALITY CHECK
# ============================================================

print("\n=== FINAL CHECK ===")
print("Shape:", data.shape)

print("\nNull values:")
print(data.isnull().sum())


# ============================================================
# 13. EXPORT CLEAN DATA
# ============================================================

OUTPUT_PATH = os.path.join(PROJECT_ROOT, "Data", "SuperMarket_Clean.csv")

data.to_csv(OUTPUT_PATH, index=False)

print("\n🎉 CLEAN DATA SAVED SUCCESSFULLY")
print("📁", OUTPUT_PATH)
