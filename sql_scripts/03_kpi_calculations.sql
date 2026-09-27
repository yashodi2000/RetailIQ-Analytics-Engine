-- 1. Gross Revenue & Net Revenue
SELECT 
    SUM(quantity * unit_price) AS gross_revenue,
    SUM((quantity * unit_price) * (1 - discount)) AS net_revenue
FROM sales_items;

-- 2. Average Order Value (AOV)
SELECT 
    SUM((quantity * unit_price) * (1 - discount)) / COUNT(DISTINCT order_id) AS average_order_value
FROM sales_items;

-- 3. Total Return Rate %
SELECT 
    (SUM(r.return_quantity)::DECIMAL / SUM(s.quantity)) * 100 AS return_rate_percentage
FROM sales_items s
LEFT JOIN returns r ON s.line_id = r.line_id;

-- 4. Supplier On-Time In-Full (OTIF) %
SELECT 
    supplier_id,
    COUNT(CASE WHEN received_date <= expected_date AND status = 'Completed' THEN 1 END) * 100.0 / COUNT(*) AS otif_percentage
FROM purchase_orders
GROUP BY supplier_id;