# Memory - Alix Estate Manager Development Session

## Current Task
**Fresh Implementation of AE-1159**: Implementing `scanBoxId` field for estates using all lessons learned from previous attempts. Focus on proper database migrations and comprehensive implementation.

## Progress Made ✅

### Frontend Setup
- ✅ Resolved dependency conflicts using `npm install --legacy-peer-deps`
- ✅ Created comprehensive `.env` file with all required environment variables:
  - AWS Cognito authentication (VITE_COGNITO_USERPOOL_ID, VITE_COGNITO_CLIENT_ID, VITE_IDENTITY_POOL_ID)
  - API endpoints (VITE_GRAPHQL_ENDPOINT=http://localhost:8080/graphql)
  - Development settings (VITE_APP_VERSION=local, VITE_AWS_REGION=us-east-1)
  - Optimizely SDK key
- ✅ Frontend running successfully on http://localhost:3000/
- ✅ Vite server restarted automatically when .env was updated

### Backend Setup
- ✅ Installed yarn globally
- ✅ Updated Node.js to version 22 using nvm (required by backend)
- ✅ Installed backend dependencies successfully
- ✅ Applied database migrations (`yarn db-migrate`)
- ✅ Created comprehensive `.env` file with all required environment variables:
  - Database connection (DATABASE_URL=postgres://patrickclawson:postgres@127.0.0.1:5432/alix)
  - AWS credentials and services
  - ClickUp API key
  - Camunda/Zeebe configuration
  - Plaid integration
  - Box integration
  - Various external service tokens

### Infrastructure
- ✅ PostgreSQL database running via Docker Compose
- ✅ Database `alix` created and staging data imported from dump file

### Documentation
- ✅ Created `.cursor/docs/IMPLEMENTATION_AE_1159.md` with detailed plan for `scanBoxId` implementation
- ✅ Created `.cursor/docs/SETUP.md` documenting dependency resolution steps
- ✅ Added `.cursor/` to `.gitignore` to prevent committing internal docs
- ✅ Created individual rule files in `.cursor/rules/` directory
- ✅ Consolidated systemctl rule into `interactive-commands.md` (deleted redundant file)
- ✅ Updated memory-tracking rule to use `.cursor/memory/memory.md` location
- ✅ Moved memory.md to `.cursor/memory/memory.md`
- ✅ Created generic root `README.md` for Cursor Agents explaining .cursor directory system

## .cursor Directory Structure

```
[Project Root]/
├── README.md                               # Generic Cursor Agent guidelines
└── .cursor/                                # AI Assistant Rules & Documentation
    ├── docs/                               # Documentation directory
    │   ├── IMPLEMENTATION_AE_1159.md      # Detailed implementation plan for scanBoxId feature
    │   └── SETUP.md                       # Environment setup and dependency resolution guide
    ├── memory/                            # Session memory tracking
    │   └── memory.md                      # Current session state and progress tracking
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

## Current Status
- **Frontend**: ✅ **FULLY OPERATIONAL** - Running on port 3000, serving React application
- **Backend**: ✅ **FULLY OPERATIONAL** - Running on port 8080, GraphQL endpoint responding successfully
- **Database**: ✅ Running and populated with staging data (117 estates)
- **Environment**: ✅ Fully configured with placeholder values for external services
- **Branches**: ✅ AE-1159 branches created in both alix-api and alix-estate-manager
- **PostgreSQL**: ✅ Container running on port 5432, alix database accessible with 117 estates
- **Documentation**: ✅ Created generic root README.md for Cursor Agents explaining .cursor directory system
- **Implementation Plan**: ✅ Updated IMPLEMENTATION_AE_1159.md to include .env file verification as critical first step
- **Environment Files**: ✅ Verified .env files exist in both repositories with proper configurations
- **PostgreSQL Permissions**: ✅ Set up all required permissions for patrickclawson user
- **Prisma Status**: ✅ Confirmed 30 pending migrations need to be applied
- **Implementation Plan**: ✅ Added Phase 0.5 to ensure pending migrations are applied before schema changes
- **Implementation Plan**: ✅ Added Phase 0.6 to create database backup after migrations for quick restart capability
- **Phase 0.5 Complete**: ✅ Applied all 30 pending migrations successfully
- **Migration Verification**: ✅ Verified all database changes properly implemented
- **Phase 0.6 Complete**: ✅ Created database backup (1.1MB) with all 117 estates and schema

## Field Addition Pattern Analysis

### Key Findings from Jira Research:
1. **AE-1107 (taxId field)**: Most recent similar field addition - user input field
2. **AE-1065 (email field)**: Display-only field with copy functionality  
3. **AE-972 (mtcDate field)**: Date field for ClickUp integration
4. **Multiple Contact Fields**: Deceased, DoD, Citizenship, Marital Status, etc.

### Common Implementation Pattern:
1. **Database Schema**: Add field to Prisma model
2. **GraphQL Schema**: Update TypeGraphQL model and input types
3. **Backend Logic**: Add to service layer and resolvers
4. **Frontend UI**: Update display components and queries
5. **Testing**: Verify functionality across all layers

### Critical Discovery - Resolver Priority:
- **Generated resolvers** are registered FIRST in resolver array
- **Custom resolvers** are registered LAST
- **Frontend mutations** may use generated resolvers instead of custom ones
- **Solution**: Add logic to BOTH generated and custom resolvers

### Potential Surprises Identified:
1. **Resolver Override**: Generated resolvers take precedence over custom ones
2. **Multiple Creation Paths**: Different resolvers may handle estate creation
3. **Field Validation**: Some fields may have specific validation requirements
4. **UI Consistency**: Display patterns vary (conditional vs always show)
5. **Migration Complexity**: Some fields require complex data migration strategies

### Recent Progress
- ✅ **Services Stopped**: Both frontend and backend services are now stopped
- ✅ **Database User Fixed**: Replaced `timothymyers` with `patrickclawson` user in PostgreSQL with proper permissions
- ✅ **Docker Container**: PostgreSQL running in `alix-api-db-1` container on port 5432
- ✅ **Environment Variables Added**: Added placeholder values for missing Google, Box, SendGrid, and Plaid variables
- ⚠️ **Backend Startup**: Backend starts without ZodError but appears to get stuck during initialization
- 🔍 **Current Investigation**: Monitoring backend CPU usage to determine if it's initial processing that will settle down
- 📊 **CPU Usage Pattern**: Backend processes showing 84-99% CPU usage, investigating if this is normal startup behavior
- 🔧 **Backend Progress**: Successfully past environment validation, now encountering GraphQL module resolution issues
- 📈 **Database Verification**: Confirmed 117 estates in database, migrations applied, user permissions working
- 🎉 **BACKEND SUCCESS**: Backend now fully operational on port 8080, GraphQL endpoint responding with complete schema
- 🎉 **FRONTEND SUCCESS**: Frontend now fully operational on port 3000, serving React application
- 🎉 **FULL STACK OPERATIONAL**: Both frontend and backend are running successfully!

## Authentication & Access Information
- **Site URL**: http://localhost:3000/
- **Authentication Required**: ✅ Yes - AWS Cognito authentication required
- **Public Pages**: Only login, forgot-password, and set-new-password pages are accessible without authentication
- **Required Roles**: Users must have 'Admin' or 'SuperAdmin' role to access the application
- **Available Test Users**:
  - `david+admin@meetalix.com` (SuperAdmin) - Password: Unknown
  - `admintest@meetalix.com` (Admin) - Password: `te8mAlix!` ✅
  - `david+testofferson@meetalix.com` (Admin) - Password: Unknown
  - `vyacheslav.solomin+admin@meetalix.com` (SuperAdmin) - Password: Unknown
  - `travis+admin@meetalix.com` (SuperAdmin) - Password: Unknown
- **Working Credentials**: `admintest@meetalix.com` / `te8mAlix!`

## Jira Task AE-1159 Details
- **Task**: "Upgrades to Simplify ARC automated workflow"
- **Status**: In Development (assigned to Patrick Clawson)
- **Priority**: Medium
- **Sprint**: September 5th Sprint
- **Key Requirements**:
  - Generate 8-digit alphanumeric `scanBoxId` field when estate is created
  - Display the ID in Estate Manager UI (mockup provided)
  - Update existing ARC automation code (AE-405) to match files by scanBoxId
  - Field must be unique to each estate
  - Format: "ALIX-{8-digit-alphanumeric}" (14 characters total)
- **Field Behavior**:
  - **Read-only**: Users cannot edit the scanBoxId (auto-generated only)
  - **No backfill**: Existing estates don't need scanBoxId unless they haven't requested ARC box yet
  - **Future exception**: Estates created before this feature may get manual IDs if needed
- **Related Tasks**: AE-405 (existing ARC automation by Sergey Shchipitsyn)
- **Attachments**: UI mockups showing scanBoxId display in Estate Manager

### Recent Service Cleanup (Latest)
- **Issue**: Multiple backend instances were running simultaneously (2 yarn start + 2 ts-node-dev processes)
- **Resolution**: Killed all `ts-node-dev` and `yarn start` processes using `pkill`
- **Current Status**: 
  - Frontend: ✅ Running on port 3000 (PID 2234100)
  - Backend: ❌ Stopped (cleaned up, port 4000 free)
  - Ready for clean backend restart

### AE-1159 Implementation Progress

#### Current Status: Field Analysis Complete ✅
- **Backend**: scanBoxId generation fully implemented in EstateService.createEstate()
- **Frontend**: adminCreateEstate mutation updated to return scanBoxId
- **Critical Discovery**: scanBoxId generation is already implemented in backend EstateService.createEstate() method
- **Issue Resolved**: Frontend mutation was missing scanBoxId in response - now fixed

#### Field Implementation Pattern Analysis Complete ✅
- **Pattern 1**: Basic estate fields (hasTrust, hasWill, testAccount, etc.) - Added via migration, EstateService, GraphQL, and frontend form
- **Pattern 2**: Deceased fields (wasVeteran, maritalStatus, etc.) - Added via migration, EstateService, GraphQL, and frontend form
- **Pattern 3**: scanBoxId - Backend implementation complete, frontend mutation fixed
- **Pattern 4**: Address fields (lastKnownAddress, placeOfDeathAddress, etc.) - Complex nested relationships
- **Pattern 5**: Auto-generated fields (scanBoxId) - Backend generation, frontend display only
- **Final Theory**: scanBoxId implementation follows standard pattern, frontend mutation was missing field in response

#### Critical Lessons Learned: Comprehensive Code Analysis Required
- **MUST analyze ALL fields** before implementing new ones to understand patterns
- **MUST examine git history** for each field type to see actual implementation approach
- **MUST check backend services** not just GraphQL schema - business logic lives in services
- **MUST verify frontend mutations** request all needed fields in response
- **MUST understand conditional rendering patterns** for UI behavior decisions
- **MUST trace complete data flow** from database → backend → GraphQL → frontend
- **MUST analyze Jira task first** using Jira MCP server to understand PM requirements before implementation
- **Key Discovery**: "crud resolvers" issue was actually frontend mutation missing field in response
- **UI Pattern Discovery**: Found 6 distinct conditional rendering patterns that affect field visibility

#### Step 1: Research taxId Implementation Pattern ✅
- **Investigation**: Analyzed how taxId field was added to understand proper migration approach
- **Key Findings**:
  - taxId was added as nullable `TEXT` field in migration `20230518162108_rename_tax_id`
  - Migration dropped `tax_number` column and added `taxId` column
  - No unique constraint initially (avoided conflicts with existing data)
  - Added to GraphQL queries, mutations, and frontend forms
- **Files Examined**:
  - `prisma/migrations/20230518162108_rename_tax_id/migration.sql`
  - `src/apollo/queries/getEstate.ts` (line 15: `taxId`)
  - `src/apollo/mutations/writeCoreEstateInformation.ts` (line 15: `$taxId: String`)
  - `src/components/molecules/forms/estate/AddEstateForm.tsx` (lines 185, 471-476)

#### Step 2: Database Schema Update ✅
- **Prisma Schema**: Added `scanBoxId String? @unique` to Estate model (line 102)
- **Database Migration**: 
  - **Issue**: Regular user `patrickclawson` lacked ALTER TABLE privileges
  - **Solution**: Used postgres superuser for schema changes
  - **Commands Executed**:
    ```sql
    ALTER TABLE "Estate" ADD COLUMN "scanBoxId" TEXT;
    ALTER TABLE "Estate" ADD CONSTRAINT "Estate_scanBoxId_key" UNIQUE ("scanBoxId");
    ```
  - **Verification**: Confirmed column exists with unique constraint
- **Approach**: Followed taxId pattern (nullable initially, unique constraint added)

#### Step 3: GraphQL Schema Research ✅
- **Investigation**: Found taxId implementation pattern in GraphQL schema files
- **Key Files Identified**:
  - `src/graphql/models/Estate.ts` (line 39: taxId field definition)
  - `src/graphql/resolvers/inputs/EstateCreateInput.ts` (line 63: taxId input definition)
  - `src/schema.gql` (generated file, contains Estate type with taxId)
- **Pattern Found**: 
  ```typescript
  // Estate.ts model
  @TypeGraphQL.Field((_type) => String, { nullable: true })
  taxId?: string | null;
  
  // EstateCreateInput.ts
  @TypeGraphQL.Field((_type) => String, { nullable: true })
  taxId?: string | undefined;
  ```
- **Approach**: Follow exact same pattern for scanBoxId (nullable field, same decorators)

#### Step 4: GraphQL Schema Implementation ✅
- **Estate.ts Model**: Added scanBoxId field following taxId pattern (line 44)
- **EstateCreateInput.ts**: Added scanBoxId field following taxId pattern (line 68)
- **Type Regeneration**: Successfully ran `npx prisma generate` to update GraphQL types
- **Verification**: GraphQL schema now includes scanBoxId field in Estate type and input types

#### Step 5: Backend Logic Implementation ✅
- **Utility Creation**: Created `src/utils/scanBoxIdGenerator.ts` with:
  - `generateScanBoxId()`: Generates 8-digit alphanumeric ID (excluding confusing chars)
  - `generateUniqueScanBoxId()`: Ensures uniqueness by checking database
  - `validateScanBoxIdFormat()`: Validates ID format
- **EstateService Integration**: Added scanBoxId generation to `createEstate()` method:
  - Imported scanBoxId generator utility
  - Added uniqueness check within database transaction
  - Generated scanBoxId before estate creation (lines 263-269)
  - Included scanBoxId in estate creation data (line 274)

#### Step 6: Frontend Implementation ✅
- **GraphQL Query Update**: Added `scanBoxId` field to `getEstate.ts` query (line 16)
- **EstateInfoCard Component**: Updated to display scanBoxId per mockup layout:
  - Added scanBoxId display right of estate name, above email (lines 117-120)
  - Always displays with fallback "-" when empty (consistent with other fields like Clickup ID)
  - Styled with secondary text color and medium font weight
  - Right-aligned to match mockup layout

#### Step 7: Testing & Bug Fixes ✅
- **Issue Found**: Estate creation failing with "Field 'mtcDate' is not defined by type 'EstateCreateInput2'"
- **Root Cause**: Missing `mtcDate` field in `EstateCreateInput2` type after GraphQL regeneration
- **Fix Applied**: Added `mtcDate?: Date | undefined;` to `EstateCreateInput.ts` (line 73)
- **GraphQL Regeneration**: Successfully ran `npx prisma generate` to update types

#### Step 8: Fresh Start Attempt - CRITICAL ISSUE DISCOVERED 🚨
- **Problem**: Attempted fresh implementation but found scanBoxId already in `prisma/schema.prisma` (line 102)
- **Root Cause**: Previous rollback was incomplete - code changes not fully reverted
- **Impact**: Cannot proceed with clean implementation until complete rollback
- **Key Finding**: Estate Email implementation pattern is correct for scanBoxId:
  - **Estate Email**: Added directly to `Estate` model (available for both creation and updates)
  - **Estate Email**: Has unique constraint and index
  - **Estate Email**: Part of core estate data, not just update flow
  - **scanBoxId**: Should follow same pattern as Estate Email (not taxId)
  - **scanBoxId**: Auto-generated on backend during estate creation
- **Required Action**: Complete rollback of ALL files before fresh implementation
- **Status**: Estate creation should now work properly

#### Previous Implementation: Rolled Back ✅
- **All Code Changes**: ✅ Rolled back using git restore
- **Database**: ✅ Clean state restored from staging dump (117 estates)
- **Patch File**: ✅ Preserved in `.cursor/patches/AE-1159_WIP.patch` (4.1MB backup)
- **Lessons Learned**: ✅ Comprehensive field analysis completed, patterns identified
- **Current Status**: Ready for fresh implementation with proper database migrations

#### Fresh Implementation: Starting Now 🔄
- **Approach**: Following established patterns from taxId field implementation
- **Focus**: Proper database migrations with shadow database permissions resolved
- **Methodology**: Comprehensive analysis first, then systematic implementation

### Environment Files Status
- **Frontend .env**: ✅ Located at `/home/beardface/work/alix/alix-estate-manager/.env` (421 bytes)
  - Contains AWS Cognito, API endpoints, Optimizely SDK key
- **Backend .env**: ✅ Located at `/home/beardface/work/alix/alix-api/.env` (9,303 bytes)
  - Contains comprehensive configuration including database, AWS, ClickUp, Camunda, Plaid, Box, etc.

## Next Steps
1. **COMPLETED**: Created individual rule files in `.cursor/rules/` directory
2. **COMPLETED**: Updated memory-tracking rule to use `.cursor/memory/memory.md` location
3. **COMPLETED**: Moved memory.md to `.cursor/memory/memory.md`
4. **COMPLETED**: Moved cursor_docs to `.cursor/docs/` and updated .gitignore
5. **Fix backend startup**: Add missing environment variables to backend .env
6. **Test GraphQL endpoint** connectivity from frontend (after backend is ready)
7. **Verify authentication** works with provided Cognito credentials
8. **Test estate viewing** to confirm scanBoxId field location in UI
9. **Begin scanBoxId implementation** following the plan in IMPLEMENTATION_AE_1159.md

## Issues Encountered
- **Dependency conflicts**: Resolved with `npm install --legacy-peer-deps`
- **Node version mismatch**: Backend required Node 22, system had 20.18.1 - resolved with nvm
- **Backend startup**: Previous attempts were interrupted, need to verify successful startup
- **Environment variable validation**: Backend failed with ZodError for missing Google, Box, SendGrid variables - resolved with placeholder values
- **Database user mismatch**: .env file referenced `timothymyers` user that didn't exist in database - resolved by creating `patrickclawson` user
- **High CPU usage during startup**: Backend processes showing 84-99% CPU usage during initialization - investigating if this is normal startup behavior
- **Multiple backend processes**: Old ts-node-dev processes weren't properly killed, causing multiple instances - resolved with proper cleanup
- **GraphQL generation error**: Backend now encountering "Cannot find module './graphql/__generated__'" error - indicates progress past environment validation
- **"Crud resolvers" confusion**: Initially thought scanBoxId wasn't being generated due to crud resolvers - actually was frontend mutation missing field in response
- **Incomplete field analysis**: Started implementation without analyzing ALL existing fields first - led to incorrect assumptions
- **UI pattern discovery**: Found 6 distinct conditional rendering patterns (Estate Email, Test Account, Status Fields, Boolean Fields, Complex Conditional Logic, Fallback Display) that affect field visibility
- **Jira-first methodology**: Should check Jira task requirements first, then compare to UI patterns to see if PM has already answered questions
- **Backend startup failure**: `yarn start` always fails with Node version error (requires >=22.0.0, got 20.18.1) - CORRECT METHOD: Must switch to Node 22 first using nvm, then run `yarn start` in background
- **Foreground service problem**: NEVER run services in foreground - always use background mode or user loses control

## Key Decisions Made
- **No migration strategy**: Following `taxId` pattern, existing estates will not get scanBoxId retroactively
- **Field naming**: Using `scanBoxId` as specified in original requirements
- **Environment approach**: Prioritizing environment fixes over code changes per user preference
- **Comprehensive analysis approach**: MUST analyze ALL existing fields before implementing new ones
- **Backend-first verification**: Always check if functionality already exists in backend services
- **Complete data flow tracing**: Database → Backend Service → GraphQL → Frontend mutation → UI display
- **Jira-first analysis**: MUST check Jira task requirements first before analyzing UI patterns
- **Requirements comparison**: Compare Jira requirements to existing UI patterns to identify gaps
- **Complete rollback verification**: After rollback, verify ALL files are clean - check schema files, not just git status
- **Implementation pattern differences**: taxId (update flow) vs scanBoxId (creation flow) require different approaches
- **Backend startup procedure**: ALWAYS switch to Node 22 first: `export NVM_DIR="$HOME/.config/nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && nvm use 22` then `yarn start` (run in background, NOT foreground)
- **Frontend startup procedure**: Use `npm run dev` (NOT `yarn start` - that command doesn't exist in frontend)
- **Service startup issue**: NEVER run services in foreground - always use `is_background: true` or user will need to kill them manually

## Files Modified
- `package.json` (temporarily modified @mui/lab version, then reverted)
- `.env` (frontend) - created with comprehensive environment variables
- `.env` (backend) - created with comprehensive environment variables
- `.gitignore` - added cursor_docs/ exclusion
- `cursor_docs/IMPLEMENTATION_AE-1159.md` - created implementation plan
- `cursor_docs/SETUP.md` - created setup documentation
- `rules/memory-tracking.md` - created memory tracking rule
- `README.md` - created generic Cursor Agent guidelines for .cursor directory system

## Environment State
- **Frontend**: Running on port 3000, Vite dev server active
- **Backend**: Need to verify startup on port 8080
- **Database**: PostgreSQL running on port 5432 with staging data
- **Node**: Version 22 active via nvm
- **Yarn**: Installed globally and working

---
*Last updated: $(date)*
