-- 1. Identify Duplicate Orders
SELECT order_id, COUNT(*)
FROM sales_header
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 2. Identify Guest Checkouts (Null Customer IDs)
SELECT COUNT(*) AS null_customers
FROM sales_header
WHERE customer_id IS NULL;

-- 3. Identify Invalid Prices or Quantities
SELECT * 
FROM sales_items 
WHERE unit_price <= 0 OR quantity <= 0;

-- 4. Check Orphan Records in Sales Items
SELECT i.*
FROM sales_items i
LEFT JOIN sales_header h ON i.order_id = h.order_id
WHERE h.order_id IS NULL;