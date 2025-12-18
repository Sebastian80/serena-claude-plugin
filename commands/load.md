---
description: Restore Serena session context by loading memories from previous sessions
allowed-tools:
  - Bash
  - Read
---

# /serena:load - Restore Session Context

Quick session restoration with memory recovery.

## Execute These Steps

### 1. Check Status & Activate

```bash
serena get_current_config
```

If no project active:
```bash
serena activate_project --project "$(pwd)"
```

### 2. Show Memory Structure

```bash
serena tree_memories
```

### 3. List Available Memories

```bash
serena list_memories
```

### 4. Load Key Memories

```bash
serena read_memory --memory_file_name project_overview
serena read_memory --memory_file_name task_context
```

Load any session-specific memories that exist.

### 5. Report Session State

Present a structured summary:

```
## Session Restored

**Project**: [project path]
**Languages**: PHP

### Available Memories
[List from list_memories]

### Project Context
[Summary from project_overview]

### Previous Task
[Summary from task_context if exists]

Ready to continue.
```
