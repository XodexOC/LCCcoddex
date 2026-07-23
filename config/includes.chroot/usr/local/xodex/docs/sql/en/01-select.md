# [01] SELECT basics
> **Track:** SQL · **Level:** 01 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

You have data in a table. Now you need to ask questions: "Who are my users?" "Which products cost more than $50?" "What are the top 10 most recent orders?" The `SELECT` statement is how you retrieve data — and it's the most used SQL command in existence.

## 2. Core concept (absolute zero)

### What does SELECT do?

`SELECT` retrieves data from a table. It's like asking the database a question.

```sql
SELECT columns FROM table WHERE condition ORDER BY column LIMIT count;
```

You can think of it as:
1. **FROM** — which table?
2. **WHERE** — which rows?
3. **SELECT** — which columns?
4. **ORDER BY** — in what order?
5. **LIMIT** — how many?

### Sample data for this lesson

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0
);

INSERT INTO products VALUES (1, 'Laptop', 'Electronics', 999.99, 5);
INSERT INTO products VALUES (2, 'Mouse', 'Electronics', 25.50, 50);
INSERT INTO products VALUES (3, 'Keyboard', 'Electronics', 75.00, 30);
INSERT INTO products VALUES (4, 'Notebook', 'Stationery', 3.99, 200);
INSERT INTO products VALUES (5, 'Pen', 'Stationery', 1.50, 500);
INSERT INTO products VALUES (6, 'Desk', 'Furniture', 299.00, 10);
INSERT INTO products VALUES (7, 'Chair', 'Furniture', 199.00, 15);
INSERT INTO products VALUES (8, 'Monitor', 'Electronics', 349.00, 8);
```

## 3. Step-by-step breakdown (examples)

### SELECT all columns

```sql
SELECT * FROM products;
```

`*` means "all columns".

```
id  name      category      price    stock
--  --------  ------------  -------  -----
1   Laptop    Electronics   999.99   5
2   Mouse     Electronics   25.5     50
3   Keyboard  Electronics   75.0     30
4   Notebook  Stationery    3.99     200
5   Pen       Stationery    1.5      500
6   Desk      Furniture     299.0    10
7   Chair     Furniture     199.0    15
8   Monitor   Electronics   349.0    8
```

### SELECT specific columns

```sql
SELECT name, price FROM products;
```

```
name      price
--------  -------
Laptop    999.99
Mouse     25.5
Keyboard  75.0
Notebook  3.99
Pen       1.5
Desk      299.0
Chair     199.0
Monitor   349.0
```

### WHERE — filtering rows

WHERE filters rows based on a condition.

```sql
SELECT name, price FROM products WHERE price < 50;
```

```
name     price
-------  -----
Mouse    25.5
Notebook 3.99
Pen      1.5
```

Comparison operators:

| Operator | Meaning |
|----------|---------|
| `=` | Equal |
| `<>` or `!=` | Not equal |
| `<` | Less than |
| `<=` | Less than or equal |
| `>` | Greater than |
| `>=` | Greater than or equal |

Text comparison:

```sql
SELECT * FROM products WHERE category = 'Electronics';
```

```
id  name      category      price    stock
--  --------  ------------  -------  -----
1   Laptop    Electronics   999.99   5
2   Mouse     Electronics   25.5     50
3   Keyboard  Electronics   75.0     30
8   Monitor   Electronics   349.0    8
```

### AND, OR, NOT

Combine conditions:

```sql
SELECT * FROM products WHERE category = 'Electronics' AND price < 100;
```

```
id  name      category      price    stock
--  --------  ------------  -------  -----
2   Mouse     Electronics   25.5     50
3   Keyboard  Electronics   75.0     30
```

```sql
SELECT * FROM products WHERE category = 'Furniture' OR price < 10;
```

```
id  name      category    price   stock
--  --------  ----------  ------  -----
4   Notebook  Stationery  3.99    200
5   Pen       Stationery  1.5     500
6   Desk      Furniture   299.0   10
7   Chair     Furniture   199.0   15
```

```sql
SELECT * FROM products WHERE NOT category = 'Electronics';
```

```
id  name      category    price   stock
--  --------  ----------  ------  -----
4   Notebook  Stationery  3.99    200
5   Pen       Stationery  1.5     500
6   Desk      Furniture   299.0   10
7   Chair     Furniture   199.0   15
```

### ORDER BY — sorting

```sql
SELECT name, price FROM products ORDER BY price;
```

```
name      price
--------  -------
Pen       1.5
Notebook  3.99
Mouse     25.5
Keyboard  75.0
Chair     199.0
Desk      299.0
Monitor   349.0
Laptop    999.99
```

Ascending (`ASC`) is default:

```sql
SELECT name, price FROM products ORDER BY price ASC;   -- same as above
SELECT name, price FROM products ORDER BY price DESC;  -- descending
```

```
name      price
--------  -------
Laptop    999.99
Monitor   349.0
Desk      299.0
Chair     199.0
Keyboard  75.0
Mouse     25.5
Notebook  3.99
Pen       1.5
```

Sort by multiple columns:

```sql
SELECT name, category, price FROM products ORDER BY category, price DESC;
```

```
name      category      price
--------  ------------  -------
Monitor   Electronics   349.0
Laptop    999.99        999.99
Keyboard  Electronics   75.0
Mouse     Electronics   25.5
Desk      Furniture     299.0
Chair     Furniture     199.0
Notebook  Stationery    3.99
Pen       Stationery    1.5
```

### LIMIT and OFFSET

Limit the number of rows returned:

```sql
SELECT name, price FROM products ORDER BY price DESC LIMIT 3;
```

```
name    price
------  -------
Laptop  999.99
Monitor 349.0
Desk    299.0
```

Skip rows with OFFSET:

```sql
SELECT name, price FROM products ORDER BY price DESC LIMIT 3 OFFSET 3;
```

```
name    price
------  -------
Chair   199.0
Keyboard 75.0
Mouse   25.5
```

(3rd-5th most expensive)

Short syntax: `LIMIT 3 OFFSET 3` = `LIMIT 3, 3` (MySQL), but SQLite uses the first form.

### DISTINCT — unique values

Remove duplicates from results:

```sql
SELECT DISTINCT category FROM products;
```

```
category
-----------
Electronics
Stationery
Furniture
```

With multiple columns:

```sql
SELECT DISTINCT category, price FROM products;
```

(Each unique combination of category and price)

### Aliases — AS

Rename columns or tables for readability:

```sql
SELECT name AS product_name, price AS retail_price FROM products;
```

```
product_name  retail_price
-----------  -------------
Laptop        999.99
Mouse         25.5
Keyboard      75.0
Notebook      3.99
Pen           1.5
Desk          299.0
Chair         199.0
Monitor       349.0
```

Alias with spaces (use quotes):

```sql
SELECT name AS "Product Name", price AS "Price (USD)" FROM products;
```

Table aliases:

```sql
SELECT p.name, p.price FROM products AS p WHERE p.price > 100;
```

### Comments in SQL

```sql
-- This is a single-line comment
SELECT * FROM products;  -- inline comment

/*
   This is a
   multi-line comment
*/
SELECT * FROM products;
```

### Combining everything

```sql
-- Find the cheapest furniture item in stock
SELECT name, price
FROM products
WHERE category = 'Furniture'
  AND stock > 0
ORDER BY price
LIMIT 1;
```

```
name   price
-----  -----
Chair  199.0
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `WHERE price = '50'` | Comparing a numeric column to a string | `WHERE price = 50` |
| `WHERE name = Alice` (no quotes) | SQL thinks Alice is a column name | `WHERE name = 'Alice'` |
| `WHERE price BETWEEN 10, 20` | Wrong syntax for BETWEEN | `WHERE price BETWEEN 10 AND 20` |
| `SELECT * WHERE price > 10` | Missing FROM clause | `SELECT * FROM products WHERE price > 10` |
| `ORDER BY price DISC` | Typo: DESC not DISC | `ORDER BY price DESC` |
| `LIMIT 5, 10` expecting first 5 | SQLite uses `LIMIT 5 OFFSET 10` | `LIMIT 5 OFFSET 10` |
| `SELECT name, price AS cost WHERE ...` | Can't use alias in WHERE | Use original column name in WHERE |

## 5. Exercises

Use the `products` table from this lesson.

1. Select all products with `SELECT * FROM products;`.
2. Select only product names and stock.
3. Find all products in the 'Stationery' category.
4. Find all products with price less than 100.
5. Find all products with price between 50 and 500.
6. Find all Electronics with stock greater than 10.
7. List products sorted by stock (highest first).
8. List the top 3 most expensive products.
9. List all distinct categories.
10. Find the cheapest product in the Furniture category.
11. Use an alias to rename `price` to `cost` in the output.
12. Write a query that returns products where category is NOT Electronics and price is under 50, ordered by name.

## 6. Self-check questions

1. What does `SELECT * FROM products;` return?
2. How do you filter rows based on a condition?
3. What is the difference between `=` and `<>` in SQL?
4. How do you sort results in descending order?
5. What does `LIMIT 5 OFFSET 10` return?
6. What does `DISTINCT` do?
7. What is the purpose of `AS` in a SELECT statement?
8. How do you write a single-line comment in SQL?
9. Can you use column aliases in a WHERE clause? Why or why not?
10. What's the difference between `AND` and `OR` in WHERE conditions?

## 7. What's next

You can retrieve and filter data with SELECT. In **Level 02**, you'll learn to **modify data** — inserting new records with `INSERT`, updating existing data with `UPDATE`, deleting rows with `DELETE`, and using **transactions** to safely group operations.
