# Memory - Alix Estate Manager Development Insights

## Architecture Patterns Discovered

### Field Implementation Patterns
- **Estate Email Pattern**: Field added directly to Estate model with @unique constraint, available for both creation and updates
- **taxId Pattern**: Field added via migration, nullable initially, unique constraint added later
- **scanBoxId Pattern**: Auto-generated on backend during estate creation, display-only in frontend
- **Deceased Fields Pattern**: Added to Deceased table via migration, handled in writeCoreEstateInformation mutation

### GraphQL Resolver Priority
- **Generated resolvers** are registered FIRST in resolver array
- **Custom resolvers** are registered LAST
- **Frontend mutations** may use generated resolvers instead of custom ones
- **Solution**: Add logic to BOTH generated and custom resolvers

### UI Conditional Rendering Patterns
- **Estate Email**: Always display with fallback "-" when empty
- **Test Account**: Boolean field with conditional styling
- **Status Fields**: Color-coded based on status values
- **Boolean Fields**: Checkbox or toggle display
- **Complex Conditional Logic**: Multiple conditions for field visibility
- **Fallback Display**: Show "-" or placeholder when field is null/empty

### Database Migration Strategy
- **Use postgres superuser** for schema changes when regular user lacks privileges
- **Follow established patterns** (taxId, Estate Email) for new field implementations
- **Apply pending migrations** before making schema changes
- **Create database backups** after migrations for quick restart capability

## Environment Gotchas

### Backend Startup Procedure
- **ALWAYS switch to Node 22 first**: `export NVM_DIR="$HOME/.config/nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && nvm use 22`
- **Then run in background**: `yarn start` (NEVER foreground - user loses control)
- **Frontend commands**: Use `npm run dev` (NOT `yarn start` - that command doesn't exist in frontend)

### Dependency Resolution
- **Always use**: `npm install --legacy-peer-deps` for frontend dependencies
- **MUI Lab conflicts**: React 19 vs MUI Lab compatibility resolved with legacy peer deps
- **Backend requires Node 22+**: Use nvm to switch versions

### Service Management
- **NEVER run services in foreground**: Always use `is_background: true` or user will need to kill them manually
- **Multiple instances**: Old ts-node-dev processes weren't properly killed, causing conflicts
- **Clean startup**: Kill all existing processes before restarting services

### Database User Setup
- **patrickclawson user**: Requires specific permissions for Prisma migrations
- **Permission setup commands** (run immediately after database restore):
  ```sql
  -- Grant CREATEDB privilege for shadow database
  ALTER USER patrickclawson WITH CREATEDB;
  
  -- Grant ownership of all enum types
  DO $$ DECLARE r RECORD; 
  BEGIN 
    FOR r IN SELECT typname FROM pg_type WHERE typtype = 'e' AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public') 
    LOOP 
      EXECUTE 'ALTER TYPE "' || r.typname || '" OWNER TO patrickclawson;'; 
    END LOOP; 
  END $$;
  
  -- Grant ownership of all tables
  DO $$ DECLARE r RECORD; 
  BEGIN 
    FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' 
    LOOP 
      EXECUTE 'ALTER TABLE "' || r.tablename || '" OWNER TO patrickclawson;'; 
    END LOOP; 
  END $$;
  
  -- Grant all privileges
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO patrickclawson;
  GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO patrickclawson;
  GRANT ALL PRIVILEGES ON TABLE _prisma_migrations TO patrickclawson;
  ```

## Key Lessons Learned

### Implementation Methodology
- **Jira-First Analysis**: MUST check Jira task requirements first before analyzing UI patterns
- **Complete Field Analysis**: MUST analyze ALL existing fields before implementing new ones to understand patterns
- **Backend-First Verification**: Always check if functionality already exists in backend services
- **Complete Data Flow Tracing**: Database → Backend Service → GraphQL → Frontend mutation → UI display

### Code Analysis Requirements
- **MUST examine git history** for each field type to see actual implementation approach
- **MUST check backend services** not just GraphQL schema - business logic lives in services
- **MUST verify frontend mutations** request all needed fields in response
- **MUST understand conditional rendering patterns** for UI behavior decisions

### Common Issues and Solutions
- **"Crud resolvers" confusion**: Generated resolvers take precedence over custom ones
- **Frontend mutation missing fields**: Check if mutation response includes all needed fields
- **Database migration drift**: Use proper Prisma migrations, not db push
- **Incomplete rollback**: Verify ALL files are clean after rollback, not just git status

## Critical Commands

### Backend Startup
```bash
# Switch to Node 22
export NVM_DIR="$HOME/.config/nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && nvm use 22

# Start backend in background
yarn start
```

### Frontend Startup
```bash
# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev
```

### Database Operations
```bash
# Check migration status
npx prisma migrate status

# Apply pending migrations
npx prisma migrate deploy

# Regenerate Prisma client
npx prisma generate

# Create database backup
pg_dump -h localhost -p 5432 -U patrickclawson -d alix > alix_backup.sql
```

### Service Management
```bash
# Kill all backend processes
pkill -f "ts-node-dev"
pkill -f "yarn start"

# Check running services
ps aux | grep -E "(yarn|ts-node|npm)"
```

## Authentication Information

### Working Credentials
- **Email**: `admintest@meetalix.com`
- **Password**: `te8mAlix!`
- **Role**: Admin
- **Site URL**: http://localhost:3000/

### Other Available Users
- `david+admin@meetalix.com` (SuperAdmin) - Password: Unknown
- `david+testofferson@meetalix.com` (Admin) - Password: Unknown
- `vyacheslav.solomin+admin@meetalix.com` (SuperAdmin) - Password: Unknown
- `travis+admin@meetalix.com` (SuperAdmin) - Password: Unknown

### Access Requirements
- **Authentication Required**: Yes - AWS Cognito authentication required
- **Public Pages**: Only login, forgot-password, and set-new-password pages
- **Required Roles**: Users must have 'Admin' or 'SuperAdmin' role

## Environment Configuration

### Frontend Environment Variables
```bash
# AWS Cognito Authentication (REQUIRED)
VITE_COGNITO_USERPOOL_ID=your_user_pool_id
VITE_COGNITO_CLIENT_ID=your_client_id  
VITE_IDENTITY_POOL_ID=your_identity_pool_id

# GraphQL Backend (REQUIRED)
VITE_GRAPHQL_ENDPOINT=http://localhost:8080/graphql
VITE_API_ENDPOINT=http://localhost:8080

# Development Settings
VITE_APP_VERSION=local
VITE_AWS_REGION=us-east-1
VITE_OPTIMIZELY_SDK_KEY=your_optimizely_key
```

### Backend Environment Variables
```bash
# Database Connection (REQUIRED)
DATABASE_URL=postgres://patrickclawson:postgres@127.0.0.1:5432/alix

# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# External Services (placeholders acceptable for development)
CLICKUP_API_KEY=your_clickup_key
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
BOX_CLIENT_ID=your_box_client_id
BOX_CLIENT_SECRET=your_box_client_secret
```

## Current Environment Status

### Services Status
- **Frontend**: ✅ Running on port 3000 (React application)
- **Backend**: ✅ Running on port 8080 (GraphQL endpoint)
- **Database**: ✅ PostgreSQL running on port 5432 with staging data (117 estates)
- **Node**: Version 22 active via nvm
- **Yarn**: Installed globally and working

### Database Status
- **PostgreSQL**: Container running on port 5432
- **Database**: `alix` accessible with 117 estates
- **User**: `patrickclawson` with proper permissions
- **Migrations**: All 30 pending migrations applied successfully
- **Backup**: Available for quick restart capability

---

*Last updated: $(date)*
*This file contains cross-cutting insights useful across multiple implementations and sessions.*