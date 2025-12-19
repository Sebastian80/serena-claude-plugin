# Serena Integration Plugin

Claude Code integration with Serena LSP for semantic PHP code navigation.

## Architecture

```
serena CLI (bin/serena)
    ↓ MCP streamable-http
Serena MCP Server (port 9121)
    ↓
Intelephense LSP
```

Standalone MCP client - no bridge dependency.

## Setup

### 1. Serena MCP Server

Run Serena via Docker:

```bash
cd ~/workspace/KI_Tools/serena
docker compose up -d
```

### 2. CLI Setup

```bash
# One-time setup (creates venv, installs deps, adds permissions)
~/.claude/plugins/.../serena-integration/bin/serena setup

# Or run any command (auto-setup on first use)
serena get_current_config
```

### 3. Permissions

Added automatically by setup:
- `Bash(serena:*)` - CLI access
- `Skill(serena:*)` - Skill access

## CLI Commands

```bash
serena get_current_config                    # Check status
serena activate_project --project /path      # Activate project
serena find_symbol --name_path_pattern X     # Find symbol
serena find_referencing_symbols --name_path X --relative_path file.php
serena get_symbols_overview --relative_path file.php
serena search_for_pattern --substring_pattern "pattern"
serena list_memories                         # List memories
serena read_memory --memory_file_name name   # Read memory
serena help                                  # Full command list
serena help <tool>                           # Tool-specific help
```

## Skills

### serena

Core Serena usage - semantic PHP code navigation via LSP:
- Iron law: Use Serena for PHP, not grep
- Tool selection: `find_symbol` for PHP, `search_for_pattern` for JS
- Command reference and troubleshooting

## Slash Commands

- `/serena:onboard` - Activate project and load memories
- `/serena:load` - Load memories from previous session
- `/serena:save` - Save session state to memories

## Project Configuration

Per-project settings in `.serena/project.yml`:

```yaml
languages:
- php

ignore_all_files_in_gitignore: false
ignored_paths:
  - node_modules
  - var/cache
```

## Changelog

- **2.0.0**: Standalone MCP client - no bridge dependency
- **1.1.0**: Added slash commands, memory management
- **1.0.0**: Initial release with bridge dependency
