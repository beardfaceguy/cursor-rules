# Extended Time Commands Rule

## Rule: Run Long Commands in Background

**MANDATORY**: For commands expected to take an extended amount of time, you MUST run them in a separate terminal or in the background so you can monitor them and maintain communication with the user.

### When This Rule Applies:
- **Build processes** (`npm run build`, `yarn build`, `make`, etc.)
- **Installation commands** (`npm install`, `yarn install`, `pip install`, etc.)
- **Database operations** (migrations, dumps, restores)
- **Compilation processes** (TypeScript, webpack, etc.)
- **Testing suites** that run for extended periods
- **Any command** that might run for more than 30 seconds

### Required Actions:
1. **Set `is_background: true`** for extended time commands
2. **Monitor progress** and report status to user
3. **Stay in communication** - don't let long commands block chat
4. **Provide updates** on command progress when possible

### Examples:
- `npm install` → Run in background, report when complete
- `yarn build` → Run in background, monitor for errors
- `docker-compose up` → Run in background, check status periodically

### Enforcement:
This rule ensures the user can continue communicating while long-running processes execute. Never block communication for extended periods.

---

**This rule maintains responsive communication during lengthy operations.**


