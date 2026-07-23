# [06] Processes
> **Track:** Linux · **Level:** 06 · **Difficulty:** ★★☆☆☆

## 1. Problem we're solving

When you run a program, it becomes a **process** — a running instance. A Linux system runs hundreds of processes simultaneously. You need to know: which processes are running? How much CPU/memory are they using? How to stop a frozen program? How to run tasks in the background? How to keep a process alive after you log out?

## 2. Core concept (absolute zero)

### What is a process?

A **process** is a running instance of a program. Each process has:

- **PID** — Process ID (a unique number)
- **PPID** — Parent Process ID (who started it)
- **UID** — User ID that owns the process
- **State** — running, sleeping, stopped, zombie
- **Memory** — how much RAM it's using
- **CPU** — how much processor time it's consuming

### Process lifecycle

```
Program (on disk)  →  Process (in memory)  →  Termination
       │                    │                       │
   ./script.sh        PID 1234 running         exit code 0
```

- A process can create children (fork)
- The parent waits for the child, or the child is adopted by `init` (PID 1) if the parent dies
- Zombie process: child finished but parent hasn't collected exit status

### Signals

Signals are messages sent to a process to control it:

| Signal | Number | Meaning |
|--------|--------|---------|
| SIGTERM | 15 | Politely ask to terminate (default) |
| SIGKILL | 9 | Force kill (cannot be caught/ignored) |
| SIGINT | 2 | Interrupt (like Ctrl+C) |
| SIGSTOP | 19 | Pause the process (like Ctrl+Z) |
| SIGCONT | 18 | Continue a stopped process |

## 3. Step-by-step breakdown (examples)

### `ps` — process snapshot

`ps` (process status) shows running processes.

Basic:

```
alice@xodex:~$ ps
  PID TTY          TIME CMD
 1234 pts/0    00:00:00 bash
 5678 pts/0    00:00:00 ps
```

- **PID**: process ID
- **TTY**: terminal the process is connected to
- **TIME**: total CPU time used
- **CMD**: command that started the process

`ps aux` — detailed view of all processes:

```
alice@xodex:~$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.4 168092 11920 ?        Ss   10:00   0:03 /sbin/init
root       456  0.0  0.2  78564  5844 ?        Ss   10:00   0:00 /usr/sbin/sshd
alice     1234  0.0  0.1  22876  4568 pts/0    Ss   10:05   0:00 -bash
alice     5678  0.0  0.0  41672  3420 pts/0    R+   10:10   0:00 ps aux
```

Columns:
- **%CPU**: CPU usage percentage
- **%MEM**: memory usage percentage
- **VSZ**: virtual memory size (KB)
- **RSS**: resident set size (physical memory, KB)
- **STAT**: process state (R=running, S=sleeping, Z=zombie)
- **START**: time the process started

`ps -ef` — another common format:

```
alice@xodex:~$ ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 10:00 ?        00:00:03 /sbin/init
root       456     1  0 10:00 ?        00:00:00 /usr/sbin/sshd
alice     1234   456  0 10:05 pts/0    00:00:00 -bash
```

`ps` with options to show a tree:

```
alice@xodex:~$ ps auxf
```

Shows parent-child relationships with ASCII tree lines.

### `top` — interactive process viewer

`top` refreshes every few seconds and shows live system stats:

```
alice@xodex:~$ top
top - 10:15:01 up 1:23, 2 users, load average: 0.08, 0.03, 0.01
Tasks: 123 total,   1 running, 122 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.3 us,  0.7 sy,  0.0 ni, 96.7 id,  0.3 wa
MiB Mem :   7864.5 total,   4123.4 free,   2345.6 used,   1395.5 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   5210.9 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 alice     20   0  22876   4568   3456 S   0.0   0.1   0:00.23 bash
 5678 alice     20   0  41672   3420   2800 R   0.0   0.0   0:00.12 top
```

While `top` is running:
- `q` — quit
- `k` — kill a process (prompts for PID)
- `u` — filter by user
- `P` — sort by CPU
- `M` — sort by memory
- `1` — toggle per-core CPU

### `htop` — enhanced `top`

`htop` is a modern version with colors, mouse support, and scroll:

```
alice@xodex:~$ htop
```

(If not installed: `sudo apt install htop`)

### `kill` — send signals

```
alice@xodex:~$ kill 1234          # send SIGTERM (15) — polite termination
alice@xodex:~$ kill -9 1234       # send SIGKILL (9) — force kill
alice@xodex:~$ kill -15 1234      # SIGTERM explicitly
alice@xodex:~$ kill -SIGTERM 1234 # same, by name
```

`killall` — kill by name:

```
alice@xodex:~$ killall firefox    # kill all processes named "firefox"
alice@xodex:~$ killall -9 chrome  # force kill all chrome processes
```

`pkill` — kill by pattern:

```
alice@xodex:~$ pkill -f "python server.py"   # kill by full command line
```

### Background and foreground

Running in the background with `&`:

```
alice@xodex:~$ sleep 100 &
[1] 12345
```

The command runs in the background. You get a job number `[1]` and PID `12345`.

Check background jobs:

```
alice@xodex:~$ jobs
[1]+  Running                 sleep 100 &
```

Bring a job to the foreground:

```
alice@xodex:~$ fg %1
sleep 100
```

(Press `Ctrl+C` to kill it now.)

Put a currently running job into the background:

1. Press `Ctrl+Z` to suspend (stop) the job:

```
alice@xodex:~$ sleep 100
^Z
[1]+  Stopped                 sleep 100
```

2. Resume in the background with `bg`:

```
alice@xodex:~$ bg %1
[1]+ sleep 100 &
```

### Keyboard shortcuts for signals

| Key | Signal | Action |
|-----|--------|--------|
| `Ctrl+C` | SIGINT | Interrupt (kill foreground process) |
| `Ctrl+Z` | SIGTSTP | Suspend (stop) foreground process |
| `Ctrl+D` | EOF | Close stdin (often exits shell) |
| `Ctrl+\` | SIGQUIT | Quit with core dump |

### `nohup` — ignore hangup signals

If you close the terminal, the shell sends SIGHUP to its child processes, which usually kills them. `nohup` makes the process immune:

```
alice@xodex:~$ nohup long-running-script.sh &
[1] 12345
nohup: ignoring input and appending output to 'nohup.out'
```

- Process keeps running even after you log out
- Output goes to `nohup.out` by default

### `/proc` filesystem

Every process has a directory in `/proc`:

```
alice@xodex:~$ ls /proc/1/
attr/       cwd/       fd/        mem        root/      task/
autogroup   environ    fdinfo/    mounts     sched      timers
auxv        exe        gid_map    net/       sessionid  uid_map
cgroup      fd/        io         ns/        smaps      wchan
```

Useful proc entries:

```
alice@xodex:~$ cat /proc/1/cmdline    # command line of PID 1
/sbin/init

alice@xodex:~$ cat /proc/$$/status    # $$ is your shell's PID
Name:   bash
Pid:    1234
...
VmRSS:       4568 kB
```

```
alice@xodex:~$ ls -l /proc/$$/fd/     # file descriptors of current shell
total 0
lrwx------ 1 alice alice 64 Jan 15 10:00 0 -> /dev/pts/0
lrwx------ 1 alice alice 64 Jan 15 10:00 1 -> /dev/pts/0
lrwx------ 1 alice alice 64 Jan 15 10:00 2 -> /dev/pts/0
```

- `0` = stdin, `1` = stdout, `2` = stderr
- All pointing to the terminal (`/dev/pts/0`)

### Running at startup

To run a command at a specific time, use `at`:

```
alice@xodex:~$ echo "backup.sh" | at 2:00 AM
```

To run commands periodically, use `cron` (covered in Level 10).

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| `kill -9` as first resort | Doesn't give process chance to clean up | Try `kill` (SIGTERM) first, then `kill -9` |
| `kill 1234` when you mean `killall firefox` | Kills PID 1234 (which might not be firefox) | Use `killall` or `pkill` for name-based |
| Forgetting `&` for background | Process blocks your terminal | Append `&`: `command &` |
| Closing terminal without `nohup` | Background jobs die with SIGHUP | Use `nohup` or `disown` |
| `kill -9` on PID 1 (init) | Crashes the system | Never kill PID 1 unless you're shutting down |
| Ctrl+Z instead of Ctrl+C | Suspends, doesn't kill — process still exists in memory | Use `fg` then `Ctrl+C`, or `kill %1` |

## 5. Exercises

1. Run `ps aux`. How many processes are running? Find the one with the highest memory usage.
2. Run `top`. What's the CPU load average? Press `q` to quit.
3. Start `sleep 300` in the background with `&`. Check it with `jobs`.
4. Bring the sleep job to the foreground with `fg`. Suspend it with `Ctrl+Z`. Resume it in the background with `bg`.
5. Kill the sleep job with `kill %1`.
6. Run `nohup sleep 200 &`. Check that `nohup.out` was created. Close the terminal, reopen it, and check that the process is still running with `ps aux | grep sleep`.
7. Use `ps auxf` to see the process tree. Find the parent of your shell.
8. Read `cat /proc/cpuinfo` and `cat /proc/meminfo`. What CPU and RAM does your system have?
9. Check the file descriptors of your current shell: `ls -l /proc/$$/fd/`.
10. Run a persistent command like `ping 8.8.8.8` and stop it with `Ctrl+C`.
11. Use `ps aux | grep` to find the PID of your shell. Then use `kill` on it (what happens?).
12. Use `htop` if installed. Compare it to `top`.

## 6. Self-check questions

1. What is a PID? What is a PPID?
2. What is the difference between SIGTERM and SIGKILL?
3. How do you run a command in the background?
4. What does `Ctrl+Z` do to a foreground process?
5. How do you reattach a background job to the foreground?
6. What does `nohup` do?
7. How can you see a list of all processes on the system?
8. How do you view kernel and process info through the filesystem?
9. What file in `/proc` shows your shell's current memory usage?
10. How do you send a specific signal to a process by name?

## 7. What's next

You can monitor, control, and manage processes like a sysadmin. In **Level 07**, you'll learn about **package management** — installing, updating, and removing software with `apt`, `dpkg`, and repositories.
