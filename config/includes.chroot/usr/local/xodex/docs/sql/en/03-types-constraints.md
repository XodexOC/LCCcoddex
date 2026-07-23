# [03] Types and constraints
> **Track:** SQL · **Level:** 03 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

A database isn't just a place to throw data — it needs rules. What kind of data goes in each column? Can a value be empty? Must values be unique? How do you connect tables? These rules are called **constraints**, and they protect your data from being corrupted by invalid entries.

## 2. Core concept (absolute zero)

### Data types

Every column has a **type** that defines what kind of data it can hold.

SQLite's five storage classes:

| Type | Meaning | Examples |
|------|---------|---------|
| `INTEGER` | Whole number | 42, -5, 0 |
| `REAL` | Floating-point number | 3.14, -0.001 |
| `TEXT` | String of text | 'hello', 'Alice' |
| `BLOB` | Binary data (image, file) | (raw bytes) |
| `NULL` | No value | NULL |

Other databases have more types (e.g., PostgreSQL has `DATE`, `TIMESTAMP`, `BOOLEAN`, `JSON`), but SQLite uses these five internally with type affinities.

### Constraints

Constraints enforce rules on the data:

| Constraint | What it does |
|-----------|-------------|
| `NOT NULL` | Column cannot be empty (must have a value) |
| `UNIQUE` | Every value in this column must be different |
| `PRIMARY KEY` | Unique identifier for each row (implies NOT NULL + UNIQUE) |
| `FOREIGN KEY` | Value must exist in another table's column |
| `DEFAULT` | Value to use if none is provided |
| `CHECK` | Values must satisfy a condition |

## 3. Step-by-step breakdown (examples)

### Creating a table with constraints

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,           -- unique ID, auto-incrementing
    name TEXT NOT NULL,                -- must have a name
    email TEXT NOT NULL UNIQUE,        -- must be unique, cannot be null
    age INTEGER CHECK (age >= 0),      -- age must be 0 or more
    grade TEXT DEFAULT 'Freshman',     -- defaults to 'Freshman'
    enrollment_date TEXT DEFAULT (date('now'))  -- defaults to today
);
```

Explanation:

| Column | Constraint | Effect |
|--------|-----------|--------|
| `id` | `PRIMARY KEY` | Each row gets a unique ID; can never be NULL |
| `name` | `NOT NULL` | You can't insert a student without a name |
| `email` | `NOT NULL UNIQUE` | Email is required AND no two students can share one |
| `age` | `CHECK (age >= 0)` | Prevents negative ages |
| `grade` | `DEFAULT 'Freshman'` | If you omit grade, it defaults to Freshman |
| `enrollment_date` | `DEFAULT (date('now'))` | Defaults to the current date |

### PRIMARY KEY and AUTOINCREMENT

Every table should have a primary key. In SQLite, `INTEGER PRIMARY KEY` auto-increments:

```sql
INSERT INTO students (name, email) VALUES ('Alice', 'alice@school.edu');
INSERT INTO students (name, email) VALUES ('Bob', 'bob@school.edu');

SELECT * FROM students;
```

```
id  name   email              age  grade     enrollment_date
--  -----  -----------------  ---  --------  ---------------
1   Alice  alice@school.edu   NULL Freshman  2026-07-23
2   Bob    bob@school.edu     NULL Freshman  2026-07-23
```

With `AUTOINCREMENT` (explicit):

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
);
```

`AUTOINCREMENT` guarantees IDs never reuse numbers, even deleted ones. Without it, SQLite may reuse IDs. For most cases, plain `INTEGER PRIMARY KEY` is fine.

### NOT NULL in action

```sql
-- This will FAIL: name is required
INSERT INTO students (email) VALUES ('no-name@school.edu');
-- Error: NOT NULL constraint failed: students.name
```

### UNIQUE in action

```sql
-- This will FAIL: duplicate email
INSERT INTO students (name, email) VALUES ('Charlie', 'alice@school.edu');
-- Error: UNIQUE constraint failed: students.email
```

### CHECK in action

```sql
-- This will FAIL: age cannot be negative
INSERT INTO students (name, email, age) VALUES ('Charlie', 'charlie@school.edu', -5);
-- Error: CHECK constraint failed: students.age
```

### DEFAULT in action

```sql
INSERT INTO students (name, email, age) VALUES ('Diana', 'diana@school.edu', 22);
SELECT name, grade FROM students WHERE name = 'Diana';
-- grade is 'Freshman' (the default)
```

### FOREIGN KEY ... REFERENCES

Foreign keys link tables together. They ensure **referential integrity** — you can't reference a row that doesn't exist.

```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    instructor TEXT
);

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

Enable foreign keys in SQLite (off by default):

```sql
PRAGMA foreign_keys = ON;
```

```sql
INSERT INTO courses VALUES (1, 'SQL 101', 'Prof. Smith');
INSERT INTO courses VALUES (2, 'Linux Basics', 'Prof. Jones');

-- Valid: references existing students and courses
INSERT INTO enrollments (student_id, course_id) VALUES (1, 1);
INSERT INTO enrollments (student_id, course_id) VALUES (1, 2);
INSERT INTO enrollments (student_id, course_id) VALUES (2, 1);

-- This will FAIL: student_id 999 doesn't exist
INSERT INTO enrollments (student_id, course_id) VALUES (999, 1);
-- Error: FOREIGN KEY constraint failed
```

Foreign key actions: what happens when the referenced row is deleted or updated?

```sql
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
```

- `ON DELETE CASCADE` — if a student is deleted, their enrollments are also deleted
- `ON DELETE SET NULL` — set the foreign key to NULL
- `ON DELETE RESTRICT` — prevent deletion if references exist
- `ON DELETE NO ACTION` — do nothing (default)

### ALTER TABLE — modifying table structure

SQLite supports limited ALTER TABLE operations.

**Add a column:**

```sql
ALTER TABLE students ADD COLUMN phone TEXT;
```

**Rename a column** (SQLite 3.25+):

```sql
ALTER TABLE students RENAME COLUMN grade TO year;
```

**Rename a table:**

```sql
ALTER TABLE students RENAME TO pupils;
```

SQLite does NOT support `DROP COLUMN` or `ALTER COLUMN` directly. You'd need to recreate the table.

### Putting it all together

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    year INTEGER CHECK (year > 1400),  -- printing press era
    pages INTEGER CHECK (pages > 0),
    price REAL DEFAULT 0.00,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
);

INSERT INTO authors (name, email) VALUES ('Jane Austen', 'jane@austen.com');
INSERT INTO authors (name, email) VALUES ('George Orwell', 'george@orwell.com');

INSERT INTO books (title, author_id, year, pages, price) VALUES
    ('Pride and Prejudice', 1, 1813, 432, 9.99),
    ('Emma', 1, 1815, 474, 11.99),
    ('1984', 2, 1949, 328, 10.99),
    ('Animal Farm', 2, 1945, 112, 7.99);

-- This fails: year must be > 1400
INSERT INTO books (title, author_id, year) VALUES ('Bad Book', 1, 1300);

-- This fails: author_id 999 doesn't exist
INSERT INTO books (title, author_id, year, pages) VALUES ('Ghost Book', 999, 2000, 100);

-- This succeeds
SELECT * FROM books;
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Forgetting `PRAGMA foreign_keys = ON` | Foreign key constraints are silently ignored | Enable at start of session |
| `CHECK(price >= 0)` without column name | Valid but confusing | `price REAL CHECK (price >= 0)` |
| Inserting a string into an INTEGER column | SQLite is flexible but PostgreSQL will reject it | Match data to column type |
| `FOREIGN KEY (col) REFERENCES table` without `(col)` | Must specify the referenced column | `REFERENCES table(id)` |
| Using `AUTOINCREMENT` when not needed | Wastes a few bytes; usually unnecessary | Use plain `INTEGER PRIMARY KEY` |
| `ALTER TABLE ... DROP COLUMN` | Not supported in SQLite | Recreate the table |

## 5. Exercises

1. Create a table `movies` with: `id INTEGER PRIMARY KEY`, `title TEXT NOT NULL`, `year INTEGER CHECK (year > 1888)`, `rating REAL DEFAULT 0.0`.
2. Create a table `actors` with: `id INTEGER PRIMARY KEY`, `name TEXT NOT NULL UNIQUE`, `birth_year INTEGER`.
3. Create a table `cast_members` with foreign keys to `movies` and `actors`, and a `character_name TEXT`.
4. Enable foreign keys with `PRAGMA foreign_keys = ON`.
5. Insert 3 movies and 3 actors.
6. Insert cast_members linking actors to movies.
7. Try inserting a cast_member with an invalid movie_id — what happens?
8. Add a `genre` column to `movies` with `ALTER TABLE`.
9. Try inserting a movie with year 1000 — what happens?
10. Insert a movie without specifying rating — what default value does it get?
11. Try inserting a duplicate actor name — what happens?
12. Rename the `rating` column to `score` (if your SQLite supports it).

## 6. Self-check questions

1. What are the five storage classes in SQLite?
2. What does `NOT NULL` guarantee?
3. What does `UNIQUE` guarantee?
4. What is a PRIMARY KEY? Can a table have more than one?
5. What does a FOREIGN KEY constraint do?
6. What is the purpose of `ON DELETE CASCADE`?
7. How do you give a column a default value?
8. What does `CHECK` do?
9. How do you add a new column to an existing table?
10. Why might `AUTOINCREMENT` not be necessary?

## 7. What's next

You can design tables with proper types and constraints. In **Level 04**, you'll learn about **JOINs** — the heart of relational databases — to combine data from multiple tables using `INNER JOIN`, `LEFT JOIN`, and more.
