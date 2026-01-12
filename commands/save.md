---
description: Save current session state to Serena memories for cross-session continuity
allowed-tools:
  - Bash
---

# /serena:save - Persist Session Context

## Steps

### 1. Analyze Current Session

Before saving, identify:
- What tasks were worked on?
- What was accomplished?
- What's still in progress?

### 2. Save Session State

```bash
serena write_memory --memory_file_name "active/sessions/current" --content "## Session: $(date '+%Y-%m-%d')

### Working On
- [task/ticket]

### Progress
- [what was done]

### Next
- [what's remaining]
"
```

### 3. Save/Update Task Progress

```bash
serena write_memory --memory_file_name "active/tasks/TICKET-ID" --content "## TICKET-ID: [title]

### Status: in_progress

### Done
- [x] Completed step

### Next
- [ ] Remaining step

### Key Files
- [paths]
"
```

### 4. Archive Completed Tasks

```bash
serena archive_memory --memory_file_name "active/tasks/TICKET-ID" --category "completed"
```

### 5. Save Learnings (if any)

```bash
serena write_memory --memory_file_name "learnings/discoveries/[topic]" --content "## [Topic]

[what you learned and when it's useful]
"
```

### 6. Confirm

```bash
serena tree_memories
serena memory_stats
```

Report:
```
## Session Saved

**Updated:**
- active/sessions/current
- active/tasks/[ticket]

**Archived:**
- [completed tickets]

Ready for handoff.
```
