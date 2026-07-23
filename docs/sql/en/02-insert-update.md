# [02] INSERT / UPDATE / DELETE
> **Track:** SQL · **Level:** 02 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Databases aren't just for reading — you need to add new data, change existing data, and remove data you no longer need. These operations (Create, Update, Delete) are the other three parts of CRUD (Create, Read, Update, Delete). Without them, your database is read-only.

## 2. Core concept (absolute zero)

### The three modification commands

| Command | Purpose |
|---------|---------|
| `INSERT` | Add new rows to a table |
| `UPDATE` | Modify existing rows |
| `DELETE` | Remove rows |

**Critical rule**: `UPDATE` and `DELETE` without a `WHERE` clause affect **ALL rows** in the table. Always double-check your WHERE before running these.

### Transactions

A **transaction** groups one or more operations into a single unit. Either **all** the operations succeed, or **none** of them do. This is called **atomicity**.

```sql
BEGIN;       -- start transaction
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;      -- save changes
-- or
ROLLBACK;    -- undo all changes since BEGIN
```

## 3. Step-by-step breakdown (examples)

### Sample table

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL,
    hired DATE
);

INSERT INTO employees VALUES (1, 'Alice', 'Engineering', 85000, '2022-03-15');
INSERT INTO employees VALUES (2, 'Bob', 'Marketing', 65000, '2021-07-01');
INSERT INTO employees VALUES (3, 'Carol', 'Engineering', 92000, '2023-01-10');
INSERT INTO employees VALUES (4, 'Dave', 'Sales', 55000, '2020-11-20');
INSERT INTO employees VALUES (5, 'Eve', 'Marketing', 72000, '2022-06-05');
```

### INSERT INTO ... VALUES

Insert a single row:

```sql
INSERT INTO employees (name, department, salary, hired)
VALUES ('Frank', 'Engineering', 78000, '2024-02-01');
```

If you omit columns, you must provide values for ALL columns in order:

```sql
INSERT INTO employees VALUES (7, 'Grace', 'Sales', 59000, '2024-03-15');
```

But always prefer specifying columns — it's clearer and more robust:

```sql
INSERT INTO employees (name, department, salary)
VALUES ('Hank', 'Marketing', 68000);
```

(`hired` will be NULL)

Insert multiple rows at once:

```sql
INSERT INTO employees (name, department, salary, hired) VALUES
    ('Ivy', 'Engineering', 81000, '2023-09-01'),
    ('Jack', 'Sales', 62000, '2024-01-15'),
    ('Kate', 'Marketing', 70000, '2023-11-01');
```

### INSERT INTO ... SELECT

Insert data from another table or query:

```sql
CREATE TABLE engineering_team (
    id INTEGER PRIMARY KEY,
    name TEXT,
    salary REAL
);

INSERT INTO engineering_team (name, salary)
SELECT name, salary FROM employees WHERE department = 'Engineering';
```

### UPDATE ... SET ... WHERE

Update a single column:

```sql
UPDATE employees SET salary = 90000 WHERE name = 'Bob';
```

Update multiple columns:

```sql
UPDATE employees
SET salary = 95000, department = 'Engineering'
WHERE name = 'Alice';
```

Increase everyone's salary by 10% (with condition):

```sql
UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Engineering';
```

**Danger**: This updates ALL rows:

```sql
UPDATE employees SET salary = 50000;  -- ALL salaries are now 50000!
```

Always test with SELECT first:

```sql
-- First: check what will be updated
SELECT * FROM employees WHERE department = 'Engineering';

-- Then: run the UPDATE with the same WHERE
UPDATE employees SET salary = salary * 1.10 WHERE department = 'Engineering';
```

### DELETE FROM ... WHERE

Delete a specific row:

```sql
DELETE FROM employees WHERE name = 'Dave';
```

Delete by condition:

```sql
DELETE FROM employees WHERE department = 'Sales' AND salary < 60000;
```

**Danger**: This deletes ALL rows:

```sql
DELETE FROM employees;  -- table is now empty!
```

### Transactions in practice

Without transactions, if a power failure happens between two updates, you can end up with inconsistent data.

```sql
-- Transfer $500 from Alice to Bob

BEGIN;

UPDATE employees SET salary = salary - 500 WHERE name = 'Alice';
-- What if the server crashes here? Alice lost $500, Bob never got it.

UPDATE employees SET salary = salary + 500 WHERE name = 'Bob';

COMMIT;
```

With a transaction, if the crash happens, the database automatically rolls back Alice's deduction. Either both happen, or neither happens.

### Rollback example

```sql
BEGIN;

DELETE FROM employees WHERE department = 'Marketing';
-- Oops, I didn't mean to do that!

ROLLBACK;
-- Everything is back to normal
```

### Savepoints (advanced but useful)

You can set savepoints within a transaction and roll back to them:

```sql
BEGIN;
UPDATE employees SET salary = 100000 WHERE name = 'Alice';
SAVEPOINT alice_updated;

UPDATE employees SET salary = 100000 WHERE name = 'Bob';
-- Actually, Bob doesn't deserve that
ROLLBACK TO SAVEPOINT alice_updated;

COMMIT;
-- Only Alice's salary was changed
```

### Putting it all together

```sql
-- 1. Create a new hire
INSERT INTO employees (name, department, salary, hired)
VALUES ('Mia', 'Engineering', 87000, '2024-06-01');

-- 2. Give her a signing bonus
UPDATE employees SET salary = salary + 5000 WHERE name = 'Mia';

-- 3. Remove old employee who left
DELETE FROM employees WHERE name = 'Eve' AND department = 'Marketing';

-- 4. Verify the changes
SELECT * FROM employees ORDER BY name;
```

### Using SELECT to verify before modifications

```sql
-- Before DELETE, check which rows match
SELECT * FROM employees WHERE salary < 50000;

-- Safe DELETE
DELETE FROM employees WHERE salary < 50000;

-- Before UPDATE, preview the new values
SELECT name, salary, salary * 1.15 AS new_salary
FROM employees WHERE department = 'Engineering';

-- Safe UPDATE
UPDATE employees SET salary = salary * 1.15 WHERE department = 'Engineering';
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `UPDATE employees SET salary = 100000` without WHERE | Updates every row to the same salary | Always add a WHERE clause |
| `DELETE FROM employees` without WHERE | Deletes all rows | Filter with WHERE |
| Forgetting `BEGIN` before transaction | Each statement is auto-committed | `BEGIN; ... COMMIT;` |
| `INSERT INTO VALUES ('Alice')` without column list | Unclear which column gets 'Alice' | `INSERT INTO table (name) VALUES ('Alice')` |
| `UPDATE SET price = '50'` on a numeric column | String works but wrong type | `UPDATE SET price = 50` |
| `DELETE FROM employees WHERE salary = NULL` | NULL comparison needs IS, not = | `WHERE salary IS NULL` |

## 5. Exercises

Use the `employees` table.

1. Insert a new employee named 'Nina', 'Engineering', 83000, hired '2024-07-01'.
2. Insert two more employees in a single INSERT statement.
3. Update Bob's department to 'Engineering'.
4. Give all Sales employees a 5% raise.
5. Delete the employee named 'Dave'.
6. Delete all employees hired before 2021.
7. Start a transaction, insert a new employee, then rollback. Verify it wasn't added.
8. Insert a new employee using INSERT INTO ... SELECT (copy from yourself).
9. Update Carol's salary to 100000 and her department to 'Lead Engineering' in one statement.
10. Delete all employees who earn less than 60000.
11. Use SELECT to preview before running a 20% salary increase for Engineering.
12. Count employees before and after a DELETE to verify.

## 6. Self-check questions

1. What happens if you run `UPDATE employees SET salary = 0` without WHERE?
2. What happens if you run `DELETE FROM employees` without WHERE?
3. How do you insert multiple rows in one statement?
4. What is a transaction and why is it important?
5. What is the difference between `COMMIT` and `ROLLBACK`?
6. How do you copy data from one table to another?
7. Why should you always specify columns in an INSERT statement?
8. Can you use `DELETE FROM employees WHERE salary = NULL`? Why not?
9. How do you preview what an UPDATE will change before running it?
10. What happens to auto-committed statements if you don't use BEGIN/COMMIT?

## 7. What's next

You can create, read, update, and delete data. In **Level 03**, you'll learn about **data types and constraints** — how to define the structure of your tables with `INTEGER`, `TEXT`, `NOT NULL`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `DEFAULT`, and `ALTER TABLE`.
