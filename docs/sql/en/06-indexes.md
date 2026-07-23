# [06] Indexes
> **Track:** SQL · **Level:** 06 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

As your database grows, queries get slower. Searching for one row in a million-row table requires scanning every row — that's slow. **Indexes** are data structures that speed up lookups dramatically, like the index at the back of a book: instead of reading every page, you jump directly to the right one.

## 2. Core concept (absolute zero)

### What is an index?

An **index** is a separate data structure (usually a B-tree) that stores a sorted copy of a column's values, mapped to their row locations. When you search by that column, the database uses the index to find the rows instantly.

### Book analogy

- Without an index: read every page until you find "SQL" (full table scan)
- With an index: look up "SQL" in the index, get page number 342, jump directly there

### Trade-offs

| Pros | Cons |
|------|------|
| Faster SELECT queries | Slower INSERT/UPDATE/DELETE (index must be updated) |
| Faster JOINs | Takes extra disk space |
| Faster ORDER BY and GROUP BY | Not all queries benefit |

## 3. Step-by-step breakdown (examples)

### Sample data

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    city TEXT,
    age INTEGER
);

-- Insert 1000 users (simulated)
-- In reality: millions
INSERT INTO users VALUES (1, 'alice', 'alice@example.com', 'New York', 25);
INSERT INTO users VALUES (2, 'bob', 'bob@example.com', 'London', 30);
-- ... imagine thousands more
```

### Without an index

Searching by email (assuming no index):

```sql
SELECT * FROM users WHERE email = 'alice@example.com';
```

Without an index, SQLite must scan **every row** — this is a "full table scan". With millions of rows, this is slow.

### CREATE INDEX

```sql
CREATE INDEX idx_users_email ON users(email);
```

Now the database maintains a sorted B-tree of emails:

```
Index: idx_users_email
-------------------------
'alice@example.com'   -> rowid 1
'an@example.com'      -> rowid 42
'bob@example.com'     -> rowid 2
...
```

Searching is now O(log n) instead of O(n).

### Creating indexes

Single-column index:

```sql
CREATE INDEX idx_users_city ON users(city);
```

Unique index (prevents duplicates AND speeds lookups):

```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
```

This is like a `UNIQUE` constraint but also creates an index.

Composite index (multiple columns):

```sql
CREATE INDEX idx_users_city_age ON users(city, age);
```

Order matters! This index helps queries that filter by `city`, or by `city AND age`, but NOT by `age` alone.

Covering index (includes all needed columns):

```sql
CREATE INDEX idx_users_covering ON users(city, age, username);
```

### When does an index help?

```sql
-- Exact match: YES
SELECT * FROM users WHERE email = 'alice@example.com';

-- Range query: YES
SELECT * FROM users WHERE age BETWEEN 20 AND 30;

-- ORDER BY on indexed column: YES
SELECT * FROM users ORDER BY email;

-- JOIN on indexed column: YES (huge improvement)
SELECT * FROM orders o JOIN users u ON o.user_id = u.id;
-- Index on users.id (already has PK index) and orders.user_id

-- Prefix match on composite index: YES
SELECT * FROM users WHERE city = 'New York' AND age > 25;

-- Column without leading index column: LIMIT
SELECT * FROM users WHERE age = 25;
-- (idx_users_city_age doesn't help here — city is first)
```

### When does an index NOT help?

```sql
-- Pattern with leading wildcard: NO
SELECT * FROM users WHERE email LIKE '%@example.com';

-- Small table: NO (full scan is faster)
-- High % of rows returned: NO (index overhead > scan)

-- Function on column: NO (unless function-based index)
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';
```

### EXPLAIN QUERY PLAN

See how SQLite executes a query:

```sql
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'alice@example.com';
```

Without index:

```
SEARCH TABLE users USING INTEGER PRIMARY KEY (rowid=?)
-- Actually for non-PK column without index:
SCAN TABLE users
```

With index:

```
SEARCH TABLE users USING INDEX idx_users_email (email=?)
```

Check if your query uses an index:

```sql
EXPLAIN QUERY PLAN
SELECT * FROM users
WHERE city = 'New York' AND age > 25
ORDER BY username;
```

### Primary key is automatically indexed

```sql
-- This query automatically uses the PK index (id)
SELECT * FROM users WHERE id = 42;
```

```sql
EXPLAIN QUERY PLAN SELECT * FROM users WHERE id = 42;
-- SEARCH TABLE users USING INTEGER PRIMARY KEY (rowid=?)
```

### Indexes on JOIN columns

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Index on the foreign key column (huge speedup for JOINs)
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

```sql
EXPLAIN QUERY PLAN
SELECT u.username, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.city = 'London';
```

### Dropping an index

```sql
DROP INDEX idx_users_email;
```

### Viewing all indexes

```sql
-- In SQLite
SELECT * FROM sqlite_master WHERE type = 'index';
```

Or with dot commands:

```
sqlite> .indexes
idx_users_email
idx_users_city
idx_users_city_age
```

### Performance test (demonstration)

```sql
-- Create a big table
CREATE TABLE big_data AS
SELECT value AS id, 'user_' || value AS name, abs(random() % 1000) AS group_id
FROM generate_series(1, 100000);

-- Slow query (no index)
EXPLAIN QUERY PLAN SELECT * FROM big_data WHERE group_id = 42;

-- Create index
CREATE INDEX idx_big_group ON big_data(group_id);

-- Fast query (with index)
EXPLAIN QUERY PLAN SELECT * FROM big_data WHERE group_id = 42;
```

(Note: `generate_series` may not exist in all SQLite versions. Use a loop or CSV import instead.)

### Practical index strategy

Not every column needs an index. Here's a decision guide:

1. **Primary keys**: automatically indexed — always
2. **Foreign keys**: almost always index them (JOIN performance)
3. **Columns in WHERE**: index columns you filter by frequently
4. **Columns in ORDER BY**: index helps sorting
5. **Columns in JOIN conditions**: essential for performance
6. **High-cardinality columns**: benefit more (e.g., email > gender)
7. **Small tables**: don't bother (full scan is fast enough)

```sql
-- A reasonable set of indexes for a typical app
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Indexing every column | Wastes disk space, slows writes | Index only columns used in WHERE/JOIN/ORDER BY |
| Composite index with wrong column order | Can't use index for queries missing the leading column | Put high-selectivity column first |
| Forgetting to index foreign keys | JOINs are slow | Always index FK columns |
| Indexing a boolean column | Low selectivity — index barely helps | Only index if you query the rare value often |
| Not running ANALYZE after creating index | Query planner may still choose full scan | Let the database update statistics |
| Index on a frequently updated column | Index maintenance overhead on every UPDATE | Consider whether the query benefit outweighs update cost |

## 5. Exercises

Use the `users` and `orders` tables (or create your own).

1. Create a table `products` with 1000 rows (use a loop or INSERT many rows).
2. Create an index on `products(name)`.
3. Use `EXPLAIN QUERY PLAN` to check if a SELECT by name uses the index.
4. Create a composite index on `products(category, price)`.
5. Check if `SELECT * FROM products WHERE category = 'Electronics'` uses the composite index.
6. Check if `SELECT * FROM products WHERE price > 50` uses the composite index (it shouldn't).
7. Create an index on a foreign key column.
8. Use `EXPLAIN QUERY PLAN` on a JOIN query with and without the FK index.
9. Drop an index and verify it's gone with `.indexes`.
10. Create a UNIQUE index and try to insert a duplicate value.
11. Show all indexes for a table using `SELECT * FROM sqlite_master WHERE type = 'index' AND tbl_name = 'table_name';`.
12. Measure the difference: create a table with 100k rows, query without index, create index, query again, compare EXPLAIN output.

## 6. Self-check questions

1. What problem do indexes solve?
2. How does a database use an index to find data faster?
3. What are the downsides of having too many indexes?
4. What type of queries benefit from indexes?
5. Why does a PRIMARY KEY automatically create an index?
6. In a composite index `(a, b)`, which queries can use it?
7. How do you see if a query is using an index?
8. What does `CREATE UNIQUE INDEX` do?
9. Why index foreign key columns?
10. When would an index NOT improve performance?

## 7. What's next

Indexes make your queries fast. In **Level 07**, you'll learn about **subqueries** — embedding one query inside another using `IN`, `EXISTS`, `ANY`, `ALL`, and subqueries in `SELECT` and `FROM` clauses.
