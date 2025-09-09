# Cursor Rules Overview

This directory contains rules and guidelines for AI assistant behavior when working on the Alix Estate Manager project.

## Rule Files Summary

### 1. `memory-tracking.md`
**Purpose**: Maintain comprehensive session memory
**Key Requirements**:
- Update `.cursor/memory/memory.md` after each significant action
- Track progress, decisions, issues, and lessons learned
- Include current status, environment state, and next steps
- Document all file modifications and key discoveries

### 2. `implementation-tracking.md`
**Purpose**: Track detailed implementation progress for Jira tasks
**Key Requirements**:
- Create `IMPLEMENTATION_[Jira task name].md` files in `.cursor/docs/`
- Update both memory.md and implementation files together
- Document comprehensive progress, code changes, and decisions
- Maintain task-specific detailed documentation

### 3. `no-unescaped-exclamation.md`
**Purpose**: Prevent shell command issues with exclamation marks
**Key Requirements**:
- Never use unescaped `!` in shell commands
- Use `\!` or single quotes to escape exclamation marks
- Prevents bash history expansion errors

### 4. `interactive-commands.md`
**Purpose**: Handle interactive commands properly
**Key Requirements**:
- Use `--yes` or `--non-interactive` flags for non-interactive execution
- Avoid commands that require user input
- Use background mode for long-running processes

### 5. `extended-time-commands.md`
**Purpose**: Handle time-consuming operations
**Key Requirements**:
- Use `is_background: true` for long-running commands
- Provide progress updates for extended operations
- Allow user to continue working while commands run

### 6. `filesystem-command-timing.md`
**Purpose**: Optimize filesystem operations
**Key Requirements**:
- Use appropriate tools for different file operations
- Batch file operations when possible
- Consider performance implications of file operations

## Usage Guidelines

### When Starting a New Session
1. Read `memory-tracking.md` to understand current project state
2. Check for existing implementation files for current tasks
3. Review any pending work or issues from previous sessions

### During Development Work
1. Follow `implementation-tracking.md` for Jira task work
2. Apply `no-unescaped-exclamation.md` for shell commands
3. Use `interactive-commands.md` for automated processes
4. Apply `extended-time-commands.md` for long operations
5. Follow `filesystem-command-timing.md` for file operations

### After Each Work Session
1. Update memory.md with session summary
2. Update relevant implementation files with progress
3. Document any new issues or discoveries
4. Note next steps for future sessions

## Rule Priority
1. **Safety First**: Always follow `no-unescaped-exclamation.md` and `interactive-commands.md`
2. **Documentation**: Maintain `memory-tracking.md` and `implementation-tracking.md`
3. **Performance**: Apply `extended-time-commands.md` and `filesystem-command-timing.md`

## File Locations
- **Rules**: `.cursor/rules/`
- **Memory**: `.cursor/memory/memory.md`
- **Implementation Docs**: `.cursor/docs/IMPLEMENTATION_[Task].md`
- **General Docs**: `.cursor/docs/`

## Maintenance
- Review and update rules as project evolves.  Note: **Any changes to the rules *HAVE TO* be approved by the user**
- Add new rules for recurring patterns or issues
- Ensure rules remain relevant and helpful
- Document any rule changes in this README
