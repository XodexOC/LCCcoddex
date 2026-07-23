# [08] CTEs and window functions
> **Track:** SQL · **Level:** 08 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

Some queries are too complex to write in a single SELECT. **CTEs** (Common Table Expressions) let you break a query into named, readable steps. **Window functions** let you perform calculations across "windows" of rows — like row numbers, rankings, running totals — without collapsing rows like GROUP BY does.

## 2. Core concept (absolute zero)

### What is a CTE?

A **CTE** is a named temporary result set that exists only for the duration of a query. Think of it as a named subquery that you can reference multiple times.

```sql
WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;
```

### What is a window function?

A **window function** performs a calculation across a set of rows related to the current row. Unlike aggregate functions (which collapse rows), window functions preserve all rows.

```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank
FROM employees;
```

Each row keeps its identity, but gets a computed value based on the "window" of rows.

## 3. Step-by-step breakdown (examples)

### Sample data

```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    category TEXT,
    amount REAL,
    sale_date TEXT
);

INSERT INTO sales VALUES
    (1, 'Laptop', 'Electronics', 1200, '2026-01-15'),
    (2, 'Mouse', 'Electronics', 25, '2026-01-15'),
    (3, 'Laptop', 'Electronics', 1200, '2026-01-16'),
    (4, 'Desk', 'Furniture', 299, '2026-01-16'),
    (5, 'Chair', 'Furniture', 199, '2026-01-17'),
    (6, 'Mouse', 'Electronics', 25, '2026-01-17'),
    (7, 'Laptop', 'Electronics', 1200, '2026-01-18'),
    (8, 'Desk', 'Furniture', 299, '2026-01-18');
```

### Basic CTE

```sql
WITH electronics_sales AS (
    SELECT * FROM sales WHERE category = 'Electronics'
)
SELECT product, SUM(amount) AS total
FROM electronics_sales
GROUP BY product;
```

```
product   total
-------  ------
Laptop    3600
Mouse     50
```

### Multiple CTEs

```sql
WITH
electronics AS (
    SELECT * FROM sales WHERE category = 'Electronics'
),
furniture AS (
    SELECT * FROM sales WHERE category = 'Furniture'
)
SELECT 'Electronics' AS category, SUM(amount) AS total FROM electronics
UNION ALL
SELECT 'Furniture', SUM(amount) FROM furniture;
```

```
category      total
------------  ------
Electronics   3650
Furniture     498
```

### CTE for readability — multi-step query

Find categories where the total sales are above average:

```sql
WITH category_totals AS (
    SELECT category, SUM(amount) AS total
    FROM sales
    GROUP BY category
),
overall_avg AS (
    SELECT AVG(total) AS avg_total FROM category_totals
)
SELECT ct.category, ct.total
FROM category_totals ct, overall_avg oa
WHERE ct.total > oa.avg_total;
```

```
category      total
------------  ------
Electronics   3650
```

Much more readable than nested subqueries!

### Recursive CTE (simple example)

A recursive CTE calls itself. Useful for hierarchies and sequences.

Count from 1 to 5:

```sql
WITH RECURSIVE counter(n) AS (
    SELECT 1           -- anchor member
    UNION ALL
    SELECT n + 1       -- recursive member
    FROM counter
    WHERE n < 5
)
SELECT * FROM counter;
```

```
n
-
1
2
3
4
5
```

**How it works**:
1. Start with `n = 1` (anchor)
2. Generate `n + 1 = 2`, then `3`, `4`, `5`
3. Stop when `n < 5` is false

### Recursive CTE: organization hierarchy

```sql
CREATE TABLE org (
    id INTEGER PRIMARY KEY,
    name TEXT,
    manager_id INTEGER
);

INSERT INTO org VALUES
    (1, 'Alice', NULL),
    (2, 'Bob', 1),
    (3, 'Carol', 1),
    (4, 'Dave', 2),
    (5, 'Eve', 2),
    (6, 'Frank', 3);

WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 0 AS level
    FROM org
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM org e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY level, id;
```

```
id  name   manager_id  level
--  -----  ----------  -----
1   Alice  NULL        0
2   Bob    1           1
3   Carol  1           1
4   Dave   2           2
5   Eve    2           2
6   Frank  3           2
```

### Window functions: ROW_NUMBER()

Assign a unique number to each row within a partition:

```sql
SELECT
    product,
    amount,
    sale_date,
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS overall_rank
FROM sales;
```

```
product  amount  sale_date   overall_rank
-------  ------  ----------  ------------
Laptop   1200    2026-01-15  1
Laptop   1200    2026-01-16  2
Laptop   1200    2026-01-18  3
Desk     299     2026-01-16  4
Desk     299     2026-01-18  5
Chair    199     2026-01-17  6
Mouse    25      2026-01-15  7
Mouse    25      2026-01-17  8
```

### ROW_NUMBER() with PARTITION BY

Number rows within each category:

```sql
SELECT
    product,
    category,
    amount,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS cat_rank
FROM sales;
```

```
product   category      amount  cat_rank
--------  ------------  ------  --------
Laptop    Electronics   1200    1
Laptop    Electronics   1200    2
Mouse     Electronics   25      3
Laptop    Electronics   1200    4
Mouse     Electronics   25      5
Desk      Furniture     299     1
Chair     Furniture     199     2
Desk      Furniture     299     3
```

### RANK() and DENSE_RANK()

`RANK()` — same rank for ties, skips numbers.
`DENSE_RANK()` — same rank for ties, NO skips.

```sql
SELECT
    product,
    amount,
    RANK() OVER (ORDER BY amount DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS dense_rank
FROM sales;
```

```
product  amount  rank  dense_rank
-------  ------  ----  ----------
Laptop   1200    1     1
Laptop   1200    1     1
Laptop   1200    1     1
Desk     299     4     2
Desk     299     4     2
Chair    199     6     3
Mouse    25      7     4
Mouse    25      7     4
```

- RANK: after three 1200s, next rank is 4 (skips 2, 3)
- DENSE_RANK: after three 1200s, next rank is 2 (no skip)

### Window functions with aggregation

Running total (SUM as window function):

```sql
SELECT
    sale_date,
    amount,
    SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM sales;
```

```
sale_date    amount  running_total
----------  ------  -------------
2026-01-15  1200    1200
2026-01-15  25      1225
2026-01-16  1200    2425
2026-01-16  299     2724
2026-01-17  199     2923
2026-01-17  25      2948
2026-01-18  1200    4148
2026-01-18  299     4447
```

Moving average (last 3 rows):

```sql
SELECT
    sale_date,
    amount,
    AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
FROM sales;
```

### Window functions with PARTITION BY

Average per category, shown on each row:

```sql
SELECT
    product,
    category,
    amount,
    AVG(amount) OVER (PARTITION BY category) AS cat_avg,
    amount - AVG(amount) OVER (PARTITION BY category) AS diff_from_avg
FROM sales;
```

```
product   category      amount  cat_avg     diff_from_avg
--------  ------------  ------  ----------  -------------
Laptop    Electronics   1200    730.0       470.0
Laptop    Electronics   1200    730.0       470.0
Mouse     Electronics   25      730.0       -705.0
Laptop    Electronics   1200    730.0       470.0
Mouse     Electronics   25      730.0       -705.0
Desk      Furniture     299     265.67      33.33
Chair     Furniture     199     265.67      -66.67
Desk      Furniture     299     265.67      33.33
```

### CTE + window function: top product per category

```sql
WITH ranked AS (
    SELECT
        product,
        category,
        amount,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rn
    FROM sales
)
SELECT category, product, amount
FROM ranked
WHERE rn = 1;
```

```
category      product  amount
------------  -------  ------
Electronics   Laptop   1200
Furniture     Desk     299
```

### Putting it all together

Find the top-selling product per category, plus category average:

```sql
WITH product_totals AS (
    SELECT
        category,
        product,
        SUM(amount) AS total_sold
    FROM sales
    GROUP BY category, product
),
ranked AS (
    SELECT
        category,
        product,
        total_sold,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_sold DESC) AS rn,
        AVG(total_sold) OVER (PARTITION BY category) AS cat_avg
    FROM product_totals
)
SELECT category, product, total_sold, cat_avg
FROM ranked
WHERE rn = 1;
```

```
category      product  total_sold  cat_avg
------------  -------  ----------  --------
Electronics   Laptop   3600        1825.0
Furniture     Desk     598         498.0
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Forgetting `RECURSIVE` for recursive CTE | Error: "circular reference" | `WITH RECURSIVE cte AS (...)` |
| No `UNION ALL` in recursive CTE | Must separate anchor and recursive members | Anchor `SELECT ... UNION ALL SELECT ...` |
| No `ORDER BY` in window function | Rows are in undefined order | Always specify `ORDER BY` in `OVER()` |
| Using `RANK()` when you want no gaps | RANK skips numbers on ties | Use `DENSE_RANK()` |
| `WHERE rn = 1` without CTE | Can't use window function in WHERE directly | Wrap in CTE or subquery |
| `PARTITION BY` on high-cardinality column | Each partition has 1 row — pointless window | Choose meaningful partitions |

## 5. Exercises

1. Write a CTE that selects all Electronics sales, then query it.
2. Write a multi-CTE query: one CTE for Electronics totals, one for Furniture totals, then combine.
3. Use a recursive CTE to generate numbers from 10 to 1 (descending).
4. Use `ROW_NUMBER()` to rank products by total sales.
5. Use `RANK()` and `DENSE_RANK()` to rank sales by amount. Note the difference.
6. Use `ROW_NUMBER()` with `PARTITION BY category` to rank products within each category.
7. Compute a running total of sales by date using `SUM(...) OVER (ORDER BY date)`.
8. Find the top 2 products per category using a CTE + window function.

## 6. Self-check questions

1. What is a CTE and why is it useful?
2. What does `RECURSIVE` do in a CTE?
3. What is the difference between a window function and an aggregate function?
4. What does `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)` do?
5. What is the difference between `RANK()` and `DENSE_RANK()`?
6. What is a "running total" and how do you compute it with a window function?
7. Can you use a window function in a WHERE clause? Why or why not?
8. What does `LAG()` do?
9. What does `PARTITION BY` do in a window function?
10. How do you get the top N rows per group using window functions?

## 7. What's next

CTEs and window functions are powerful tools for complex queries. In **Level 09**, you'll learn about **normalization** — designing database schemas to avoid duplication and maintain data integrity through 1NF, 2NF, 3NF, and when to denormalize.
