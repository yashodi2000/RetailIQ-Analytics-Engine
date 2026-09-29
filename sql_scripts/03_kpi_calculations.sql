-- 1. Gross Revenue, Discounts & Net Revenue
SELECT 
    SUM(quantity * unit_price) AS gross_revenue,
    SUM(quantity * unit_price * discount) AS total_discounts,
    SUM((quantity * unit_price) * (1 - discount)) AS net_revenue
FROM sales_items;

-- 2. Gross Margin % (Profitability after COGS)
SELECT 
    SUM((i.quantity * i.unit_price) * (1 - i.discount)) AS net_revenue,
    SUM(i.quantity * p.unit_cost) AS total_cogs,
    (SUM((i.quantity * i.unit_price) * (1 - i.discount)) - SUM(i.quantity * p.unit_cost)) AS gross_profit,
    ROUND(
        ((SUM((i.quantity * i.unit_price) * (1 - i.discount)) - SUM(i.quantity * p.unit_cost)) / 
        NULLIF(SUM((i.quantity * i.unit_price) * (1 - i.discount)), 0)) * 100, 2
    ) AS gross_margin_percentage
FROM sales_items i
JOIN products p ON i.product_id = p.product_id;

-- 3. Average Order Value (AOV)
SELECT 
    ROUND(SUM((quantity * unit_price) * (1 - discount)) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM sales_items;

-- 4. Total Return Rate %
SELECT 
    COALESCE(SUM(r.quantity), 0) AS total_returned_units,
    SUM(s.quantity) AS total_sold_units,
    ROUND((COALESCE(SUM(r.quantity), 0)::DECIMAL / SUM(s.quantity)) * 100, 2) AS return_rate_percentage
FROM sales_items s
LEFT JOIN returns r ON s.order_id = r.order_id AND s.product_id = r.product_id;

-- 5. Supplier On-Time In-Full (OTIF) % (Fixed with NULL safe checks)
SELECT 
    s.supplier_name,
    COUNT(po.po_id) AS total_orders,
    COUNT(CASE WHEN po.received_date IS NOT NULL AND po.received_date <= po.expected_date AND po.status = 'Completed' THEN 1 END) AS otif_orders,
    ROUND(
        COUNT(CASE WHEN po.received_date IS NOT NULL AND po.received_date <= po.expected_date AND po.status = 'Completed' THEN 1 END) * 100.0 / NULLIF(COUNT(po.po_id), 0), 2
    ) AS otif_percentage
FROM purchase_orders po
JOIN suppliers s ON po.supplier_id = s.supplier_id
GROUP BY s.supplier_name;