# [05] Aggregation
> **Track:** SQL · **Level:** 05 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

You have hundreds of orders and need answers: "How many customers?" "What's total revenue?" "Average order value?" "Best-selling category?" Looking at individual rows won't help — you need to **summarize** many rows into a single result. That's aggregation.

## 2. Core concept (absolute zero)

### What is aggregation?

Aggregation takes many rows and produces **one** summary value per group. The tools are **aggregate functions**: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, and SQLite's `GROUP_CONCAT`.

```sql
SELECT COUNT(*) FROM orders;        -- how many orders total?
SELECT SUM(total) FROM orders;      -- total revenue
SELECT AVG(total) FROM orders;      -- average order value
SELECT MIN(total) FROM orders;      -- smallest order
SELECT MAX(total) FROM orders;      -- biggest order
```

### Sample data for this lesson

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0
);

INSERT INTO products VALUES
    (1, 'Laptop',   'Electronics', 999.99,  5),
    (2, 'Mouse',    'Electronics',  25.50, 50),
    (3, 'Keyboard', 'Electronics',  75.00, 30),
    (4, 'Notebook', 'Stationery',    3.99,200),
    (5, 'Pen',      'Stationery',    1.50,500),
    (6, 'Desk',     'Furniture',    299.00,10),
    (7, 'Chair',    'Furniture',    199.00,15),
    (8, 'Monitor',  'Electronics',  349.00, 8);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    total REAL,
    order_date TEXT
);

INSERT INTO orders VALUES
    (101, 1, 250.00, '2026-06-01'),
    (102, 1,  75.50, '2026-06-15'),
    (103, 2, 320.00, '2026-06-10'),
    (104, 3, 150.00, '2026-06-20'),
    (105, 5,  99.99, '2026-06-25'),
    (106, 2,  50.00, '2026-07-01');

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT
);

INSERT INTO customers VALUES
    (1, 'Alice', 'New York'),
    (2, 'Bob',   'London'),
    (3, 'Carol', 'Paris'),
    (4, 'Dave',  'Berlin');

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL,
    manager_id INTEGER
);

INSERT INTO employees VALUES
    (1, 'Alice', 'Engineering', 120000, NULL),
    (2, 'Bob',   'Engineering',  95000,    1),
    (3, 'Carol', 'Design',       85000,    1),
    (4, 'Dave',  'Engineering', 110000,    1),
    (5, 'Eve',   'Design',       78000,    3),
    (6, 'Frank', 'Marketing',    70000, NULL),
    (7, 'Grace', 'Marketing',    65000,    6),
    (8, NULL,    'Temp',         40000, NULL);

CREATE TABLE null_demo (val INTEGER);
INSERT INTO null_demo VALUES (10), (20), (NULL), (30), (NULL);
```

## 3. Step-by-step breakdown (examples)

### COUNT(*) — count all rows

```sql
SELECT COUNT(*) AS total_products FROM products;
```

```
total_products
--------------
8
```

Every row is counted, NULLs included:

```sql
SELECT COUNT(*) FROM null_demo;   -- 5
```

### COUNT(column) — count non-null values

```sql
SELECT COUNT(name) FROM employees;   -- 7 (one name is NULL)
```

### COUNT(DISTINCT column) — unique values

```sql
SELECT COUNT(DISTINCT category) FROM products;   -- 3
SELECT COUNT(DISTINCT department) FROM employees; -- 4
```

### SUM — total of a numeric column

```sql
SELECT SUM(price) AS inventory_value FROM products;   -- 1952.48
SELECT SUM(total) AS revenue FROM orders;              -- 945.49
```

SUM ignores NULLs:

```sql
SELECT SUM(val) FROM null_demo;   -- 60 (10+20+30, NULLs skipped)
```

### AVG — average

```sql
SELECT AVG(price) FROM products;     -- 244.06
SELECT AVG(salary) FROM employees;   -- 82857.14
```

AVG = SUM / COUNT(non-null). NULLs are excluded from both:

```sql
SELECT AVG(val) FROM null_demo;   -- 20 (60/3, NOT 60/5)
```

To treat NULLs as 0, use `SUM(val) / COUNT(*)`:

```sql
SELECT SUM(val) / COUNT(*) FROM null_demo;   -- 12 (60/5)
```

### MIN and MAX — min and max

```sql
SELECT MIN(price) AS cheapest, MAX(price) AS priciest FROM products;
```

```
cheapest  priciest
-------  ---------
1.50     999.99
```

Works on text too (alphabetical):

```sql
SELECT MIN(name), MAX(name) FROM products;   -- Chair, Pen
SELECT MIN(order_date), MAX(order_date) FROM orders;
```

### GROUP BY — grouping before aggregation

Without GROUP BY, aggregates summarize the whole table. GROUP BY splits into groups:

```sql
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;
```

```
category      product_count
-----------  -------------
Electronics   4
Furniture     2
Stationery    2
```

Multiple aggregates per group:

```sql
SELECT
    category,
    COUNT(*) AS cnt,
    MIN(price) AS min_p,
    MAX(price) AS max_p,
    AVG(price) AS avg_p,
    SUM(stock) AS total_stock
FROM products
GROUP BY category;
```

```
category      cnt  min_p    max_p    avg_p     total_stock
-----------  ----  ------  -------  --------  -----------
Electronics   4    25.50   999.99   362.37    93
Furniture     2    199.0   299.0    249.0     25
Stationery    2    1.50    3.99     2.745     700
```

Group by expression:

```sql
SELECT
    CASE WHEN price < 100 THEN 'budget' WHEN price < 500 THEN 'mid' ELSE 'premium' END AS tier,
    COUNT(*) AS cnt
FROM products
GROUP BY tier;
```

```
tier     cnt
------  ----
budget   3
mid      2
premium  3
```

### HAVING — filtering groups

`WHERE` filters rows **before** grouping. `HAVING` filters groups **after** grouping:

```sql
SELECT category, AVG(price) AS avg_price
FROM products
WHERE stock > 10              -- exclude products with low stock
GROUP BY category
HAVING AVG(price) > 50;       -- keep only groups meeting condition
```

```
category      avg_price
-----------  ---------
Electronics   50.25
Furniture     199.0
```

(Stationery avg=2.745 is filtered by HAVING; Laptop & Monitor & Desk excluded by WHERE)

```sql
SELECT category, COUNT(*) AS cnt
FROM products
GROUP BY category
HAVING cnt >= 3;
```

```
category      cnt
-----------  ---
Electronics   4
```

### GROUP_CONCAT — SQLite's string aggregator

```sql
SELECT category, GROUP_CONCAT(name) AS products
FROM products
GROUP BY category;
```

```
category      products
-----------  ----------------------------
Electronics   Laptop,Mouse,Keyboard,Monitor
Furniture     Desk,Chair
Stationery    Notebook,Pen
```

Custom separator:

```sql
SELECT category, GROUP_CONCAT(name, ' | ') FROM products GROUP BY category;
```

### Combining GROUP BY with JOINs

```sql
SELECT customers.name, SUM(orders.total) AS total_spent
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.name;
```

```
name   total_spent
-----  -----------
Alice  325.5
Bob    370.0
Carol  150.0
Dave   NULL
```

Dave has no orders — SUM of NULL is NULL. Fix with `COALESCE`:

```sql
SELECT customers.name, COALESCE(SUM(orders.total), 0) AS total_spent
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.name;
```

```
name   total_spent
-----  -----------
Alice  325.5
Bob    370.0
Carol  150.0
Dave   0
```

**Common bug**: `COUNT(*)` vs `COUNT(column)` in LEFT JOIN:

```sql
-- Correct: counts only non-null order IDs (Dave = 0)
SELECT customers.name, COUNT(orders.id) FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.name;

-- Wrong: counts the LEFT JOIN row itself (Dave = 1!)
SELECT customers.name, COUNT(*) FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.name;
```

Always use `COUNT(right_table.id)` not `COUNT(*)` in LEFT JOIN aggregations.

Multiple JOINs:

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    price REAL
);

INSERT INTO order_items VALUES
    (1, 101, 'Laptop',   1, 999.99),
    (2, 101, 'Mouse',    2,  25.50),
    (3, 102, 'Keyboard', 1,  75.00),
    (4, 103, 'Monitor',  2, 349.00),
    (5, 104, 'Desk',     1, 299.00);

SELECT customers.name, SUM(order_items.quantity) AS total_items
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id
INNER JOIN order_items ON orders.id = order_items.order_id
GROUP BY customers.name;
```

```
name   total_items
-----  -----------
Alice  4
Bob    2
Carol  1
```

### Order of execution

SQL runs in this order:

```
FROM   →  pick tables
JOIN   →  combine tables
WHERE  →  filter rows
GROUP  →  form groups
HAVING →  filter groups
SELECT →  compute expressions, aliases
ORDER  →  sort
LIMIT  →  paginate
```

This explains why **aliases created in SELECT can't be used in WHERE or GROUP BY**:

```sql
-- OK: alias used in ORDER BY (runs after SELECT)
SELECT category, AVG(price) AS avg_p FROM products
GROUP BY category HAVING avg_p > 100 ORDER BY avg_p;

-- ERROR: alias doesn't exist yet in WHERE
SELECT category, AVG(price) AS avg_p FROM products WHERE avg_p > 100;
```

### NULL handling summary

| Function | NULL behaviour |
|----------|---------------|
| `COUNT(*)` | Counts every row |
| `COUNT(col)` | Skips NULLs |
| `COUNT(DISTINCT col)` | Skips NULLs |
| `SUM(col)` | Ignores NULLs (treats as 0) |
| `AVG(col)` | Excludes NULLs from numerator AND denominator |
| `MIN/MAX(col)` | Ignores NULLs |
| `GROUP_CONCAT(col)` | Ignores NULLs |

```sql
SELECT
    COUNT(*)           AS star,
    COUNT(val)         AS non_null,
    COUNT(DISTINCT val) AS distinct_vals,
    SUM(val)           AS total,
    AVG(val)           AS avg_val,
    MIN(val)           AS min_val,
    MAX(val)           AS max_val
FROM null_demo;
```

```
star  non_null  distinct_vals  total  avg_val  min_val  max_val
----  --------  -------------  -----  -------  -------  -------
5     3         3              60     20       10       30
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `SELECT name, COUNT(*) FROM products` | `name` not in GROUP BY and not aggregated | `SELECT category, COUNT(*) FROM products GROUP BY category` |
| `WHERE COUNT(*) > 1` | Aggregates can't go in WHERE | `HAVING COUNT(*) > 1` |
| Mixing aggregated and non-aggregated columns without GROUP BY | SQLite returns arbitrary values | Always add `GROUP BY` for non-aggregated columns |
| `COUNT(col)` when you meant `COUNT(*)` | NULLs are skipped | `COUNT(*)` for total rows |
| `COUNT(*)` in LEFT JOIN | Counts the NULL row as 1 | `COUNT(right_table.id)` |
| `AVG(col)` expecting `SUM/COUNT(*)` | NULLs excluded from count | Use `SUM(col)/COUNT(*)` if needed |

## 5. Exercises

Use the `products`, `orders`, `customers`, `employees`, `order_items` tables.

1. Count all products.
2. Count employees with non-null names.
3. How many distinct departments?
4. Total value of all orders.
5. Average salary of all employees.
6. Cheapest and most expensive product.
7. Earliest and latest order date.
8. Count products per category.
9. Average price per category.
10. Total stock per category.
11. Categories with more than 2 products (HAVING).
12. Departments with avg salary above 80000.
13. List all product names per category with GROUP_CONCAT.
14. Each customer's total spent (include customers with no orders, show 0).
15. Each customer's order count and total spent.
16. Each customer's total item quantity (join customers → orders → order_items).
17. Customers who spent more than $200.
18. Categories where total stock exceeds 50.
19. Department with the highest-paid employee.
20. Each department's min, max, and avg salary.
21. Difference between highest and lowest salary per department.
22. Each customer with order count and most recent order date.
23. Count orders in June 2026 vs July 2026.
24. Each category with product count and alphabetically sorted comma-separated product names.

## 6. Self-check questions

1. What's the difference between `COUNT(*)` and `COUNT(column)`?
2. What does `COUNT(DISTINCT column)` do?
3. How does `AVG` handle NULLs?
4. What's the purpose of `GROUP BY`?
5. Difference between `WHERE` and `HAVING`?
6. Can you use both `WHERE` and `HAVING` in one query? What's the execution order?
7. Why does `SELECT name, COUNT(*) FROM table` fail?
8. What does `GROUP_CONCAT` do in SQLite?
9. How do you find customers with zero orders using aggregation?
10. What's the SQL execution order (FROM → ? → ? → ? → ? → ? → ?)?
11. Why can't you use SELECT aliases in WHERE or GROUP BY?
12. What's the difference in NULL behaviour between `SUM(col)` and `AVG(col)`?

## 7. What's next

You can now summarize data with aggregation. In **Level 06**, you'll learn about **indexes** — speeding up queries with database structures for fast lookups.
