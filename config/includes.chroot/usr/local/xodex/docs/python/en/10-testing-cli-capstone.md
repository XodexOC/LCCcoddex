# [10] Testing, CLI Tools & Capstone
> **Track:** Python · **Level:** 10 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

You now know enough Python to write substantial programs. But how do you know
they work correctly for all inputs? How do you make your programs usable from
the terminal with proper command-line arguments? And how do you structure a
complete project that others can install and run?

This capstone lesson answers all three questions:
- **Testing** with `pytest` — automated checks that your code works
- **`argparse`** — building professional command-line interfaces
- **Practical standard library** — `datetime`, `re` (regex basics),
  `collections` (Counter, defaultdict)
- **Packaging basics** — `pyproject.toml`
- **Capstone project** — a complete CLI tool: read a file, process data,
  write output

---

## 2. Core concept

### 2.1 Why test?

Manual testing is slow and unreliable. Automated tests let you:
- Verify code works after every change
- Catch regressions (old features breaking when you add new ones)
- Document expected behavior
- Refactor with confidence

### 2.2 `pytest`

`pytest` is the most popular testing framework for Python. Tests are functions
whose names start with `test_`. You use plain `assert` statements.

### 2.3 `argparse`

`argparse` is the standard library module for parsing command-line arguments.
It generates help text, handles type conversion, and validates input.

### 2.4 Capstone mindset

A complete tool follows this pattern:
1. Accept input (file path, arguments)
2. Process data (parse, transform, analyze)
3. Produce output (stdout, file, report)

---

## 3. Step-by-step breakdown

### Step 1: Install pytest

```bash
pip install pytest
```

Create a file `test_example.py`:

```python
# test_example.py
def test_addition():
    assert 2 + 2 == 4

def test_string():
    assert "hello".upper() == "HELLO"
```

Run tests:
```bash
pytest
```

Output:
```
collected 2 items
test_example.py .. [100%]
```

### Step 2: `assert` and test organization

Group tests in a class (optional):

```python
class TestMath:
    def test_add(self):
        assert 1 + 1 == 2

    def test_subtract(self):
        assert 5 - 3 == 2
```

### Step 3: `pytest` fixtures with `tmp_path`

`tmp_path` is a built-in fixture that gives you a temporary directory:

```python
def test_write_and_read(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    f = d / "hello.txt"
    f.write_text("Hello, world!")
    assert f.read_text() == "Hello, world!"
```

### Step 4: `pytest.mark.parametrize`

Test a function with multiple inputs:

```python
import pytest

def is_even(n):
    return n % 2 == 0

@pytest.mark.parametrize("n,expected", [
    (2, True),
    (3, False),
    (0, True),
    (-2, True),
    (-3, False),
])
def test_is_even(n, expected):
    assert is_even(n) == expected
```

### Step 5: `argparse` basics

```python
# greet.py
import argparse

parser = argparse.ArgumentParser(description="Greet someone.")
parser.add_argument("name", help="The person to greet")
parser.add_argument("--greeting", default="Hello", help="Custom greeting")
parser.add_argument("--count", type=int, default=1, help="How many times")

args = parser.parse_args()

for _ in range(args.count):
    print(f"{args.greeting}, {args.name}!")
```

Usage:
```bash
$ python greet.py Alice --greeting Hi --count 3
Hi, Alice!
Hi, Alice!
Hi, Alice!
```

### Step 6: `datetime` module

```python
from datetime import datetime, date, timedelta

# Current date and time
now = datetime.now()
today = date.today()

print(now.year, now.month, now.day)   # 2026 7 23

# Formatting
print(now.strftime("%Y-%m-%d %H:%M:%S"))   # 2026-07-23 14:30:00

# Parsing
dt = datetime.strptime("2026-07-23", "%Y-%m-%d")

# Arithmetic
yesterday = today - timedelta(days=1)
print(yesterday)
```

### Step 7: `re` (regex) basics

Regular expressions match patterns in text.

```python
import re

# Search — returns first match
match = re.search(r"\d+", "Order #42: 3 items")
if match:
    print(match.group())   # 42

# Find all
nums = re.findall(r"\d+", "a1 b2 c3 d4")
print(nums)   # ['1', '2', '3', '4']

# Split
parts = re.split(r"[,\s]+", "apple,banana cherry,date")
print(parts)  # ['apple', 'banana', 'cherry', 'date']

# Substitution
result = re.sub(r"\d+", "NUM", "Item 1: 5 dollars")
print(result)  # "Item NUM: NUM dollars"

# Common patterns
# \d+     — one or more digits
# \w+     — one or more word chars (letters, digits, underscore)
# \s+     — one or more whitespace chars
# [abc]   — any of a, b, or c
# ^       — start of string
# $       — end of string
```

### Step 8: `collections.Counter`

Counter counts hashable items:

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(words)
print(counts)               # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(counts["apple"])      # 3
print(counts.most_common(2)) # [('apple', 3), ('banana', 2)]

# Counter from a string
letter_counts = Counter("hello world")
print(letter_counts)  # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
```

### Step 9: `collections.defaultdict`

A dict that provides a default value for missing keys:

```python
from collections import defaultdict

# Group items by their first letter
words = ["apple", "apricot", "banana", "cherry", "blueberry"]
groups = defaultdict(list)

for word in words:
    first = word[0]
    groups[first].append(word)

print(dict(groups))
# {'a': ['apple', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}

# Without defaultdict you would need:
# groups = {}
# for word in words:
#     first = word[0]
#     if first not in groups:
#         groups[first] = []
#     groups[first].append(word)
```

### Step 10: Building the capstone — word frequency tool

Let's build a complete CLI tool: `wordfreq.py` — reads a text file, counts
word frequencies, and writes results.

```python
#!/usr/bin/env python3
"""
wordfreq.py — Count word frequencies in a text file.

Usage:
    python wordfreq.py input.txt -o output.csv -n 10
"""

import argparse
import re
import csv
from collections import Counter


def get_words(text: str) -> list[str]:
    """Extract lowercase words from text."""
    return re.findall(r"\w+", text.lower())


def count_words(words: list[str]) -> Counter:
    """Count word frequencies."""
    return Counter(words)


def write_csv(word_counts: Counter, filepath: str, top_n: int | None = None):
    """Write word counts to a CSV file."""
    items = word_counts.most_common(top_n)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(items)


def main():
    parser = argparse.ArgumentParser(
        description="Count word frequencies in a text file."
    )
    parser.add_argument("input", help="Path to input text file")
    parser.add_argument("-o", "--output", default="frequencies.csv",
                        help="Output CSV file (default: frequencies.csv)")
    parser.add_argument("-n", type=int, default=None,
                        help="Only show top N words")

    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: file '{args.input}' not found.")
        raise SystemExit(1)

    words = get_words(text)
    counts = count_words(words)
    write_csv(counts, args.output, args.n)

    print(f"Processed {len(words)} words ({len(counts)} unique).")
    print(f"Output written to {args.output}")


if __name__ == "__main__":
    main()
```

### Step 11: Testing the capstone

```python
# test_wordfreq.py
import pytest
from wordfreq import get_words, count_words
from collections import Counter


def test_get_words_basic():
    result = get_words("Hello, World! Hello.")
    assert result == ["hello", "world", "hello"]


def test_get_words_empty():
    assert get_words("") == []


def test_get_words_punctuation():
    result = get_words("Don't stop! #python")
    assert result == ["don", "t", "stop", "python"]


def test_count_words():
    words = ["a", "b", "a", "c", "a", "b"]
    result = count_words(words)
    assert result == Counter({"a": 3, "b": 2, "c": 1})


def test_count_words_empty():
    assert count_words([]) == Counter()


@pytest.mark.parametrize("text,expected_count", [
    ("one one two", 2),
    ("hello hello hello", 1),
    ("", 0),
])
def test_get_words_unique_count(text, expected_count):
    words = get_words(text)
    assert len(set(words)) == expected_count
```

### Step 12: `pyproject.toml` basics

A minimal `pyproject.toml` for your tool:

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "wordfreq"
version = "0.1.0"
description = "Count word frequencies in text files"
authors = [
    {name = "Xodex User", email = "user@xodex.com"}
]
requires-python = ">=3.10"

[project.scripts]
wordfreq = "wordfreq:main"
```

After creating this file, install your tool in editable mode:
```bash
pip install -e .
```

Now you can run `wordfreq` from anywhere:
```bash
wordfreq input.txt -o results.csv -n 20
```

---

## 4. Common mistakes

### Not isolating tests
Tests should not depend on each other. Each test should set up its own data.

### Using `tmp_path` incorrectly
Always use the `tmp_path` fixture — do not hardcode temporary paths.

### Forgetting `__name__ == "__main__"` guard
Without it, running the script directly does nothing if `main()` isn't called.

### Over-complicating regex
Start simple. `r"\w+"` covers most word-extraction needs.

### Testing implementation, not behavior
Test what a function *does*, not how it does it. That way you can refactor
without breaking tests.

### Overusing Counter/ defaultdict
Standard dicts with `dict.get(key, default)` work fine for simple cases.

---

## 5. Exercises

1. **Test a function** — Write a function `is_palindrome(s: str) -> bool` that
   ignores case and spaces. Write 5 parametrized tests for it.

2. **CLI calculator** — Use `argparse` to build a calculator that takes
   `--add`, `--subtract`, `--multiply`, `--divide` with two numbers.

3. **Date arithmetic** — Write a script that accepts a date string
   (`--date "2026-07-23"`) and prints the date 30 days later and 30 days
   earlier.

4. **Log parser** — Given a log file with lines like
   `[2026-07-23 10:30:00] ERROR: Something broke`, use `re` to extract all
   timestamps and error messages. Write them to a CSV.

5. **Defaultdict practice** — Given a list of tuples
   `[("fruit", "apple"), ("fruit", "banana"), ("color", "red"), ("fruit", "cherry")]`,
   use `defaultdict` to group items by category. Print the result.

6. **Test with tmp_path** — Write a function `save_greeting(name, path)` that
   writes `"Hello, {name}!"` to a file. Write a test using `tmp_path` to
   verify the file content.

7. **Extend the capstone** — Add an option `--min-length` to filter out words
   shorter than a given length. Add a test. Update the CLI.

8. **Package it** — Create a `pyproject.toml` for the wordfreq tool. Install
   it with `pip install -e .` and run it from any directory.

---

## 6. Self-check questions

1. Why should you write automated tests?
2. What does `pytest.mark.parametrize` do?
3. What is the `tmp_path` fixture for?
4. How does `argparse` generate help text?
5. What is the difference between a positional argument and an optional
   argument in `argparse`?
6. How do you capture the current date and time with `datetime`?
7. What does `re.findall(r"\d+", text)` return?
8. What is `Counter` and what does `.most_common(5)` return?
9. What is `defaultdict` and when would you use it?
10. What is the purpose of `pyproject.toml`?

---

## 7. What's next

Congratulations — you have completed the Python track!

You have built a complete, tested CLI tool and learned professional practices:
- Automated testing with `pytest` (fixtures, parametrize)
- Command-line interfaces with `argparse`
- Practical modules: `datetime`, `re`, `collections`
- Packaging basics with `pyproject.toml`
- A complete capstone project from start to finish

You now possess a solid foundation in Python. From here you can explore:

- **GUIs** — Tkinter, PyQt, or web frameworks (Flask, FastAPI)
- **Data science** — NumPy, Pandas, Matplotlib
- **Advanced Python** — Decorators, generators, async/await, context managers
- **Databases** — SQLite, SQLAlchemy
- **DevOps** — Docker, CI/CD, deployment

Keep coding. Every expert was once a beginner who refused to give up.
