# Data dictionary and calculation contract

`data_dictionary.csv` specifies every source column, intended Silver type, nullability, definition, and real example from the supplied files. Bronze reads every column as STRING so invalid data can be explained rather than lost during type inference. Nullability describes accepted data after cleaning, except the two explicitly marked dirty input fields.

## Tables, grain, and relationships
| Source | Rows | What one row means | Key |
|---|---:|---|---|
| stores.csv | 10 | One branch | store_id |
| products.csv | 12 | One product | product_id |
| customers.csv | 20 | One fictional customer | customer_id |
| sales_batch_01.csv | 60 | One initial sale version | sale_id + record_version |
| sales_dirty.csv | 68 | One raw exported row, including duplicates/errors | source_row_id |
| sales_batch_02.csv | 23 | One arriving sale version or replay | source_row_id |
| returns.csv | 6 | One return/refund event | return_id |

Sales joins many-to-one to stores, products, and (optionally) customers. Returns joins many-to-one to the current sale. Current Silver sales has one row per sale_id. There are no customer contact fields.

## Column definitions

### customers.csv

| Column | Type after cleaning | Null allowed | Meaning |
|---|---|---|---|
| customer_id | STRING | no | Customer primary key in customers; nullable sales foreign key. Blank sales customer means guest. |
| customer_name | STRING | no | Invented first name, no real customer identity. |
| city | STRING | no | Indian city; customer city may differ from purchase store city. |
| signup_date | DATE | no | Date this fictional customer joined; yyyy-MM-dd. |

### products.csv

| Column | Type after cleaning | Null allowed | Meaning |
|---|---|---|---|
| product_id | STRING | no | Product primary key in products; sales foreign key to products.product_id. |
| product_name | STRING | no | Product label with pack size where relevant. |
| category | STRING | no | Grocery, Personal Care, Stationery, Home. |
| list_price | DECIMAL(12,2) | no | Reference INR price per unit; used only to fill absent sale prices. |

### returns.csv

| Column | Type after cleaning | Null allowed | Meaning |
|---|---|---|---|
| return_id | STRING | no | Unique return-event primary key. |
| sale_id | STRING | no | One product-line transaction; primary key in current sales; foreign key in returns. |
| return_date | DATE | no | Date refund is paid; on/after original sale_date; yyyy-MM-dd. |
| return_quantity | INT | no | Positive whole returned units; cumulative units cannot exceed sold quantity. |
| refund_amount | DECIMAL(12,2) | no | Positive INR refund for this event, discounted unit price times return_quantity. |
| reason | STRING | no | Damaged, Changed mind, or Wrong item. |
| available_batch | STRING | no | 01 visible initially; 02 becomes visible only after sales batch 02. Preserve leading zero. |

### sales_batch_01.csv

| Column | Type after cleaning | Null allowed | Meaning |
|---|---|---|---|
| source_row_id | STRING | no | Physical row identity within a file; retain for tracing. Not the sale business key. |
| sale_id | STRING | no | One product-line transaction; primary key in current sales; foreign key in returns. |
| sale_date | DATE | no | Business date in Asia/Kolkata, normally yyyy-MM-dd. |
| store_id | STRING | no | Store primary key in stores; sales foreign key to stores.store_id. |
| product_id | STRING | no | Product primary key in products; sales foreign key to products.product_id. |
| customer_id | STRING | yes | Customer primary key in customers; nullable sales foreign key. Blank sales customer means guest. |
| quantity | INT | no | Whole units sold, integer >=1. Returns are separate positive events. |
| unit_price | DECIMAL(12,2) | dirty input only | Historical INR price per unit before discount. Must be >0 after repair. |
| discount_pct | DECIMAL(5,2) | dirty input only | Percentage points in [0,100]; 5 means 5%, not 0.05. |
| payment_method | STRING | no | UPI, CARD, CASH after trim/uppercase. |
| record_version | INT | no | Positive version per sale_id; highest version is current. Equal version must have same business payload. |

### sales_batch_02.csv

| Column | Type after cleaning | Null allowed | Meaning |
|---|---|---|---|
| source_row_id | STRING | no | Physical row identity within a file; retain for tracing. Not the sale business key. |
| sale_id | STRING | no | One product-line transaction; primary key in current sales; foreign key in returns. |
| sale_date | DATE | no | Business date in Asia/Kolkata, normally yyyy-MM-dd. |
| store_id | STRING | no | Store primary key in stores; sales foreign key to stores.store_id. |
| product_id | STRING | no | Product primary key in products; sales foreign key to products.product_id. |
| customer_id | STRING | yes | Customer primary key in customers; nullable sales foreign key. Blank sales customer means guest. |
| quantity | INT | no | Whole units sold, integer >=1. Returns are separate positive events. |
| unit_price | DECIMAL(12,2) | dirty input only | Historical INR price per unit before discount. Must be >0 after repair. |
| discount_pct | DECIMAL(5,2) | dirty input only | Percentage points in [0,100]; 5 means 5%, not 0.05. |
| payment_method | STRING | no | UPI, CARD, CASH after trim/uppercase. |
| record_version | INT | no | Positive version per sale_id; highest version is current. Equal version must have same business payload. |

### sales_dirty.csv

| Column | Type after cleaning | Null allowed | Meaning |
|---|---|---|---|
| source_row_id | STRING | no | Physical row identity within a file; retain for tracing. Not the sale business key. |
| sale_id | STRING | no | One product-line transaction; primary key in current sales; foreign key in returns. |
| sale_date | DATE | no | Business date in Asia/Kolkata, normally yyyy-MM-dd. |
| store_id | STRING | no | Store primary key in stores; sales foreign key to stores.store_id. |
| product_id | STRING | no | Product primary key in products; sales foreign key to products.product_id. |
| customer_id | STRING | yes | Customer primary key in customers; nullable sales foreign key. Blank sales customer means guest. |
| quantity | INT | no | Whole units sold, integer >=1. Returns are separate positive events. |
| unit_price | DECIMAL(12,2) | dirty input only | Historical INR price per unit before discount. Must be >0 after repair. |
| discount_pct | DECIMAL(5,2) | dirty input only | Percentage points in [0,100]; 5 means 5%, not 0.05. |
| payment_method | STRING | no | UPI, CARD, CASH after trim/uppercase. |
| record_version | INT | no | Positive version per sale_id; highest version is current. Equal version must have same business payload. |

### stores.csv

| Column | Type after cleaning | Null allowed | Meaning |
|---|---|---|---|
| store_id | STRING | no | Store primary key in stores; sales foreign key to stores.store_id. |
| store_name | STRING | no | Fictional branch display name. |
| city | STRING | no | Indian city; customer city may differ from purchase store city. |
| state | STRING | no | Indian state or territory. |
| region | STRING | no | Teaching grouping: North, South, East, West. |

## Derived columns and metrics (INR unless stated)
Round monetary amounts to two decimals with HALF_UP. Use Decimal in Python and decimal types in Spark. Do not use binary float for an answer-key comparison. All supplied prices/discounts produce exact paise and discounted unit prices, avoiding partial-refund rounding ambiguity.

| Name | Definition |
|---|---|
| gross_sales | quantity * unit_price, before discount and before returns |
| discount_amount | round(gross_sales * discount_pct / 100, 2) |
| net_sales | gross_sales - discount_amount, before returns |
| returned_units | sum of return_quantity for the sale, 0 if none |
| refund_amount | sum of available refund events for the sale, 0 if none |
| net_revenue | net_sales - refund_amount; revenue retained, not profit |
| sale_count | Count of current sale_id records; not arrival count |
| units_sold | Sum of current quantity |
| net_units | units_sold - returned_units |
| average_sale_value | Total net_sales / sale_count; before refunds, rounded to 2 decimals |
| identified_customers | Distinct non-null purchasing customer_id values; excludes guests |
| guest_sales | Count of sales with blank customer_id |
| return_events | Count of visible return_id values |
| refunds_paid | Refund sum grouped by return_date in the cash-date view |
| cash_movement | Sale-date net_sales less refunds_paid on that event_date |

Expected `initial_*` files use 60 initial current sales and available_batch=01 returns. `final_*` uses 80 current sales and all returns. `_sales.csv` preserves the winning source row; `_line_amounts.csv` adds six derived columns; `_metrics.csv` is metric/value; `_by_store`, `_by_product`, `_by_category`, and `_by_sale_date` contain sale_count, units_sold, gross_sales, discount_amount, net_sales, returned_units, refund_amount, and net_revenue. The product view includes unsold products with zero values. Sale-date views attribute refunds back to the original sale date. `_by_cash_date` instead uses event_date, net_sales, refunds_paid, cash_movement. `quarantine.csv` contains raw sale fields plus rejection_reason. All sort orders are deterministic (ascending IDs, categories, or dates); metrics follow the order above.
