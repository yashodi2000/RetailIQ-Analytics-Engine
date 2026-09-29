-- =============================================================================
-- RetailIQ: Database Schema Definition
-- Target Database Name: RetailIQ_DB
-- =============================================================================

DROP TABLE IF EXISTS stock_transfers CASCADE;
DROP TABLE IF EXISTS purchase_orders CASCADE;
DROP TABLE IF EXISTS inventory_snapshots CASCADE;
DROP TABLE IF EXISTS returns CASCADE;
DROP TABLE IF EXISTS sales_items CASCADE;
DROP TABLE IF EXISTS sales_header CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS warehouses CASCADE;
DROP TABLE IF EXISTS stores CASCADE;
DROP TABLE IF EXISTS regions CASCADE;

-- 1. REGIONS
CREATE TABLE regions (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL
);

-- 2. STORES
CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    region_id INT NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    CONSTRAINT fk_stores_region FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE CASCADE
);

-- 3. WAREHOUSES
CREATE TABLE warehouses (
    warehouse_id INT PRIMARY KEY,
    region_id INT NOT NULL,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    CONSTRAINT fk_warehouses_region FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE CASCADE
);

-- 4. CATEGORIES
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

-- 5. SUPPLIERS
CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(150)
);

-- 6. PRODUCTS
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    category_id INT NOT NULL,
    supplier_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    unit_cost DECIMAL(10,2) NOT NULL CHECK (unit_cost >= 0),
    CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CONSTRAINT fk_products_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- 7. CUSTOMERS
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL
);

-- 8. SALES_HEADER
CREATE TABLE sales_header (
    order_id INT PRIMARY KEY,
    store_id INT NOT NULL,
    customer_id INT, -- NULL allowed for Guest checkout
    order_date TIMESTAMP NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('In-Store', 'E-Commerce')),
    CONSTRAINT fk_sales_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 9. SALES_ITEMS
CREATE TABLE sales_items (
    line_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    discount DECIMAL(10,2) DEFAULT 0.00 CHECK (discount >= 0.00),
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES sales_header(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 10. RETURNS
CREATE TABLE returns (
    return_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    return_date TIMESTAMP NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    reason VARCHAR(100),
    CONSTRAINT fk_returns_order FOREIGN KEY (order_id) REFERENCES sales_header(order_id),
    CONSTRAINT fk_returns_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 11. INVENTORY_SNAPSHOTS
CREATE TABLE inventory_snapshots (
    snapshot_id INT PRIMARY KEY,
    store_id INT,
    warehouse_id INT,
    product_id INT NOT NULL,
    snapshot_date TIMESTAMP NOT NULL,
    stock_on_hand INTEGER NOT NULL CHECK (stock_on_hand >= 0),
    reorder_level INTEGER DEFAULT 20,
    CONSTRAINT fk_inv_product FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_inv_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_inv_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

-- 12. PURCHASE_ORDERS
CREATE TABLE purchase_orders (
    po_id INT PRIMARY KEY,
    supplier_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    expected_date TIMESTAMP,
    received_date TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Pending', 'Completed', 'In-Transit', 'Delayed', 'Cancelled')),
    total_cost DECIMAL(10,2),
    CONSTRAINT fk_po_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    CONSTRAINT fk_po_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

-- 13. STOCK_TRANSFERS
CREATE TABLE stock_transfers (
    transfer_id INT PRIMARY KEY,
    from_warehouse_id INT NOT NULL,
    to_store_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    transfer_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_trans_wh FOREIGN KEY (from_warehouse_id) REFERENCES warehouses(warehouse_id),
    CONSTRAINT fk_trans_store FOREIGN KEY (to_store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_trans_prod FOREIGN KEY (product_id) REFERENCES products(product_id)
);