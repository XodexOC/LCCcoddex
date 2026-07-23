# [01] Filesystem
> **Track:** Linux · **Level:** 01 · **Difficulty:** ★☆☆☆☆

## 1. Problem we're solving

You can run `ls /` and see a bunch of directories with strange names like `/bin`, `/etc`, `/proc`. What are they for? Why are they there? Understanding the Linux filesystem hierarchy is essential for navigating the system, finding files, configuring software, and troubleshooting. Without this map, you're wandering blind.

## 2. Core concept (absolute zero)

The Linux filesystem is a single tree starting at `/` (the root). Everything — files, devices, running processes — is represented as a file somewhere in this tree.

### The Filesystem Hierarchy Standard (FHS)

The FHS defines where things go. Here are the top-level directories you'll see:

| Directory | Purpose | Example contents |
|-----------|---------|-----------------|
| `/bin`    | Essential user command binaries (programs) | `ls`, `cp`, `mv`, `bash` |
| `/sbin`   | System/admin binaries | `fdisk`, `mkfs`, `mount` |
| `/usr`    | User system resources — the big one | `/usr/bin`, `/usr/lib`, `/usr/share` |
| `/etc`    | Configuration files (text files) | `/etc/passwd`, `/etc/ssh/sshd_config` |
| `/home`   | Users' personal directories | `/home/alice`, `/home/bob` |
| `/root`   | Root user's home directory | (not under `/home`) |
| `/var`    | Variable data that changes frequently | `/var/log/syslog`, `/var/spool/cron` |
| `/tmp`    | Temporary files (deleted on boot) | (anyone can write here) |
| `/proc`   | Virtual filesystem for processes and kernel | `/proc/cpuinfo`, `/proc/meminfo` |
| `/dev`    | Device files (hardware as files) | `/dev/sda`, `/dev/tty`, `/dev/null` |
| `/lib`    | Shared libraries (like DLLs on Windows) | `/lib/x86_64-linux-gnu/libc.so.6` |
| `/opt`    | Optional (third-party) software | `/opt/google/chrome` |
| `/mnt`    | Temporary mount points | `/mnt/usb` |
| `/media`  | Removable media mount points | `/media/cdrom` |

### Inodes: what are they?

Every file on a Linux filesystem has an **inode** (index node). The inode stores **metadata** about the file — everything **except its name and its data**.

What's in an inode:
- File type (regular file, directory, symlink, etc.)
- Permissions (rwx)
- Owner (UID) and group (GID)
- File size in bytes
- Timestamps: access (atime), modify (mtime), change (ctime)
- Number of hard links
- Pointers to the data blocks on disk

The **filename** is stored in the directory entry, not in the inode. The directory maps names to inode numbers.

### The `stat` command

`stat` shows the inode metadata for a file:

```
alice@xodex:~$ stat /etc/passwd
  File: /etc/passwd
  Size: 2654            Blocks: 8          IO Block: 4096   regular file
Device: 801h/2049d      Inode: 1310821     Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2026-01-15 10:30:45.000000000 +0300
Modify: 2026-01-10 08:22:12.000000000 +0300
Change: 2026-01-10 08:22:12.000000000 +0300
 Birth: 2024-06-01 12:00:00.000000000 +0300
```

- **Inode: 1310821** — the inode number (unique per filesystem)
- **Links: 1** — number of hard links pointing to this inode
- The three timestamps: access, modify, change

## 3. Step-by-step breakdown (examples)

### File types

In `ls -l`, the first character tells you the **file type**:

```
-rw-r--r--  1 alice alice   1024 Jan 15 10:00 file.txt   # - = regular file
drwxr-xr-x  2 alice alice   4096 Jan 15 10:00 dir/        # d = directory
lrwxrwxrwx  1 alice alice     24 Jan 15 10:00 link -> target  # l = symlink
brw-rw----  1 root  disk   8, 0 Jan 15 10:00 /dev/sda   # b = block device
crw-rw-rw-  1 root  root   1, 3 Jan 15 10:00 /dev/null  # c = character device
```

| Character | Type |
|-----------|------|
| `-` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |
| `b` | Block device (disks) |
| `c` | Character device (terminals, serial ports) |
| `p` | Named pipe (FIFO) |
| `s` | Socket |

### `ls -la` in detail

```
alice@xodex:~$ ls -la /etc/hostname
-rw-r--r-- 1 root root 16 Jan 10 08:20 /etc/hostname
│││││││ │ │    │    │    │        │
│││││││ │ │    │    │    │        └─ filename
│││││││ │ │    │    │    └─ modification date/time
│││││││ │ │    │    └─ size in bytes
│││││││ │ │    └─ group owner
│││││││ │ └─ owner (user)
│││││││ └─ number of hard links
││││││└─ other permissions (r--)
│││││└─ group permissions (r--)
││││└─ owner permissions (rw-)
│││└─ ACL indicator (space = no ACL, . = SELinux, + = ACL set)
││└─ file type (- = regular file)
│└─ sticky bit / setuid / setgid (usually empty)
└─ (sticky bit / setuid / setgid - advanced)
```

Let's break down `-rw-r--r--`:
- **Position 1**: file type (`-`)
- **Positions 2-4**: owner permissions (`rw-` = read + write, no execute)
- **Positions 5-7**: group permissions (`r--` = read only)
- **Positions 8-10**: others (everyone else) permissions (`r--` = read only)

### `df -h` — disk usage of filesystems

`df` (disk free) shows available disk space. `-h` makes it human-readable:

```
alice@xodex:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        98G   45G   53G  46% /
tmpfs           3.8G  1.2M  3.8G   1% /dev/shm
/dev/sdb1       250G  120G  130G  48% /mnt/backup
```

- **Filesystem** — the device or virtual filesystem
- **Size** — total capacity
- **Used** — space used
- **Avail** — space available to non-root users
- **Use%** — percentage used
- **Mounted on** — where it appears in the tree

### `du -sh` — directory sizes

`du` (disk usage) shows how much space a directory uses. `-s` gives a summary (not each subdirectory). `-h` is human-readable:

```
alice@xodex:~$ du -sh Documents
1.2G    Documents
```

```
alice@xodex:~$ du -sh *
1.2G    Documents
4.3M    Downloads
2.1G    Pictures
```

You can check specific directories:

```
alice@xodex:~$ du -sh /var/log
 85M    /var/log
```

Combine with `ls` to sort by size:

```
alice@xodex:~$ du -sh * | sort -rh
2.1G    Pictures
1.2G    Documents
4.3M    Downloads
```

### Navigating the hierarchy

```
alice@xodex:~$ cd /bin
alice@xodex:/bin$ ls | head -5
bash
cat
chmod
cp
dash
```

```
alice@xodex:/bin$ cd /etc
alice@xodex:/etc$ ls | head -5
adduser.conf
alternatives
apt
bash.bashrc
bindresvport.blacklist
```

```
alice@xodex:/etc$ cat /etc/hostname
xodex-pc
```

```
alice@xodex:/etc$ cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
```

```
alice@xodex:/etc$ cd /proc
alice@xodex:/proc$ ls | head -10
1/
4/
6/
acpi/
buddyinfo
bus/
cgroups
cmdline
cpuinfo
crypto/
```

```
alice@xodex:/proc$ cat /proc/cpuinfo | head -5
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 142
model name      : Intel(R) Core(TM) i7-10510U CPU @ 1.80GHz
```

```
alice@xodex:/proc$ cat /proc/meminfo | head -5
MemTotal:        8060220 kB
MemFree:         4123456 kB
MemAvailable:    6789012 kB
Buffers:          123456 kB
Cached:          2345678 kB
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Deleting `/etc` | Destroys system configuration | Never delete system directories |
| Writing to `/proc` or `/sys` | These are virtual — changes are transient or dangerous | Read only unless you know exactly what you're doing |
| `rm -rf /` from a script | Destroys the entire system | Always double-check paths in scripts; use `--no-preserve-root` guard |
| Confusing `/` (root) with `~` (home) | `/` is the top of the filesystem tree, `~` is your home directory | Remember: `/` is the root of everything |
| Thinking `/tmp` is permanent | `/tmp` is cleared on reboot | Use `/var/tmp` for persistent temp files |
| Ignoring `/var/log` filling up | Logs can consume all disk space | Monitor with `df -h` and set up log rotation |

## 5. Exercises

1. Run `ls -la /`. Identify the type of each entry (directory, file, symlink).
2. Use `stat` on `/etc/passwd`. What is its inode number? How many links does it have?
3. Find your home directory's inode with `stat ~`. What inode number is it?
4. Run `df -h`. How much space is free on your root filesystem?
5. Run `du -sh /var/log`. How much space do logs use?
6. List the contents of `/proc`. Find the file `cpuinfo` and check your processor information.
7. Navigate to `/usr/bin`. How many files are in this directory? (Hint: `ls | wc -l`)
8. Create a file in `/tmp`: Run `touch /tmp/test.txt`. Then `stat /tmp/test.txt`. Delete it with `rm /tmp/test.txt`.
9. What type of file is `/dev/null`? Check with `ls -l /dev/null`.
10. Use `cat /proc/meminfo` to find out your total RAM.
11. Run `ls -la /var/log`. How many log files are there? What are their sizes?
12. Go to `/etc`, run `ls -la`, and find a file you can read as a normal user. Use `cat` to read it.

## 6. Self-check questions

1. What is the purpose of the `/etc` directory?
2. What information does an inode store? What doesn't it store?
3. How do you determine the file type of `/dev/sda`?
4. What does `df -h` tell you that `ls` doesn't?
5. How does `du -sh` differ from `df -h`?
6. What is the root filesystem? Write its absolute path.
7. Why is `/proc` called a "virtual" filesystem?
8. What command shows inode metadata for a file?
9. What does the first character of `ls -l` output represent?
10. Under what directory would you find system log files?

## 7. What's next

You now know the filesystem map. In **Level 02**, you'll learn how to create, copy, move, and delete files and directories — the basic file operations that you'll use every single day.
