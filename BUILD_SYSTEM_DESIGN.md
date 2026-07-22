# Xodex Build System Design

## 1. Purpose
The build system creates reproducible Xodex ISO images while:
- Maintaining complete transparency
- Allowing component modification
- Documenting the build process
- Following UNIX philosophy

Core principle: "From configuration to ISO should be fully traceable"

## 2. Build Architecture
```
Source Repository
↓
Configuration
↓
Debian Base
↓
Package Installation
↓
Xodex Customization
↓
Documentation Integration
↓
ISO Generation
↓
Testing
```

## 3. Repository Structure
```
/build/
├── config/        # Build configurations
├── packages/      # Package selections
├── hooks/         # Customization scripts
├── overlays/      # Filesystem overlays
├── scripts/       # Build utilities
├── tests/         # Test cases
└── output/        # Generated ISOs
```

## 4. Build Configuration
`config/build.yaml` contains:
```yaml
debian:
  version: "bookworm"
  architecture: "amd64"
  mirror: "http://deb.debian.org/debian"
  
xodex:
  modules: ["core", "c", "linux"]
  locale: "en_US.UTF-8"
  timezone: "UTC"
  user:
    name: "student"
    password: "xodex"
```

## 5. Package Management
### Package Categories:
1. **Base Packages**
   - Essential system components
   - Small footprint
   - Documented in core docs

2. **Development Packages**
   - Compilers and tools
   - Debugging utilities
   - Size/benefit justified

3. **Research Packages**
   - System inspection tools
   - Kernel development
   - Advanced debugging

Each package requires:
- Justification in docs
- Size documentation
- Dependency mapping

## 6. Build Tools
### Options Considered:
1. **Debian live-build**
   - (+) Official Debian tool
   - (+) Mature and stable
   - (-) Complex configuration

2. **debootstrap + custom**
   - (+) More control
   - (+) Simpler debugging
   - (-) More manual work

Selected approach:
- live-build for main ISO
- Custom scripts for modules

## 7. Testing System
### ISO Boot Test:
- Boot in QEMU
- Verify:
  - Auto-login
  - Shell environment
  - Basic commands

### System Test:
- Package verification
- Command availability
- Documentation access

### Educational Test:
- Example execution
- Documentation navigation
- Module functionality

## 8. Release Versions
### Xodex Alpha
- Experimental builds
- Frequent changes
- Testing focus

### Xodex Beta
- Stable environment
- Core features complete
- Educational focus

### Xodex Stable
- Production-ready
- Thoroughly tested
- Long-term support

## 9. Development Workflow
```
Documentation/Code Change
↓
Git Commit
↓
Automated Build
↓
Test Suite
↓
Release Candidate
↓
Final ISO
```

## 10. Build Rules
1. **Reproducibility** - Same config → same ISO
2. **Version Control** - All changes via Git
3. **No Manual ISO Edits** - Only through build system
4. **Configuration First** - Source over binaries
5. **Purposeful Components** - No unused packages
