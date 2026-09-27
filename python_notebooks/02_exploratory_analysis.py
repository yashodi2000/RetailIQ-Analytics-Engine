import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Chart Formatting Setup
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Database Connection
DB_URL = "postgresql://postgres:your_postgres_password@localhost:5432/apex_retail"
engine = create_engine(DB_URL)

# 1. Monthly Revenue Trend Analysis
monthly_rev_query = """
SELECT 
    DATE_TRUNC('month', h.order_date) AS month,
    SUM((i.quantity * i.unit_price) * (1 - i.discount)) AS net_revenue
FROM sales_header h
JOIN sales_items i ON h.order_id = i.order_id
GROUP BY month
ORDER BY month;
"""
df_monthly = pd.read_sql(monthly_rev_query, engine)

plt.figure()
sns.lineplot(data=df_monthly, x='month', y='net_revenue', marker='o', color='b')
plt.title('Monthly Net Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Net Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Top 10 Revenue-Generating Products
top_products_query = """
SELECT 
    p.product_name,
    SUM((s.quantity * s.unit_price) * (1 - s.discount)) AS total_revenue
FROM sales_items s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 10;
"""
df_top_prod = pd.read_sql(top_products_query, engine)

plt.figure()
sns.barplot(data=df_top_prod, x='total_revenue', y='product_name', palette='Blues_r')
plt.title('Top 10 Products by Revenue')
plt.xlabel('Total Revenue ($)')
plt.ylabel('Product Name')
plt.tight_layout()
plt.show()