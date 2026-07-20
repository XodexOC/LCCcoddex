# [5/10] OOP

> **Track:** Python · **Level:** 5 · **Slug:** `05-oop`

## Learning goals

- Understand: OOP
- Complete the lab exercise
- Know which man/docs to open next

## Theory

class, __init__, methods, inheritance, dunder methods, dataclasses overview.

### Objects
```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    def deposit(self, amount):
        if amount < 0: raise ValueError("negative")
        self.balance += amount
```
Prefer composition over deep inheritance trees.

## Practice

Model BankAccount with deposit/withdraw; raise on insufficient funds.

**Live paths:**
- Examples: `/usr/local/xodex/examples/python`
- Lab: `/usr/local/xodex/courses/python/level-05`

```bash
cd /usr/local/xodex/courses/python/level-05
./test.sh
```

## Self-check

- [ ] Explain the topic without notes
- [ ] Exercise runs successfully
- [ ] Name one failure mode if you skip checks

## Further reading

- https://docs.python.org/3/tutorial/

## Navigation

- Previous: level 4
- Go to the next numbered lesson.
- Index: `docs/python/en/README.md`
