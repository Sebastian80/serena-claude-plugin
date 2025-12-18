---
description: Save current session state to Serena memories for cross-session continuity
allowed-tools:
  - Bash
---

# /serena:save - Persist Session Context

Save current session state to Serena memories.

## Execute These Steps

### 1. Gather Session Context

Before saving, analyze the current session:
- What tasks were worked on?
- What was accomplished?
- What's still in progress?
- What was learned?

### 2. Save Session State

```bash
serena write_memory --memory_file_name "sessions/$(date '+%Y-%m-%d')" --content "## Session: $(date '+%Y-%m-%d')

### What I Worked On
- [list main tasks]

### Current State
[describe where things are at]

### Key Files Modified
- [file paths]
"
```

### 3. Save Task Progress (if working on ticket)

```bash
serena write_memory --memory_file_name "tasks/HMKG-XXXX" --content "## Task: [name]

### Status: in_progress

### Completed
- [x] Step 1

### Remaining
- [ ] Next step

### Key Files
- [file paths]
"
```

### 4. Save Learnings (if discovered something)

```bash
serena write_memory --memory_file_name "learnings/[topic]" --content "## [Topic]

### Context
[when you might need this]

### Details
[what you learned]
"
```

### 5. Archive Completed Tasks

```bash
serena archive_memory --memory_file_name "tasks/HMKG-XXXX" --category "completed"
```

### 6. Confirm Save

```bash
serena list_memories
serena memory_stats
```

Report what was saved:
```
## Session Saved

**Memories Updated:**
- sessions/[date]
- tasks/[ticket]

**Learnings Added:**
- learnings/[topic]

Ready for session handoff.
```
