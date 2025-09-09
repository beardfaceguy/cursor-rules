#!/bin/bash

# Migration Script: v0.1 to v0.2 Cursor Agent Rules
# This script helps migrate an existing Cursor Agent from v0.1 to v0.2

set -e  # Exit on any error

echo "🔄 Cursor Rules Migration Script v0.1 → v0.2"
echo "=============================================="

# Check if we're in a project with .cursor directory
if [ ! -d ".cursor" ]; then
    echo "❌ Error: No .cursor directory found in current location"
    echo "   Please run this script from your project root directory"
    exit 1
fi

# Check if v0.2 source exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
V0_2_SOURCE="$SCRIPT_DIR/cursorRules_v_0_2"

if [ ! -d "$V0_2_SOURCE" ]; then
    echo "❌ Error: v0.2 source directory not found at $V0_2_SOURCE"
    echo "   Please ensure cursorRules_v_0_2 directory exists"
    exit 1
fi

echo "📁 Found .cursor directory in: $(pwd)"
echo "📁 v0.2 source directory: $V0_2_SOURCE"
echo ""

# Step 1: Backup current memory
echo "🔄 Step 1: Backing up current memory..."
if [ -f ".cursor/memory/memory.md" ]; then
    cp ".cursor/memory/memory.md" ".cursor/memory/memory_v0_1_backup.md"
    echo "✅ Backup created: .cursor/memory/memory_v0_1_backup.md"
else
    echo "⚠️  Warning: No existing memory.md found to backup"
fi

# Step 2: Copy updated rule files
echo ""
echo "🔄 Step 2: Updating rule files..."
cp "$V0_2_SOURCE/.cursor/rules/"* ".cursor/rules/"
echo "✅ Rule files updated"

# Step 3: Copy new memory template
echo ""
echo "🔄 Step 3: Creating new memory template..."
cp "$V0_2_SOURCE/.cursor/memory/memory.md" ".cursor/memory/memory_v0_2_template.md"
echo "✅ Memory template created: .cursor/memory/memory_v0_2_template.md"

# Step 4: Copy updated README if it exists
if [ -f "$V0_2_SOURCE/README.md" ]; then
    echo ""
    echo "🔄 Step 4: Updating README..."
    cp "$V0_2_SOURCE/README.md" ".cursor/rules/README.md"
    echo "✅ README updated"
fi

echo ""
echo "🎉 Migration files copied successfully!"
echo ""
echo "📋 Next Steps:"
echo "   1. Review the backup: .cursor/memory/memory_v0_1_backup.md"
echo "   2. Review the template: .cursor/memory/memory_v0_2_template.md"
echo "   3. Tell your Cursor Agent to migrate using the MIGRATION_GUIDE.md"
echo ""
echo "💡 The key change: Memory now focuses on cross-cutting insights"
echo "   rather than current task progress."
echo ""
echo "📖 See MIGRATION_GUIDE.md for detailed instructions"
