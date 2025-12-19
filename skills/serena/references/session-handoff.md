# Session Handoff Patterns

How to persist context across Claude Code sessions using Serena memories.

## Why Session Handoff?

Claude Code sessions are stateless. Serena memories provide:
- Persistent storage across sessions
- Project-specific context
- Task continuation without re-explaining
- Shared knowledge between agents

## Memory Naming Conventions

| Memory Name | Purpose |
|-------------|---------|
| `project_overview` | High-level project description |
| `code_conventions` | Coding standards and patterns |
| `bundle_architecture` | Module/bundle structure |
| `task_context` | Current task state |
| `task_completion` | Completed task summary |
| `suggested_commands` | Useful commands for project |

## Handoff Workflow

### End of Session

Before ending work, save context:

```bash
serena write_memory --memory_file_name task_context --content "## Current Task
Implementing customer validation

## Progress
- [x] Added CustomerValidator class
- [x] Added validation rules
- [ ] Add unit tests
- [ ] Wire into form

## Key Files
- src/Validator/CustomerValidator.php
- src/Form/CustomerType.php

## Notes
- Using Symfony Validator component
- Need to handle legacy customers specially"
```

### Start of Session

Resume work by reading memories:

```bash
# List available memories
serena list_memories

# Read relevant context
serena read_memory --memory_file_name project_overview
serena read_memory --memory_file_name task_context
```

### After Completing Task

Update completion status:

```bash
serena write_memory --memory_file_name task_completion --content "## Completed: Customer Validation
Date: 2025-12-05

### What was done
- CustomerValidator with all rules
- Unit tests (15 passing)
- Wired into CustomerType form
- Legacy customer handling

### Files changed
- src/Validator/CustomerValidator.php (new)
- src/Form/CustomerType.php (modified)
- tests/Validator/CustomerValidatorTest.php (new)"
```

## Memory Templates

### Project Overview Template

```markdown
# Project Name

## Tech Stack
- Language: PHP 8.2
- Framework: Symfony 5.4
- Database: PostgreSQL 15

## Key Directories
- src/Entity/ - Doctrine entities
- src/Service/ - Business logic
- src/Controller/ - HTTP handlers

## Important Patterns
- Repository pattern for data access
- Event-driven architecture
- DI for all services
```

### Task Context Template

```markdown
## Current Task
[Brief description]

## Progress
- [x] Completed step
- [ ] Pending step

## Key Files
- path/to/file.php

## Blockers/Notes
- Any issues or important notes
```

## Agent-to-Agent Handoff

Agents can write findings to memory for the main context:

```bash
# Agent writes exploration results
serena write_memory --memory_file_name exploration_results --content "## Architecture Analysis: Authentication

### Key Classes
- AuthenticationManager (src/Security/AuthenticationManager.php)
- TokenValidator (src/Security/TokenValidator.php)

### Flow
1. Request hits AuthenticatorMiddleware
2. Token extracted and validated
3. User loaded from UserProvider
4. SecurityContext populated

### Entry Points
- /api/login -> LoginController
- /api/refresh -> TokenController"
```

Then in main context:

```bash
# Read agent's findings
serena read_memory --memory_file_name exploration_results
```

## Tips

1. **Keep memories focused**: One topic per memory
2. **Use markdown**: For readability and structure
3. **Include dates**: For time-sensitive context
4. **List files changed**: Helps resume work
5. **Note blockers**: Don't lose important issues
6. **Clean up old memories**: `serena delete_memory --memory_file_name old_task`
