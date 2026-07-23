# Урок 01: SELECT

```sql
-- Все строки
SELECT * FROM students;

-- С условием
SELECT name FROM students WHERE language = 'C';

-- Сортировка
SELECT name, language FROM students ORDER BY language;

-- Агрегация
SELECT language, COUNT(*) FROM students GROUP BY language;
```
