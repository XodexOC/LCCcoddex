# [04] JOINs
> **Track:** SQL · **Level:** 04 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

In a relational database, data is spread across multiple tables. Users are in one table, their orders in another, order items in a third. To answer questions like "Show me all orders with customer names and product details," you need to **join** these tables together. JOINs are the superpower of SQL.

## 2. Core concept (absolute zero)

### What is a JOIN?

A **JOIN** combines rows from two (or more) tables based on a related column between them.

### Sample data for this lesson

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    total REAL,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO customers VALUES (1, 'Alice', 'New York');
INSERT INTO customers VALUES (2, 'Bob', 'London');
INSERT INTO customers VALUES (3, 'Carol', 'Paris');
INSERT INTO customers VALUES (4, 'Dave', 'Berlin');

INSERT INTO orders VALUES (101, 1, 250.00, '2026-06-01');
INSERT INTO orders VALUES (102, 1, 75.50, '2026-06-15');
INSERT INTO orders VALUES (103, 2, 320.00, '2026-06-10');
INSERT INTO orders VALUES (104, 3, 150.00, '2026-06-20');
INSERT INTO orders VALUES (105, 5, 99.99, '2026-06-25');  -- customer 5 does NOT exist!
INSERT INTO orders VALUES (106, 2, 50.00, '2026-07-01');
```

### The types of JOINs

| JOIN type | What it returns |
|-----------|----------------|
| `INNER JOIN` | Only rows that match in BOTH tables |
| `LEFT JOIN` | ALL rows from the left table, matching rows from the right (NULL if no match) |
| `RIGHT JOIN` | ALL rows from the right table, matching rows from the left (NULL if no match) |
| `FULL OUTER JOIN` | ALL rows from BOTH tables (NULL where no match) |
| `CROSS JOIN` | Every combination of rows (cartesian product) |

### The Venn diagram analogy

- **INNER JOIN**: the overlapping middle section
- **LEFT JOIN**: the entire left circle + overlapping section
- **RIGHT JOIN**: the entire right circle + overlapping section
- **FULL OUTER JOIN**: everything in both circles

## 3. Step-by-step breakdown (examples)

### INNER JOIN — the most common

Return only customers who have orders (and only orders that have customers):

```sql
SELECT customers.name, orders.id, orders.total
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

```
name   order_id  total
-----  --------  ------
Alice  101       250.0
Alice  102       75.5
Bob    103       320.0
Carol  104       150.0
Bob    106       50.0
```

- Alice appears twice (she has 2 orders)
- Dave never ordered — excluded (no matching order)
- Order 105 has customer_id 5 (no matching customer) — excluded
- `INNER JOIN` = only matching rows

### LEFT JOIN — all from left, matching from right

```sql
SELECT customers.name, orders.id, orders.total
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;
```

```
name   order_id  total
-----  --------  ------
Alice  101       250.0
Alice  102       75.5
Bob    103       320.0
Bob    106       50.0
Carol  104       150.0
Dave   NULL      NULL
```

- Dave has no orders, but he still appears — with NULL values
- `LEFT JOIN` = all customers, with order data where available

Useful to find customers with no orders:

```sql
SELECT customers.name
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
WHERE orders.id IS NULL;
```

```
name
----
Dave
```

### RIGHT JOIN — all from right, matching from left

SQLite does NOT support `RIGHT JOIN` directly. But you can simulate it with a `LEFT JOIN` by swapping the tables:

```sql
SELECT customers.name, orders.id, orders.total
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.id;
```

This gives all orders, with customer data where available (order 105 will have NULL customer name).

Wait — what would a real RIGHT JOIN look like?

```sql
-- PostgreSQL / MySQL syntax (NOT SQLite):
SELECT customers.name, orders.id, orders.total
FROM customers
RIGHT JOIN orders ON customers.id = orders.customer_id;
```

Returns: all orders (101-106) with customer names where they exist. Order 105 has no customer → NULL name.

### FULL OUTER JOIN — all from both

SQLite doesn't support FULL OUTER JOIN. Workaround using UNION:

```sql
SELECT customers.name, orders.id, orders.total
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
UNION
SELECT customers.name, orders.id, orders.total
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.id;
```

This combines result of LEFT JOIN (all customers) and LEFT JOIN reversed (all orders). Every customer and every order appears at least once.

### CROSS JOIN — every combination

```sql
SELECT customers.name, orders.id
FROM customers
CROSS JOIN orders;
```

```
name   order_id
-----  --------
Alice  101
Alice  102
Alice  103
Alice  104
Alice  105
Alice  106
Bob    101
Bob    102
... (24 rows total)
```

Each customer paired with every order. Usually not what you want, but useful for generating combinations.

### Multiple JOINs

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

INSERT INTO order_items VALUES
    (1, 101, 'Laptop', 1, 999.99),
    (2, 101, 'Mouse', 2, 25.50),
    (3, 102, 'Keyboard', 1, 75.00),
    (4, 103, 'Monitor', 2, 349.00),
    (5, 104, 'Desk', 1, 299.00);
```

Join three tables:

```sql
SELECT
    customers.name AS customer,
    orders.id AS order_id,
    order_items.product_name,
    order_items.quantity
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id
INNER JOIN order_items ON orders.id = order_items.order_id;
```

```
customer  order_id  product_name  quantity
--------  --------  ------------  --------
Alice     101       Laptop        1
Alice     101       Mouse         2
Alice     102       Keyboard      1
Bob       103       Monitor       2
Carol     104       Desk          1
```

### JOIN with USING

When the column name is the same in both tables, you can use `USING` instead of `ON`:

```sql
-- If both tables have a column named 'customer_id'
SELECT customers.name, orders.id
FROM customers
INNER JOIN orders USING (id);
-- Wait, that's wrong — the column name must be the SAME

-- Correct example: if both tables have 'department_id':
-- SELECT * FROM employees INNER JOIN departments USING (department_id);
```

In our case, the join column is `customers.id` and `orders.customer_id` — different names, so we use `ON`.

### Self-JOIN

Join a table to itself:

```sql
CREATE TABLE employees2 (
    id INTEGER PRIMARY KEY,
    name TEXT,
    manager_id INTEGER
);

INSERT INTO employees2 VALUES (1, 'Alice', NULL);
INSERT INTO employees2 VALUES (2, 'Bob', 1);
INSERT INTO employees2 VALUES (3, 'Carol', 1);
INSERT INTO employees2 VALUES (4, 'Dave', 2);
INSERT INTO employees2 VALUES (5, 'Eve', 2);

SELECT
    e.name AS employee,
    m.name AS manager
FROM employees2 e
LEFT JOIN employees2 m ON e.manager_id = m.id;
```

```
employee  manager
--------  -------
Alice     NULL
Bob       Alice
Carol     Alice
Dave      Bob
Eve       Bob
```

### Putting it all together: a real query

Find all customers who spent more than $300 total:

```sql
SELECT
    customers.name,
    SUM(orders.total) AS total_spent
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.name
HAVING total_spent > 300
ORDER BY total_spent DESC;
```

```
name  total_spent
----  -----------
Bob   370.0
Alice 325.5
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Forgetting the JOIN condition (`ON`) | Creates a CROSS JOIN — every row paired with every other row | Always specify `ON` or `USING` |
| `LEFT JOIN` when you meant `INNER JOIN` | Returns rows with NULL where no match exists | Use INNER JOIN for only matching rows |
| `INNER JOIN ... ON a.id = b.id` when data mismatches | No rows returned! | Check that the columns have matching values |
| No table aliases | Verbose queries, ambiguous columns | `FROM customers c JOIN orders o ON c.id = o.customer_id` |
| `ON a.id = b.id AND b.col = 'x'` as filter | Moves filter into JOIN condition (still works but confusing) | WHERE for filtering, ON for joining |
| RIGHT JOIN in SQLite | SQLite doesn't support it | Swap tables and use LEFT JOIN |

## 5. Exercises

Use the `customers`, `orders`, and `order_items` tables.

1. Write an INNER JOIN to show customer names and their order IDs.
2. Write a LEFT JOIN to show all customers, including those without orders.
3. Find customers who have never placed an order (using LEFT JOIN + WHERE IS NULL).
4. Join all three tables (customers, orders, order_items) to show customer names, order IDs, and product names.
5. Add a WHERE clause to the above to show only Alice's orders.
6. Write a CROSS JOIN between customers and orders. How many rows do you get?
7. Use a self-JOIN on the employees2 table to find everyone who reports to Alice.
8. Find the total spent by each customer using JOIN + GROUP BY + SUM.
9. Find customers who bought more than 2 items total.
10. Write a LEFT JOIN to show all orders, even those with no matching customer (order 105).
11. Combine customers and orders with a UNION-based FULL OUTER JOIN.
12. Find the most expensive item each customer ordered.

## 6. Self-check questions

1. What is the difference between INNER JOIN and LEFT JOIN?
2. What does a CROSS JOIN do?
3. When would you use `ON` vs `USING` in a JOIN?
4. How do you find rows in one table that have no match in another?
5. What is a self-JOIN and why would you use it?
6. Does SQLite support RIGHT JOIN? How do you work around it?
7. What happens if you JOIN two tables without an ON clause?
8. How do you JOIN more than two tables?
9. What is the purpose of table aliases in JOINs?
10. Can you use WHERE and JOIN together? What's the difference putting a condition in ON vs WHERE?

## 7. What's next

You can combine data from multiple tables with JOINs. In **Level 05**, you'll learn about **aggregation** — using `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, and `HAVING` to summarize and analyze data.
