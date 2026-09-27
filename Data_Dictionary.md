# RetailIQ — Data Dictionary & Metric Glossary

This document provides a detailed description of the database tables, schema attributes, foreign key relationships, data types, and KPI calculation business logic for the RetailIQ analytics platform.

---

## 🗄️ Database Tables Overview

| Table Name | Description | Primary Key | Foreign Keys |
| :--- | :--- | :--- | :--- |
| **`regions`** | Geographical operating regions | `region_id` | None |
| **`stores`** | Physical and e-commerce store outlets | `store_id` | `region_id` |
| **`warehouses`** | Regional inventory storage hubs | `warehouse_id` | `region_id` |
| **`categories`** | Product classification hierarchy | `category_id` | None |
| **`suppliers`** | Product vendors and manufacturers | `supplier_id` | None |
| **`products`** | Master list of active SKUs | `product_id` | `category_id`, `supplier_id` |
| **`customers`** | Customer demographic and segment data | `customer_id` | None |
| **`sales_header`** | Order-level sales transactions | `order_id` | `store_id`, `customer_id` |
| **`sales_items`** | Line-item product sales transactions | `line_id` | `order_id`, `product_id` |
| **`returns`** | Product return records | `return_id` | `line_id` |
| **`inventory_snapshots`** | Periodic inventory stock levels | `snapshot_id` | `product_id`, `store_id`, `warehouse_id` |
| **`purchase_orders`** | Supplier orders placed by operations | `po_id` | `supplier_id` |
| **`stock_transfers`** | Stock movement between locations | `transfer_id` | `po_id` |

---

## 📐 Table Schema Specifications

### 1. `regions`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `region_id` | `VARCHAR(10)` | `PRIMARY KEY` | Unique identifier for the region |
| `region_name` | `VARCHAR(50)` | `NOT NULL` | Name of the operating region |

### 2. `stores`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `store_id` | `VARCHAR(10)` | `PRIMARY KEY` | Unique identifier for the store |
| `region_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `regions.region_id` |
| `store_name` | `VARCHAR(100)`| `NOT NULL` | Store name or outlet identifier |
| `location` | `VARCHAR(100)`| `NOT NULL` | Physical location or address |

### 3. `warehouses`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `warehouse_id` | `VARCHAR(10)` | `PRIMARY KEY` | Unique identifier for the warehouse |
| `region_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `regions.region_id` |
| `warehouse_name`| `VARCHAR(100)`| `NOT NULL` | Warehouse facility name |
| `location` | `VARCHAR(100)`| `NOT NULL` | Location of the warehouse |

### 4. `categories`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `category_id` | `VARCHAR(10)` | `PRIMARY KEY` | Unique identifier for the category |
| `category_name` | `VARCHAR(50)` | `NOT NULL` | Product category classification |

### 5. `suppliers`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `supplier_id` | `VARCHAR(10)` | `PRIMARY KEY` | Unique identifier for the supplier |
| `supplier_name` | `VARCHAR(100)`| `NOT NULL` | Vendor company name |
| `contact_info` | `VARCHAR(150)`| `NULLABLE` | Contact email or phone number |

### 6. `products`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | `VARCHAR(10)` | `PRIMARY KEY` | Unique SKU identifier |
| `category_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `categories.category_id` |
| `supplier_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `suppliers.supplier_id` |
| `product_name` | `VARCHAR(100)`| `NOT NULL` | Full product title |
| `unit_price` | `DECIMAL(10,2)`| `CHECK (> 0)` | Retail selling price per unit |
| `unit_cost` | `DECIMAL(10,2)`| `CHECK (> 0)` | Cost price per unit paid to supplier |

### 7. `customers`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | `VARCHAR(10)` | `PRIMARY KEY` | Unique customer identifier |
| `customer_name` | `VARCHAR(100)`| `NOT NULL` | Customer full name |
| `segment` | `VARCHAR(50)` | `NOT NULL` | Customer segment (e.g., Retail, Wholesale, VIP) |

### 8. `sales_header`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | `VARCHAR(20)` | `PRIMARY KEY` | Unique sales transaction ID |
| `store_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `stores.store_id` |
| `customer_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `customers.customer_id` |
| `order_date` | `DATE` | `NOT NULL` | Transaction date |
| `channel` | `VARCHAR(20)` | `NOT NULL` | In-store vs. E-commerce |

### 9. `sales_items`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `line_id` | `VARCHAR(20)` | `PRIMARY KEY` | Unique item line ID |
| `order_id` | `VARCHAR(20)` | `FOREIGN KEY` | Reference to `sales_header.order_id` |
| `product_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `products.product_id` |
| `quantity` | `INTEGER` | `CHECK (> 0)` | Number of units purchased |
| `unit_price` | `DECIMAL(10,2)`| `NOT NULL` | Price applied per unit at sale time |
| `discount` | `DECIMAL(5,2)` | `DEFAULT 0.00`| Discount percentage applied (0.00 to 1.00) |

### 10. `returns`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `return_id` | `VARCHAR(20)` | `PRIMARY KEY` | Unique return record ID |
| `line_id` | `VARCHAR(20)` | `FOREIGN KEY` | Reference to `sales_items.line_id` |
| `return_date` | `DATE` | `NOT NULL` | Date product was returned |
| `return_quantity`| `INTEGER` | `CHECK (> 0)` | Number of returned units |
| `return_reason` | `VARCHAR(100)`| `NULLABLE` | Customer reason for return |

### 11. `inventory_snapshots`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `snapshot_id` | `VARCHAR(20)` | `PRIMARY KEY` | Unique snapshot record ID |
| `product_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `products.product_id` |
| `store_id` | `VARCHAR(10)` | `NULLABLE FK` | Reference to `stores.store_id` (if store stock) |
| `warehouse_id`| `VARCHAR(10)` | `NULLABLE FK` | Reference to `warehouses.warehouse_id` (if warehouse stock) |
| `snapshot_date`| `DATE` | `NOT NULL` | Periodic snapshot date |
| `quantity_on_hand`|`INTEGER` | `CHECK (>= 0)`| Physical stock count |

### 12. `purchase_orders`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `po_id` | `VARCHAR(20)` | `PRIMARY KEY` | Unique purchase order ID |
| `supplier_id` | `VARCHAR(10)` | `FOREIGN KEY` | Reference to `suppliers.supplier_id` |
| `order_date` | `DATE` | `NOT NULL` | Date order placed with supplier |
| `expected_date`| `DATE` | `NOT NULL` | Agreed delivery date |
| `received_date`| `DATE` | `NULLABLE` | Actual delivery date |
| `status` | `VARCHAR(20)` | `NOT NULL` | Status (Pending, Completed, Delayed, Cancelled) |

### 13. `stock_transfers`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `transfer_id` | `VARCHAR(20)` | `PRIMARY KEY` | Unique transfer record ID |
| `po_id` | `VARCHAR(20)` | `FOREIGN KEY` | Reference to `purchase_orders.po_id` |
| `from_location`| `VARCHAR(20)` | `NOT NULL` | Origin facility ID |
| `to_location` | `VARCHAR(20)` | `NOT NULL` | Destination facility ID |
| `transfer_date`| `DATE` | `NOT NULL` | Date of stock transfer |
| `quantity` | `INTEGER` | `CHECK (> 0)` | Total units moved |

---

## 🧮 KPI Formulas & Metric Glossary

| Metric Name | Mathematical Formula | Description & Business Purpose |
| :--- | :--- | :--- |
| **Gross Revenue** | $\sum (\text{Quantity} \times \text{Unit Price})$ | Total revenue generated before discounts and returns |
| **Net Revenue** | $\text{Gross Revenue} - \text{Discounts} - \text{Returned Amount}$ | Total actual revenue earned by the business |
| **Gross Margin %** | $\left( \frac{\text{Net Revenue} - \text{COGS}}{\text{Net Revenue}} \right) \times 100$ | Proportion of revenue retained after direct product costs |
| **Average Order Value (AOV)** | $\frac{\text{Net Revenue}}{\text{Total Orders}}$ | Average monetary value per completed order |
| **Inventory Turnover** | $\frac{\text{Cost of Goods Sold (COGS)}}{\text{Average Inventory Value}}$ | Number of times inventory is sold and replaced in a period |
| **Days of Inventory (DIO)**| $\left( \frac{\text{Average Inventory Value}}{\text{COGS}} \right) \times 365$ | Average number of days stock remains held before sale |
| **Return Rate %** | $\left( \frac{\text{Returned Units}}{\text{Total Units Sold}} \right) \times 100$ | Percentage of sold merchandise returned by customers |
| **Supplier OTIF %** | $\left( \frac{\text{On-Time \& In-Full Deliveries}}{\text{Total Purchase Orders}} \right) \times 100$ | Percentage of supplier orders delivered on schedule and complete |
| **Reorder Point (ROP)** | $(\text{Daily Usage} \times \text{Lead Time}) + \text{Safety Stock}$ | Stock threshold level that triggers a new replenishment order |