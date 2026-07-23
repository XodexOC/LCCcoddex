# [08] Modules, Packages & Virtual Environments
> **Track:** Python · **Level:** 08 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

A single file works for tiny programs, but real projects grow to hundreds or
thousands of lines. You need to split code across multiple files. You also need
to use code written by other people (libraries). And you must manage
dependencies so different projects don't conflict with each other.

In this lesson you will learn:
- **`import`** — using the standard library and third-party modules
- **`from ... import ...`** — selective imports
- Creating your **own module** — a `.py` file you import
- **`if __name__ == '__main__'`** — making files runnable and importable
- **`sys` module** — `sys.argv`, `sys.path`, `sys.exit()`
- **`os` module** — `os.path`, `os.listdir`, `os.system`
- **`subprocess`** — running shell commands and capturing output
- **`pip`** — installing third-party packages
- **Virtual environments** — isolating project dependencies
- **`requirements.txt`** — listing your project's dependencies

---

## 2. Core concept

### 2.1 What is a module?

A **module** is any `.py` file. The filename (minus `.py`) becomes the module
name. You can `import` it and use its contents.

Python ships with a large **standard library** — hundreds of built-in modules
(`os`, `sys`, `json`, `csv`, `math`, `random`, `datetime`, etc.).

### 2.2 What is a package?

A **package** is a directory containing a special `__init__.py` file (often
empty) and other modules. It gives you a hierarchical namespace:

```python
import os.path        # os is a package, path is a module
```

### 2.3 What is a virtual environment?

A **virtual environment** is an isolated Python installation for one project.
Each project gets its own `site-packages` directory where `pip` installs
libraries. This prevents version conflicts between projects.

### 2.4 `pip`

`pip` is Python's package installer. It downloads packages from PyPI (the
Python Package Index) and installs them into your environment.

### 2.5 `requirements.txt`

A plain text file listing all packages your project needs. Anyone can install
them with `pip install -r requirements.txt`.

---

## 3. Step-by-step breakdown

### Step 1: Importing the standard library

```python
import math
import random
import datetime

print(math.sqrt(16))        # 4.0
print(random.randint(1, 6))  # random die roll
print(datetime.date.today()) # today's date
```

### Step 2: `from ... import ...`

```python
from math import sqrt, pi
print(sqrt(25))   # 5.0
print(pi)         # 3.141592653589793
```

Import everything (usually discouraged — pollutes namespace):

```python
from math import *    # brings in all math names
```

### Step 3: Creating your own module

Create `greetings.py`:
```python
def hello(name):
    return f"Hello, {name}!"

def bye(name):
    return f"Goodbye, {name}!"
```

Create `main.py` in the same directory:
```python
import greetings

print(greetings.hello("Alice"))
print(greetings.bye("Bob"))
```

### Step 4: `if __name__ == '__main__'`

When you `import` a module, Python runs it top-to-bottom. Sometimes you want
code that runs **only** when you execute the file directly, not when imported.

```python
# greetings.py
def hello(name):
    return f"Hello, {name}!"

def bye(name):
    return f"Goodbye, {name}!"

if __name__ == "__main__":
    # This block runs ONLY when you run: python greetings.py
    print(hello("World"))
    print(bye("World"))
```

When imported, `__name__` is `"greetings"`. When run directly, `__name__` is
`"__main__"`.

### Step 5: `sys` module

```python
import sys

# Command-line arguments
print(sys.argv)          # ['script.py', 'arg1', 'arg2']

# Python path (where imports are searched)
print(sys.path)          # list of directories

# Exit the program
sys.exit(0)              # 0 = success, non-zero = error

# Python version
print(sys.version)
```

### Step 6: `os` module

```python
import os

# Current directory
print(os.getcwd())

# List files in a directory
for item in os.listdir("."):
    print(item)

# Path manipulations
print(os.path.join("folder", "sub", "file.txt"))
print(os.path.exists("data.txt"))
print(os.path.isfile("data.txt"))
print(os.path.isdir("data/"))

# Environment variables
print(os.environ.get("HOME"))

# Run a command (simple — prefer subprocess for real use)
os.system("echo Hello from shell")
```

### Step 7: `subprocess` module

Better than `os.system()` for running commands:

```python
import subprocess

# Run and capture output
result = subprocess.run(
    ["echo", "Hello", "World"],
    capture_output=True,
    text=True,
)
print(result.stdout)    # "Hello World\n"

# Check return code
result = subprocess.run(["ls", "nonexistent"], capture_output=True, text=True)
print(result.returncode)   # 2
print(result.stderr)       # error message
```

### Step 8: `pip`

```bash
# Install a package
pip install requests

# Install a specific version
pip install requests==2.31.0

# Install latest compatible
pip install "requests>=2.0"

# List installed packages
pip list

# Show info about a package
pip show requests

# Uninstall
pip uninstall requests
```

### Step 9: Virtual environments

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it (Linux/macOS)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Once activated, pip installs into this environment
pip install requests

# Deactivate
deactivate
```

Always activate the venv before working on your project. Your prompt usually
changes to show `(venv)`.

### Step 10: `requirements.txt`

Freeze your dependencies:

```bash
# Generate requirements.txt from current environment
pip freeze > requirements.txt
```

Example `requirements.txt`:
```
requests==2.31.0
click==8.1.7
pytest==8.0.0
```

Install from it:
```bash
pip install -r requirements.txt
```

### Step 11: The `__pycache__` directory

When you import a module, Python compiles it to bytecode and stores it in a
`__pycache__` directory. This speeds up subsequent imports. You can safely
ignore/delete these directories.

### Step 12: Putting it all together — a mini project

```
my_project/
├── main.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── requirements.txt
```

`utils/__init__.py` (can be empty):
```python
# This file makes "utils" a package
```

`utils/helpers.py`:
```python
def add(x, y):
    return x + y
```

`main.py`:
```python
from utils.helpers import add
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <x> <y>")
        sys.exit(1)
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    print(f"{x} + {y} = {add(x, y)}")

if __name__ == "__main__":
    main()
```

---

## 4. Common mistakes

### Module name conflicts with standard library
```python
# Don't name your file random.py — it shadows the stdlib random module
```

### Forgetting `__init__.py` in packages
Before Python 3.3, `__init__.py` was required for a directory to be importable.
Python 3.3+ has **implicit namespace packages**, but it is still best practice
to include `__init__.py`.

### Running `pip` without activating the venv
```bash
# ❌ installs globally or into wrong venv
pip install requests

# ✅ activate first
source venv/bin/activate
pip install requests
```

### Not using `if __name__ == '__main__'`
Without it, test code inside your module runs when anyone imports it.

### Importing with circular dependencies
Module A imports Module B, Module B imports Module A → can cause errors.

### Committing `venv/` to git
Add `venv/` to `.gitignore`. Only commit `requirements.txt`.

---

## 5. Exercises

1. **Standard library** — Write a script that:
   - Generates 10 random numbers between 1 and 100
   - Computes their mean (use `statistics.mean`)
   - Prints the date and time of execution

2. **Custom module** — Create `math_utils.py` with functions `add`, `subtract`,
   `multiply`, `divide`. Create `main.py` that imports it and runs a simple
   calculator from the command line.

3. **`if __name__`** — Add the guard to `math_utils.py`. Add a test section
   that runs only when you execute the file directly.

4. **`sys.argv`** — Write a script that accepts two numbers as command-line
   arguments and prints their sum. Handle the case where arguments are missing.

5. **`os` module** — Write a script that lists all `.txt` files in the current
   directory using `os.listdir()`.

6. **`subprocess`** — Write a script that runs `ls -la` (or `dir` on Windows)
   and prints the output.

7. **Virtual environment** — Create a new directory, set up a venv, activate it,
   install a package (e.g., `requests`), freeze requirements, then deactivate.

8. **Project structure** — Create a package `shapes/` with modules `circle.py`
   (area, circumference) and `rectangle.py` (area, perimeter). Create a
   `main.py` that imports both and demonstrates usage.

---

## 6. Self-check questions

1. What is the difference between `import math` and `from math import sqrt`?
2. What is the purpose of `if __name__ == '__main__'`?
3. What does `sys.argv` contain?
4. What is the difference between `os.system()` and `subprocess.run()`?
5. How do you create a virtual environment?
6. How do you activate/deactivate a virtual environment?
7. What file lists a project's dependencies?
8. What is the purpose of `__init__.py`?
9. What does `pip freeze` do?
10. Why should you not commit `venv/` to version control?

---

## 7. What's next

You now know how to organize code across files, use the standard library,
install third-party packages, and manage environments. You have learned:
- `import`, `from ... import ...`, custom modules
- `if __name__ == '__main__'`
- `sys`, `os`, `subprocess` modules
- `pip`, virtual environments, `requirements.txt`

In **Level 09** you will learn about **Object-Oriented Programming (OOP)** —
defining your own types with `class`, inheritance, properties, dunder methods,
and dataclasses.

Close this lesson and open `09-oop.md`.
