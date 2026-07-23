# [04] Text tools
> **Track:** Linux · **Level:** 04 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

Linux stores everything as text — configuration files, logs, CSV data, source code. You need tools to **search**, **transform**, **filter**, and **analyze** text. Doing this by hand with a text editor is slow; these tools let you process text from the command line instantly.

## 2. Core concept (absolute zero)

### What are text tools?

Text tools are small, single-purpose programs that read text, do something to it, and output the result. They follow the Unix philosophy: **do one thing well**. You combine them with pipes (`|`) to build complex text-processing pipelines.

### The toolbox at a glance

| Tool | Purpose | Example |
|------|---------|---------|
| `grep` | Search for patterns in text | `grep "error" log.txt` |
| `sed` | Find and replace, edit streams | `sed 's/old/new/g' file` |
| `awk` | Process structured text (columns) | `awk '{print $1}' file` |
| `sort` | Sort lines | `sort names.txt` |
| `uniq` | Remove / count duplicates | `uniq -c sorted.txt` |
| `wc` | Count lines, words, characters | `wc -l file.txt` |
| `cut` | Extract columns by delimiter | `cut -d',' -f1 data.csv` |
| `tr` | Translate or delete characters | `tr 'a-z' 'A-Z' < file` |
| `head` | First N lines | `head -20 file` |
| `tail` | Last N lines | `tail -f log` |

## 3. Step-by-step breakdown (examples)

### `grep` — global regular expression print

`grep` searches for lines that match a pattern.

Basic search:

```
alice@xodex:~$ grep "root" /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

Search multiple files:

```
alice@xodex:~$ grep "error" /var/log/*.log
```

Common options:

| Option | Meaning |
|--------|---------|
| `-i` | Case-insensitive (`grep -i "error" log`) |
| `-v` | Invert match — show lines that do NOT match |
| `-r` | Recursive — search all files in directories |
| `-l` | List only filenames (not matching lines) |
| `-n` | Show line numbers |
| `-c` | Count matching lines per file |
| `-w` | Match whole words only |

```
alice@xodex:~$ grep -i "warning" /var/log/syslog
Jan 15 10:00:01 xodex kernel: [12345] warning: CPU temperature high

alice@xodex:~$ grep -v "^#" /etc/ssh/sshd_config    # remove comments
alice@xodex:~$ grep -r "TODO" ~/project/             # find all TODOs

alice@xodex:~$ grep -l "error" /var/log/*            # which logs have errors?
/var/log/syslog
/var/log/kern.log

alice@xodex:~$ grep -c "failed" /var/log/auth.log    # how many failed logins?
42

alice@xodex:~$ grep -w "the" file.txt                # match "the" not "there"
```

### `sed` — stream editor

`sed` transforms text. The most common use is **find and replace**:

```
alice@xodex:~$ echo "Hello World" | sed 's/World/Linux/'
Hello Linux
```

Replace in a file (show result, file unchanged):

```
alice@xodex:~$ sed 's/old/new/g' file.txt
```

Edit the file in-place (with `-i`):

```
alice@xodex:~$ sed -i 's/old/new/g' file.txt
```

| Pattern | Meaning |
|---------|---------|
| `s/old/new/` | Replace first occurrence on each line |
| `s/old/new/g` | Replace ALL occurrences on each line (`g` = global) |
| `s/old/new/2` | Replace second occurrence on each line |
| `s/old/new/gi` | Global + case-insensitive |
| `/pattern/d` | Delete lines matching pattern |

```
alice@xodex:~$ sed 's/foo/bar/' file.txt          # first foo per line
alice@xodex:~$ sed 's/foo/bar/g' file.txt         # every foo
alice@xodex:~$ sed '/^#/d' file.txt               # delete comment lines
alice@xodex:~$ sed 's/[0-9]//g' file.txt          # remove all digits
```

### `awk` — pattern scanning and processing

`awk` is ideal for column-based data. It splits each line by whitespace and gives you `$1`, `$2`, etc.

```
alice@xodex:~$ echo "Alice 25 engineer" | awk '{print $1}'
Alice
```

```
alice@xodex:~$ echo "Alice 25 engineer" | awk '{print $1, $3}'
Alice engineer
```

With a file:

```
alice@xodex:~$ cat employees.txt
Alice 25 engineer
Bob 30 designer
Carol 28 manager

alice@xodex:~$ awk '{print $1, $2}' employees.txt
Alice 25
Bob 30
Carol 28
```

Using `-F` to set a custom field separator:

```
alice@xodex:~$ echo "Alice,25,engineer" | awk -F',' '{print $1}'
Alice
```

Conditional printing:

```
alice@xodex:~$ awk '$2 > 28 {print $1, $2}' employees.txt
Bob 30
```

Print line numbers:

```
alice@xodex:~$ awk '{print NR, $0}' employees.txt
1 Alice 25 engineer
2 Bob 30 designer
3 Carol 28 manager
```

### `sort` — sort lines

```
alice@xodex:~$ cat names.txt
Charlie
Alice
Bob

alice@xodex:~$ sort names.txt
Alice
Bob
Charlie
```

| Option | Meaning |
|--------|---------|
| `-n` | Numeric sort (10 comes after 2) |
| `-r` | Reverse order |
| `-u` | Unique (same as `sort | uniq`) |
| `-k` | Sort by a specific column |
| `-t` | Field separator (with `-k`) |

```
alice@xodex:~$ sort -n numbers.txt        # numeric sort
alice@xodex:~$ sort -r names.txt          # reverse alphabetical
alice@xodex:~$ sort -k2 -n scores.txt     # sort by column 2 numerically

alice@xodex:~$ sort -t: -k3 -n /etc/passwd  # sort passwd by UID (col 3)
```

### `uniq` — unique values (requires sorted input!)

`uniq` removes **adjacent** duplicates. Always sort first!

```
alice@xodex:~$ cat duplicates.txt
apple
banana
apple
apple
banana

alice@xodex:~$ sort duplicates.txt | uniq
apple
banana

alice@xodex:~$ sort duplicates.txt | uniq -c    # count occurrences
      2 apple
      3 banana
```

### `wc` — word count

```
alice@xodex:~$ wc file.txt
 12  45 320 file.txt
│   │   │
│   │   └─ bytes/characters
│   └─ words
└─ lines
```

Common flags:

```
alice@xodex:~$ wc -l file.txt    # lines only
12 file.txt

alice@xodex:~$ wc -w file.txt    # words only
45 file.txt

alice@xodex:~$ wc -c file.txt    # bytes/characters
320 file.txt
```

Count files in a directory:

```
alice@xodex:~$ ls /bin | wc -l
1024
```

### `cut` — extract columns

```
alice@xodex:~$ echo "Alice,25,engineer" | cut -d',' -f1
Alice

alice@xodex:~$ cut -d',' -f1,3 data.csv     # columns 1 and 3
alice@xodex:~$ cut -d':' -f1 /etc/passwd    # all usernames

alice@xodex:~$ cut -c1-5 file.txt           # first 5 characters per line
```

### `tr` — translate or delete characters

```
alice@xodex:~$ echo "hello" | tr 'a-z' 'A-Z'
HELLO

alice@xodex:~$ echo "hello  world" | tr -s ' '     # squeeze spaces
hello world

alice@xodex:~$ cat file.txt | tr -d '\n'            # remove all newlines
alice@xodex:~$ cat file.txt | tr -d '[:space:]'     # remove all whitespace

alice@xodex:~$ cat messy.txt | tr -d '\r' > clean.txt   # remove Windows \r
```

### `head` and `tail` in depth

```
alice@xodex:~$ head -20 /etc/passwd              # first 20 lines
alice@xodex:~$ tail -30 /var/log/syslog          # last 30 lines
alice@xodex:~$ tail -f /var/log/syslog           # follow new lines
alice@xodex:~$ tail -n +10 file.txt              # lines 10 onward
```

### Combining tools in a pipeline

The real power is combining tools:

Find the top 3 largest files in `/var/log`:

```
alice@xodex:~$ ls -l /var/log/*.log | awk '{print $5, $9}' | sort -rn | head -3
```

Count unique IPs in a web server log:

```
alice@xodex:~$ grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' access.log | sort -u | wc -l
```

Find the most common word in a file:

```
alice@xodex:~$ tr -s ' ' '\n' < file.txt | sort | uniq -c | sort -rn | head -5
```

Find users with UID >= 1000 (real users):

```
alice@xodex:~$ awk -F: '$3 >= 1000 {print $1}' /etc/passwd
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `uniq` without `sort` first | Only removes adjacent duplicates | `sort file \| uniq` |
| `grep -r "pattern"` from `/` | Searches everything (huge, slow) | Restrict to a specific directory |
| `sed 's/foo/bar/g' file` without `-i` | Only prints result; file unchanged | Use `-i` to edit in place |
| Using `awk` with `-F,` (space after comma) | Wrong field separator | `awk -F','` (no space) |
| `grep "error"` matching "error123" | Matches partial words | Use `grep -w "error"` |
| Forgetting quotes around patterns | Shell interprets special characters | Always quote: `grep "pattern" file` |
| `tail -f` and forgetting `Ctrl+C` | Stays running forever | Press `Ctrl+C` to stop |

## 5. Exercises

1. Use `grep` to find all lines containing "root" in `/etc/passwd`.
2. Use `grep -i` to count how many times "error" appears in `/var/log/syslog`.
3. Use `sed` to replace all occurrences of "Alice" with "Bob" in a test file.
4. Use `awk` to print only the usernames (first column, colon-separated) from `/etc/passwd`.
5. Create a file with numbers (one per line), sort them numerically with `sort -n`.
6. Use `sort` and `uniq -c` together to count duplicate lines in a file.
7. Use `wc -l` to count how many files are in `/usr/bin`.
8. Use `cut -d:` to extract just the home directory paths from `/etc/passwd` (field 6).
9. Use `tr` to convert a file to uppercase.
10. Combine `ls -l`, `awk`, and `sort` to list the 5 largest files in a directory.
11. Use `grep -v "^#"` to show `/etc/ssh/sshd_config` without comments.
12. Use `tail -f` to watch `/var/log/syslog` for new messages. Stop with `Ctrl+C`.

## 6. Self-check questions

1. What does `grep -v` do?
2. How do you make `sed` edit a file in place?
3. In `awk`, what do `$0`, `$1`, and `NF` represent?
4. Why must you `sort` before `uniq`?
5. What does `wc -l` count?
6. How do you extract the second column from a comma-separated file?
7. What does `tr -d '\n'` do?
8. What is the difference between `head` and `tail`?
9. How would you find all TODO comments in your project recursively?
10. What does `sort -rn` do?

## 7. What's next

You now wield the core text-processing tools. In **Level 05**, you'll master **pipes and redirection** — connecting commands together, handling stdout and stderr, using `tee` and `xargs`, and building complex data pipelines.
