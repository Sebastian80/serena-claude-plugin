---
name: onboard
description: Activate project in Serena, run onboarding, and load existing memories for session handoff
allowed-tools:
  - Bash
  - Read
---

# Serena Project Onboarding

Perform complete Serena project setup and session initialization.

## Steps to Execute

### 1. Check Status & Activate Project

```bash
serena get_current_config
```

If no project is active or wrong project is active:

```bash
serena activate_project --project "$(pwd)"
```

If activation times out (common for large codebases), run `serena get_current_config` to verify.

### 2. List Available Memories

```bash
serena list_memories
```

### 3. Read Key Memories

```bash
# Project overview
serena read_memory --memory_file_name project_overview

# Any task context from previous session
serena read_memory --memory_file_name task_context
```

## Output

After completing all steps, summarize:

1. **Project Status**: Activated and onboarded?
2. **Available Memories**: List of memory names
3. **Key Context**: Summary of project_overview and task_context
4. **Ready for Work**: Confirm Serena is ready

## Example Summary

```
## Serena Onboarding Complete

**Project**: /home/sebastian/workspace/hmkg
**Status**: Activated and onboarded

### Available Memories
- project_overview
- code_conventions
- bundle_architecture
- task_context

### Project Context
[Summary from project_overview memory]

### Previous Task
[Summary from task_context memory, if exists]

Serena is ready. 23 tools available.
```
