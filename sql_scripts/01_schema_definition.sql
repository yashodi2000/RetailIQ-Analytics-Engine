-- =============================================================================
-- RetailIQ: Database Schema Definition
-- Target Database Name: apex_retail
-- Description: Creates all 13 core relational tables with updated constraints
--              for seamless CSV data ingestion.
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

-- 1. REGIONS TABLE
CREATE TABLE regions (
    region_id VARCHAR(10) PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL
);

-- 2. STORES TABLE
CREATE TABLE stores (
    store_id VARCHAR(10) PRIMARY KEY,
    region_id VARCHAR(10) NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    CONSTRAINT fk_stores_region FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE CASCADE
);

-- 3. WAREHOUSES TABLE
CREATE TABLE warehouses (
    warehouse_id VARCHAR(10) PRIMARY KEY,
    region_id VARCHAR(10) NOT NULL,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    CONSTRAINT fk_warehouses_region FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE CASCADE
);

-- 4. CATEGORIES TABLE
CREATE TABLE categories (
    category_id VARCHAR(10) PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

-- 5. SUPPLIERS TABLE
CREATE TABLE suppliers (
    supplier_id VARCHAR(10) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(150)
);

-- 6. PRODUCTS TABLE
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    category_id VARCHAR(10) NOT NULL,
    supplier_id VARCHAR(10) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    unit_cost DECIMAL(10,2) NOT NULL CHECK (unit_cost >= 0),
    CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CONSTRAINT fk_products_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- 7. CUSTOMERS TABLE
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL
);

-- 8. SALES_HEADER TABLE (MODIFIED: customer_id can be NULL for Guest checkouts)
CREATE TABLE sales_header (
    order_id VARCHAR(20) PRIMARY KEY,
    store_id VARCHAR(10) NOT NULL,
    customer_id VARCHAR(10),
    order_date DATE NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('In-Store', 'E-Commerce', 'Mobile App', 'Web')),
    CONSTRAINT fk_sales_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 9. SALES_ITEMS TABLE (MODIFIED: discount checked >= 0)
CREATE TABLE sales_items (
    line_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    discount DECIMAL(10,2) DEFAULT 0.00 CHECK (discount >= 0.00),
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES sales_header(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 10. RETURNS TABLE
CREATE TABLE returns (
    return_id VARCHAR(20) PRIMARY KEY,
    line_id VARCHAR(20) NOT NULL,
    return_date DATE NOT NULL,
    return_quantity INTEGER NOT NULL CHECK (return_quantity > 0),
    return_reason VARCHAR(100),
    CONSTRAINT fk_returns_line FOREIGN KEY (line_id) REFERENCES sales_items(line_id)
);

-- 11. INVENTORY_SNAPSHOTS TABLE
CREATE TABLE inventory_snapshots (
    snapshot_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(10) NOT NULL,
    store_id VARCHAR(10),
    warehouse_id VARCHAR(10),
    snapshot_date DATE NOT NULL,
    quantity_on_hand INTEGER NOT NULL CHECK (quantity_on_hand >= 0),
    CONSTRAINT fk_inv_product FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_inv_store FOREIGN KEY (store_id) REFERENCES stores(store_id),
    CONSTRAINT fk_inv_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    CONSTRAINT chk_location_defined CHECK (
        (store_id IS NOT NULL AND warehouse_id IS NULL) OR
        (store_id IS NULL AND warehouse_id IS NOT NULL)
    )
);

-- 12. PURCHASE_ORDERS TABLE
CREATE TABLE purchase_orders (
    po_id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(10) NOT NULL,
    order_date DATE NOT NULL,
    expected_date DATE NOT NULL,
    received_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Pending', 'Completed', 'Delayed', 'Cancelled')),
    CONSTRAINT fk_po_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- 13. STOCK_TRANSFERS TABLE
CREATE TABLE stock_transfers (
    transfer_id VARCHAR(20) PRIMARY KEY,
    po_id VARCHAR(20) NOT NULL,
    from_location VARCHAR(20) NOT NULL,
    to_location VARCHAR(20) NOT NULL,
    transfer_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    CONSTRAINT fk_transfer_po FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id)
);