# Serena Memory System

Persistent project knowledge across sessions. Supports folders, archiving, and search.

## Folder Structure

Run `serena init_memories` to create recommended structure:

```
.serena/memories/
├── active/
│   ├── tasks/          # Current tickets (HMKG-2064, etc.)
│   └── sessions/       # Current session context
├── reference/
│   ├── architecture/   # System design docs
│   ├── patterns/       # Code patterns
│   ├── integrations/   # External system docs
│   └── workflows/      # Process documentation
├── learnings/
│   ├── mistakes/       # What went wrong
│   ├── discoveries/    # What we learned
│   └── commands/       # Useful commands
├── archive/            # Historical records (auto-organized by date)
└── .templates/         # Reusable templates
```

## Quick Reference

| Task | Command |
|------|---------|
| Write memory | `serena write_memory --memory_file_name "active/tasks/HMKG-2064" --content "..."` |
| Read memory | `serena read_memory --memory_file_name "active/tasks/HMKG-2064"` |
| List all | `serena list_memories` |
| List folder | `serena list_memories --folder "active/tasks"` |
| Tree view | `serena tree_memories` |
| Search | `serena search_memories --pattern "PaymentMethod"` |
| Archive | `serena archive_memory --memory_file_name "active/tasks/HMKG-2064" --category "completed"` |
| Move/rename | `serena move_memory --source "old" --dest "learnings/discoveries/new"` |
| Edit in-place | `serena edit_memory --memory_file_name "x" --needle "old" --repl "new"` |
| Stats | `serena memory_stats` |
| Init structure | `serena init_memories` |

## Session Workflow

### Start of Session

```bash
serena list_memories --folder "active"
serena read_memory --memory_file_name "active/sessions/current"
serena read_memory --memory_file_name "active/tasks/HMKG-2064"  # if resuming ticket
```

### During Work

```bash
# Update task progress
serena write_memory --memory_file_name "active/tasks/HMKG-2064" --content "## HMKG-2064
Status: in_progress

### Done
- [x] Created validator

### Next
- [ ] Add tests"
```

### End of Session

```bash
# Save session state
serena write_memory --memory_file_name "active/sessions/current" --content "## Session $(date)
Working on: HMKG-2064
Next: Add unit tests for CustomerValidator"

# Archive completed tasks
serena archive_memory --memory_file_name "active/tasks/HMKG-2064" --category "completed"
```

## Memory Types

| Folder | Purpose | Lifecycle |
|--------|---------|-----------|
| `active/tasks/` | Current tickets | Archive when done |
| `active/sessions/` | Session context | Overwrite each session |
| `reference/` | Documentation | Long-term, update as needed |
| `learnings/` | Knowledge base | Permanent |
| `archive/` | Historical | Never delete |

## Tips

- **Nested paths**: `active/tasks/HMKG-2064` creates folders automatically
- **Archive preserves history**: Moves to `archive/YYYY-MM/category/YYYYMMDD_name`
- **Search is regex**: `serena search_memories --pattern "class.*Controller"`
- **Keep active/ clean**: Archive completed work, don't delete
