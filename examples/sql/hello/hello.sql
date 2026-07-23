-- hello.sql — Пример работы с SQLite
-- Запуск: sqlite3 :memory: < hello.sql

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    language TEXT NOT NULL
);

INSERT INTO students VALUES (1, 'Xodex', 'C');
INSERT INTO students VALUES (2, 'Xodex', 'Python');
INSERT INTO students VALUES (3, 'Xodex', 'Assembly');
INSERT INTO students VALUES (4, 'Xodex', 'SQL');

SELECT 'Hello, Xodex!' AS greeting;
SELECT name, language FROM students ORDER BY language;
