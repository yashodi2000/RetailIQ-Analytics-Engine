import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Path Setup
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(f"⚙️ Generating Raw CSV Files matching DB Schema (Jan 2024 - Dec 2025) into: {DATA_DIR}...")

np.random.seed(42)

# 1. Regions
df_regions = pd.DataFrame([
    {'region_id': 1, 'region_name': 'North'},
    {'region_id': 2, 'region_name': 'South'},
    {'region_id': 3, 'region_name': 'East'},
    {'region_id': 4, 'region_name': 'West'}
])
df_regions.to_csv(DATA_DIR / 'regions.csv', index=False)

# 2. Stores
df_stores = pd.DataFrame([
    {
        'store_id': i, 
        'region_id': np.random.choice([1, 2, 3, 4]), 
        'store_name': f'Store_{i}', 
        'location': f'City_{i}'
    }
    for i in range(1, 26)
])
df_stores.to_csv(DATA_DIR / 'stores.csv', index=False)

# 3. Warehouses
df_warehouses = pd.DataFrame([
    {
        'warehouse_id': i, 
        'region_id': np.random.choice([1, 2, 3, 4]),
        'warehouse_name': f'WH_{i}', 
        'location': f'Industrial_Zone_{i}'
    }
    for i in range(1, 5)
])
df_warehouses.to_csv(DATA_DIR / 'warehouses.csv', index=False)

# 4. Categories
df_categories = pd.DataFrame([
    {'category_id': 1, 'category_name': 'Electronics'},
    {'category_id': 2, 'category_name': 'Apparel'},
    {'category_id': 3, 'category_name': 'Home & Kitchen'},
    {'category_id': 4, 'category_name': 'Beauty & Health'}
])
df_categories.to_csv(DATA_DIR / 'categories.csv', index=False)

# 5. Suppliers
df_suppliers = pd.DataFrame([
    {
        'supplier_id': i, 
        'supplier_name': f'Supplier_{i}',
        'contact_info': f'contact_supplier_{i}@apexretail.com'
    }
    for i in range(1, 11)
])
df_suppliers.to_csv(DATA_DIR / 'suppliers.csv', index=False)

# 6. Products (1,200 Active SKUs as per project brief)
df_products = []
for i in range(1, 1201):
    cost = round(float(np.random.uniform(10, 100)), 2)
    price = round(cost * float(np.random.uniform(1.2, 1.8)), 2)
    df_products.append({
        'product_id': i, 
        'category_id': int(np.random.choice([1, 2, 3, 4])), 
        'supplier_id': int(np.random.choice(range(1, 11))), 
        'product_name': f'Product_{i}', 
        'unit_price': price,
        'unit_cost': cost
    })
pd.DataFrame(df_products).to_csv(DATA_DIR / 'products.csv', index=False)

# 7. Customers
df_customers = pd.DataFrame([
    {
        'customer_id': int(i), 
        'customer_name': f'Customer_{i}',
        'segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'])
    }
    for i in range(1, 501)
])
df_customers.to_csv(DATA_DIR / 'customers.csv', index=False)

# 8. Sales Header (Jan 2024 - Dec 2025)
dates_2years = pd.date_range(start='2024-01-01', end='2025-12-31').strftime('%Y-%m-%d %H:%M:%S').tolist()
df_sales_header = pd.DataFrame([
    {
        'order_id': i,
        'store_id': int(np.random.choice(range(1, 26))),
        'customer_id': int(np.random.choice(range(1, 501))) if np.random.rand() > 0.1 else None, # Nulls for Guest checkout
        'order_date': np.random.choice(dates_2years),
        'channel': np.random.choice(['In-Store', 'E-Commerce'])
    }
    for i in range(1, 2501)
])
df_sales_header.to_csv(DATA_DIR / 'sales_header.csv', index=False)

# 9. Sales Items (Column name corrected to line_id to match SQL Schema)
df_sales_items = pd.DataFrame([
    {
        'line_id': i,
        'order_id': int(np.random.choice(range(1, 2501))),
        'product_id': int(np.random.choice(range(1, 1201))),
        'quantity': int(np.random.randint(1, 5)),
        'unit_price': round(float(np.random.uniform(15, 150)), 2),
        'discount': round(float(np.random.choice([0.0, 0.05, 0.1, 0.15])), 2)
    }
    for i in range(1, 6001)
])
df_sales_items.to_csv(DATA_DIR / 'sales_items.csv', index=False)

# 10. Returns
df_returns = pd.DataFrame([
    {
        'return_id': i,
        'order_id': int(np.random.choice(range(1, 2000))),
        'product_id': int(np.random.choice(range(1, 1201))),
        'return_date': np.random.choice(dates_2years),
        'quantity': int(np.random.randint(1, 3)),
        'reason': np.random.choice(['Defective', 'Wrong Item', 'Changed Mind'])
    }
    for i in range(1, 151)
])
df_returns.to_csv(DATA_DIR / 'returns.csv', index=False)

# 11. Inventory Snapshots
df_inventory = pd.DataFrame([
    {
        'snapshot_id': i,
        'store_id': int(np.random.choice(range(1, 26))),
        'warehouse_id': int(np.random.choice(range(1, 5))),
        'product_id': int(np.random.choice(range(1, 1201))),
        'snapshot_date': '2025-12-31 00:00:00',
        'stock_on_hand': int(np.random.randint(0, 100)),
        'reorder_level': 15
    }
    for i in range(1, 1001)
])
df_inventory.to_csv(DATA_DIR / 'inventory_snapshots.csv', index=False)

# 12. Purchase Orders
po_list = []
for i in range(1, 101):
    ord_dt = datetime(2024, 1, 1) + timedelta(days=int(np.random.randint(0, 700)))
    exp_dt = ord_dt + timedelta(days=7)
    rec_dt = exp_dt + timedelta(days=int(np.random.choice([-1, 0, 1, 3]))) if np.random.rand() > 0.1 else None
    po_list.append({
        'po_id': i,
        'supplier_id': int(np.random.choice(range(1, 11))),
        'warehouse_id': int(np.random.choice(range(1, 5))),
        'order_date': ord_dt.strftime('%Y-%m-%d %H:%M:%S'),
        'expected_date': exp_dt.strftime('%Y-%m-%d %H:%M:%S'),
        'received_date': rec_dt.strftime('%Y-%m-%d %H:%M:%S') if rec_dt else None,
        'status': 'Completed' if rec_dt else 'Pending',
        'total_cost': round(float(np.random.uniform(500, 5000)), 2)
    })
pd.DataFrame(po_list).to_csv(DATA_DIR / 'purchase_orders.csv', index=False)

# 13. Stock Transfers
df_stock_transfers = pd.DataFrame([
    {
        'transfer_id': i,
        'from_warehouse_id': int(np.random.choice(range(1, 5))),
        'to_store_id': int(np.random.choice(range(1, 26))),
        'product_id': int(np.random.choice(range(1, 1201))),
        'quantity': int(np.random.randint(5, 50)),
        'transfer_date': np.random.choice(dates_2years)
    }
    for i in range(1, 151)
])
df_stock_transfers.to_csv(DATA_DIR / 'stock_transfers.csv', index=False)

print("✨ Successfully generated all 13 raw CSV files matching DB schema!")