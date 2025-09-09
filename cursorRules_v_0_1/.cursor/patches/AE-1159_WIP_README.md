# AE-1159 WIP Patch - scanBoxId Implementation

## Overview
This patch contains all the changes made for implementing the scanBoxId field for estates. The scanBoxId is an 8-digit alphanumeric unique identifier that is auto-generated when an estate is created.

## Files Modified

### Frontend (alix-estate-manager)
- `src/apollo/mutations/adminCreateOneEstate.ts` - Added scanBoxId to mutation response
- `src/apollo/queries/getEstate.ts` - Added scanBoxId to query fields
- `src/components/molecules/forms/estate/EstateInfoCard.tsx` - Added scanBoxId display with fallback
- `package.json` - Updated dependencies
- `yarn.lock` - Updated lock file
- `.gitignore` - Updated ignore patterns

### Backend (alix-api)
- `prisma/schema.prisma` - Added scanBoxId field to Estate model
- `src/services/EstateService.ts` - Added scanBoxId generation logic in createEstate method
- `src/utils/scanBoxIdGenerator.ts` - **NEW FILE** - Utility functions for generating unique scanBoxIds
- `src/graphql/__generated__/` - All generated GraphQL types updated to include scanBoxId
- `src/schema.gql` - Updated GraphQL schema

### Database
- Added `scanBoxId` column to Estate table with unique constraint
- Field is nullable and auto-generated on estate creation

## Key Features Implemented
1. **Backend Generation**: scanBoxId is generated using 8-digit alphanumeric characters (excluding confusing chars like 0, O, I, 1)
2. **Uniqueness Check**: Ensures generated IDs are unique across all estates
3. **Frontend Display**: Shows scanBoxId in EstateInfoCard with fallback "-" for null values
4. **GraphQL Integration**: Full GraphQL schema support for scanBoxId field

## Status
- ✅ Database schema updated
- ✅ Backend generation logic implemented
- ✅ Frontend display implemented
- ✅ GraphQL integration complete
- ❌ **ISSUE**: scanBoxId not being generated for new estates (needs investigation)

## Next Steps
1. Resolve database migration issues (shadow database permissions)
2. Test estate creation through UI to verify scanBoxId generation
3. Debug why scanBoxId generation is not working despite correct implementation

## Notes
- The implementation follows the established patterns from other estate fields
- All changes are backward compatible
- scanBoxId is immutable once generated
