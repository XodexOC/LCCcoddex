# Lesson 01: SELECT

```sql
-- All rows
SELECT * FROM students;

-- With condition
SELECT name FROM students WHERE language = 'C';

-- Sorting
SELECT name, language FROM students ORDER BY language;

-- Aggregation
SELECT language, COUNT(*) FROM students GROUP BY language;
```
