# Xodex User and Security Design

## 1. Philosophy
Xodex is designed for learning and exploration. Security must:
- Protect against accidental damage
- Not hide Linux internals
- Allow root access for study
- Enable safe experimentation

Core principle: "Safe to break, easy to restore"

## 2. User Model

### Student User
Primary user account:
- Home: /home/student
- Purpose:
  - Programming
  - Documentation study
  - System exploration
- Default shell: bash with Xodex extensions

### Root Access
Administrative account:
- Purpose:
  - System configuration
  - Kernel experiments
  - Security study
- Access:
  - Direct login disabled
  - Available via `sudo`
  - Requires explicit user action

Educational rationale:
Root access is essential for:
- Understanding Linux security model
- Studying system administration
- Conducting advanced experiments

## 3. Default Permissions
```
/home/student/
├── projects/    # User projects (rwx)
├── examples/    # Example code (r-x)
├── notes/       # User notes (rwx)
├── docs/        # Local docs (r-x)
└── .xodex/      # Configs and progress (rwx)
```

System files:
- /etc/ - Read-only for student
- /var/ - Limited access
- /proc/ - Read-only for study

## 4. Recovery System
Xodex Recovery Mode provides:
1. System snapshot restoration
2. Configuration reset
3. Root shell access
4. System integrity check

Future commands:
```bash
xodex recovery          # Enter recovery mode
xodex snapshot create   # Create system snapshot
xodex snapshot restore  # Restore from snapshot
```

## 5. Snapshots
Snapshot features:
- Manual creation
- Automatic daily snapshots
- Storage: /var/lib/xodex/snapshots/
- Technologies:
  - Btrfs snapshots (preferred)
  - Timeshift-like approach
  - Filesystem-level backups

Usage example:
```bash
xodex snapshot create before_kernel_test
# Experiment with kernel
xodex snapshot restore before_kernel_test
```

## 6. Network Security
Default network configuration:
- No open ports
- SSH disabled by default
- Minimal network services

Educational access:
```bash
xodex network enable ssh  # Enable SSH for study
xodex network disable ssh # Disable SSH
```

## 7. Educational Security
Xodex exposes:
- Running processes
- File permissions
- System services
- Access controls
- System logs

Tools:
```bash
xodex processes  # View processes
xodex logs       # View system logs
xodex files      # Explore file permissions
```

## 8. Backup Strategy
Backed up:
- User projects
- Notes
- Xodex configurations
- Documentation progress

Not backed up:
- Temporary files
- Package cache
- System logs

## 9. Privacy
Privacy principles:
- No telemetry
- No mandatory accounts
- Local-only progress storage
- Clear data collection policy

## 10. Security Rules
1. User controls the system
2. All automated actions are explained
3. No hidden services
4. Recovery prioritized over prevention
5. User mistakes are part of learning
