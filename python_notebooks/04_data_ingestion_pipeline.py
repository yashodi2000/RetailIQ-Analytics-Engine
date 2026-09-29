import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# Database Configuration
DB_USER = "postgres"
DB_PASS = "ny31#"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "RetailIQ_DB"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

# Sequence of tables for Ingestion & Cleanup
TABLE_MAP = [
    ('regions', 'Regions'),
    ('stores', 'Stores'),
    ('warehouses', 'Warehouses'),
    ('categories', 'Categories'),
    ('suppliers', 'Suppliers'),
    ('products', 'Products'),
    ('customers', 'Customers'),
    ('sales_header', 'Sales Header'),
    ('sales_items', 'Sales Items'),
    ('returns', 'Returns'),
    ('inventory_snapshots', 'Inventory Snapshots'),
    ('purchase_orders', 'Purchase Orders'),
    ('stock_transfers', 'Stock Transfers')
]

DATETIME_COLS = {
    'sales_header': ['order_date'],
    'returns': ['return_date'],
    'inventory_snapshots': ['snapshot_date'],
    'purchase_orders': ['order_date', 'expected_date', 'received_date'],
    'stock_transfers': ['transfer_date']
}

def ingest_data():
    print("📍 Connecting to Database & Starting Data Ingestion Pipeline...")

    try:
        engine = create_engine(DATABASE_URL)
        
        # 1. Truncate existing data to avoid PK/FK conflicts
        with engine.connect() as conn:
            for table_name, _ in reversed(TABLE_MAP):
                conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE;"))
            conn.commit()
            print("🧹 Cleaned existing records across all 13 tables\n")

        # 2. Ingest raw CSV files step-by-step
        for idx, (table_name, display_name) in enumerate(TABLE_MAP, start=1):
            csv_path = DATA_DIR / f"{table_name}.csv"
            
            if not csv_path.exists():
                print(f"❌ File not found: {csv_path}")
                continue

            df = pd.read_csv(csv_path)

            # Clean integer/nullable columns
            if 'customer_id' in df.columns:
                df['customer_id'] = df['customer_id'].astype('Int64')

            # Convert text columns to native datetime objects for PostgreSQL
            if table_name in DATETIME_COLS:
                for col in DATETIME_COLS[table_name]:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')

            # Append to DB
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            print(f"✅ {idx}/13 {display_name} Ingested")

        print("\n🎉 ALL 13 TABLES INGESTED SUCCESSFULLY!")

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_data()