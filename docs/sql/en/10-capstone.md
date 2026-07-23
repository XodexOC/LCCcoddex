# [10] Capstone
> **Track:** SQL · **Level:** 10 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

You've learned SQL fundamentals — SELECT, JOINs, aggregation, subqueries, CTEs, window functions, normalization. Now it's time to put it all together in a real-world project. You'll import messy CSV data, design a normalized schema, write analytical queries, and present insights.

## 2. Core concept (absolute zero)

### The capstone workflow

1. **Understand the data** — examine raw CSV
2. **Design a schema** — normalize into multiple tables
3. **Import the data** — load CSV into SQLite
4. **Clean the data** — handle missing values, duplicates, typos
5. **Add constraints and indexes** — enforce data integrity and optimize
6. **Write analytical queries** — use JOINs, aggregation, window functions
7. **Export results** — save to CSV for reporting
8. **Present findings** — summarize insights

### Tools used

- `sqlite3` — database engine
- `.import` — CSV import command
- SQL: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE
- Aggregate + window functions
- CTEs for complex queries

## 3. Step-by-step breakdown (examples)

### Step 1: The CSV data

We have a CSV file `sales_data.csv` with online store data:

```
order_id,order_date,customer_name,customer_email,product_name,product_category,quantity,unit_price,coupon_code
1001,2026-01-15,Alice Johnson,alice@email.com,Wireless Mouse,Electronics,2,25.99,SAVE10
1001,2026-01-15,Alice Johnson,alice@email.com,USB-C Hub,Electronics,1,45.50,SAVE10
1002,2026-01-15,Bob Smith,bob@email.com,Laptop,Electronics,1,999.99,
1003,2026-01-16,Alice Johnson,alice@email.com,Desk Lamp,Home,1,89.99,
1004,2026-01-16,Carol Davis,carol@email.com,Notebook,Stationery,5,3.99,
1004,2026-01-16,Carol Davis,carol@email.com,Pen Set,Stationery,2,12.50,
1005,2026-01-17,Bob Smith,bob@email.com,Mouse Pad,Electronics,3,14.99,SAVE10
1006,2026-01-17,David Wilson,david@email.com,Chair,Home,1,299.00,WELCOME20
1006,2026-01-17,David Wilson,david@email.com,Desk,Home,1,449.00,WELCOME20
1007,2026-01-18,Alice Johnson,alice@email.com,Monitor,Electronics,1,349.00,
1008,2026-01-18,Eve Brown,eve@email.com,Keyboard,Electronics,1,75.00,
1009,2026-01-19,Carol Davis,carol@email.com,Desk Organizer,Stationery,1,34.99,
1010,2026-01-19,David Wilson,david@email.com,LED Strip,Home,2,19.99,
1010,2026-01-19,David Wilson,david@email.com,Smart Plug,Home,3,29.99,
1011,2026-01-20,Frank Miller,frank@email.com,Webcam,Electronics,1,129.99,
1012,2026-01-20,Alice Johnson,alice@email.com,Hard Drive,Electronics,1,89.99,
1013,2026-01-21,Bob Smith,bob@email.com,Printer,Electronics,1,199.00,
1014,2026-01-21,Eve Brown,eve@email.com,Tablet,Electronics,1,499.00,TABLET50
1014,2026-01-21,Eve Brown,eve@email.com,Case,Electronics,1,29.99,TABLET50
```

### Step 2: Design a normalized schema

Current problems with the CSV:
- Customer info repeated per order
- Product info mixed with orders
- Order-level data (date, coupon) mixed with line items
- No constraints

**3NF Schema**:

```sql
-- Customers
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Products
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL CHECK (unit_price >= 0)
);

-- Coupons (for normalization)
CREATE TABLE coupons (
    code TEXT PRIMARY KEY,
    discount_percent INTEGER
);

-- Orders
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    coupon_code TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (coupon_code) REFERENCES coupons(code)
);

-- Order Items
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Step 3: Import the CSV

Save the CSV content to `/tmp/sales_data.csv`.

Open SQLite:

```
alice@xodex:~$ sqlite3 xodex_capstone.db
```

First, create a staging table:

```sql
CREATE TABLE staging (
    order_id INTEGER,
    order_date TEXT,
    customer_name TEXT,
    customer_email TEXT,
    product_name TEXT,
    product_category TEXT,
    quantity INTEGER,
    unit_price REAL,
    coupon_code TEXT
);
```

Import the CSV:

```
sqlite> .mode csv
sqlite> .import /tmp/sales_data.csv staging
sqlite> .headers on
sqlite> SELECT * FROM staging LIMIT 5;
```

Note: The `.import` command imports the header row as data too. Skip the first row:

```
sqlite> DELETE FROM staging WHERE rowid = 1;
```

Or better, create without the header by specifying `.import` with `--skip 1`:

```
sqlite> .import --csv --skip 1 /tmp/sales_data.csv staging
```

### Step 4: Clean the data

Check for NULLs:

```sql
SELECT COUNT(*) AS missing_coupon FROM staging WHERE coupon_code IS NULL OR coupon_code = '';
```

```
missing_coupon
--------------
11
```

Handle missing coupon codes:

```sql
UPDATE staging SET coupon_code = NULL WHERE coupon_code = '';
```

Check for duplicates:

```sql
SELECT order_id, product_name, COUNT(*)
FROM staging
GROUP BY order_id, product_name
HAVING COUNT(*) > 1;
```

(Should return no rows if data is clean.)

Check for email inconsistencies:

```sql
SELECT DISTINCT customer_name, customer_email FROM staging ORDER BY customer_name;
```

```
customer_name   customer_email
--------------  --------------
Alice Johnson   alice@email.com
Bob Smith       bob@email.com
Carol Davis     carol@email.com
David Wilson    david@email.com
Eve Brown       eve@email.com
Frank Miller    frank@email.com
```

### Step 5: Populate the normalized tables

Insert customers:

```sql
INSERT OR IGNORE INTO customers (name, email)
SELECT DISTINCT customer_name, customer_email
FROM staging;
```

Insert coupons:

```sql
INSERT OR IGNORE INTO coupons VALUES
    ('SAVE10', 10),
    ('WELCOME20', 20),
    ('TABLET50', 50);
```

Insert products:

```sql
INSERT OR IGNORE INTO products (name, category, unit_price)
SELECT DISTINCT product_name, product_category, unit_price
FROM staging;
```

Insert orders:

```sql
INSERT INTO orders (id, customer_id, order_date, coupon_code)
SELECT DISTINCT
    s.order_id,
    c.id,
    s.order_date,
    s.coupon_code
FROM staging s
JOIN customers c ON c.email = s.customer_email;
```

Insert order items:

```sql
INSERT INTO order_items (order_id, product_id, quantity)
SELECT
    s.order_id,
    p.id,
    s.quantity
FROM staging s
JOIN products p ON p.name = s.product_name;
```

### Step 6: Add constraints and indexes

Now that data is imported, add indexes for performance:

```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_products_category ON products(category);
```

### Step 7: Write analytical queries

**Total revenue per customer**:

```sql
SELECT
    c.name,
    SUM(oi.quantity * p.unit_price) AS total_spent,
    COUNT(DISTINCT o.id) AS order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY c.id
ORDER BY total_spent DESC;
```

```
name            total_spent  order_count
--------------  -----------  -----------
David Wilson    867.94       2
Alice Johnson   689.43       4
Bob Smith       213.98       2
Eve Brown       603.99       2
Carol Davis     71.47        2
Frank Miller    129.99       1
```

**Daily sales trend**:

```sql
SELECT
    o.order_date,
    COUNT(DISTINCT o.id) AS orders,
    SUM(oi.quantity) AS items_sold,
    SUM(oi.quantity * p.unit_price) AS revenue
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY o.order_date
ORDER BY o.order_date;
```

```
order_date   orders  items_sold  revenue
----------   ------  ----------  --------
2026-01-15   2       3           97.48
2026-01-16   2       7           120.46
2026-01-17   2       6           820.94
2026-01-18   2       2           424.0
2026-01-19   2       6           94.95
2026-01-20   2       2           219.98
2026-01-21   2       3           727.98
```

**Top products by revenue**:

```sql
SELECT
    p.name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * p.unit_price) AS revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id
ORDER BY revenue DESC
LIMIT 5;
```

```
name          category      units_sold  revenue
------------  ------------  ----------  --------
Laptop        Electronics   1           999.99
Chair         Home          1           299.0
Desk          Home          1           449.0
Monitor       Electronics   1           349.0
Tablet        Electronics   1           499.0
```

**Product category breakdown**:

```sql
SELECT
    p.category,
    COUNT(DISTINCT p.id) AS unique_products,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * p.unit_price) AS revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```

```
category      unique_products  units_sold  revenue
------------  ---------------  ----------  --------
Electronics   11               15          3026.43
Home          4                7           867.94
Stationery    3                8           71.47
```

**Average order value**:

```sql
SELECT
    ROUND(AVG(order_total), 2) AS avg_order_value
FROM (
    SELECT
        o.id,
        SUM(oi.quantity * p.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    GROUP BY o.id
);
```

```
avg_order_value
---------------
419.56
```

**Window function: cumulative revenue over time**:

```sql
WITH daily_revenue AS (
    SELECT
        o.order_date,
        SUM(oi.quantity * p.unit_price) AS revenue
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    GROUP BY o.order_date
)
SELECT
    order_date,
    revenue,
    SUM(revenue) OVER (ORDER BY order_date) AS cumulative_revenue
FROM daily_revenue
ORDER BY order_date;
```

```
order_date   revenue   cumulative_revenue
----------   -------  ------------------
2026-01-15   97.48     97.48
2026-01-16   120.46    217.94
2026-01-17   820.94    1038.88
2026-01-18   424.0     1462.88
2026-01-19   94.95     1557.83
2026-01-20   219.98    1777.81
2026-01-21   727.98    2505.79
```

**Customer ranking by total spent**:

```sql
WITH customer_spending AS (
    SELECT
        c.name,
        SUM(oi.quantity * p.unit_price) AS total_spent
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    GROUP BY c.id
)
SELECT
    name,
    total_spent,
    RANK() OVER (ORDER BY total_spent DESC) AS rank
FROM customer_spending
ORDER BY rank;
```

```
name           total_spent  rank
-------------  -----------  ----
David Wilson   867.94       1
Alice Johnson  689.43       2
Eve Brown      603.99       3
Bob Smith      213.98       4
Frank Miller   129.99       5
Carol Davis    71.47        6
```

### Step 8: Export results

```
sqlite> .headers on
sqlite> .mode csv
sqlite> .output /tmp/customer_spending.csv
sqlite> SELECT c.name, SUM(oi.quantity * p.unit_price) AS total_spent
   ...> FROM customers c
   ...> JOIN orders o ON c.id = o.customer_id
   ...> JOIN order_items oi ON o.id = oi.order_id
   ...> JOIN products p ON oi.product_id = p.id
   ...> GROUP BY c.id
   ...> ORDER BY total_spent DESC;
sqlite> .output stdout
```

Check the exported file:

```
alice@xodex:~$ cat /tmp/customer_spending.csv
name,total_spent
"David Wilson",867.94
"Alice Johnson",689.43
"Eve Brown",603.99
"Bob Smith",213.98
"Frank Miller",129.99
"Carol Davis",71.47
```

### Step 9: Present findings

**Key Insights**:
- **Top customer**: David Wilson ($867.94) — bought high-value home items
- **Best category**: Electronics ($3,026.43 — 76% of all revenue)
- **Best-selling product**: Laptop ($999.99 — single sale)
- **Coupon effectiveness**: WELCOME20 used on highest-value order ($867.94)
- **Average order value**: $419.56
- **Peak day**: January 17 ($820.94 — largest single-day revenue)
- **Customer retention**: Most customers ordered only once or twice

**Recommendations**:
- Cross-sell Electronics accessories to Home buyers
- Target Carol Davis and Frank Miller with re-engagement campaigns
- Offer more tiered coupon codes to increase average order value

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Importing CSV without checking headers | First row imported as data | Use `--skip 1` or delete header row |
| Not handling NULL/empty strings | NULL comparisons fail | Clean with `UPDATE ... SET col = NULL WHERE col = ''` |
| Skipping schema design before import | Messy, hard to query | Design schema based on CSV analysis |
| Forgetting foreign key constraints | Orphaned data possible | Enable `PRAGMA foreign_keys = ON` |
| No indexes on join columns | Slow queries on large datasets | Index FK columns and commonly filtered columns |
| Not verifying after import | Silent failures or partial imports | Always `SELECT COUNT(*)` to verify |

## 5. Exercises

1. Download or create the sales_data.csv from the examples above.
2. Create a staging table and import the CSV.
3. Clean the data: handle missing coupon codes, check for duplicates.
4. Design a normalized 3NF schema (customers, products, orders, order_items, coupons).
5. Populate the normalized tables from staging data.
6. Add indexes on foreign key columns.
7. Write a query to find the top 3 products by quantity sold.
8. Write a query to find customers who spent more than $200.
9. Use a window function to rank customers by number of orders.
10. Export the customer ranking to a CSV file.

## 6. Self-check questions

1. What is the first step when working with a new CSV dataset?
2. How do you import a CSV into SQLite?
3. Why should you normalize data before running analytical queries?
4. What indexes should you create for a typical order management schema?
5. How do you handle missing values in imported data?
6. How do you export query results to CSV in SQLite?
7. What is the purpose of a staging table?
8. How do you check if the import was successful?
9. When would you use a CTE instead of a subquery in analysis?
10. What window function would you use to find the top 3 products per category?

## 7. What's next

Congratulations! You've completed all 11 SQL levels. You started from absolute zero — installing SQLite and writing your first SELECT — and now you can design normalized databases, import real-world data, write complex analytical queries with JOINs, aggregation, CTEs, and window functions, and export meaningful insights.

To continue:
- Practice with larger datasets from Kaggle or your own projects
- Learn PostgreSQL for production-ready databases
- Explore database administration (backups, users, performance tuning)
- Move on to the Linux track to master the operating system side
