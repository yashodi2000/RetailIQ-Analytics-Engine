import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Database Connection Setup
DB_USER = "postgres"
DB_PASS = "your_postgres_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "apex_retail"

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

def run_quality_audit(table_name):
    print(f"==========================================")
    print(f"   DATA QUALITY AUDIT: {table_name.upper()}")
    print(f"==========================================")
    
    # Query Data from PostgreSQL
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    
    # 1. Dataset Shape & Overview
    print(f"\n1. Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\n2. Missing Values:")
    print(df.isnull().sum())
    
    # 3. Duplicate Rows Check
    duplicates = df.duplicated().sum()
    print(f"\n3. Duplicate Rows Count: {duplicates}")
    
    # 4. Data Types Summary
    print("\n4. Data Types:")
    print(df.dtypes)

# Example Audit Execution across main tables
tables_to_audit = ['sales_header', 'sales_items', 'products', 'inventory_snapshots', 'purchase_orders']

for t in tables_to_audit:
    try:
        run_quality_audit(t)
    except Exception as e:
        print(f"Error auditing table {t}: {e}")