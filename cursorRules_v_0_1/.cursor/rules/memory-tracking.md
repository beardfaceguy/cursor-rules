# Memory Tracking Rule

## Rule: Always Update Memory.md

**MANDATORY**: You MUST always update `.cursor/memory/memory.md` to keep track of what you are doing throughout the entire session.

### When to Update Memory.md:

1. **At the start of each new task or major change in direction**
2. **After completing significant steps or milestones**
3. **When encountering errors or issues that require troubleshooting**
4. **Before making major code changes or architectural decisions**
5. **When switching between different parts of the codebase (frontend/backend)**
6. **At the end of each session or when handing off to another agent**

### What to Include in .cursor/memory/memory.md:

- **Current task/goal**: What you're working on right now
- **Progress made**: What has been completed successfully
- **Current status**: Where you are in the process
- **Next steps**: What needs to be done next
- **Issues encountered**: Any problems or blockers
- **Environment state**: Current configuration, running services, etc.
- **Key decisions made**: Important choices or changes made
- **Files modified**: Important files that have been changed

### Format:

Use clear, concise bullet points with timestamps when relevant. Keep it updated in real-time, not as an afterthought.

### Enforcement:

This rule takes precedence over other tasks. If you find yourself working on something without updating .cursor/memory/memory.md, STOP and update it immediately before continuing.

---

**This rule ensures continuity, prevents duplicate work, and maintains context across sessions.**
