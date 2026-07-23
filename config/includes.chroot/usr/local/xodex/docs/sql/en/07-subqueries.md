# [07] Subqueries
> **Track:** SQL · **Level:** 07 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

Sometimes you need to answer a question that depends on another question. "Which employees earn more than the average salary?" requires first computing the average, then comparing each employee. **Subqueries** — queries inside queries — let you do this in a single SQL statement.

## 2. Core concept (absolute zero)

### What is a subquery?

A **subquery** (or inner query) is a `SELECT` statement nested inside another SQL statement. The outer query uses the subquery's result.

```sql
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

The subquery `(SELECT AVG(salary) FROM employees)` runs first, produces a single value (e.g., 70250), and the outer query uses it.

### Where subqueries can appear

| Location | Example |
|----------|---------|
| `WHERE` clause | `WHERE x IN (SELECT ...)` |
| `FROM` clause (derived table) | `FROM (SELECT ...) AS t` |
| `SELECT` clause (scalar subquery) | `SELECT (SELECT ...) AS val` |
| `HAVING` clause | `HAVING COUNT(*) > (SELECT ...)` |
| `EXISTS` | `WHERE EXISTS (SELECT ...)` |

### Correlated vs non-correlated

- **Non-correlated**: subquery runs once, independently
- **Correlated**: subquery references the outer query, runs once per outer row

## 3. Step-by-step breakdown (examples)

### Sample data

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL,
    manager_id INTEGER
);

INSERT INTO employees VALUES
    (1, 'Alice', 'Engineering', 95000, NULL),
    (2, 'Bob', 'Engineering', 72000, 1),
    (3, 'Carol', 'Engineering', 68000, 1),
    (4, 'Dave', 'Marketing', 65000, NULL),
    (5, 'Eve', 'Marketing', 55000, 4),
    (6, 'Frank', 'Sales', 80000, NULL),
    (7, 'Grace', 'Sales', 45000, 6),
    (8, 'Hank', 'Sales', 42000, 6),
    (9, 'Ivy', 'Engineering', 110000, 1);

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    budget REAL
);

INSERT INTO departments VALUES
    (1, 'Engineering', 500000),
    (2, 'Marketing', 200000),
    (3, 'Sales', 300000);
```

### Subquery in WHERE with IN

Find employees in departments with a budget over $250,000:

```sql
SELECT name, department
FROM employees
WHERE department IN (
    SELECT name FROM departments WHERE budget > 250000
);
```

```
name   department
-----  ------------
Alice  Engineering
Bob    Engineering
Carol  Engineering
Frank  Sales
Grace  Sales
Hank   Sales
Ivy    Engineering
```

The subquery returns `('Engineering', 'Sales')`, then the outer query uses `IN`.

### Subquery in WHERE with comparison

Find employees who earn more than the average salary:

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

```
name   salary
-----  ------
Alice  95000
Frank  80000
Ivy    110000
```

### Subquery in FROM (derived table)

Use a subquery as a virtual table. Must have an alias.

Find average salary per department, then find departments above the overall average:

```sql
SELECT dept_avg.department, dept_avg.avg_salary
FROM (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_avg
WHERE dept_avg.avg_salary > (SELECT AVG(salary) FROM employees);
```

```
department    avg_salary
------------  ----------
Engineering   86250.0
```

Top earner per department:

```sql
SELECT e.name, e.department, e.salary
FROM employees e
INNER JOIN (
    SELECT department, MAX(salary) AS max_salary
    FROM employees
    GROUP BY department
) m ON e.department = m.department AND e.salary = m.max_salary;
```

```
name   department    salary
-----  ------------  ------
Ivy    Engineering   110000
Dave   Marketing     65000
Frank  Sales         80000
```

### Subquery in SELECT (scalar subquery)

A subquery that returns a single value can be used as a column:

```sql
SELECT
    name,
    salary,
    (SELECT AVG(salary) FROM employees) AS company_avg,
    salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

```
name   salary   company_avg   diff_from_avg
-----  -------  -----------  --------------
Alice  95000    70250.0       24750.0
Bob    72000    70250.0       1750.0
Carol  68000    70250.0       -2250.0
Dave   65000    70250.0       -5250.0
Eve    55000    70250.0       -15250.0
Frank  80000    70250.0       9750.0
Grace  45000    70250.0       -25250.0
Hank   42000    70250.0       -28250.0
Ivy    110000   70250.0       39750.0
```

### EXISTS and NOT EXISTS

`EXISTS` returns `TRUE` if the subquery returns any rows.

Find departments that have at least one employee:

```sql
SELECT name
FROM departments d
WHERE EXISTS (
    SELECT 1 FROM employees e WHERE e.department = d.name
);
```

```
name
-----------
Engineering
Marketing
Sales
```

Find departments with NO employees:

```sql
SELECT name
FROM departments d
WHERE NOT EXISTS (
    SELECT 1 FROM employees e WHERE e.department = d.name
);
```

(No results — all departments have employees.)

`EXISTS` is often faster than `IN` for large datasets because it can stop at the first match.

### Correlated subqueries

A **correlated subquery** references columns from the outer query. It runs once for each row in the outer query.

Find employees who earn more than the average in their own department:

```sql
SELECT e1.name, e1.department, e1.salary
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department = e1.department
);
```

```
name   department    salary
-----  ------------  ------
Alice  Engineering   95000
Ivy    Engineering   110000
Frank  Sales         80000
```

For each employee:
1. The subquery computes the average salary for `e1.department`
2. The outer query checks if `e1.salary` > that average

### ANY and ALL

`ANY` — true if the comparison is true for ANY subquery result:

```sql
SELECT name, salary
FROM employees
WHERE salary > ANY (
    SELECT salary FROM employees WHERE department = 'Marketing'
);
```

Marketing salaries: 65000, 55000. "More than ANY" means more than the minimum (55000).

```
name   salary
-----  ------
Alice  95000
Bob    72000
Carol  68000
Dave   65000
Frank  80000
Ivy    110000
(Grace 45000 and Hank 42000 excluded)
```

`ALL` — true if the comparison is true for ALL subquery results:

```sql
SELECT name, salary
FROM employees
WHERE salary > ALL (
    SELECT salary FROM employees WHERE department = 'Marketing'
);
```

"More than ALL" means more than the maximum Marketing salary (65000).

```
name   salary
-----  ------
Alice  95000
Bob    72000
Carol  68000
Frank  80000
Ivy    110000
```

### Subquery with EXISTS: find employees who manage someone

```sql
SELECT name
FROM employees e
WHERE EXISTS (
    SELECT 1 FROM employees sub WHERE sub.manager_id = e.id
);
```

```
name
-----
Alice
Dave
Frank
```

### Subquery in HAVING

Find departments where the max salary is more than double the min:

```sql
SELECT department, MAX(salary) AS max_sal, MIN(salary) AS min_sal
FROM employees
GROUP BY department
HAVING MAX(salary) > 2 * MIN(salary);
```

```
department  max_sal   min_sal
----------  --------  -------
Sales       80000     42000
```

### Putting it all together

Find the department with the highest average salary:

```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC
LIMIT 1;
```

Or using subqueries:

```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) = (
    SELECT MAX(dept_avg)
    FROM (
        SELECT AVG(salary) AS dept_avg
        FROM employees
        GROUP BY department
    )
);
```

```
department    avg_salary
------------  ----------
Engineering   86250.0
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Subquery returns multiple rows with `=` | Error: "subquery returns more than 1 row" | Use `IN` or `ANY` |
| Forgetting alias for subquery in FROM | Error: "subquery in FROM must have an alias" | `FROM (SELECT ...) AS t` |
| Correlated subquery without table alias | Column reference ambiguous | Use distinct aliases: `e1`, `e2` |
| `SELECT *` in EXISTS subquery | Valid but wasteful | `SELECT 1` |
| `NOT IN (SELECT ...)` with NULLs | NOT IN returns no rows if subquery has NULL | Use `NOT EXISTS` instead |
| Using subquery when JOIN would be clearer | Often slower, harder to read | Prefer JOIN when possible |

## 5. Exercises

1. Find employees who earn less than the average salary.
2. Find employees in departments whose budget is less than $250,000.
3. Use a subquery in FROM to find the average salary per department.
4. Use a scalar subquery in SELECT to show each employee's salary as a percentage of the company average.
5. Use EXISTS to find departments that have Engineering-level salaries (> 68000).
6. Use a correlated subquery to find employees who earn less than the average in their department.
7. Use ANY to find employees who earn more than at least one Engineering employee.
8. Use ALL to find employees who earn more than all Engineering employees.
9. Find employees who are managers (use EXISTS).
10. Find departments with no employees using NOT EXISTS.
11. Use a subquery in HAVING to find departments with above-average headcount.
12. Write a query that returns the highest-paid employee in each department using a subquery in FROM.

## 6. Self-check questions

1. What is the difference between a correlated and non-correlated subquery?
2. Where can subqueries appear in a SQL statement?
3. What operator should you use when a subquery returns multiple rows?
4. Why must a subquery in FROM have an alias?
5. What is the difference between `IN` and `EXISTS`?
6. When would you use `NOT EXISTS` instead of `NOT IN`?
7. What does `> ANY (SELECT ...)` mean?
8. What does `> ALL (SELECT ...)` mean?
9. Can you use a subquery in a SELECT clause? What must it return?
10. How does a correlated subquery differ from a regular subquery in terms of execution?

## 7. What's next

Subqueries give you powerful ways to combine queries. In **Level 08**, you'll learn about **CTEs (Common Table Expressions)** and **window functions** — `WITH`, `ROW_NUMBER()`, `RANK()`, `OVER`, `PARTITION BY` — for even more advanced querying.
