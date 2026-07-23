# [05] Pipes
> **Track:** Linux · **Level:** 05 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

Individual text tools are useful, but their real power comes from **combining them**. You might want to search a log file, extract certain columns, sort the results, and save them — all in one command. Pipes and redirection let you chain commands together so the output of one becomes the input of the next.

## 2. Core concept (absolute zero)

### Three standard streams

Every Linux program has three standard data streams:

| Stream | Name | Number | Direction | Default target |
|--------|------|--------|-----------|----------------|
| `stdin` | Standard input | `0` | Data into the program | Keyboard |
| `stdout` | Standard output | `1` | Data out of the program | Terminal screen |
| `stderr` | Standard error | `2` | Error messages | Terminal screen |

### The pipe `|`

The pipe connects `stdout` of one command to `stdin` of another:

```
command1 | command2
```

Think of it as a physical pipe: data flows from left to right.

```
ls -la / | grep "^d" | awk '{print $NF}'
    │          │            │
    │          │            └─ commands in the pipeline
    │          └─ pipe sends stdout of ls to stdin of grep
    └─ pipe sends stdout of grep to stdin of awk
```

### Redirection operators

| Operator | Meaning |
|----------|---------|
| `>` | Redirect stdout to a file (overwrite) |
| `>>` | Redirect stdout to a file (append) |
| `2>` | Redirect stderr to a file |
| `2>>` | Append stderr to a file |
| `&>` | Redirect both stdout and stderr (overwrite) |
| `&>>` | Append both stdout and stderr |
| `<` | Read stdin from a file |
| `<<` | Here-document (inline stdin) |
| `<<<` | Here-string (single string as stdin) |

## 3. Step-by-step breakdown (examples)

### Basic pipes

List files, filter for directories, count them:

```
alice@xodex:~$ ls -la / | grep "^d" | wc -l
```

Find running processes containing "sshd", extract PID:

```
alice@xodex:~$ ps aux | grep sshd | awk '{print $2}'
```

Sort files by size (descending), show top 5:

```
alice@xodex:~$ ls -l /usr/bin | sort -k5 -rn | head -5
```

### Redirecting stdout: `>`

Save output to a file:

```
alice@xodex:~$ ls -la > directory-listing.txt
alice@xodex:~$ cat directory-listing.txt
total 123
drwxr-xr-x  5 alice alice  4096 Jan 15 10:00 .
drwxr-xr-x 12 alice alice  4096 Jan 15 09:00 ..
...
```

**Warning**: `>` **overwrites** without warning:

```
alice@xodex:~$ echo "important data" > data.txt
alice@xodex:~$ echo "oh no" > data.txt     # previous data GONE
alice@xodex:~$ cat data.txt
oh no
```

### Appending: `>>`

Add to a file rather than replace it:

```
alice@xodex:~$ echo "line 1" > log.txt
alice@xodex:~$ echo "line 2" >> log.txt
alice@xodex:~$ echo "line 3" >> log.txt
alice@xodex:~$ cat log.txt
line 1
line 2
line 3
```

### Redirecting stderr: `2>`

Some commands write errors to stderr. Capture it separately:

```
alice@xodex:~$ ls /nonexistent
ls: cannot access '/nonexistent': No such file or directory

alice@xodex:~$ ls /nonexistent 2> errors.txt
(no output on screen — error went to file)

alice@xodex:~$ cat errors.txt
ls: cannot access '/nonexistent': No such file or directory
```

### Merge stdout and stderr: `2>&1` and `&>`

Send both stdout and stderr to the same place:

```
alice@xodex:~$ ls /exist /nonexistent > output.txt 2>&1
alice@xodex:~$ cat output.txt
/exist:   file1.txt
ls: cannot access '/nonexistent': No such file or directory
```

Shortcut (bash): `&>`

```
alice@xodex:~$ ls /exist /nonexistent &> output.txt
```

### Discard output: `/dev/null`

`/dev/null` is a special file that throws away anything written to it:

```
alice@xodex:~$ ls /nonexistent 2> /dev/null    # suppress error
```

```
alice@xodex:~$ noisy-command > /dev/null 2>&1   # suppress everything
```

### Redirecting stdin: `<`

Read input from a file instead of the keyboard:

```
alice@xodex:~$ sort < unsorted.txt
```

This is equivalent to `sort unsorted.txt`.

```
alice@xodex:~$ tr 'a-z' 'A-Z' < lowercase.txt > uppercase.txt
```

### Here-document `<<`

Provide multi-line input inline (useful in scripts):

```
alice@xodex:~$ cat << EOF
> Line one
> Line two
> EOF
Line one
Line two
```

### Here-string `<<<`

Provide a single string as stdin:

```
alice@xodex:~$ grep "error" <<< "no errors here"
(no match)

alice@xodex:~$ grep "error" <<< "this line has an error"
this line has an error
```

### `tee` — split output

`tee` sends output to both a file **and** the screen:

```
alice@xodex:~$ ls -la | tee directory.txt | wc -l
152
alice@xodex:~$ cat directory.txt
total 152
...
```

Append with `-a`:

```
alice@xodex:~$ echo "new entry" | tee -a log.txt
```

### `xargs` — build and execute commands

`xargs` reads items from stdin and passes them as arguments to another command.

Without `xargs`:

```
alice@xodex:~$ grep "pattern" file1.txt file2.txt file3.txt
```

With `xargs` (find files first):

```
alice@xodex:~$ ls *.txt | xargs grep "pattern"
```

Delete files found by `find`:

```
alice@xodex:~$ find /tmp -name "*.tmp" | xargs rm
```

(Modern alternative: `find /tmp -name "*.tmp" -delete`)

Count lines in each file:

```
alice@xodex:~$ ls *.py | xargs wc -l
  45 main.py
  12 utils.py
  10 test.py
  67 total
```

With `-I` for placeholder:

```
alice@xodex:~$ ls *.txt | xargs -I {} cp {} {}.backup
```

(Each `{}` is replaced with the filename.)

With `-n` to control how many arguments per command:

```
alice@xodex:~$ echo "1 2 3 4 5 6" | xargs -n 3 echo
1 2 3
4 5 6
```

### Putting it all together

**Real-world pipeline: find and kill a process**

```
alice@xodex:~$ ps aux | grep "sleep 60" | grep -v grep | awk '{print $2}' | xargs kill
```

Step by step:
1. `ps aux` — list all processes
2. `grep "sleep 60"` — find the one we want
3. `grep -v grep` — exclude the grep process itself
4. `awk '{print $2}'` — extract PID (column 2)
5. `xargs kill` — send SIGTERM to that PID

**Find largest directories**

```
alice@xodex:~$ du -sh /var/* | sort -rh | head -5 | tee top5.txt
```

**Count unique error types in a log**

```
alice@xodex:~$ grep "ERROR" /var/log/app.log | awk '{print $NF}' | sort | uniq -c | sort -rn
```

**Create a backup of all `.conf` files**

```
alice@xodex:~$ ls /etc/*.conf | xargs -I {} cp {} {}.bak
```

**Redirect everything to a log file**

```
alice@xodex:~$ ./build.sh > build.log 2>&1
```

Or using the shorthand:

```
alice@xodex:~$ ./build.sh &> build.log
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `command > file 2> file` | Opens the file twice — risk of race/loss | `command > file 2>&1` |
| `command | grep pattern | file.txt` | Missing `>` for redirection | `command | grep pattern > file.txt` |
| `command 2>&1 > file` | Wrong order: stderr goes to screen, stdout to file | `command > file 2>&1` (redirect before merge) |
| `ls \| grep pattern \| xargs rm` without checking | Dangerous if filenames have spaces | Use `xargs -I {} rm "{}"` or `find ... -delete` |
| `>` inside a pipe chain | `>` creates a file, doesn't pipe | `command1 \| command2 > output.txt` |
| `tail -f log > file` | `tail -f` never ends, file keeps growing forever | Use `tail -n 100 log > file` instead |

## 5. Exercises

1. Run `ls -la /usr/bin | head -20`. What do you see?
2. Use pipes to count how many directories exist in `/` (hint: `ls -la / | grep "^d" | wc -l`).
3. Find all `.conf` files in `/etc` and count them: `ls /etc/*.conf | wc -l`.
4. Use `ps aux`, `grep`, and `awk` to print the PID of your shell (bash).
5. Redirect the output of `echo "Hello World"` to a file called `greeting.txt` using `>`.
6. Append the date (`date` command) to `greeting.txt` using `>>`.
7. Run a command that produces an error (like `ls /fake`). Redirect only stderr to `error.log`.
8. Use `tee` to save the output of `ls -la` to a file while also seeing it on screen.
9. Use `xargs` with `echo` to print each word from `echo "a b c"` on its own line.
10. Use `xargs` to find and count lines in all `.txt` files in a directory.
11. Build a pipeline: find all processes running `cron`, extract their PIDs, and display them.
12. Use `grep`, `awk`, and `sort` to find the 5 most frequent words in a file.

## 6. Self-check questions

1. What does the pipe operator `|` do?
2. What is the difference between `>` and `>>`?
3. How do you redirect stderr to a file without affecting stdout?
4. How do you redirect both stdout and stderr to the same file?
5. What does `tee` do?
6. What is `/dev/null` used for?
7. How does `xargs` differ from a regular pipe?
8. What does `2>&1` mean? Why does order matter?
9. How would you suppress all output of a command (both stdout and stderr)?
10. What's the difference between `command < file` and `command file`?

## 7. What's next

Pipes and redirection are the glue that connects everything. In **Level 06**, you'll learn about **processes** — how Linux manages running programs, how to monitor them, kill them, run them in the background, and make them survive terminal closure.
