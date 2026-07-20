# Xodex Architecture

## Core Components

### Xodex Core
- Minimal Debian-based system
- Terminal environment with:
  - Basic development tools
  - System exploration utilities
  - Documentation browser

### ISO Builder
- Debian live image configuration
- Package selection:
  - Base system
  - Development tools
  - Documentation tools
- Custom hooks for:
  - User environment setup
  - Default configurations

### Documentation System
- Local materials:
  - Fundamental concepts
  - Examples
  - How-to guides
- Online references:
  - Man pages
  - Official docs
  - External books
- Bilingual structure (RU/EN)
- Knowledge graph navigation

### External Repository
- Optional components:
  - Additional languages
  - Specialized tools
  - Extended documentation
- Installable via `xodex install`

## Three Layer Model

### Layer 1: Xodex Core
Minimal system:
- Debian base
- Shell environment
- Documentation engine
- Basic development tools

### Layer 2: Knowledge Repository
Materials:
- Documentation
- Examples
- References
- Book links
- Source explanations

### Layer 3: Extensions
Optional modules:
- Python
- Rust
- C++
- JavaScript
- SQL
- Networking
- Security

Core principle:
Core must remain small.
User chooses their extensions.

## Design Constraints
1. No GUI dependencies in Core
2. All documentation accessible via CLI
3. No mandatory components beyond Core
4. Clear separation between:
   - System fundamentals
   - Optional additions
