# [10] systemd + capstone
> **Track:** Linux · **Level:** 10 · **Difficulty:** ★★★☆☆

## 1. Problem we're solving

When Linux boots, something has to start all the background services — networking, SSH, cron, display manager, and so on. Traditionally this was done by SysV init. Modern Linux uses **systemd** — a service manager that starts, stops, monitors, and logs everything. Understanding systemd is essential for deploying applications, managing services, and troubleshooting boot issues.

## 2. Core concept (absolute zero)

### What is systemd?

**systemd** is an init system and service manager. It's the first process (PID 1) that runs after the kernel boots. systemd:

- Starts services in parallel (faster boot)
- Tracks service dependencies
- Restarts crashed services
- Logs everything via **journald**
- Manages timers (like cron)
- Handles network, power management, and more

### Units

Everything systemd manages is a **unit**. Common unit types:

| Unit type | Extension | Purpose |
|-----------|-----------|---------|
| Service | `.service` | A daemon or application |
| Timer | `.timer` | Scheduled task (cron replacement) |
| Socket | `.socket` | Network or IPC socket |
| Mount | `.mount` | Filesystem mount point |
| Target | `.target` | Group of units (like runlevels) |

### systemctl

`systemctl` is the main command to interact with systemd.

## 3. Step-by-step breakdown (examples)

### `systemctl` — controlling services

Check status:

```
alice@xodex:~$ systemctl status sshd
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2026-07-23 10:00:01 MSK; 2h 30min ago
       Docs: man:sshd(8)
   Main PID: 789 (sshd)
      Tasks: 1 (limit: 2345)
     Memory: 5.2M
        CPU: 123ms
     CGroup: /system.slice/ssh.service
             └─789 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
```

Start, stop, restart:

```
alice@xodex:~$ sudo systemctl start nginx
alice@xodex:~$ sudo systemctl stop nginx
alice@xodex:~$ sudo systemctl restart nginx
alice@xodex:~$ sudo systemctl reload nginx        # reload config without stopping
```

Enable / disable (run at boot):

```
alice@xodex:~$ sudo systemctl enable nginx         # start at boot
alice@xodex:~$ sudo systemctl disable nginx        # don't start at boot
alice@xodex:~$ sudo systemctl is-enabled nginx     # check if enabled
```

List all running services:

```
alice@xodex:~$ systemctl list-units --type=service --state=running
```

List all services (including stopped):

```
alice@xodex:~$ systemctl list-units --type=service --all
```

Check if a service is active:

```
alice@xodex:~$ systemctl is-active sshd
active
```

### `journalctl` — viewing logs

systemd logs everything to a binary journal. `journalctl` reads it.

View all logs:

```
alice@xodex:~$ journalctl
```

View logs for a specific service:

```
alice@xodex:~$ journalctl -u ssh.service
```

Follow new log entries (like `tail -f`):

```
alice@xodex:~$ journalctl -u nginx.service -f
```

Logs since last boot:

```
alice@xodex:~$ journalctl -b
```

Logs since a specific time:

```
alice@xodex:~$ journalctl --since "1 hour ago"
alice@xodex:~$ journalctl --since "2026-07-23 08:00:00" --until "2026-07-23 10:00:00"
```

Show only kernel messages:

```
alice@xodex:~$ journalctl -k
```

Limit output lines:

```
alice@xodex:~$ journalctl -n 50
```

### Writing a `.service` unit file

Let's create a simple service that runs a Python web app.

Create the service unit at `/etc/systemd/system/xodex-web.service`:

```
[Unit]
Description=Xodex Web Application
After=network.target

[Service]
Type=simple
User=alice
WorkingDirectory=/home/alice/xodex-web
ExecStart=/usr/bin/python3 -m http.server 8080
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Explanation:

| Field | Meaning |
|-------|---------|
| `[Unit]` | Metadata and dependencies |
| `Description` | Human-readable name |
| `After=network.target` | Start after network is up |
| `[Service]` | How to run the service |
| `Type=simple` | Main process is ExecStart (default) |
| `User` | Run as this user (security!) |
| `WorkingDirectory` | Where to run the command |
| `ExecStart` | The command to run |
| `Restart=on-failure` | Auto-restart if it crashes |
| `RestartSec=5` | Wait 5 seconds before restart |
| `[Install]` | When to start at boot |
| `WantedBy=multi-user.target` | Start in normal multi-user mode |

Enable and start:

```
alice@xodex:~$ sudo systemctl daemon-reload           # reload unit files
alice@xodex:~$ sudo systemctl enable xodex-web.service # enable at boot
alice@xodex:~$ sudo systemctl start xodex-web.service  # start now
alice@xodex:~$ sudo systemctl status xodex-web.service # verify
```

### Timers (cron replacement)

systemd timers replace cron. You need two files:
- `.timer` — when to run
- `.service` — what to run

Create `/etc/systemd/system/backup.service`:

```
[Unit]
Description=Daily backup service

[Service]
Type=oneshot
ExecStart=/home/alice/scripts/backup.sh
```

Create `/etc/systemd/system/backup.timer`:

```
[Unit]
Description=Run backup daily at 2 AM

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Activate the timer:

```
alice@xodex:~$ sudo systemctl daemon-reload
alice@xodex:~$ sudo systemctl enable backup.timer
alice@xodex:~$ sudo systemctl start backup.timer
```

List active timers:

```
alice@xodex:~$ systemctl list-timers
NEXT                        LEFT     LAST                        PASSED  UNIT         ACTIVATES
Thu 2026-07-24 02:00:00 MSK 16h left n/a                         n/a     backup.timer  backup.service
```

More timer examples:

| OnCalendar expression | Meaning |
|----------------------|---------|
| `daily` | Every day at midnight |
| `hourly` | Every hour at 0 minutes |
| `weekly` | Every Monday at midnight |
| `Mon..Fri 09:00:00` | Weekdays at 9 AM |
| `*-*-1,15 00:00:00` | 1st and 15th of each month |
| `*:0/5` | Every 5 minutes |

### Capstone: automate a multi-step build process

Let's write a script that automates everything we've learned.

**The scenario**: You maintain a small web project. You need to:
1. Pull the latest code from a repo
2. Run tests
3. Build the project
4. Deploy it
5. Restart the service
6. Log everything
7. Notify on failure

Create `/home/alice/xodex-deploy/deploy.sh`:

```bash
#!/bin/bash

# Xodex Deployment Script
# Usage: ./deploy.sh [--dry-run]

set -euo pipefail   # safe mode: exit on error, undefined vars, pipe failures

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
BACKUP_DIR="/var/backups/xodex"
DEPLOY_DIR="/opt/xodex"
SERVICE_NAME="xodex-web.service"
LOG_FILE="/var/log/xodex-deploy.log"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
DRY_RUN=false

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $1"
    # Send alert (e.g., email, webhook)
    echo "Deploy failed at $(date)" | mail -s "Deploy FAILED: $1" admin@xodex.com || true
    exit 1
}

# Parse arguments
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=true
    log "DRY RUN MODE — no changes will be made"
fi

# Step 1: Check prerequisites
log "Step 1/5: Checking prerequisites..."

for cmd in git python3 systemctl; do
    if ! command -v "$cmd" &> /dev/null; then
        error_exit "Required command not found: $cmd"
    fi
done
log "  All prerequisites met"

# Step 2: Pull latest code
log "Step 2/5: Pulling latest code..."
if [ "$DRY_RUN" = false ]; then
    cd "$PROJECT_DIR"
    git pull origin main || error_exit "Git pull failed"
    log "  Updated to $(git rev-parse --short HEAD)"
else
    log "  [DRY RUN] Would run: git pull origin main"
fi

# Step 3: Run tests
log "Step 3/5: Running tests..."
if [ "$DRY_RUN" = false ]; then
    cd "$PROJECT_DIR"
    python3 -m pytest tests/ -v --tb=short 2>&1 | tee -a "$LOG_FILE" || error_exit "Tests failed"
    log "  All tests passed"
else
    log "  [DRY RUN] Would run: python3 -m pytest tests/"
fi

# Step 4: Build and deploy
log "Step 4/5: Building and deploying..."
if [ "$DRY_RUN" = false ]; then
    if [ -d "$DEPLOY_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        tar -czf "$BACKUP_DIR/xodex-backup-$TIMESTAMP.tar.gz" -C "$(dirname "$DEPLOY_DIR")" "$(basename "$DEPLOY_DIR")"
        log "  Backup saved"
    fi
    mkdir -p build && cp -r src/* build/
    sudo rsync -av --delete "$PROJECT_DIR/build/" "$DEPLOY_DIR/" 2>&1 | tail -3
    sudo chown -R alice:alice "$DEPLOY_DIR" && sudo chmod -R 755 "$DEPLOY_DIR"
    log "  Deployed to $DEPLOY_DIR"
else
    log "  [DRY RUN] Would build and deploy"
fi

# Step 5: Restart service
log "Step 5/5: Restarting service..."
if [ "$DRY_RUN" = false ]; then
    sudo systemctl daemon-reload
    sudo systemctl restart "$SERVICE_NAME" || error_exit "Service restart failed"
    sleep 2
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log "  Service $SERVICE_NAME is running"
    else
        journalctl -u "$SERVICE_NAME" -n 20 --no-pager
        error_exit "Service $SERVICE_NAME failed to start"
    fi
else
    log "  [DRY RUN] Would restart $SERVICE_NAME"
fi

log "Deployment completed successfully!"
```

Create the systemd service for this project (`/etc/systemd/system/xodex-web.service`):

```
[Unit]
Description=Xodex Web Application
After=network.target

[Service]
Type=simple
User=alice
Group=alice
WorkingDirectory=/opt/xodex
ExecStart=/usr/bin/python3 -m http.server 8080
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Set up the timer for automatic daily deployment:

Create `/etc/systemd/system/xodex-deploy.service`:

```
[Unit]
Description=Auto-deploy Xodex application

[Service]
Type=oneshot
ExecStart=/home/alice/xodex-deploy/deploy.sh
User=alice
```

Create `/etc/systemd/system/xodex-deploy.timer`:

```
[Unit]
Description=Deploy Xodex daily at 3 AM

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Final verification checklist:

```
# 1. Check the script
alice@xodex:~$ shellcheck deploy.sh

# 2. Dry run
alice@xodex:~$ ./deploy.sh --dry-run

# 3. Real deploy
alice@xodex:~$ ./deploy.sh

# 4. Check service
alice@xodex:~$ sudo systemctl status xodex-web.service

# 5. Check logs
alice@xodex:~$ journalctl -u xodex-web.service -f

# 6. Enable timer
alice@xodex:~$ sudo systemctl enable --now xodex-deploy.timer

# 7. List timers
alice@xodex:~$ systemctl list-timers

# 8. Verify deployment
alice@xodex:~$ curl http://localhost:8080
```

## 4. Common mistakes

| Mistake | Why it's wrong | Correct |
|---------|---------------|---------|
| Forgetting `systemctl daemon-reload` after editing unit | systemd doesn't see changes | Always reload after editing unit files |
| `Type=simple` for long-running setup scripts | systemd thinks the service is done after the script exits | Use `Type=oneshot` for scripts that exit |
| Not using absolute paths in `ExecStart` | systemd doesn't have a PATH | Always use full paths like `/usr/bin/python3` |
| Running service as root | Security risk | Create a dedicated user |
| `Restart=always` without `RestartSec` | May restart-loop on failure | Use `Restart=on-failure` with `RestartSec=5` |
| Not checking journalctl on failure | You miss the error message | Always run `journalctl -u service -n 50` |
| `set -e` in a script that runs commands you expect to fail | Script exits unexpectedly | Use `set -e` but handle expected failures with `|| true` |

## 5. Exercises

1. Check the status of the `sshd` service with `systemctl status sshd`.
2. View logs for the SSH service: `journalctl -u ssh.service -n 20`.
3. Create a simple service file that runs `echo "Hello from systemd" > /tmp/systemd-test.txt` on start.
4. Create a timer that runs the above service every minute. Check it with `systemctl list-timers`.
5. Use `journalctl --since "5 minutes ago"` to see recent system logs.
6. Enable a service to start automatically at boot.
7. Use `systemctl list-units --failed` to check for failed services.
8. Write the capstone deploy script from this lesson and test it with `--dry-run`.

## 6. Self-check questions

1. What is PID 1 on a modern Linux system?
2. What does `systemctl enable` do that `systemctl start` doesn't?
3. How do you view logs for a specific systemd service?
4. What is the difference between `Type=simple` and `Type=oneshot`?
5. After editing a unit file, what command must you run?
6. How do you schedule a recurring task with systemd?
7. What does `journalctl -u nginx.service -f` do?
8. How do you check which timers are active on the system?
9. What is the `[Install]` section of a unit file for?
10. How do you make a service restart automatically if it crashes?

## 7. What's next

You've completed all 11 Linux levels! You can navigate the filesystem, manage files and permissions, process text, chain commands with pipes, control processes, install packages, troubleshoot networking, write shell scripts, and manage services with systemd. The capstone project ties everything together into a real-world automated deployment pipeline. Try the SQL track next for database skills!
