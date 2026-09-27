-- 1. Top 5 Best Selling Products by Net Revenue
SELECT 
    p.product_name,
    SUM((s.quantity * s.unit_price) * (1 - s.discount)) AS total_revenue
FROM sales_items s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 5;

-- 2. Monthly Revenue Trend
SELECT 
    DATE_TRUNC('month', h.order_date) AS month,
    SUM((i.quantity * i.unit_price) * (1 - i.discount)) AS monthly_revenue
FROM sales_header h
JOIN sales_items i ON h.order_id = i.order_id
GROUP BY month
ORDER BY month;