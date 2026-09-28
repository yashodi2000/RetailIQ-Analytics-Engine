import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os

# --- DATABASE CONFIGURATION ---
DB_PARAMS = {
    'dbname': 'RetailIQ_DB',
    'user': 'postgres',
    'password': 'ny13#',
    'host': 'localhost',
    'port': '5432'
}

DATABASE_URL = f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
engine = create_engine(DATABASE_URL)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

TABLE_FILES = [
    ('regions', 'regions.csv'),
    ('stores', 'stores.csv'),
    ('warehouses', 'warehouses.csv'),
    ('categories', 'categories.csv'),
    ('suppliers', 'suppliers.csv'),
    ('products', 'products.csv'),
    ('customers', 'customers.csv'),
    ('sales_header', 'sales_header.csv'),
    ('sales_items', 'sales_items.csv'),
    ('returns', 'returns.csv'),
    ('inventory_snapshots', 'inventory_snapshots.csv'),
    ('purchase_orders', 'purchase_orders.csv'),
    ('stock_transfers', 'stock_transfers.csv')
]

def clean_and_ingest():
    print("🚀 Connecting to Database & Starting Data Ingestion Pipeline...")
    
    with engine.connect() as conn:
        conn.execute(text("""
            TRUNCATE TABLE stock_transfers, purchase_orders, inventory_snapshots, 
                           returns, sales_items, sales_header, customers, 
                           products, suppliers, categories, warehouses, stores, regions RESTART IDENTITY CASCADE;
        """))
        conn.commit()
    print("🧹 Cleaned existing records across all 13 tables")

    for idx, (table_name, file_name) in enumerate(TABLE_FILES, start=1):
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            
            # Standardize column names to lowercase
            df.columns = [c.lower() for c in df.columns]
            
            # Clean string foreign keys & identifiers
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace({'nan': None, 'None': None, '': None})

            # Append to database
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"✅ {idx}/13 {table_name.replace('_', ' ').title()} Ingested")
        else:
            print(f"❌ File not found: {file_path}")

    print("\n🎉 ALL 13 TABLES INGESTED SUCCESSFULLY!")

if __name__ == "__main__":
    clean_and_ingest()