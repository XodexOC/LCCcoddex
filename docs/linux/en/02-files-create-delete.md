# [02] Files: create and delete
> **Track:** Linux · **Level:** 02 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

Now that you know how to navigate the filesystem, you need to actually **do things** — create files, edit them, copy them, move them, and delete them. These are the most common operations in the shell. Without these commands, you can only look, not act.

## 2. Core concept (absolute zero)

### The files as building blocks

Everything in Linux is a file. Here are the operations you'll perform most often:

| Operation | Command |
|-----------|---------|
| Create empty file | `touch file.txt` |
| Create directory | `mkdir dirname` |
| Create nested directories | `mkdir -p a/b/c` |
| Copy file | `cp source dest` |
| Copy directory | `cp -r source dest` |
| Move / rename | `mv source dest` |
| Delete file | `rm file.txt` |
| Delete directory (empty) | `rmdir dirname` |
| Delete directory (with contents) | `rm -r dirname` |
| Delete forcefully (no confirm) | `rm -f file.txt` |
| View file | `cat file.txt` |
| View page by page | `less file.txt` |
| View first 10 lines | `head file.txt` |
| View last 10 lines | `tail file.txt` |
| Write text to file | `echo "text" > file.txt` |
| Append text to file | `echo "text" >> file.txt` |
| Edit file (simple) | `nano file.txt` |

## 3. Step-by-step breakdown (examples)

### `touch` — create or update timestamp

`touch` creates an **empty file** if it doesn't exist, or updates its timestamp if it does:

```
alice@xodex:~$ touch notes.txt
alice@xodex:~$ ls -l notes.txt
-rw-r--r-- 1 alice alice 0 Jan 15 10:00 notes.txt
```

The file has zero bytes (empty).

If the file already exists, `touch` updates its access and modification times to now:

```
alice@xodex:~$ touch notes.txt   # timestamp updated
alice@xodex:~$ ls -l notes.txt
-rw-r--r-- 1 alice alice 0 Jan 15 11:30 notes.txt   # time changed
```

Create multiple files at once:

```
alice@xodex:~$ touch file1.txt file2.txt file3.txt
```

### `mkdir` and `mkdir -p` — create directories

```
alice@xodex:~$ mkdir project
alice@xodex:~$ ls -ld project/
drwxr-xr-x 2 alice alice 4096 Jan 15 10:05 project/
```

Create a nested structure (fails if parents don't exist):

```
alice@xodex:~$ mkdir project/src/css
mkdir: cannot create directory 'project/src/css': No such file or directory
```

With `-p` (parents), it creates everything needed:

```
alice@xodex:~$ mkdir -p project/src/css
alice@xodex:~$ ls -R project/
project/:
src/

project/src:
css/
```

### `cp` — copy files and directories

```
alice@xodex:~$ cp notes.txt backup.txt
alice@xodex:~$ ls
backup.txt  notes.txt
```

Copy a file into a directory:

```
alice@xodex:~$ cp notes.txt project/
alice@xodex:~$ ls project/
notes.txt
```

To copy a whole directory, use `-r` (recursive):

```
alice@xodex:~$ cp -r project/ project-backup/
alice@xodex:~$ ls
project/  project-backup/
```

### `mv` — move or rename

Rename a file:

```
alice@xodex:~$ mv notes.txt journal.txt
alice@xodex:~$ ls
journal.txt
```

Move a file into a directory:

```
alice@xodex:~$ mv journal.txt Documents/
alice@xodex:~$ ls Documents/
journal.txt
```

Rename a directory:

```
alice@xodex:~$ mv project/ old-project
```

Move multiple files into a directory:

```
alice@xodex:~$ mv file1.txt file2.txt file3.txt mydir/
```

### `rm` — delete files and directories

Delete a file:

```
alice@xodex:~$ rm journal.txt
```

Delete a directory (if empty):

```
alice@xodex:~$ rmdir empty-dir/
```

Delete a directory and everything inside it (recursive):

```
alice@xodex:~$ rm -r project-backup/
```

Force delete (no confirmation prompt):

```
alice@xodex:~$ rm -f protected-file.txt
```

**WARNING**: `rm -rf` is very powerful and dangerous. It deletes everything in the path without asking.

```
alice@xodex:~$ rm -rf ~/some-dir    # deletes some-dir and ALL contents
```

### `nano` — simple text editor

Nano is a beginner-friendly terminal text editor:

```
alice@xodex:~$ nano myfile.txt
```

Inside nano:
- Type normally to insert text
- `Ctrl + O` — save (WriteOut)
- `Ctrl + X` — exit
- `Ctrl + K` — cut a line
- `Ctrl + U` — paste
- `Ctrl + W` — search

```
  GNU nano 7.2          myfile.txt
Hello, Xodex!
This is my first file.
I am learning Linux.

^G Get Help  ^O Write Out  ^W Where Is  ^K Cut Text
^X Exit      ^R Read File  ^\ Replace   ^U Paste Text
```

### `cat` — concatenate and display

```
alice@xodex:~$ cat myfile.txt
Hello, Xodex!
This is my first file.
I am learning Linux.
```

View multiple files:

```
alice@xodex:~$ cat a.txt b.txt c.txt
```

### `less` — page through files

For long files, `less` opens a pager (like `man`):

```
alice@xodex:~$ less /var/log/syslog
```

Keys: `Space` (page down), `b` (page up), `/search` (search), `q` (quit).

### `head` and `tail` — top and bottom of files

Show first 10 lines (default):

```
alice@xodex:~$ head /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
```

Show first 5 lines:

```
alice@xodex:~$ head -5 /etc/passwd
```

Show last 10 lines:

```
alice@xodex:~$ tail /var/log/syslog
```

Follow a growing file (like logs):

```
alice@xodex:~$ tail -f /var/log/syslog
```

Press `Ctrl + C` to stop following.

### `echo` and redirection (`>`, `>>`)

`echo` prints text:

```
alice@xodex:~$ echo "Hello, World!"
Hello, World!
```

Redirect (`>`) output to a file (overwrites):

```
alice@xodex:~$ echo "Hello, World!" > greeting.txt
alice@xodex:~$ cat greeting.txt
Hello, World!
```

Append (`>>`) to a file (adds to end):

```
alice@xodex:~$ echo "Second line" >> greeting.txt
alice@xodex:~$ cat greeting.txt
Hello, World!
Second line
```

Overwrite vs append — important difference:

```
alice@xodex:~$ echo "NEW" > greeting.txt    # file now has only "NEW"
alice@xodex:~$ echo "MORE" >> greeting.txt   # file now has "NEW" + "MORE"
```

Create a multi-line file with `cat` and heredoc (`<<`):

```
alice@xodex:~$ cat > myfile.txt << EOF
Line one
Line two
Line three
EOF
```

### Putting it all together

Let's create a project structure:

```
alice@xodex:~$ mkdir -p myproject/src myproject/tests myproject/docs
alice@xodex:~$ touch myproject/src/main.py
alice@xodex:~$ touch myproject/tests/test_main.py
alice@xodex:~$ echo "# My Project" > myproject/README.md
alice@xodex:~$ echo "print('hello')" > myproject/src/main.py
alice@xodex:~$ ls -R myproject/
myproject/:
README.md  docs/  src/  tests/

myproject/docs:

myproject/src:
main.py

myproject/tests:
test_main.py
```

Now copy the whole thing:

```
alice@xodex:~$ cp -r myproject/ myproject-backup/
```

Rename it:

```
alice@xodex:~$ mv myproject-backup/ archive/
```

Delete it:

```
alice@xodex:~$ rm -r archive/
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `cp -r` on a file (not a directory) | Flag not needed; file copies fine without `-r` | Just `cp file1 file2` |
| `rm -rf /some/path/ ` with trailing slash | On some shells this could behave unexpectedly | Avoid trailing slash with `rm -rf` |
| `rm file1 file2` when you meant to move them | Deletes files | `mv file1 file2` (but beware: `file2` would be overwritten) |
| `mkdir a/b/c` without `-p` | Fails if parent doesn't exist | `mkdir -p a/b/c` |
| `> file.txt` without a command | Truncates the file to zero bytes | Use with `echo` or another command: `echo "text" > file.txt` |
| Typo: `rm -rf / home/` (space after /) | Destroys entire system! The space makes it two arguments: `rm -rf /` (everything) and `home/` | Never put a space between `/` and the path |
| `cp a.txt b.txt` when b.txt exists | **Silently overwrites** b.txt without warning | Use `cp -i` for interactive (prompts before overwrite) |

## 5. Exercises

1. Create a file called `hello.txt` using `touch`.
2. Write "Hello, Linux!" into the file using `echo` and `>`.
3. Append a second line to `hello.txt` using `>>`.
4. Create a directory structure: `school/math/homework` using a single `mkdir` command.
5. Copy `hello.txt` into `school/math/`.
6. Rename `hello.txt` in the `school/math/` directory to `greeting.txt`.
7. Create a file called `data.txt` with 3 lines using `cat > data.txt` and heredoc.
8. Use `head` to show the first 2 lines of `/etc/passwd`.
9. Use `tail` to show the last 3 lines of `/etc/passwd`.
10. Open `nano` to create a shopping list with at least 5 items. Save and exit.
11. Delete the `school/math/homework` directory (should be empty).
12. Delete the entire `school` directory with its contents.
13. Create 5 empty files at once: `a.txt b.txt c.txt d.txt e.txt`.
14. Use `ls -la` to check that all files were created with zero bytes.
15. Delete all 5 files with a single `rm` command.

## 6. Self-check questions

1. What does `touch` do if the file already exists?
2. What flag is needed for `mkdir` to create parent directories?
3. What's the difference between `>` and `>>` when redirecting output?
4. How do you copy a directory and everything in it?
5. What happens if you `mv file1.txt file2.txt` and `file2.txt` already exists?
6. What's the difference between `rmdir` and `rm -r`?
7. How do you view a file that's constantly growing (like a log)?
8. What key combination saves a file in `nano`?
9. What does `rm -f` do differently from `rm` without `-f`?
10. How would you create the path `one/two/three/file.txt` in one command?

## 7. What's next

You can now create, edit, move, copy, and delete files. In **Level 03**, you'll learn about **permissions** — who can read, write, and execute files, and how to change those permissions with `chmod`, `chown`, and related commands.
