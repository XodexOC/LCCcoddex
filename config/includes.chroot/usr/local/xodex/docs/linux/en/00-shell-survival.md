# [00] Shell survival
> **Track:** Linux · **Level:** 00 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Computers are controlled with a mouse and a graphical interface (GUI). But many powerful operations — installing software, managing files, running servers, automating tasks — are faster or only possible through a **terminal**. The terminal gives you text-based access to the operating system. Learning to survive in the shell is the first skill every Linux user needs.

## 2. Core concept (absolute zero)

### What is a terminal?

A **terminal** is a program that opens a window where you can type text commands. It connects to a **shell** — the program that interprets your commands and tells the OS what to do.

### What is a shell?

The **shell** is a command-line interpreter. The most common shell is **Bash** (Bourne Again SHell). When you type a command and press Enter, the shell reads it, executes it, and shows you the result.

### Opening the terminal

- On most Linux desktops: press `Ctrl + Alt + T`
- Or find "Terminal" in the applications menu
- In some environments (like a server), you're already in a terminal when you log in

### The prompt: `$` vs `#`

When the shell is ready for your command, it shows a **prompt**:

```
user@xodex:~$
```

The last character tells you about your privileges:
- `$` — you are a **normal user** (limited permissions)
- `#` — you are **root** (superuser, full permissions)

```
alice@xodex:~$    # normal user
root@xodex:~#     # root user
```

### First commands

| Command | What it does | Example |
|---------|-------------|---------|
| `pwd`   | Print working directory — shows where you are | `/home/alice` |
| `ls`    | List files and directories in current folder | `ls` |
| `cd`    | Change directory — move into a folder | `cd Documents` |
| `clear` | Clear the terminal screen | `clear` |

```
alice@xodex:~$ pwd
/home/alice

alice@xodex:~$ ls
Desktop  Documents  Downloads  Music  Pictures

alice@xodex:~$ cd Documents

alice@xodex:~/Documents$ pwd
/home/alice/Documents

alice@xodex:~/Documents$ ls
homework.txt  notes.txt

alice@xodex:~/Documents$ clear
```
(clears screen)

## 3. Step-by-step breakdown (examples)

### Command syntax

Every command follows this pattern:

```
command [options] [arguments]
```

- **command** — the program to run (e.g., `ls`)
- **options** — modify behavior, start with `-` (e.g., `-l` for long format)
- **arguments** — what the command acts on (e.g., a filename)

```
ls -l Documents
│    │     │
│    │     └─ argument: the target folder
│    └─ option: long format
└─ command: list
```

Options can be short (`-l`) or long (`--all`):

```
ls -l --all
```

Short options can often be combined:

```
ls -la       # same as ls -l -a
```

### The `man` pages (built-in documentation)

Every command has a manual. Type `man` followed by the command name:

```
alice@xodex:~$ man ls
```

This opens a pager. Navigation:
- `↑` / `↓` — scroll one line
- `Space` / `b` — page down / page up
- `/word` — search for "word"
- `q` — quit

```
alice@xodex:~$ man ls

LS(1)                            User Commands                            LS(1)

NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION
       List information about the FILEs (the current directory by default).
       Sort entries alphabetically if none of -cftuvSUX nor --sort is
       specified.
...
```

### File paths: absolute vs relative

A **path** tells you where a file or directory lives.

**Absolute path** — starts from the root `/`:

```
/home/alice/Documents/notes.txt
/etc/passwd
/usr/bin/python3
```

**Relative path** — starts from where you are right now:

```
Documents/notes.txt
../Pictures/photo.jpg
./script.sh
```

| Symbol | Meaning | Example |
|--------|---------|---------|
| `.`    | Current directory | `./script.sh` |
| `..`   | Parent directory | `cd ..` |
| `~`    | Your home directory | `cd ~` or `ls ~/Documents` |
| `/`    | Root of filesystem | `cd /` |

### TAB completion

Type part of a command or filename, then press **Tab**. The shell fills in the rest. If multiple matches exist, press Tab twice to see all possibilities.

```
alice@xodex:~$ cd Docu[Tab]  →  cd Documents/
```

```
alice@xodex:~$ ls -[Tab][Tab]
--all       --almost-all      --backup
--block-size  --classify      --color
...
```

### Command history

- `↑` / `↓` — scroll through previous commands
- `history` — show all recent commands with numbers
- `!123` — re-run command number 123 from history
- `Ctrl + R` — search history interactively

```
alice@xodex:~$ history
  1  ls
  2  pwd
  3  cd Documents/
  4  ls -la
  5  clear
```

Press `Ctrl + R`, then start typing:

```
(reverse-i-search)`pwd': pwd
```

Press `Ctrl + R` again to cycle through matches. Press `Enter` to run.

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `cd Documents` from `/` | `Documents` does not exist in `/` — you need an absolute or correct relative path | `cd /home/alice/Documents` |
| `ls -la /nonexistent` | Path doesn't exist → `ls: cannot access '/nonexistent': No such file or directory` | Check the path first with `ls` |
| Forgetting spaces around options | `ls -la` is correct, `ls -l a` is not the same | `ls -la` |
| Tab not working | You may have a typo in the partial path | Check spelling |
| `rm file /` | Forgetting you're in a dangerous directory | Always use `pwd` before destructive commands |

## 5. Exercises

1. Open a terminal. What does your prompt look like? What user are you?
2. Type `pwd`. Where are you?
3. Type `ls`. What files do you see?
4. Type `ls -la`. What's different from plain `ls`?
5. Change to the `/` directory with `cd /`. Then type `ls`. What do you see?
6. Go back to your home directory with `cd ~` or `cd`. Confirm with `pwd`.
7. Use `cd ..` to go up one directory. Where are you now? Use `pwd` to check.
8. Open the manual for `ls` with `man ls`. Find out what `-h` does. Press `q` to quit.
9. Practice TAB completion: type `cd /` then press Tab twice. What directories exist?
10. Press `Ctrl + R`, type `pwd`, and re-run the command from history.
11. Use `ls -l` on the root directory (`ls -l /`). What are the first three columns?
12. Navigate: from your home directory, go to `/usr/bin`. Use a relative path to go back to your home directory.

## 6. Self-check questions

1. What is the difference between `$` and `#` in a shell prompt?
2. What command shows your current location in the filesystem?
3. What is the difference between `/home/alice` and `~/Documents`?
4. What does `..` mean in a path? What about `.`?
5. How do you find out what options a command supports?
6. What does `ls -la` do that `ls` doesn't?
7. How do you search through your command history?
8. How can you complete a partially typed filename without writing the whole thing?
9. What is the difference between an absolute and a relative path?
10. What key quits the `man` pager?

## 7. What's next

You have survived the shell. You know how to move around, list files, read help, and navigate the filesystem. In **Level 01**, you'll dive deep into the Linux filesystem hierarchy and understand how the system is organized — from `/bin` to `/proc`, inodes, file types, and disk usage.
