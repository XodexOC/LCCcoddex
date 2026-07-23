# [00] Why SQL?
> **Track:** SQL · **Level:** 00 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Every application needs to store data — user accounts, products, orders, messages. You could store data in plain text files, but that quickly becomes messy: how do you search for a specific record? How do you handle multiple users writing at the same time? How do you ensure data is consistent? SQL databases solve all of this by providing a structured, reliable way to store and query data.

## 2. Core concept (absolute zero)

### What is a database?

A **database** is an organized collection of data. Think of it as a digital filing cabinet.

### What is a relational database?

Data is stored in **tables** (like spreadsheets). Each table has:

- **Columns** — named fields (like "name", "email", "age")
- **Rows** — individual records (one per entry)
- **Schema** — the structure that defines what columns and types exist

Example table: `users`

| id | name | email | age |
|----|------|-------|-----|
| 1 | Alice | alice@example.com | 25 |
| 2 | Bob | bob@example.com | 30 |
| 3 | Carol | carol@example.com | 28 |

### What is SQL?

**SQL** (Structured Query Language, pronounced "sequel" or "S-Q-L") is the language used to communicate with relational databases. It's **declarative** — you say WHAT you want, not HOW to get it.

```sql
SELECT name, email FROM users WHERE age > 25;
```

This returns: "Bob" and "Carol" — you don't need to tell the database how to search, just what to find.

### SQL vs NoSQL

- **SQL databases**: PostgreSQL, MySQL, SQLite — structured, strict schema, ACID compliant
- **NoSQL databases**: MongoDB, Redis, Cassandra — flexible schema, often faster for specific use cases

### SQLite vs PostgreSQL vs MySQL

| Feature | SQLite | PostgreSQL | MySQL |
|---------|--------|------------|-------|
| Setup | No server needed, file-based | Full client-server | Full client-server |
| Best for | Learning, embedded, small apps | Production, complex queries | Web apps, WordPress |
| Features | Minimal, great for learning | Advanced (window functions, CTEs, JSON) | Good balance |
| Concurrency | Single writer | Many concurrent writers | Many concurrent writers |

For this course we use **SQLite** — it's the simplest to start with.

## 3. Step-by-step breakdown (examples)

### Installing SQLite

```
alice@xodex:~$ sudo apt install sqlite3
```

Check installation:

```
alice@xodex:~$ sqlite3 --version
3.40.1 2022-12-28 14:03:47
```

### Opening sqlite3

```
alice@xodex:~$ sqlite3
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
sqlite>
```

To open (or create) a database file:

```
alice@xodex:~$ sqlite3 xodex.db
SQLite version 3.40.1
sqlite>
```

### Dot commands (meta-commands)

SQLite has special commands that start with a dot:

```
sqlite> .tables          -- list all tables
sqlite> .schema          -- show CREATE TABLE statements for all tables
sqlite> .schema users    -- show schema of specific table
sqlite> .databases       -- list attached databases
sqlite> .help            -- list all dot commands
sqlite> .mode column     -- pretty-print output in columns
sqlite> .headers on      -- show column headers
sqlite> .quit            -- exit sqlite3
```

### First query: SELECT 1;

```sql
sqlite> SELECT 1;
1
```

```sql
sqlite> SELECT 1 + 1;
2
```

```sql
sqlite> SELECT 'Hello, SQL!';
Hello, SQL!
```

SELECT is used to ask for data. Even without a table, you can compute values.

### Creating a table: CREATE TABLE

```sql
sqlite> CREATE TABLE users (
   ...>     id INTEGER PRIMARY KEY,
   ...>     name TEXT NOT NULL,
   ...>     email TEXT NOT NULL,
   ...>     age INTEGER
   ...> );
```

Check what we created:

```sql
sqlite> .tables
users

sqlite> .schema users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
);
```

### Inserting data: INSERT INTO

```sql
sqlite> INSERT INTO users (name, email, age) VALUES ('Alice', 'alice@example.com', 25);
sqlite> INSERT INTO users (name, email, age) VALUES ('Bob', 'bob@example.com', 30);
sqlite> INSERT INTO users (name, email, age) VALUES ('Carol', 'carol@example.com', 28);
```

### Querying data: SELECT

```sql
sqlite> .headers on
sqlite> .mode column

sqlite> SELECT * FROM users;
id  name   email              age
--  -----  -----------------  ---
1   Alice  alice@example.com  25
2   Bob    bob@example.com    30
3   Carol  carol@example.com  28
```

```sql
sqlite> SELECT name, age FROM users;
name   age
-----  ---
Alice  25
Bob    30
Carol  28
```

```sql
sqlite> SELECT name FROM users WHERE age > 26;
name
-----
Bob
Carol
```

### A second table

```sql
sqlite> CREATE TABLE posts (
   ...>     id INTEGER PRIMARY KEY,
   ...>     title TEXT NOT NULL,
   ...>     user_id INTEGER,
   ...>     FOREIGN KEY (user_id) REFERENCES users(id)
   ...> );

sqlite> INSERT INTO posts (title, user_id) VALUES ('Hello World', 1);
sqlite> INSERT INTO posts (title, user_id) VALUES ('Second Post', 1);
sqlite> INSERT INTO posts (title, user_id) VALUES ('My Journey', 2);

sqlite> SELECT * FROM posts;
id  title         user_id
--  ------------  -------
1   Hello World   1
2   Second Post   1
3   My Journey    2
```

### Exiting

```sql
sqlite> .quit
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Forgetting semicolon `;` at the end of SQL | SQL statement never executes, prompt continues with `...>` | Always end SQL with `;` |
| `SELECT * FORM users` (typo) | Misspelling `FROM` as `FORM` | `SELECT * FROM users` |
| Not using `.headers on` | Output may be confusing | Run `.headers on` before queries |
| Inserting text without quotes | SQL thinks it's a column name or keyword | `INSERT ... VALUES ('text', ...)` |
| Closing sqlite3 with `exit` instead of `.quit` | `exit` works in many shells but `.quit` is the SQLite way | `.quit` or `Ctrl+D` |
| Creating a table without defining a PRIMARY KEY | SQLite will add a hidden `rowid` but it's better to be explicit | Always define a PRIMARY KEY |

## 5. Exercises

1. Install SQLite: `sudo apt install sqlite3` (or your system's equivalent).
2. Open SQLite: `sqlite3 test.db`.
3. Run `.tables`. What do you see (should be empty)?
4. Run `SELECT 'Learning SQL!';`.
5. Create a table called `books` with columns: `id INTEGER PRIMARY KEY`, `title TEXT`, `author TEXT`, `year INTEGER`.
6. Insert 3 books into the table.
7. Query all books with `SELECT * FROM books;`.
8. Use `.headers on` and `.mode column` for pretty output.
9. Query just the titles of books published after 2020.
10. Create a second table called `readers` with `id`, `name`, `email`.
11. Insert 2 readers.
12. Run `.schema` to see all table definitions.

## 6. Self-check questions

1. What is a database table? How is it structured?
2. What does SQL stand for? Is it procedural or declarative?
3. What is the difference between SQLite and PostgreSQL?
4. What SQL command is used to create a new table?
5. What SQL command is used to insert data?
6. How do you see all tables in a SQLite database?
7. Why must SQL statements end with a semicolon?
8. What does `SELECT 1 + 1;` return?
9. What is a PRIMARY KEY used for?
10. What does `.schema` do in SQLite?

## 7. What's next

You've written your first SQL queries. In **Level 01**, you'll master **SELECT** — learning how to filter, sort, limit, and shape your data with `WHERE`, `ORDER BY`, `DISTINCT`, aliases, and more.
