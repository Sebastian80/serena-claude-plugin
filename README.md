# Serena Integration Plugin

Claude Code integration with Serena LSP for semantic PHP code navigation.

## Features

- **serena skill**: Core Serena usage guidance and command reference
- **Slash commands**: `/serena:onboard`, `/serena:load`, `/serena:save`
- **CLI wrapper**: Routes to Serena MCP server via AI Tool Bridge

## Architecture

```
serena CLI → AI Tool Bridge → Serena MCP server (port 9121)
                                    ↓
                              Intelephense LSP
```

## Setup

### 1. Serena MCP Server

Run Serena via Docker:

```bash
cd ~/workspace/KI_Tools/serena
docker compose up -d
```

### 2. CLI Wrapper

The CLI at `~/.local/bin/serena` routes through the bridge:

```bash
# Setup (one-time)
~/.claude/plugins/.../serena-integration/bin/serena setup
```

### 3. Permissions

Already configured in `~/.claude/settings.json`:
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
