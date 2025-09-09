# Setup Guide: Alix Estate Manager

## Overview
This guide documents the steps required to get the Alix Estate Manager repository dependencies working and the development environment set up.

## Environment Information
- **OS**: Linux (Ubuntu/Debian-based)
- **Node.js**: v20.18.1
- **npm**: 9.2.0
- **Repository**: Working codebase with dependency conflicts

## Initial Problem
When running `npm install`, encountered dependency resolution errors:
1. **MUI Lab vs Material conflict**: `@mui/lab@7.0.0-beta.11` required `@mui/material@^7.0.2` but project uses `@mui/material@^6.4.0`
2. **React 19 compatibility**: `@mui/lab` only supports React `^17.0.0 || ^18.0.0` but project uses React `^19.0.0`

## Solution Applied

### Step 1: Clean Environment
```bash
# Remove existing node_modules and lock file
rm -rf node_modules package-lock.json

# Clear npm cache
npm cache clean --force
```

### Step 2: Install with Legacy Peer Deps
```bash
# Use legacy peer dependency resolution
npm install --legacy-peer-deps
```

**Why this works**: The `--legacy-peer-deps` flag tells npm to use the legacy (npm v6) algorithm for resolving peer dependencies, which is more permissive and allows packages with conflicting peer dependencies to coexist.

### Step 3: Fix Code Formatting
```bash
# Fix formatting issues detected by Biome
npx biome check --write
```

## Verification Steps

### 1. Check Dependencies Installation
```bash
npm install --legacy-peer-deps
# Should complete without errors
# Expected: "added 2058 packages, and audited 2059 packages"
```

### 2. Start Development Server
```bash
npm run dev
# Expected output:
# VITE v5.4.14  ready in 269 ms
# ➜  Local:   http://localhost:3000/
```

### 3. Verify Server is Running
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# Expected: 200
```

### 4. Run Linting
```bash
npx biome check
# Expected: "Checked 363 files in 476ms. No fixes applied."
```

### 5. Run Type Checking
```bash
npm run typecheck
# Expected: No errors, clean exit
```

## Alternative Commands

### Linting (since yarn is not available)
```bash
# Instead of: npm run lint (which uses yarn)
npx biome check

# To fix formatting issues:
npx biome check --write
```

### Development Server
```bash
npm run dev
# Server runs on http://localhost:3000
```

## Common Issues & Solutions

### Issue: "yarn: not found"
**Problem**: Scripts reference `yarn` but it's not installed
**Solution**: Use `npx` commands directly:
- `npx biome check` instead of `yarn biome check`
- `npx biome check --write` instead of `yarn biome check --write`

### Issue: Dependency Conflicts
**Problem**: React 19 vs MUI Lab compatibility
**Solution**: Always use `npm install --legacy-peer-deps`

### Issue: Formatting Errors
**Problem**: Biome detects formatting issues
**Solution**: Run `npx biome check --write` to auto-fix

## Package Manager Notes

### Why npm instead of yarn?
- Repository has `yarn.lock` but `yarn` command not available
- `npm install --legacy-peer-deps` resolves dependency conflicts
- All scripts work with npm equivalents

### Dependency Warnings
The following warnings are expected and don't affect functionality:
- Deprecated packages (common in working repositories)
- Security vulnerabilities (mostly in dev dependencies)
- Peer dependency conflicts (resolved with --legacy-peer-deps)

## Environment Variables Required

For full functionality, these environment variables are needed:
```bash
# AWS Cognito Authentication (REQUIRED)
VITE_COGNITO_USERPOOL_ID=your_user_pool_id
VITE_COGNITO_CLIENT_ID=your_client_id  
VITE_IDENTITY_POOL_ID=your_identity_pool_id

# GraphQL Backend (REQUIRED)
VITE_GRAPHQL_ENDPOINT=http://localhost:8080/graphql

# API Endpoint (REQUIRED)
VITE_API_ENDPOINT=http://localhost:8080

# Optional Configuration
VITE_PORT=3000
VITE_APP_VERSION=dev
VITE_OPTIMIZELY_SDK_KEY=your_optimizely_key
VITE_CLICKUP_CHAPTER_KEY=your_clickup_key
VITE_BUILD_DESCRIPTION=local-development
```

## Quick Start Commands

```bash
# 1. Clean and install dependencies
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --legacy-peer-deps

# 2. Fix any formatting issues
npx biome check --write

# 3. Start development server
npm run dev

# 4. Verify everything works
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
npx biome check
npm run typecheck
```

## Success Indicators

✅ **Dependencies**: 2058 packages installed successfully  
✅ **Dev Server**: Running on http://localhost:3000 (HTTP 200)  
✅ **Linting**: Biome check passes with no errors  
✅ **Type Checking**: TypeScript compilation successful  
✅ **Code Formatting**: All files properly formatted  

## Notes for Future Cursor Agents

1. **Always use `--legacy-peer-deps`** when installing dependencies
2. **Don't modify package.json** - the dependency conflicts are resolved at the environment level
3. **Use `npx` commands** instead of yarn-based scripts
4. **The repository is working** - focus on environment fixes, not code changes
5. **Backend services required** for full functionality (GraphQL, AWS Cognito)

## Related Files

- `package.json` - Dependencies configuration
- `biome.json` - Linting and formatting configuration
- `vite.config.ts` - Build configuration
- `tsconfig.json` - TypeScript configuration
- `cursor_docs/IMPLEMENTATION_AE_1159.md` - scanBoxId implementation plan

## Troubleshooting

If you encounter issues:

1. **Check Node.js version**: Should be v20.18.1 or compatible
2. **Clear everything**: `rm -rf node_modules package-lock.json && npm cache clean --force`
3. **Use legacy deps**: `npm install --legacy-peer-deps`
4. **Fix formatting**: `npx biome check --write`
5. **Verify setup**: Run all verification steps above

The repository is designed to work with these specific dependency resolution strategies.
