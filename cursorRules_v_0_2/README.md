# Cursor Agent Guidelines

## For Cursor Agents

This project uses a comprehensive `.cursor/` directory system to maintain consistent AI assistant behavior and project context. **All Cursor Agents working on this project MUST follow the rules and guidelines defined in the `.cursor/` directory.**

## .cursor Directory Overview

The `.cursor/` directory contains:

### 📁 **rules/** - AI Assistant Behavior Rules
- **6 specialized rule files** governing different aspects of AI behavior
- **Mandatory compliance** - these rules MUST be followed
- Covers command execution, timing, memory management, and safety protocols

### 📁 **memory/** - Cross-Cutting Insights  
- **`memory.md`** - Cross-cutting insights and reusable knowledge
- **Updated when discovering** architecture patterns, environment gotchas, or lessons learned
- Maintains valuable knowledge across multiple implementations and sessions

### 📁 **docs/** - Project Documentation
- **Implementation plans** - Detailed implementation plans for specific tasks
- **Setup guides** - Environment setup and dependency resolution guides
- Contains comprehensive progress tracking and lessons learned

### 📁 **patches/** - Backup and Recovery
- Previous implementation attempts and rollback capabilities
- Complete patch files for recovery if needed

## Critical Rules for Cursor Agents

### 🚨 **MANDATORY RULES**
1. **Memory Tracking**: Update `.cursor/memory/memory.md` with cross-cutting insights and reusable knowledge
2. **Implementation Tracking**: Update both memory.md and implementation files together
3. **Command Safety**: Never use unescaped `!` in shell commands
4. **Interactive Commands**: Use non-interactive flags (`--no-pager`, `| cat`, etc.)
5. **Long Commands**: Run extended operations in background (`is_background: true`)
6. **Filesystem Timing**: Check size before long filesystem operations

### 📋 **Project Status**
- Check `.cursor/memory/memory.md` for cross-cutting insights and patterns
- Review `.cursor/docs/` for specific implementation plans
- Follow established patterns documented in the implementation files

## Quick Start for New Agents

1. **Read the rules**: Start with `.cursor/rules/README.md`
2. **Check memory**: Review `.cursor/memory/memory.md` for cross-cutting insights and patterns
3. **Review implementation**: Read relevant files in `.cursor/docs/` for detailed plans
4. **Follow patterns**: Use established implementation patterns from documentation
5. **Update memory**: Add cross-cutting insights to `.cursor/memory/memory.md` when discovered

## Project Structure

```
[Project Root]/
├── README.md                               # Generic Cursor Agent guidelines
└── .cursor/                                # AI Assistant Rules & Documentation
    ├── docs/                               # Documentation directory
    │   ├── IMPLEMENTATION_AE_1159.md      # Detailed implementation plan for scanBoxId feature
    │   └── SETUP.md                       # Environment setup and dependency resolution guide
    ├── memory/                            # Cross-cutting insights
    │   └── memory.md                      # Cross-cutting insights and reusable knowledge
    ├── patches/                           # Backup and patch files
    │   ├── AE-1159_WIP_README.md         # Documentation for previous implementation attempt
    │   └── AE-1159_WIP.patch             # Git patch file of previous implementation (4.1MB)
    └── rules/                             # AI assistant behavior rules
        ├── README.md                      # Rules overview and usage guidelines
        ├── extended-time-commands.md     # Rule for running long commands in background
        ├── filesystem-command-timing.md  # Rule for filesystem operation timing
        ├── implementation-tracking.md    # Rule for Jira task progress tracking
        ├── interactive-commands.md       # Rule for non-interactive command execution
        ├── memory-tracking.md            # Rule for maintaining session memory
        └── no-unescaped-exclamation.md  # Rule for safe text output
```

## Environment Requirements

- Check `.cursor/docs/SETUP.md` for specific environment requirements
- Review `.cursor/memory/memory.md` for environment gotchas and solutions
- Follow setup guides in `.cursor/docs/` for proper configuration

---

**⚠️ IMPORTANT**: This project has specific rules and patterns that have been developed through extensive analysis. Always follow the `.cursor/` directory guidelines to maintain consistency and avoid repeating previous mistakes.

**📚 For detailed information**: See `.cursor/rules/README.md` for complete rule explanations and `.cursor/docs/` for specific implementation plans and setup guides.