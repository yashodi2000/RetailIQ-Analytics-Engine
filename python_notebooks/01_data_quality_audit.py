import pandas as pd
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASS = "ny31#"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "RetailIQ_DB"

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

def run_quality_audit(table_name):
    print(f"\n==========================================")
    print(f"   DATA QUALITY AUDIT: {table_name.upper()}")
    print(f"==========================================")
    
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    
    print(f"1. Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\n2. Missing Values:")
    print(df.isnull().sum())
    
    duplicates = df.duplicated().sum()
    print(f"\n3. Duplicate Rows Count: {duplicates}")
    
    print("\n4. Data Types:")
    print(df.dtypes)

tables_to_audit = ['sales_header', 'sales_items', 'products', 'inventory_snapshots', 'purchase_orders']

for t in tables_to_audit:
    try:
        run_quality_audit(t)
    except Exception as e:
        print(f"Error auditing table {t}: {e}")