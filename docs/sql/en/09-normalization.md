# [09] Normalization
> **Track:** SQL · **Level:** 09 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

Bad database design leads to **duplicated data**, **update anomalies** (changing one value but missing another copy), **insert anomalies** (can't add data because other required data is missing), and **delete anomalies** (deleting one thing accidentally deletes something else). **Normalization** is a systematic way to design schemas that avoid these problems.

## 2. Core concept (absolute zero)

### What is normalization?

Normalization is the process of organizing a database to reduce redundancy and improve data integrity. It's done through a series of "normal forms" (NF).

### The normal forms

| Form | Rule |
|------|------|
| **1NF** | Atomic values, no repeating groups |
| **2NF** | 1NF + no partial dependencies |
| **3NF** | 2NF + no transitive dependencies |
| **BCNF** | 3NF + every determinant is a candidate key |
| 4NF | Multivalued dependencies |
| 5NF | Join dependencies |

In practice, **3NF** is usually sufficient for most applications.

### The problem: unnormalized data

```sql
CREATE TABLE orders_bad (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    customer_city TEXT,
    product1 TEXT,
    product1_qty INTEGER,
    product2 TEXT,
    product2_qty INTEGER,
    product3 TEXT,
    product3_qty INTEGER
);
```

Problems:
- Limited number of products per order (3 max)
- Customer info repeated for every order
- If customer changes city, must update ALL their orders
- If customer has no orders, we can't store their info

## 3. Step-by-step breakdown (examples)

### First Normal Form (1NF)

**Rule**: Each column must contain atomic (indivisible) values. No repeating groups or arrays.

**Bad (not 1NF)**:

```sql
CREATE TABLE student_courses_bad (
    student_id INTEGER,
    student_name TEXT,
    courses TEXT       -- "Math,Physics,Chemistry"  <- NOT atomic!
);
```

**Good (1NF)**:

```sql
CREATE TABLE student_courses_1nf (
    student_id INTEGER,
    student_name TEXT,
    course TEXT,
    PRIMARY KEY (student_id, course)
);
```

**Another example — repeating columns (bad)**:

```sql
-- BAD: repeating columns for multiple phone numbers
CREATE TABLE contacts_bad (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone1 TEXT,
    phone2 TEXT,
    phone3 TEXT
);
```

**Good (1NF):**

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE phones (
    id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    phone TEXT,
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);
```

### A complete normalization example

Let's normalize a denormalized design step by step.

**Starting point (unnormalized)**:

```
Order(OrderID, Date, CustomerName, CustomerEmail,
      Product1, Qty1, Price1, Product2, Qty2, Price2)
```

This has:
- Repeating groups (Product1/2, Qty1/2, Price1/2)
- Customer info mixed with order data
- Product info mixed with order data

### Step 1: Convert to 1NF

Remove repeating groups by creating separate rows.

```sql
CREATE TABLE order_items_1nf (
    order_id INTEGER,
    date TEXT,
    customer_name TEXT,
    customer_email TEXT,
    product TEXT,
    quantity INTEGER,
    price REAL,
    PRIMARY KEY (order_id, product)
);
```

Now each product is a separate row. This is 1NF but still has problems.

### Step 2: Convert to 2NF

**Rule**: Must be in 1NF AND all non-key columns must depend on the **entire** primary key (no partial dependencies).

Our current PK is `(order_id, product)`. Which columns depend on only part of the key?

- `date`, `customer_name`, `customer_email` depend only on `order_id` (partial dependency)
- `quantity`, `price` depend on both `order_id` AND `product` (full dependency)

To fix: split into separate tables.

```sql
-- Orders table
CREATE TABLE orders_2nf (
    id INTEGER PRIMARY KEY,
    date TEXT,
    customer_name TEXT,
    customer_email TEXT
);

-- Order items table
CREATE TABLE order_items_2nf (
    order_id INTEGER,
    product TEXT,
    quantity INTEGER,
    price REAL,
    PRIMARY KEY (order_id, product),
    FOREIGN KEY (order_id) REFERENCES orders_2nf(id)
);
```

Now 2NF is satisfied. But we still have **transitive dependencies**.

### Step 3: Convert to 3NF

**Rule**: Must be in 2NF AND no non-key column depends on another non-key column (no transitive dependencies).

In `orders_2nf`: `customer_name` and `customer_email` depend on `id` directly. But what if multiple orders share the same customer? We have redundancy.

Also, if `customer_name` -> `customer_email` (same customer always has same email), then `customer_email` transitively depends on `customer_name`, which is not the key.

Fix: extract customer into its own table.

```sql
-- Customers table
CREATE TABLE customers_3nf (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Orders table
CREATE TABLE orders_3nf (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers_3nf(id)
);

-- Products table
CREATE TABLE products_3nf (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price REAL
);

-- Order items (junction table)
CREATE TABLE order_items_3nf (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders_3nf(id),
    FOREIGN KEY (product_id) REFERENCES products_3nf(id)
);
```

### Why 3NF is good

**Before normalization (bad)**:

```sql
INSERT INTO orders_bad VALUES
(1, 'Alice', 'alice@example.com', 'New York',
 'Laptop', 1, 999.99, 'Mouse', 2, 25.50, NULL, NULL, NULL);
```

**Problems**:
- **Update anomaly**: If Alice moves to Boston, we must update ALL her orders
- **Insert anomaly**: Can't add a new customer without an order
- **Delete anomaly**: If Alice cancels her only order, we lose her data

**After normalization (good)**:

```sql
INSERT INTO customers VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO orders VALUES (1, 1, '2026-01-15');
INSERT INTO order_items VALUES (1, 1, 1);  -- 1 Laptop
INSERT INTO order_items VALUES (1, 2, 2);  -- 2 Mice
```

- **Update anomaly fixed**: Change Alice's city in ONE place (customers table)
- **Insert anomaly fixed**: Add a customer without an order
- **Delete anomaly fixed**: Deleting an order doesn't delete the customer

### Denormalization (when and why)

Sometimes you deliberately break normalization rules for **performance**. This is called **denormalization**.

**When to denormalize**:
- Read-heavy workloads (lots of SELECT, few writes)
- Reporting/analytics queries that need to avoid JOINs
- Caching computed values (e.g., `order_total` stored on order)

**Example**: Instead of computing `order_total` by joining and summing every time:

```sql
-- Normalized: compute on the fly
SELECT o.id, SUM(oi.quantity * p.price) AS total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY o.id;

-- Denormalized: store the total directly
ALTER TABLE orders ADD COLUMN total REAL;
-- Update it when order items change
```

**Trade-off**: Faster reads, but you must keep the denormalized value in sync (risk of inconsistency).

### Real-world schema design example

Let's design a blog database in 3NF.

```sql
-- Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Posts
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    published_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- Categories
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Many-to-many: posts <-> categories
CREATE TABLE post_categories (
    post_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (post_id, category_id),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Comments
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);
```

**Why this is 3NF**:
- Each table represents a single entity
- No repeating groups (1NF)
- No partial dependencies (2NF)
- No transitive dependencies (3NF)
- Foreign keys maintain referential integrity

### Checking normalization

Ask these questions about your schema:

1. **1NF**: Are all columns atomic? No arrays or comma-separated lists?
2. **2NF**: Does every non-key column depend on the whole primary key?
3. **3NF**: Does every non-key column depend ONLY on the primary key (and not on other non-key columns)?

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Storing multiple values in one column | Violates 1NF, hard to query | Separate table or separate rows |
| Repeating columns (phone1, phone2) | Violates 1NF, limited capacity | Separate phones table |
| Storing customer info in orders table | Update anomaly — change in one place | Separate customers table |
| Not using junction tables for many-to-many | Need to store multiple values per row | post_categories table |
| Over-normalizing (every column its own table) | Queries become too complex with many JOINs | Stop at 3NF or BCNF |
| Denormalizing without a plan | Data inconsistency, update anomalies | Only denormalize for measured performance reasons |

## 5. Exercises

1. Take this table and identify why it violates 1NF: `students(id, name, courses)` where courses is "Math,Physics".
2. Convert it to 1NF.
3. Take this table and identify the partial dependency: `enrollments(student_id, course_id, student_name, course_name, grade)`.
4. Convert it to 2NF.
5. Take this table and identify the transitive dependency: `employees(id, name, department_id, department_name, department_location)`.
6. Convert it to 3NF.
7. Design a library database (books, authors, members, loans) in 3NF.
8. Identify the anomalies in: `sales(sale_id, customer_name, customer_phone, product1, qty1, product2, qty2)`.
9. Normalize the sales table to 3NF.
10. Explain the update, insert, and delete anomalies in the unnormalized orders table.
11. When would you consider denormalizing a 3NF schema?
12. Normalize this: `orders(id, customer_name, customer_email, shipping_address, product_name, product_category, quantity, price_per_unit)`.

## 6. Self-check questions

1. What is the purpose of normalization?
2. What does 1NF require?
3. What is a partial dependency and which normal form removes it?
4. What is a transitive dependency and which normal form removes it?
5. What is an update anomaly?
6. What is an insert anomaly?
7. What is a delete anomaly?
8. What is a junction table and when do you need one?
9. What is denormalization and when is it appropriate?
10. What are the trade-offs of normalization?

## 7. What's next

You can design clean, normalized database schemas. In **Level 10**, the final level, you'll complete a **capstone project** — importing CSV data, cleaning and normalizing it, writing analytical queries, and presenting your findings.
