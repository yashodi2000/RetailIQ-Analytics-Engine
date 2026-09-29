import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

DB_URL = "postgresql://postgres:ny31#@localhost:5432/RetailIQ_DB"
engine = create_engine(DB_URL)

# 1. Inventory Reorder Point (ROP) Calculation
rop_query = """
SELECT 
    product_id,
    AVG(quantity) AS avg_daily_demand
FROM sales_items
GROUP BY product_id;
"""
df_demand = pd.read_sql(rop_query, engine)

LEAD_TIME_DAYS = 7
SAFETY_STOCK = 50

df_demand['reorder_point'] = (df_demand['avg_daily_demand'] * LEAD_TIME_DAYS) + SAFETY_STOCK
print("--- Calculated Reorder Points (ROP) ---")
print(df_demand.head())

# 2. Demand Forecasting Model
print("\n--- Training Demand Forecasting Model ---")

daily_sales_query = """
SELECT 
    h.order_date::date AS order_date,
    s.product_id,
    SUM(s.quantity) AS total_quantity
FROM sales_header h
JOIN sales_items s ON h.order_id = s.order_id
GROUP BY h.order_date::date, s.product_id;
"""
df_sales = pd.read_sql(daily_sales_query, engine)
df_sales['order_date'] = pd.to_datetime(df_sales['order_date'])

# Feature Engineering
df_sales['year'] = df_sales['order_date'].dt.year
df_sales['month'] = df_sales['order_date'].dt.month
df_sales['day'] = df_sales['order_date'].dt.day
df_sales['dayofweek'] = df_sales['order_date'].dt.dayofweek

X = df_sales[['year', 'month', 'day', 'dayofweek']]
y = df_sales['total_quantity']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Model MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"Model R2 Score: {r2_score(y_test, y_pred):.2f}")