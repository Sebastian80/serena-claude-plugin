# Serena CLI Reference

Complete reference for the Serena CLI. For quick overview, see SKILL.md.

## CLI Architecture

Standalone MCP client that talks directly to Serena's MCP server (port 9121).
All tools are auto-discovered from the MCP server.

```
serena <tool_name> --param value
serena help                        # List all tools
serena help <tool_name>            # Detailed tool help
```

## Core Search Tools

### find_symbol
Find symbols by pattern. This is your primary code navigation tool.

```bash
serena find_symbol --name_path_pattern <pattern> [options]

Required:
  --name_path_pattern    Symbol pattern to match

Options:
  --depth                0=symbol only, 1=include children (methods)
  --relative_path        Restrict to directory
  --include_body         Include source code (true/false)
  --substring_matching   Enable substring matching (true/false)
  --include_kinds        JSON array of LSP kind integers to include
  --exclude_kinds        JSON array of LSP kind integers to exclude
```

**Name Path Patterns:**
- Simple name: `Customer` - matches any symbol named Customer
- Relative path: `Customer/getName` - matches method in class
- Absolute path: `/Customer/getName` - exact match only

**Examples:**
```bash
serena find_symbol --name_path_pattern Customer
serena find_symbol --name_path_pattern "Customer/get" --substring_matching true
serena find_symbol --name_path_pattern CustomerService --depth 1
serena find_symbol --name_path_pattern Order --include_body true
serena find_symbol --name_path_pattern Payment --relative_path src/Service/
```

### find_referencing_symbols
Find all references to a symbol.

```bash
serena find_referencing_symbols --name_path <path> --relative_path <file>

Required:
  --name_path        Symbol path (e.g., "Class/method")
  --relative_path    File containing the symbol

Options:
  --include_kinds    JSON array of LSP kind integers to include
  --exclude_kinds    JSON array of LSP kind integers to exclude
```

**Examples:**
```bash
serena find_referencing_symbols --name_path Customer --relative_path src/Entity/Customer.php
serena find_referencing_symbols --name_path "ShippingMethod/calculate" --relative_path src/Method/ShippingMethod.php
```

### search_for_pattern
Regex search in code files.

```bash
serena search_for_pattern --substring_pattern <regex> [options]

Required:
  --substring_pattern    Regex pattern to search

Options:
  --relative_path                    Directory to search in
  --paths_include_glob              Include glob pattern
  --paths_exclude_glob              Exclude glob pattern
  --context_lines_before            Lines of context before match
  --context_lines_after             Lines of context after match
  --restrict_search_to_code_files   Only search code files (true/false)
```

**Examples:**
```bash
serena search_for_pattern --substring_pattern "implements.*Interface"
serena search_for_pattern --substring_pattern "#\[ORM\\\\Entity" --relative_path src/
```

### get_symbols_overview
Get file structure overview.

```bash
serena get_symbols_overview --relative_path <file>
```

**Examples:**
```bash
serena get_symbols_overview --relative_path src/Entity/Customer.php
```

## File Tools

### list_dir
List files in a directory.

```bash
serena list_dir --relative_path <path> --recursive <true|false>

Required:
  --relative_path    Directory to list
  --recursive        Whether to list recursively (true/false)
```

### find_file
Find files by pattern.

```bash
serena find_file --file_mask <pattern> --relative_path <dir>

Required:
  --file_mask        Filename or pattern with wildcards (* or ?)
  --relative_path    Directory to search in (use "." for project root)
```

## Memory Tools

For session continuity. See `references/session-handoff.md` for patterns.

```bash
serena list_memories
serena read_memory --memory_file_name <name>
serena write_memory --memory_file_name <name> --content "<content>"
serena search_memories --pattern <regex>
serena tree_memories
serena memory_stats
serena delete_memory --memory_file_name <name>
serena archive_memory --memory_file_name <name> [--category <category>]
serena move_memory --source <old_name> --dest <new_name>
serena edit_memory --memory_file_name <name> --needle <find> --repl <replace> [--mode literal|regex]
serena init_memories [--include_templates true]
```

## Edit Tools

Symbol-based code editing. **Use with caution - these modify files.**

### replace_symbol_body
Replace a symbol's entire body.

```bash
serena replace_symbol_body --name_path <path> --relative_path <file> --body "<code>"

Required:
  --name_path        Symbol path (e.g., "Class/method")
  --relative_path    File containing the symbol
  --body             New body code (entire symbol definition)
```

### insert_after_symbol / insert_before_symbol
Insert code relative to a symbol.

```bash
serena insert_after_symbol --name_path <path> --relative_path <file> --body "<code>"
serena insert_before_symbol --name_path <path> --relative_path <file> --body "<code>"

Required:
  --name_path        Symbol path to insert relative to
  --relative_path    File containing the symbol
  --body             Code to insert (include leading newlines)
```

### rename_symbol
Rename a symbol across the entire codebase (refactoring).

```bash
serena rename_symbol --name_path <path> --relative_path <file> --new_name <name>

Required:
  --name_path        Symbol path to rename
  --relative_path    File containing the symbol
  --new_name         New name for the symbol
```

## Project Management

### get_current_config
Check current project and available tools.

```bash
serena get_current_config
```

### activate_project
Activate a project for analysis.

```bash
serena activate_project --project_name_or_path /path/to/project
```

## Symbol Path Format

| Type | Format | Example |
|------|--------|---------|
| Class | `ClassName` | `Customer` |
| Method | `Class/method` | `Customer/getName` |
| Constructor | `Class/__construct` | `Customer/__construct` |
| Property | `Class/$property` | `Customer/$name` |
| Overload | `Class/method[0]` | `MyClass/process[0]` |

## LSP Symbol Kinds

Used with `--include_kinds` and `--exclude_kinds`. See `references/symbol-kinds.md` for full list.

| Kind | Name |
|------|------|
| 5 | Class |
| 6 | Method |
| 7 | Property |
| 9 | Constructor |
| 11 | Interface |
| 12 | Function |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No symbols found" | Use `--substring_matching true`, broaden pattern |
| Empty refs | Use `find_symbol` first to get exact file path |
| Connection error | Run `serena get_current_config`, check Serena server |
| Timeout | Add `--relative_path` to reduce scope |
| "Tool not found" | Run `serena help` to list available tools |
