# [09] Shell scripting
> **Track:** Linux · **Level:** 09 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

Typing commands one by one is fine for small tasks. But when you need to run the same sequence repeatedly — backup files, deploy code, process data — you need to automate it. Shell scripts let you write a series of commands into a file and execute them all at once, with logic, loops, and functions.

## 2. Core concept (absolute zero)

### What is a shell script?

A **shell script** is a plain text file containing shell commands. When you run it, bash executes each line in order.

### The shebang

The first line tells the system which interpreter to use:

```
#!/bin/bash
```

- `#!` — "shebang" (hash + bang)
- `/bin/bash` — path to the Bash interpreter

### Making a script executable

```
alice@xodex:~$ chmod +x myscript.sh
alice@xodex:~$ ./myscript.sh
```

Or run with bash directly:

```
alice@xodex:~$ bash myscript.sh
```

### Basic script structure

```bash
#!/bin/bash
# My first script
echo "Hello, Xodex!"
echo "Today is $(date)"
echo "I am user $USER"
```

Save as `hello.sh`, make executable, run it:

```
alice@xodex:~$ ./hello.sh
Hello, Xodex!
Today is Thu Jul 23 10:00:00 MSK 2026
I am user alice
```

## 3. Step-by-step breakdown (examples)

### Variables

Define and use variables — no spaces around `=`:

```bash
#!/bin/bash
name="Xodex"
version="1.0"
echo "Welcome to $name v$version"
echo "Project path: ${name}_v${version}"
```

Output:

```
Welcome to Xodex v1.0
Project path: Xodex_v1.0
```

Variables are case-sensitive by convention uppercase for constants:

```bash
#!/bin/bash
MAX_RETRIES=5
BACKUP_DIR="/var/backups"
```

### Command substitution

Run a command and store its output in a variable:

```bash
#!/bin/bash
current_date=$(date +%Y-%m-%d)
echo "Backing up on $current_date"
files=$(ls)
echo "Files: $files"
```

Old syntax (backticks): `` `command` `` — avoid it, use `$(...)` instead (nestable, clearer).

### Positional parameters

Script arguments are available as `$1`, `$2`, etc.:

```bash
#!/bin/bash
echo "Script name: $0"
echo "First arg: $1"
echo "Second arg: $2"
echo "Number of args: $#"
echo "All args: $@"
```

```
alice@xodex:~$ ./args.sh hello world 42
Script name: ./args.sh
First arg: hello
Second arg: world
Number of args: 3
All args: hello world 42
```

### Exit codes and `$?`

Every command returns an exit code: `0` = success, non-zero = failure.

```bash
#!/bin/bash
ls /nonexistent
echo "Exit code: $?"   # 2 (file not found)

ls /
echo "Exit code: $?"   # 0 (success)

exit 42                 # script exits with code 42
```

```
alice@xodex:~$ ./check-exit.sh; echo "Script exit code: $?"
ls: cannot access '/nonexistent': No such file or directory
Exit code: 2
Exit code: 0
Script exit code: 42
```

### `if` statements

```bash
#!/bin/bash
if [ condition ]; then
    commands
elif [ other condition ]; then
    commands
else
    commands
fi
```

### `test` and `[ ]` — conditions

**Numeric comparisons:**

| Operator | Meaning |
|----------|---------|
| `-eq` | Equal |
| `-ne` | Not equal |
| `-lt` | Less than |
| `-le` | Less than or equal |
| `-gt` | Greater than |
| `-ge` | Greater than or equal |

```bash
#!/bin/bash
score=85
if [ "$score" -ge 80 ]; then
    echo "Passed with distinction"
elif [ "$score" -ge 50 ]; then
    echo "Passed"
else
    echo "Failed"
fi
```

**String comparisons:**

| Operator | Meaning |
|----------|---------|
| `=` | Equal (string) |
| `!=` | Not equal |
| `-z` | String is empty (zero length) |
| `-n` | String is non-empty |

```bash
#!/bin/bash
name="Xodex"
if [ "$name" = "Xodex" ]; then
    echo "Hello, Xodex!"
fi

if [ -z "$empty_var" ]; then
    echo "Variable is empty"
fi
```

**File tests:**

| Operator | Meaning |
|----------|---------|
| `-f file` | File exists and is a regular file |
| `-d file` | File exists and is a directory |
| `-e file` | File exists (any type) |
| `-r file` | File is readable |
| `-w file` | File is writable |
| `-x file` | File is executable |
| `-s file` | File exists and is non-empty |

```bash
#!/bin/bash
if [ -f "/etc/passwd" ]; then
    echo "Password file exists"
fi

if [ -d "/home/alice" ]; then
    echo "Home directory exists"
fi

if [ ! -e "temp.log" ]; then
    echo "temp.log does not exist, creating it"
    touch temp.log
fi
```

**Logical operators:**

```bash
#!/bin/bash
if [ "$user" = "alice" ] && [ -f "data.txt" ]; then
    echo "Alice can process data.txt"
fi

if [ "$day" = "Saturday" ] || [ "$day" = "Sunday" ]; then
    echo "It's the weekend!"
fi

if [ ! -f "config.json" ]; then
    echo "Missing config file"
    exit 1
fi
```

### `for` loop

```bash
#!/bin/bash
for i in 1 2 3 4 5; do
    echo "Number: $i"
done
```

Loop over files:

```bash
#!/bin/bash
for file in *.txt; do
    echo "Processing $file"
    wc -l "$file"
done
```

Loop with a range:

```bash
#!/bin/bash
for i in {1..10}; do
    echo "Line $i"
done
```

Loop over command output:

```bash
#!/bin/bash
for user in $(cut -d: -f1 /etc/passwd); do
    echo "User: $user"
done
```

### `while` loop

Read a file line by line:

```bash
#!/bin/bash
while read -r line; do
    echo "Line: $line"
done < input.txt
```

### `case` statement

```bash
#!/bin/bash
echo "Select option (start/stop/restart/status):"
read -r action

case "$action" in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        echo "Restarting service..."
        ;;
    status)
        echo "Checking status..."
        ;;
    *)
        echo "Unknown option: $action"
        exit 1
        ;;
esac
```

### Functions

Define and call functions:

```bash
#!/bin/bash

greet() {
    echo "Hello, $1!"
    echo "Today is $(date)"
}

show_usage() {
    echo "Usage: $0 <name>"
    echo "Example: $0 Alice"
}

# Main script
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

greet "$1"
```

```
alice@xodex:~$ ./greet.sh Alice
Hello, Alice!
Today is Thu Jul 23 10:00:00 MSK 2026
```

Functions with return values:

```bash
#!/bin/bash

is_even() {
    if [ $(( $1 % 2 )) -eq 0 ]; then
        return 0   # true
    else
        return 1   # false
    fi
}

if is_even 42; then
    echo "42 is even"
fi
```

### Arithmetic

```bash
#!/bin/bash
a=10
b=3
sum=$((a + b))
diff=$((a - b))
prod=$((a * b))
quot=$((a / b))
rem=$((a % b))
echo "$a + $b = $sum"
echo "$a - $b = $diff"
echo "$a * $b = $prod"
echo "$a / $b = $quot"
echo "$a % $b = $rem"
```

### Putting it all together: a backup script

```bash
#!/bin/bash

# backup.sh — simple backup script
# Usage: ./backup.sh <source_dir> <backup_dir>

set -e  # exit on any error

show_usage() {
    echo "Usage: $0 <source_dir> <backup_dir>"
    exit 1
}

# Validate arguments
if [ $# -ne 2 ]; then
    show_usage
fi

src="$1"
dst="$2"

# Check source exists
if [ ! -d "$src" ]; then
    echo "Error: Source directory '$src' not found"
    exit 1
fi

# Create backup directory if needed
if [ ! -d "$dst" ]; then
    mkdir -p "$dst"
fi

# Create timestamped backup
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
archive_name="backup_$timestamp.tar.gz"
archive_path="$dst/$archive_name"

echo "Backing up $src to $archive_path ..."
tar -czf "$archive_path" "$src"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully"
    echo "Archive: $archive_path"
    echo "Size: $(du -h "$archive_path" | cut -f1)"
else
    echo "Backup failed"
    exit 1
fi
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `name = "value"` (spaces around `=`) | Bash treats `name` as a command | `name="value"` (no spaces) |
| `if [ $var = "yes" ]` without quotes | If `$var` is empty, syntax becomes `if [ = "yes" ]` → error | `if [ "$var" = "yes" ]` |
| Using `for i in $(cat file)` | Splits by whitespace, not lines | `while read -r line; do done < file` |
| `#!/bin/bash` with Windows line endings (`\r\n`) | Syntax error from carriage return | Use Unix line endings (`\n`) |
| Forgetting `exit` in error branches | Script continues after failure | `exit 1` after printing error |
| `$((i++)`) not working | Bash doesn't have `++` in all contexts | `i=$((i + 1))` |
| Not quoting `$@` | Arguments with spaces break | `"$@"` preserves arguments |

## 5. Exercises

1. Write a script `hello.sh` that prints "Hello, World!" and your username.
2. Write a script that takes a name as an argument and prints "Hello, [name]!".
3. Write a script that checks if a file exists (given as $1). If it does, print its size; if not, print an error.
4. Write a `for` loop script that iterates over all `.txt` files in the current directory and prints their line counts.
5. Write a `while` loop that reads `/etc/passwd` line by line and prints each username.
6. Write a `case` script that accepts `--help`, `--version`, or any other argument and behaves accordingly.
7. Write a function `is_file_empty` that returns 0 if a file is empty, 1 otherwise.
8. Write a script that sums all numbers given as arguments (e.g., `./sum.sh 1 2 3` → 6).

## 6. Self-check questions

1. What is the shebang and why is it needed?
2. How do you make a script executable?
3. What is the difference between `$@` and `$*`?
4. What does `$?` contain after a command runs?
5. How do you test if a file exists in a condition?
6. What's the difference between `-eq` and `=` in test conditions?
7. How do you read a file line by line in a `while` loop?
8. What does `return` do in a bash function?
9. Why should you quote variables in `[ ]` tests?
10. How do you write an arithmetic expression in bash?

## 7. What's next

You can now write scripts with logic, loops, and functions. In **Level 10**, the final level, you'll learn about **systemd** — the init system that manages services — write your own service unit files, use journalctl, set up timers, and complete a capstone project that ties everything together.
