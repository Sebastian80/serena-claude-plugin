---
name: onboard
description: Activate project in Serena, initialize memory structure, and load session context
allowed-tools:
  - Bash
  - Read
---

# Serena Project Onboarding

## Steps

### 1. Activate Project

```bash
serena get_current_config
```

If wrong project or none active:
```bash
serena activate_project --project "$(pwd)"
```

### 2. Check Memory Structure

```bash
serena tree_memories
```

If empty or missing folders:
```bash
serena init_memories
```

### 3. Load Session Context

```bash
# List active work
serena list_memories --folder "active"

# Read current session (if exists)
serena read_memory --memory_file_name "active/sessions/current"

# Read any active tasks
serena list_memories --folder "active/tasks"
```

### 4. Load Reference Docs (if needed)

```bash
serena list_memories --folder "reference"
# Read relevant ones based on task
```

## Output Summary

```
## Serena Ready

**Project**: [path]
**Status**: Activated

### Memory Structure
[tree output]

### Active Work
- Sessions: [list]
- Tasks: [list]

### Reference Available
- [folder list]

Ready for work.
```
