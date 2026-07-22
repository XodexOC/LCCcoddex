# Xodex Directory Structure

```
/Xodex
├── iso/                  # Debian ISO build configuration
│   ├── config/           # Live build configs
│   ├── packages/         # Package configurations
│   └── hooks/            # Customization scripts
│
├── core/                 # Core system components
│   ├── system/           # Core system files
│   ├── config/           # System configurations
│   └── scripts/          # Core utilities
│
├── docs/                 # Documentation system
│   ├── ru/               # Russian documentation
│   └── en/               # English documentation
│
├── library/              # Reference materials
│   ├── books/            # Book references
│   ├── references/       # External references
│   └── links/            # Online resource links
│
├── modules/              # Optional modules
│   ├── c/                # C programming
│   ├── python/           # Python programming
│   ├── rust/             # Rust programming
│   └── linux/            # Linux internals
│
├── examples/             # Example code
│
├── tools/                # Development tools
│
├── scripts/              # Build/maintenance scripts
│
└── themes/               # Terminal color schemes
```

## Key Files
- `iso/config/package-lists/` - Core package selections
- `core/config/hooks/` - System customization
- `docs/*/links.json` - Documentation graph connections
