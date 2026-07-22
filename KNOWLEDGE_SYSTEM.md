# Xodex Knowledge System

## 1. Purpose
The documentation system is designed as a knowledge graph, not a linear course. It allows:
- Non-linear topic exploration
- Progressive depth of understanding
- Natural learning paths
- Connection between concepts

## 2. Directory Structure
```
/docs
├── ru/                  # Russian materials
│   ├── linux/
│   ├── c/
│   └── ...
└── en/                  # English materials
    ├── linux/
    ├── c/
    └── ...
```

Each topic has parallel versions:
- `docs/en/linux/processes.md`
- `docs/ru/linux/processes.md`

## 3. Article Format
Each article contains:

```yaml
# metadata.yaml (optional)
title: "Processes"
level: [beginner, intermediate, advanced]
prerequisites:
  - filesystem
  - users
related:
  - threads
  - signals
references:
  - man:fork(2)
  - book: "Advanced Unix Programming"
examples:
  - /examples/process/fork.c
```

Main content (Markdown):
```markdown
# Processes

## Beginner Level
Explanation using simple analogies...

## Intermediate Level
Technical details with examples...

## Advanced Level
Kernel implementation notes...
```

## 4. Explanation Levels
Three-tiered approach:

1. **Beginner**
   - Simple analogies
   - Practical usage
   - No jargon

2. **Intermediate**  
   - Technical specifications
   - Code examples
   - System interactions

3. **Expert**
   - Kernel source references
   - Standards (POSIX)
   - Architecture diagrams

## 5. Bilingual System
Principles:
- Russian materials focus on initial learning
- English materials provide deeper technical details
- All key terms include original English names
- Gradual transition to English documentation

## 6. References System
Reference types:
- **Local**: Cross-linked Xodex docs
- **Man Pages**: Built-in documentation
- **Books**: Recommended literature
- **Standards**: POSIX, ISO C etc.
- **Source Code**: Linux kernel references

## 7. Documentation Access
Basic CLI viewer:
```bash
xodex docs memory          # View topic
xodex docs --list          # List available topics
```

## 8. Metadata Standard
Proposed format:
```yaml
# metadata.yaml
title: "Virtual Memory"
category: "linux/memory"
language: en/ru
tags:
  - memory
  - kernel
  - paging
links:
  prerequisites:
    - memory-management
  related:
    - mmap
    - page-cache
  references:
    - man:mmap(2)
    - book: "Understanding Linux Kernel"
```

## 9. Core Principles
1. **Explain "why"** - Not just how things work, but why they're designed that way
2. **Connect concepts** - Show relationships between topics
3. **Scale depth** - Support from beginner to engineer level
4. **Stay authentic** - Link to primary sources
5. **Encourage exploration** - Make navigation intuitive
