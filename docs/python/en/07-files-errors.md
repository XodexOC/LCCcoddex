# [07] Working with Files & Error Handling
> **Track:** Python · **Level:** 07 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

Programs need to **persist** data — save it between runs. If you write a to-do
app, the tasks should still be there tomorrow. Programs also need to read
existing data: configuration files, CSV spreadsheets, JSON APIs.

Real programs also **fail** — the user provides bad input, a file does not
exist, the network goes down. If you don't handle errors, the program crashes
with an ugly traceback. **Error handling** lets you respond gracefully.

In this lesson you will learn:
- Opening files with `open()` and different **modes** (`r`, `w`, `a`, `r+`)
- The **`with` statement** (context manager) for safe file handling
- Reading files: `read()`, `readline()`, `readlines()`, `for line in f`
- Writing files: `write()`, `writelines()`
- Working with **CSV** files using the `csv` module
- Working with **JSON** using `json.load()` / `json.dump()`
- **`try`/`except`/`else`/`finally`** for error handling
- **Raising** your own exceptions with `raise`
- Common exceptions: `FileNotFoundError`, `ValueError`, `TypeError`

---

## 2. Core concept

### 2.1 File modes

When you open a file, you specify the **mode** — what you want to do with it:

| Mode | What it does | File position |
|---|---|---|
| `"r"` | Read (default) | Start of file |
| `"w"` | Write — **overwrites** existing file | Start of file |
| `"a"` | Append — adds to end of file | End of file |
| `"r+"` | Read and write (no truncate) | Start of file |
| `"x"` | Exclusive creation — fails if file exists | Start |

Add `"b"` for binary mode (`"rb"`, `"wb"`) — use for images, audio, etc.

### 2.2 Context manager (`with`)

Always use `with` when opening files. It automatically closes the file when the
block ends — even if an error occurs.

```python
with open("file.txt", "r") as f:
    content = f.read()
# file is closed here automatically
```

### 2.3 Exceptions

An **exception** is an error that occurs during execution. When an exception
happens and is not handled, the program stops and prints a traceback.

Python's exception hierarchy is deep. Common ones:

| Exception | When it happens |
|---|---|
| `FileNotFoundError` | File does not exist |
| `ValueError` | Value is wrong (e.g., `int("abc")`) |
| `TypeError` | Wrong type (e.g., `"hello" + 5`) |
| `ZeroDivisionError` | Division by zero |
| `IndexError` | List index out of range |
| `KeyError` | Dict key not found |
| `PermissionError` | No permission to access a file |

---

## 3. Step-by-step breakdown

### Step 1: Opening and reading a file

```python
# read the entire file as one string
with open("hello.txt", "r") as f:
    content = f.read()
    print(content)
```

If `hello.txt` does not exist, Python raises `FileNotFoundError`.

### Step 2: Reading line by line

```python
# best for large files — only one line in memory at a time
with open("hello.txt", "r") as f:
    for line in f:          # f is an iterator of lines
        print(line, end="")  # end="" because lines already end with \n
```

### Step 3: `readline()` and `readlines()`

```python
with open("hello.txt", "r") as f:
    first_line = f.readline()   # reads one line (including \n)
    remaining = f.readlines()   # reads all remaining lines into a list
```

`readlines()` loads the entire file into memory — avoid for huge files.

### Step 4: Writing to a file

```python
with open("output.txt", "w") as f:
    f.write("Hello, world!\n")
    f.write("This is line 2.\n")
```

`"w"` overwrites the file if it exists. Use `"a"` to append instead:

```python
with open("output.txt", "a") as f:
    f.write("This line is appended.\n")
```

### Step 5: `writelines()`

Accepts an iterable of strings (note: no newlines added automatically):

```python
lines = ["line 1\n", "line 2\n", "line 3\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)
```

### Step 6: Reading and writing CSV

CSV (Comma-Separated Values) is a common data format.

```python
import csv

# Reading
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:          # each row is a list of strings
        print(row)

# Writing
data = [
    ["name", "age", "city"],
    ["Alice", "30", "NYC"],
    ["Bob", "25", "LA"],
]
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

**DictReader and DictWriter** — use the header row as keys:

```python
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

### Step 7: Reading and writing JSON

JSON (JavaScript Object Notation) stores structured data.

```python
import json

# Reading
with open("data.json", "r") as f:
    data = json.load(f)          # Python dict/list
    print(data["name"])

# Writing
person = {"name": "Alice", "age": 30, "city": "NYC"}
with open("data.json", "w") as f:
    json.dump(person, f, indent=2)   # indent for readability
```

**String versions:**

```python
json_str = json.dumps(person)        # Python → JSON string
person_again = json.loads(json_str)  # JSON string → Python
```

### Step 8: `try`/`except` basics

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(f"Result: {result}")
except ValueError:
    print("That wasn't a valid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Step 9: `else` and `finally`

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found.")
else:
    print("File read successfully.")   # runs only if no exception
finally:
    print("This always runs.")         # cleanup: close file, etc.
```

`else` runs if the `try` block completed without an exception.
`finally` runs **always** — even if there was a `return`, `break`, or exception.

### Step 10: `raise` — raising exceptions

Sometimes you need to signal that something is wrong:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")
```

**Re-raising:**

```python
try:
    process_data()
except ValueError:
    log_error()
    raise        # re-raise the same exception
```

### Step 11: Catching multiple exceptions

```python
try:
    x = int(input("x: "))
    y = int(input("y: "))
    result = x / y
except (ValueError, ZeroDivisionError) as e:
    print(f"Something went wrong: {e}")
```

### Step 12: Exception hierarchy and bare `except`

Avoid bare `except:` — it catches everything, including `KeyboardInterrupt`
(Ctrl+C) and `SystemExit`, making it impossible to stop your program.

```python
try:
    dangerous_operation()
except Exception:     # catches most "normal" errors
    handle_error()
```

Better: catch specific exceptions.

---

## 4. Common mistakes

### Forgetting to close a file (without `with`)
```python
f = open("data.txt", "r")
content = f.read()
# forgot f.close() — file stays open
```

Always use `with` — it closes automatically.

### Opening a file for writing accidentally overwrites it
```python
with open("important.txt", "w") as f:   # ❌ wipes the file!
    f.write("new content")
```

Use `"a"` to append, `"x"` to fail if file exists, or check first.

### Not handling `FileNotFoundError`
```python
with open("nope.txt", "r") as f:   # ❌ crash if file doesn't exist
    ...
```

### Reading a file twice
```python
with open("f.txt") as f:
    content = f.read()
    f.seek(0)          # reset to start if you need to read again
    # or just open once and reuse content
```

### Confusing `json.load` vs `json.loads`
- `json.load(f)` — reads from a file object
- `json.loads(s)` — reads from a string

### Silencing exceptions with bare `except`
```python
try:
    ...
except:     # ❌ hides all errors, including bugs
    pass
```

---

## 5. Exercises

1. **Write and read** — Write a program that creates a file `notes.txt`, writes
   three lines of text to it, then reads and prints the entire file.

2. **Word count** — Write a program that reads a text file and prints the
   number of lines, words, and characters.

3. **CSV gradebook** — Create a CSV file with columns `name`, `score`. Write
   5 students and their scores. Then read the CSV and compute the average
   score.

4. **JSON config** — Create a dict containing `{"theme": "dark", "language": "en",
   "volume": 75}`. Save it to `config.json`. Then write a program that reads
   `config.json` and prints each setting.

5. **Calculator with error handling** — Ask for two numbers and an operator
   (`+`, `-`, `*`, `/`). Handle `ValueError` (non-numeric input),
   `ZeroDivisionError`, and an unknown operator. Print a friendly error for
   each.

6. **Safe integer input** — Write a function `get_int(prompt)` that keeps
   asking until the user enters a valid integer. Use `try`/`except` and a
   `while` loop.

7. **Log file** — Write a program that tries to open a file. If it fails with
   `FileNotFoundError`, create the file and write "created" in it. Use
   `finally` to print "Operation complete."

8. **Custom exception** — Define a function `validate_age(age)` that raises
   `ValueError` if age is negative or over 150. Call it with invalid input
   and catch the exception.

---

## 6. Self-check questions

1. What does `with open(...) as f:` guarantee?
2. What is the difference between `"r"`, `"w"`, and `"a"` modes?
3. What happens if you open a non-existent file for reading?
4. How do you read a CSV file where the first row contains column names?
5. What is the difference between `json.load()` and `json.loads()`?
6. What is the purpose of `try`/`except`?
7. When does the `else` block in a `try` statement run?
8. When does the `finally` block run?
9. Why should you avoid a bare `except:`?
10. How do you raise an exception manually?

---

## 7. What's next

You can now persist data and handle errors professionally. You know:
- Opening files with `with` and `open()` in various modes
- Reading and writing text, CSV, and JSON
- `try`/`except`/`else`/`finally` for error handling
- `raise` for custom exceptions

In **Level 08** you will learn about **modules, packages, and virtual
environments** — organizing your code across files, importing third-party
libraries with `pip`, and isolating project dependencies.

Close this lesson and open `08-modules-venv.md`.
