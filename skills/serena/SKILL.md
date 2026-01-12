---
name: serena
description: "Use when navigating PHP code - finding class definitions, method implementations, callers, or code structure. Triggers: 'where is X defined', 'find class', 'find method', 'who calls this', 'find usages', 'find references', 'show class structure'."
---

# Serena: Semantic PHP Code Navigation

**Iron Law:** PHP code navigation = Serena. Not grep. Not glob. Not Explore agent.

## Backend Selection

Serena supports two backends. **Choose based on your project:**

| Project Type | Backend | Why |
|-------------|---------|-----|
| **Oro Commerce / Symfony** | JetBrains | Framework awareness via PhpStorm plugins |
| **Laravel / Plain PHP** | LSP | Lighter weight, no IDE required |
| **Need vendor navigation** | JetBrains | Full vendor indexing without perf hit |
| **Quick standalone analysis** | LSP | No IDE dependency |

**For Oro/Symfony projects: Use JetBrains backend.** See `references/backends.md`.

## Tool Selection

| File Type | Tool |
|-----------|------|
| PHP class/method | `serena find_symbol` |
| PHP references | `serena find_referencing_symbols` |
| Vendor/external libs | JetBrains backend required |
| JavaScript | `serena search_for_pattern` |
| Twig/YAML/XML | `grep` |

## Rationalizations = Failure

| Thought | Reality |
|---------|---------|
| "Quick grep first" | `find_symbol` is faster AND accurate |
| "Grep finds all usages" | Grep finds TEXT. `find_referencing_symbols` finds CODE |
| "Simple search" | Simple searches benefit MOST from semantic tools |
| "Search src/ first" | Integration classes live in vendor. Search globally |
| "Time pressure" | Incomplete results waste MORE time |
| "Serena timed out" | Follow timeout steps below, don't switch to grep |
| "Parallel searches for speed" | LSP is sequential. Run one serena command at a time |
| "Can't find in vendor" | Switch to JetBrains backend or configure `ignore_vendor: false` |

## Quick Reference

| Task | Command |
|------|---------|
| Find class | `serena find_symbol --name_path_pattern X` |
| With source code | `--include_body true` |
| Get methods | `--depth 1` |
| Substring match | `--substring_matching true` |
| Find callers | `serena find_referencing_symbols --name_path X --relative_path file.php` |
| Regex search | `serena search_for_pattern --substring_pattern "pattern"` |
| Check status | `serena get_current_config` |
| Activate project | `serena activate_project --project_name_or_path .` |

## Vendor Directory Access

**Problem:** LSP excludes vendor by default (15s queries with vendor).

**Solutions:**

1. **JetBrains backend** (recommended for Oro):
   ```yaml
   # ~/.serena/serena_config.yml
   language_backend: JetBrains
   ```

2. **LSP with vendor enabled** (slower):
   ```yaml
   # .serena/project.yml
   ls_specific_settings:
     php:
       ignore_vendor: false
   ```

## Timeout Recovery

1. `serena get_current_config` - verify activated
2. Broaden pattern: `PaymentMethodProvider` → `PaymentMethod`
3. Add `--relative_path` (only if NOT searching integration code)
4. Try `search_for_pattern` instead of `find_symbol`
5. Restart: `serena activate_project --project_name_or_path .`

**Only after ALL fail:** grep, but document results may be incomplete.

## Common Mistakes

| Problem | Fix |
|---------|-----|
| "No symbols found" | `--substring_matching true` or broaden pattern |
| Empty refs | Run `find_symbol` first to get exact path |
| Missing vendor code | Use JetBrains backend or `ignore_vendor: false` |
| "Tool not found" | Check backend: LSP has `find_symbol`, JetBrains has `jet_brains_find_symbol` |

## Reference Files

| File | Use For |
|------|---------|
| `references/backends.md` | JetBrains vs LSP setup and comparison |
| `references/symfony-oro.md` | Symfony/Oro framework patterns |
| `references/symbol-kinds.md` | Filter by symbol type |
| `references/editing-patterns.md` | Code edits with `replace_symbol_body` |
| `references/memory.md` | Memory system with folders, archiving, search |
| `references/cli-reference.md` | Complete CLI documentation |

**Help:** `serena help <tool_name>`
