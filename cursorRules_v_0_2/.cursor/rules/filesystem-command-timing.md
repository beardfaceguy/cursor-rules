# Filesystem Command Timing Rule

## Rule: Check Filesystem Size Before Long Commands

**MANDATORY**: Before running any command that checks filesystems, you MUST first check the size of the area of filesystem you are examining to see if the command will likely take more than 10 seconds.

### When This Rule Applies:
- Commands that scan directories (`find`, `grep -r`, `ls -la`, etc.)
- Commands that check file systems (`du`, `df`, `stat`, etc.)
- Commands that search through large codebases
- Any command that might take extended time on large filesystems

### Required Actions:
1. **Estimate command duration** based on filesystem size
2. **If command will take >10 seconds**: Run it in the background (`is_background: true`)
3. **If command will take <10 seconds**: Run normally
4. **Always inform user** when running commands in background

### Examples:
- `find . -name "*.ts"` on large codebase → Run in background
- `ls -la` on small directory → Run normally
- `grep -r "pattern"` on entire project → Run in background

### Enforcement:
This rule prevents blocking the chat interface with long-running commands. Always err on the side of running in background if uncertain.

---

**This rule ensures responsive communication while handling large filesystem operations.**


