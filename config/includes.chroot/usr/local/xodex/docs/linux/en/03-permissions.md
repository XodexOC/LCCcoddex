# [03] Permissions
> **Track:** Linux · **Level:** 03 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're running

Linux is a multi-user system. Multiple people (and programs) may share the same machine. Without permissions, any user could read, modify, or delete anyone else's files — including critical system files. Permissions prevent that. They control **who can do what** to every file and directory.

## 2. Core concept (absolute zero)

Every file and directory in Linux has:

1. **An owner** (a user)
2. **A group** (a group of users)
3. **A set of permissions** for the owner, the group, and everyone else

### The permission triplet

Permissions are divided into three categories — **read** (`r`), **write** (`w`), **execute** (`x`):

| Permission | On a file | On a directory |
|-----------|-----------|----------------|
| `r` (read) | View contents | List files |
| `w` (write) | Modify contents | Create/delete files inside |
| `x` (execute) | Run as a program | Enter the directory (cd into it) |

These are assigned to three **classes**:

| Class | Symbol | Who |
|-------|--------|-----|
| User (owner) | `u` | The file's owner |
| Group | `g` | Users who are in the file's group |
| Others | `o` | Everyone else |

### Reading `ls -l` output

```
-rwxr-xr-x  1 alice devs  12345 Jan 15 10:00 script.sh
│││││││││   │ │    │     │     │        │
│││││││││   │ │    │     │     │        └─ filename
│││││││││   │ │    │     │     └─ modification time
│││││││││   │ │    │     └─ size
│││││││││   │ │    └─ group
│││││││││   │ └─ owner (alice)
│││││││││   └─ hard links
││││││││└─ others: execute (x)
││││││││─ others: write (-)
│││││││└─ others: read (r)
││││││└─ group: execute (x)
││││││─ group: write (-)
│││││└─ group: read (r)
││││└─ owner: execute (x)
││││─ owner: write (w)
│││└─ owner: read (r)
││└─ ACL indicator (space/./+)
│└─ file type (-)
└─ setuid/setgid/sticky (not set)
```

**Example breakdown: `-rwxr-xr--`**

```
Owner: rwx  (read, write, execute)
Group: r-x  (read, execute)
Other: r--  (read only)
```

### Special modes in the first character

```
drwxr-xr-x   ... directory/
lrwxrwxrwx   ... link -> target    (symlinks are always 777)
crw-rw-rw-   ... character device
brw-rw----   ... block device
```

## 3. Step-by-step breakdown (examples)

### `chmod` with numbers (octal mode)

Permissions can be represented as **numbers** instead of letters:

| Permission | Octal |
|-----------|-------|
| `---` | 0 |
| `--x` | 1 |
| `-w-` | 2 |
| `-wx` | 3 |
| `r--` | 4 |
| `r-x` | 5 |
| `rw-` | 6 |
| `rwx` | 7 |

Each digit represents one class (owner, group, others):

```
chmod 755 script.sh
        │││
        ││└─ others (5 = r-x)
        │└─ group (5 = r-x)
        └─ owner (7 = rwx)
```

Common modes:

| Mode | Meaning | Use case |
|------|---------|----------|
| `644` | `rw-r--r--` | Regular files (everyone can read, owner can write) |
| `755` | `rwxr-xr-x` | Directories and executables |
| `600` | `rw-------` | Private files (only owner can read/write) |
| `700` | `rwx------` | Private directories |
| `777` | `rwxrwxrwx` | World-writable (dangerous!) |

Examples:

```
alice@xodex:~$ touch notes.txt
alice@xodex:~$ ls -l notes.txt
-rw-r--r-- 1 alice alice 0 Jan 15 10:00 notes.txt
                                 # default: 644

alice@xodex:~$ chmod 600 notes.txt
alice@xodex:~$ ls -l notes.txt
-rw------- 1 alice alice 0 Jan 15 10:00 notes.txt
```

```
alice@xodex:~$ chmod 755 myscript.sh
alice@xodex:~$ ls -l myscript.sh
-rwxr-xr-x 1 alice alice 42 Jan 15 10:00 myscript.sh
```

### `chmod` with letters (symbolic mode)

Use `u` (user/owner), `g` (group), `o` (others), `a` (all three).

Add permission with `+`, remove with `-`, set exactly with `=`.

```
alice@xodex:~$ chmod u+x script.sh    # add execute for owner
alice@xodex:~$ chmod g-w script.sh    # remove write for group
alice@xodex:~$ chmod o-r script.sh    # remove read for others
```

```
alice@xodex:~$ chmod a+x script.sh    # add execute for ALL (u+g+o)
alice@xodex:~$ chmod u=rwx,g=rx,o=r script.sh   # set exact permissions
```

### `chown` — change owner

Only root (or the file's owner) can change ownership.

```
root@xodex:~# chown bob file.txt        # change owner to bob
root@xodex:~# chown bob:devs file.txt   # change owner AND group
root@xodex:~# chown :devs file.txt      # change ONLY group
```

```
root@xodex:~# chown -R bob /home/bob/   # recursive (-R) for directories
```

### `chgrp` — change group

```
alice@xodex:~$ chgrp devs project/     # change group of directory
alice@xodex:~$ chgrp -R devs project/  # change group recursively
```

### `sudo` — do as superuser

`sudo` (superuser do) lets a permitted user run a command as root:

```
alice@xodex:~$ apt update
E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)

alice@xodex:~$ sudo apt update
[sudo] password for alice:
... (works)
```

- Only users in the `sudo` group (or listed in `/etc/sudoers`) can use `sudo`
- You're prompted for **your** password, not root's password
- `sudo -i` — start a root shell (be careful!)
- `sudo command` — run one command as root
- `sudo -u bob command` — run as user bob instead of root

### `su` — switch user

```
alice@xodex:~$ su bob          # switch to bob (needs bob's password)
alice@xodex:~$ su -            # switch to root (needs root password)
alice@xodex:~$ sudo su -       # switch to root using sudo (no root password needed)
```

Without `-`, you stay in the current directory with the old user's environment. With `-`, you get a login shell (as if bob logged in fresh).

### `id`, `whoami`, `groups`

```
alice@xodex:~$ whoami
alice

alice@xodex:~$ id
uid=1000(alice) gid=1000(alice) groups=1000(alice),27(sudo),44(video)

alice@xodex:~$ groups
alice sudo video
```

```
alice@xodex:~$ id bob
uid=1001(bob) gid=1001(bob) groups=1001(bob)
```

### `umask` — default permissions

`umask` defines which permissions are **removed** when creating a new file or directory. It's like a filter.

```
alice@xodex:~$ umask
0022
```

A **file** is created with base `666` (rw-rw-rw-), minus the umask.
A **directory** is created with base `777` (rwxrwxrwx), minus the umask.

Umask of `022`:
- File: `666 - 022 = 644` (rw-r--r--)
- Dir:  `777 - 022 = 755` (rwxr-xr-x)

```
alice@xodex:~$ umask 077           # set restrictive umask
alice@xodex:~$ touch secret.txt
alice@xodex:~$ ls -l secret.txt
-rw------- 1 alice alice 0 Jan 15 10:00 secret.txt
```

The umask is inherited by child processes, so setting it in your `~/.bashrc` affects all new files you create.

### Real-world example: setting up a shared project

```
alice@xodex:~$ mkdir /srv/project
alice@xodex:~$ sudo chown :devs /srv/project          # group = devs
alice@xodex:~$ sudo chmod 2775 /srv/project           # 2 = setgid bit
```

The `2` in `2775` is the **setgid bit** — new files created inside inherit the directory's group (devs), not the user's primary group.

```
alice@xodex:~$ ls -ld /srv/project
drwxrwsr-x 2 root devs 4096 Jan 15 10:00 /srv/project
#       ^— the "s" means setgid is set
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `chmod 777 file` for everything | Security risk; anyone can modify your files | Use `644` for files, `755` for directories |
| `chmod +x` without specifying `u/g/o` | Adds x for all classes; sometimes you only want owner executable | `chmod u+x script.sh` |
| `sudo chown` without `-R` on a directory | Only changes the directory, not its contents | `sudo chown -R bob:bob /home/bob/` |
| Thinking `sudo` makes you root permanently | `sudo` only affects one command | Use `sudo -i` for a root shell, but exit immediately after |
| `su` without `-` | Doesn't give a proper login environment | `su - username` |
| Setting umask to `000` | Creates world-writable files by default | `umask 022` or `077` |

## 5. Exercises

1. Create a file called `secret.txt`. Check its permissions with `ls -l`.
2. Change its permissions so only you (the owner) can read and write: `chmod 600 secret.txt`.
3. Create a script `run.sh` with `echo "hello"`. Make it executable with `chmod u+x run.sh`.
4. Use symbolic mode: remove read permission for "others" from `secret.txt`.
5. Use `whoami`, `id`, and `groups` to learn about your user.
6. Create a directory `shared`. Use `chmod 755 shared`. Check with `ls -ld shared`.
7. Use `sudo` to view `/etc/shadow` (normally inaccessible).
8. Change the group of a test file to `root` (you'll need `sudo` or `chgrp`).
9. Set umask to `077`. Create a file. Check its permissions. Set umask back to `022`.
10. Look at the files in `/usr/bin`. What are the common permissions?
11. Create a file, use `chmod u=rw,g=r,o=`. Verify with `ls -l`.
12. Use `chmod 755` on a directory. Try to create a file inside as a different user (what happens?).

## 6. Self-check questions

1. What do `r`, `w`, and `x` mean when applied to a **directory**?
2. What permission (octal) would give the owner rwx, group r-x, and others ---?
3. What does `chmod u+x file` do?
4. What is the difference between `chown bob file` and `chown bob:devs file`?
5. Why should you avoid `chmod 777`?
6. What does `sudo` allow a normal user to do?
7. What does `umask 022` mean when creating a file? What about a directory?
8. How do you change permissions on a directory and everything inside it?
9. What does the "s" in `drwxrwsr-x` mean?
10. How do you see what groups you belong to?

## 7. What's next

You understand permissions — the core of Linux security. In **Level 04**, you'll learn **text tools** — `grep`, `sed`, `awk`, `sort`, `uniq`, `wc`, `cut`, and `tr` — which let you search, filter, and manipulate text like a pro.
