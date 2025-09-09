# Migration Guide: v0.1 to v0.2 Cursor Agent Rules

## Overview

This guide helps you migrate an existing Cursor Agent from v0.1 (session-based memory) to v0.2 (cross-cutting insights) without losing your current context or starting over.

## Key Differences Between Versions

### v0.1 (Session-Based Memory)
- **Memory Focus**: Current task progress and session state
- **Memory Content**: Specific implementation details, current status, next steps
- **Memory Updates**: After each significant action
- **Memory Purpose**: Maintain continuity across work sessions

### v0.2 (Cross-Cutting Insights)
- **Memory Focus**: Reusable knowledge and architectural patterns
- **Memory Content**: Lessons learned, environment gotchas, implementation patterns
- **Memory Updates**: When discovering architecture patterns or lessons learned
- **Memory Purpose**: Maintain valuable knowledge across multiple implementations

## Migration Steps

### Step 1: Backup Current Context
Before making any changes, preserve your current agent's context:

```bash
# In your current project directory
cp .cursor/memory/memory.md .cursor/memory/memory_v0_1_backup.md
```

### Step 2: Copy New Version Files
Copy the updated files from v0.2 to your project:

```bash
# Copy the new README (if you want the updated version)
cp /path/to/cursorRules_v_0_2/README.md .cursor/rules/README.md

# Copy all rule files (they're the same, but ensures consistency)
cp /path/to/cursorRules_v_0_2/.cursor/rules/* .cursor/rules/

# Copy the new memory template
cp /path/to/cursorRules_v_0_2/.cursor/memory/memory.md .cursor/memory/memory_v0_2_template.md
```

### Step 3: Extract Cross-Cutting Insights
Review your v0.1 memory and extract reusable knowledge:

**From your current memory, identify:**
- Architecture patterns discovered
- Environment gotchas and solutions
- Implementation methodologies that worked
- Common issues and their solutions
- Critical commands and procedures
- Authentication/access information
- Environment configuration details

### Step 4: Create New Memory Structure
Create your new v0.2 memory by combining:

1. **Cross-cutting insights** from your v0.1 memory
2. **Architecture patterns** you've discovered
3. **Environment gotchas** you've encountered
4. **Key lessons learned** from your implementation

### Step 5: Tell Your Agent to Reload

Send this message to your existing Cursor Agent:

```
I've updated the .cursor directory to version 0.2. The memory system has changed from session-based tracking to cross-cutting insights. Please:

1. Read the new .cursor/rules/README.md to understand the updated guidelines
2. Read the new .cursor/memory/memory.md template to understand the new memory structure
3. Review my backup memory at .cursor/memory/memory_v0_1_backup.md
4. Extract any cross-cutting insights, architectural patterns, environment gotchas, or lessons learned from the backup
5. Update .cursor/memory/memory.md with the extracted insights, following the v0.2 structure
6. Continue with our current work using the new memory system

The key change is that memory should now focus on reusable knowledge rather than current task progress.
```

### Step 6: Verify Migration
After your agent processes the migration:

1. **Check memory structure**: Verify `.cursor/memory/memory.md` follows v0.2 format
2. **Verify rules**: Ensure all rule files are updated
3. **Test functionality**: Continue with your current work to ensure everything works

## Example Migration

### Before (v0.1 Memory):
```markdown
## Current Task
**Fresh Implementation of AE-1159**: Implementing `scanBoxId` field for estates...

## Progress Made ✅
- ✅ Resolved dependency conflicts using `npm install --legacy-peer-deps`
- ✅ Created comprehensive `.env` file...
```

### After (v0.2 Memory):
```markdown
## Architecture Patterns Discovered

### Field Implementation Patterns
- **Estate Email Pattern**: Field added directly to Estate model with @unique constraint
- **taxId Pattern**: Field added via migration, nullable initially, unique constraint added later
- **scanBoxId Pattern**: Auto-generated on backend during estate creation, display-only in frontend

## Environment Gotchas

### Dependency Resolution
- **Always use**: `npm install --legacy-peer-deps` for frontend dependencies
- **MUI Lab conflicts**: React 19 vs MUI Lab compatibility resolved with legacy peer deps
- **Backend requires Node 22+**: Use nvm to switch versions
```

## Benefits of Migration

1. **Preserve Knowledge**: Keep all your hard-earned insights and patterns
2. **Improve Reusability**: Knowledge becomes transferable across projects
3. **Better Organization**: Focus on architectural patterns rather than task details
4. **Enhanced Collaboration**: Other agents can benefit from your discoveries
5. **Future-Proof**: v0.2 structure is more maintainable long-term

## Troubleshooting

### If Migration Fails:
1. **Restore backup**: `cp .cursor/memory/memory_v0_1_backup.md .cursor/memory/memory.md`
2. **Check file permissions**: Ensure all files are readable
3. **Verify paths**: Make sure you're copying from the correct v0.2 directory

### If Agent Doesn't Understand:
1. **Be explicit**: Tell the agent exactly what to read and where
2. **Provide examples**: Show the difference between v0.1 and v0.2 memory
3. **Guide the process**: Walk through each step if needed

## Success Criteria

Your migration is successful when:
- ✅ Agent understands the new memory structure
- ✅ Cross-cutting insights are preserved in new format
- ✅ Current work continues without interruption
- ✅ Memory focuses on reusable knowledge, not task progress
- ✅ All rules are updated to v0.2

---

**Note**: This migration preserves your current context while upgrading to a more maintainable and reusable knowledge system. Your agent will continue working on the same tasks but with better long-term knowledge management.
