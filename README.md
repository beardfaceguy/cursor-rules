# Cursor Rules Project

A comprehensive collection of guidelines, rules, and best practices for Cursor AI agents working on development projects.

## Overview

This project contains structured guidelines and rules designed to ensure consistent, safe, and effective behavior from Cursor AI agents across different development environments and projects.

## Project Structure

```
cursor_rules/
├── README.md                    # This file - project overview
├── MIGRATION_GUIDE.md          # Step-by-step migration instructions
├── migrate_to_v0_2.sh          # Automated migration script
├── FINETUNING_GUIDE.md         # Complete LLM fine-tuning guide
├── QUICK_START_FINETUNING.md   # Quick start for fine-tuning
├── CURSOR_CUSTOM_MODEL_GUIDE.md # Integrate fine-tuned model into Cursor
├── ALTERNATIVE_AI_IDES_GUIDE.md # Alternative IDEs with better custom model support
├── extract_training_data.py     # Extract training data from memory.md
├── evaluate_model.py           # Evaluate fine-tuned model performance
├── cursorRules_v_0_1/          # Version 0.1 of cursor rules
│   ├── README.md               # Detailed guidelines for v0.1
│   └── cursor-system.zip       # Compressed cursor system files
└── cursorRules_v_0_2/          # Version 0.2 of cursor rules (latest)
    └── README.md               # Updated guidelines for v0.2
```

## Versions

### Version 0.2 (Latest)
- **Location**: `cursorRules_v_0_2/`
- **Focus**: Cross-cutting insights and reusable knowledge
- **Memory Management**: Updated to track cross-cutting insights rather than session-specific state
- **Key Features**:
  - Comprehensive `.cursor/` directory system
  - 6 specialized rule files for AI behavior
  - Cross-cutting insights tracking
  - Implementation plans and setup guides
  - Backup and recovery capabilities

### Version 0.1
- **Location**: `cursorRules_v_0_1/`
- **Focus**: Session state management
- **Archive**: Contains the original implementation with session-based memory tracking

## Key Features

### 🚨 Mandatory Rules
1. **Memory Tracking**: Update `.cursor/memory/memory.md` with cross-cutting insights
2. **Implementation Tracking**: Maintain both memory and implementation files
3. **Command Safety**: Never use unescaped `!` in shell commands
4. **Interactive Commands**: Use non-interactive flags (`--no-pager`, `| cat`, etc.)
5. **Long Commands**: Run extended operations in background
6. **Filesystem Timing**: Check size before long filesystem operations

### 📁 Directory Structure
- **`rules/`** - AI Assistant Behavior Rules (6 specialized files)
- **`memory/`** - Cross-cutting insights and reusable knowledge
- **`docs/`** - Implementation plans and setup guides
- **`patches/`** - Backup and recovery files

## Usage

1. **For New Projects**: Copy the `.cursor/` directory structure from `cursorRules_v_0_2/`
2. **For Existing Projects**: Review and adapt the rules to your project's needs
3. **For AI Agents**: Follow the guidelines in the README files within each version

## Getting Started

### For New Projects
1. Review the README in `cursorRules_v_0_2/` for the latest guidelines
2. Understand the `.cursor/` directory structure
3. Adapt the rules to your specific project requirements
4. Implement the memory tracking and documentation systems

### For Existing Projects (Migration from v0.1)
If you have a Cursor Agent already running on v0.1 and don't want to start over:

1. **Use the Migration Guide**: See `MIGRATION_GUIDE.md` for step-by-step instructions
2. **Run the Migration Script**: Use `./migrate_to_v0_2.sh` to copy files automatically
3. **Tell Your Agent**: Send the migration message to your existing agent to reload with new rules

**Key Migration Benefits**:
- ✅ Preserve all your current context and progress
- ✅ Keep hard-earned insights and architectural patterns
- ✅ Upgrade to more maintainable knowledge system
- ✅ Continue working without interruption

### For Advanced Users (Fine-Tuning LLMs)
Transform your memory insights into a specialized AI assistant:

1. **Extract Training Data**: Use `extract_training_data.py` to convert memory insights into training examples
2. **Fine-Tune Model**: Follow `FINETUNING_GUIDE.md` for complete implementation
3. **Quick Start**: Use `QUICK_START_FINETUNING.md` for rapid setup
4. **Evaluate Performance**: Use `evaluate_model.py` to test your fine-tuned model

**Fine-Tuning Benefits**:
- ✅ Create AI assistant that knows your codebase patterns
- ✅ Automatically provides exact commands and solutions
- ✅ Embodies your architectural knowledge and lessons learned
- ✅ Deploy for team use or personal development workflow

### For IDE Integration (Beyond Cursor)
If you want full agent mode with custom models, consider these alternatives:

1. **Continue.dev** - Best Cursor replacement with full custom model support
2. **Zed Editor** - Most advanced agent framework with custom agent development
3. **AWS Kiro** - Enterprise-grade with Model Context Protocol support
4. **Cline** - Open source VS Code agent with autonomous coding

See `ALTERNATIVE_AI_IDES_GUIDE.md` for detailed comparison and migration guides.

## Contributing

This project represents best practices developed through extensive analysis. When contributing:

1. Follow the established patterns
2. Update documentation consistently
3. Maintain the `.cursor/` directory structure
4. Test rules in different environments

## License

This project contains guidelines and best practices for AI-assisted development. Use and adapt as needed for your projects.

---

**⚠️ Important**: These rules have been developed through extensive analysis and testing. Always follow the `.cursor/` directory guidelines to maintain consistency and avoid repeating previous mistakes.
