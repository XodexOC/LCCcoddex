# Xodex ISO Design

## 1. Purpose
The Xodex ISO provides a portable Debian-based UNIX laboratory for:
- Learning computer fundamentals
- Exploring Linux internals
- Systems programming
- Safe experimentation

It is not a general-purpose distribution but a focused educational environment.

## 2. ISO Layers

### Layer 1: Debian Base
- Linux kernel (Debian stable)
- Systemd init system
- GNU core utilities
- Basic networking
- Minimal XZ tools

### Layer 2: Xodex Core
- Custom terminal environment
- Documentation browser
- User configuration:
  - Shell (bash with extensions)
  - Editor (nano + micro)
  - Pager (less with colors)
- System exploration tools

### Layer 3: Knowledge Base
- Core documentation (RU/EN)
- Example programs
- Man pages
- Reference cards
- System manuals

### Layer 4: Optional Extensions
Installable via `xodex install`:
- Programming languages (C, Python, Rust)
- Development tools
- Advanced research packages

## 3. Target Hardware
Minimum:
- Architecture: x86_64
- Boot: BIOS/UEFI
- RAM: 512MB
- Storage: 2GB

Recommended:
- RAM: 1GB+
- Storage: 5GB+
- CPU: 2+ cores

## 4. Package Philosophy

### Core Packages (Required)
- linux-image
- systemd
- bash
- coreutils
- nano
- man-db
- less

### Module Packages (Optional)
- gcc
- make
- binutils
- gdb
- strace
- procps

Each package must:
- Serve clear educational purpose
- Not hide system complexity
- Be documented in Xodex knowledge base

## 5. User Environment

First boot sequence:
1. Boot to console
2. Auto-login as `student`
3. Start customized bash shell
4. Show welcome message

User home contains:
- ~/docs/ - Local documentation
- ~/examples/ - Code examples
- ~/.xodex/ - User progress and configs

Shell features:
- Color prompts
- Documentation shortcuts
- Enhanced tab completion
- Quick access to examples

## 6. No GUI Principle
Core ISO intentionally avoids GUI to:
- Focus on terminal skills
- Reduce system complexity
- Minimize dependencies
- Stay true to UNIX philosophy

Allowed terminal enhancements:
- 256-color support
- UTF-8 characters
- Code highlighting
- Pager navigation

## 7. Offline First
Included in ISO:
- Core documentation
- Man pages
- Example programs
- Basic development tools
- System exploration utilities

Online-only:
- Additional books
- Language documentation
- Kernel source code
- Community resources

## 8. Build System Structure
```
/iso
├── config/            # Live build configs
│   ├── package-lists/ # Package selections
│   └── includes/      # Custom files
├── packages/          # Local packages
├── hooks/             # Customization scripts
├── filesystem/        # Overlay files
└── scripts/           # Build utilities
```

## 9. ISO Variants

### Xodex Core ISO
- Minimal system
- Basic tools
- Core documentation

### Xodex Developer ISO
- Adds:
  - Full development toolchain
  - Additional languages
  - Debugging tools

### Xodex Research ISO
- Adds:
  - Kernel headers
  - System tracing tools
  - Advanced debugging

## 10. Design Rules
1. **Minimalism** - Only what's essential for learning
2. **Transparency** - No hidden automation
3. **Control** - User owns the system
4. **Explainability** - Every component documented
5. **Consistency** - Follow UNIX philosophy
