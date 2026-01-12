---
description: Restore Serena session context by loading memories from previous sessions
allowed-tools:
  - Bash
  - Read
---

# /serena:load - Restore Session Context

## Steps

### 1. Activate Project

```bash
serena get_current_config
```

If not active:
```bash
serena activate_project --project "$(pwd)"
```

### 2. Show Structure

```bash
serena tree_memories
```

### 3. Load Active Context

```bash
# Current session
serena read_memory --memory_file_name "active/sessions/current"

# Active tasks
serena list_memories --folder "active/tasks"
```

Read any active tasks found.

### 4. Report

```
## Session Restored

**Project**: [path]

### Active Work
[from active/sessions/current]

### Tasks In Progress
[list from active/tasks/]

### Reference Available
[list folders from reference/]

Ready to continue.
```
