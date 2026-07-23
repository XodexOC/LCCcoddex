# [04] Loops & Iteration
> **Track:** Python · **Level:** 04 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Writing out the same action 100 times by hand is impossible. Programs need to
**repeat** actions — process every item in a list, count from 1 to 1,000, keep
asking until the user types the right answer.

**Loops** let you execute a block of code multiple times without copying and
pasting.

In this lesson you will learn:
- **`for` loop** over a `range()` of numbers
- **`for` loop** over a list of items
- **`enumerate()`** — getting both the index and the value
- **`zip()`** — iterating over multiple sequences in parallel
- **`while` loop** — repeat until a condition becomes false
- **`break`** — exit a loop early
- **`continue`** — skip to the next iteration
- **`else` clause** on loops — runs when the loop finishes normally
- Common loop patterns: accumulate, filter, transform

---

## 2. Core concept

### 2.1 What is iteration?

**Iteration** means visiting each element of a sequence, one by one. A **loop**
is the mechanism that performs iteration.

### 2.2 `for` loop

The `for` loop is the most common loop in Python. It iterates over any
**iterable** — something you can loop over (strings, lists, ranges, files...).

```python
for variable in iterable:
    # body — runs once for each element
```

At each iteration, the current element is assigned to `variable`, and the body
runs.

### 2.3 `while` loop

The `while` loop repeats as long as a condition is true:

```python
while condition:
    # body — keeps running while condition is True
```

Be careful: if the condition never becomes False, you get an **infinite loop**.

### 2.4 Controlling loops

- `break` — immediately exits the loop
- `continue` — skips the rest of the body and goes to the next iteration
- `else` — runs if the loop finished *without* hitting `break`

---

## 3. Step-by-step breakdown

### Step 1: `for` loop with `range()`

`range(n)` generates numbers from `0` to `n-1`:

```python
for i in range(5):
    print(i)
```
Output:
```
0
1
2
3
4
```

**Variants of `range()`:**
- `range(stop)` — 0 to stop-1
- `range(start, stop)` — start to stop-1
- `range(start, stop, step)` — start to stop-1, incrementing by step

```python
>>> list(range(2, 7))          # [2, 3, 4, 5, 6]
>>> list(range(0, 10, 2))      # [0, 2, 4, 6, 8]
>>> list(range(10, 0, -2))     # [10, 8, 6, 4, 2]
```

**Summing numbers with a loop:**

```python
total = 0
for n in range(1, 101):    # 1 to 100
    total += n
print(total)                # 5050
```

### Step 2: `for` loop over a list

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```
Output:
```
apple
banana
cherry
```

### Step 3: `for` loop over a string

```python
for char in "Python":
    print(char, end=" ")   # end=" " replaces the newline with a space
```
Output: `P y t h o n`

### Step 4: `enumerate()` — index and value

When you need the index as well as the value:

```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```
Output:
```
0: apple
1: banana
2: cherry
```

`enumerate()` starts at 0 by default. Change the start:

```python
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
```
Output:
```
1. apple
2. banana
3. cherry
```

### Step 5: `zip()` — parallel iteration

Loop over two or more lists at the same time:

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```
Output:
```
Alice: 85
Bob: 92
Charlie: 78
```

If lists are different lengths, `zip()` stops at the shortest:

```python
list(zip([1, 2, 3], ["a", "b"]))   # [(1, 'a'), (2, 'b')]
```

Use `itertools.zip_longest()` to pad shorter lists.

### Step 6: `while` loop

```python
count = 0
while count < 5:
    print(count)
    count += 1
```
Output: 0 1 2 3 4

**Loop until correct input:**

```python
password = "secret"
guess = ""
while guess != password:
    guess = input("Enter password: ")
print("Access granted!")
```

**Infinite loop (be careful):**

```python
while True:
    print("This never ends!")
```

### Step 7: `break` — exit early

```python
for i in range(1, 10):
    if i == 5:
        break          # stop when i reaches 5
    print(i)
```
Output: `1 2 3 4`

**Use case:** searching for something. Stop once found.

```python
numbers = [3, 7, 1, 9, 4, 2]
target = 9

for num in numbers:
    if num == target:
        print("Found!")
        break
```

### Step 8: `continue` — skip to next

```python
for i in range(1, 11):
    if i % 2 == 0:     # even numbers
        continue       # skip printing them
    print(i, end=" ")
```
Output: `1 3 5 7 9`

### Step 9: `else` clause on loops

The `else` block runs if the loop finished without hitting `break`.

```python
for n in range(2, 10):
    for divisor in range(2, n):
        if n % divisor == 0:
            print(f"{n} is not prime ({divisor} × {n//divisor})")
            break
    else:                            # else belongs to inner for
        print(f"{n} is prime")
```

Output:
```
2 is prime
3 is prime
4 is not prime (2 × 2)
5 is prime
6 is not prime (2 × 3)
7 is prime
8 is not prime (2 × 4)
9 is not prime (3 × 3)
```

### Step 10: Common loop patterns

**Accumulate** — build up a result:

```python
# Sum of squares
total = 0
for x in range(1, 6):
    total += x ** 2
print(total)    # 55
```

**Filter** — keep only items matching a condition:

```python
numbers = [1, 5, 3, 8, 2, 9, 4]
evens = []
for n in numbers:
    if n % 2 == 0:
        evens.append(n)
print(evens)    # [8, 2, 4]
```

**Transform** — map each item to something new:

```python
words = ["hello", "world", "python"]
uppers = []
for word in words:
    uppers.append(word.upper())
print(uppers)   # ['HELLO', 'WORLD', 'PYTHON']
```

**Loop and a half** — read until sentinel:

```python
while True:
    line = input("> ")
    if line == "quit":
        break
    print(f"You said: {line}")
```

---

## 4. Common mistakes

### Infinite loops
```python
x = 0
while x < 10:   # forgot to increment x
    print(x)    # runs forever
```

### Off-by-one with `range()`
```python
for i in range(5):   # runs for i = 0,1,2,3,4
    print(i)         # never prints 5!
```

### Modifying a list while iterating over it
```python
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)   # ❌ skips elements!
```

Instead, iterate over a copy:
```python
for n in numbers[:]:   # copy with [:]
```

### Forgetting `break` in `while True`
```python
while True:
    print("stuck")    # no break — infinite!
```

### `else` on loop — confusing with `if`/`else`
The `else` on a loop runs only if the loop was *not* exited via `break`.

### Using `range(len(...))` when you don't need the index
```python
for i in range(len(fruits)):      # unnecessary
    print(fruits[i])

for fruit in fruits:              # ✅ cleaner
    print(fruit)
```

Use `enumerate()` when you need the index.

---

## 5. Exercises

1. **Countdown** — Use a `for` loop with `range()` to print numbers from 10
   down to 1, then "Liftoff!".

2. **Sum of evens** — Ask the user for a number `n`. Use a loop to sum all
   even numbers from 1 to `n`. Print the result.

3. **Word counter** — Ask for a sentence. Use a `for` loop to count how many
   words have more than 4 letters. Print the count.

4. **Multiplication table** — Use nested `for` loops to print the
   multiplication table from 1 to 5 (a 5×5 grid).

5. **Guessing game** — Use a `while` loop to implement a number guessing game.
   Generate a random number (use `import random; target = random.randint(1, 10)`).
   Keep asking until the user guesses correctly. Tell them if they're too high
   or too low.

6. **Enumerate practice** — Given a list of names, print each one numbered
   starting from 1:
   ```
   1. Alice
   2. Bob
   3. Charlie
   ```

7. **Zip practice** — Given `colors = ["red", "green", "blue"]` and
   `hex_codes = ["#FF0000", "#00FF00", "#0000FF"]`, use `zip()` to print:
   ```
   red -> #FF0000
   green -> #00FF00
   blue -> #0000FF
   ```

8. **Prime finder** — Use a loop with `else` to find and print all prime
   numbers from 2 to 50.

---

## 6. Self-check questions

1. What is the difference between a `for` loop and a `while` loop?
2. What does `range(5)` produce? What about `range(3, 8)`?
3. What does `enumerate()` do?
4. What does `zip()` do?
5. What happens if you `zip()` two lists of different lengths?
6. What does `break` do? What does `continue` do?
7. When does the `else` clause on a loop run?
8. What is an infinite loop and how do you avoid it?
9. How do you iterate over a list and get both the index and value?
10. How do you iterate over multiple lists at the same time?

---

## 7. What's next

You can now repeat actions and process sequences efficiently. You know:
- `for` loops with `range()`, lists, and strings
- `enumerate()` for index + value
- `zip()` for parallel iteration
- `while` loops for condition-based repetition
- `break`, `continue`, and loop `else`
- Common patterns: accumulate, filter, transform

In **Level 05** you will explore Python's **collection types** in depth:
lists, tuples, sets, and dictionaries. You will learn which one to use for
which situation, and powerful features like list/dict comprehensions.

Close this lesson and open `05-collections.md`.
