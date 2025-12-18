---
name: serena
description: "MANDATORY for PHP code navigation - use INSTEAD of grep/glob when finding PHP definitions, callers, or code structure. Semantic LSP search via Intelephense. Triggers: where is X defined, find class, find method, who calls this, find usages, show methods, find implementations, what calls this, find references, show class structure. Use grep for JS/Twig/YAML."
---

<EXTREMELY-IMPORTANT>
# MANDATORY: Code Navigation = Serena First

**Use Serena FIRST. Always. No exceptions.**

## The Iron Law

```
CODE NAVIGATION IN CONFIGURED LANGUAGES = SERENA
```

Using grep/glob when Serena is available? Delete your search. Use Serena.

**No exceptions:**
- Not for "quick" searches
- Not because user asked for grep
- Not under time pressure
- Not for "simple" lookups

## Rationalizations That Mean You're About To Fail

If you catch yourself thinking ANY of these, STOP:

- "Let me just grep quickly" → WRONG. `serena find_symbol` is faster AND accurate.
- "Grep will find all usages" → WRONG. Grep finds TEXT. `serena find_referencing_symbols` finds CODE REFERENCES.
- "I'll use the Task/Explore agent" → WRONG. Use Serena directly.
- "This is a simple search" → WRONG. Simple searches benefit MOST from semantic tools.
- "I'll search src/ first, then global" → WRONG. For integration classes, this ALWAYS fails.
- "It's probably in our custom code" → WRONG. Custom code extends vendor classes. Search globally.
- "I'm under time pressure" → WRONG. Incomplete results waste MORE time.
- "User explicitly asked for grep" → WRONG. Users want RESULTS, not tools. Use Serena, explain why.
- "I don't want to seem pedantic" → WRONG. Using the right tool is professional, not pedantic.
- "I'll run parallel searches for speed" → WRONG. LSP is sequential. Run one search at a time.
- "Serena timed out, I'll use grep" → WRONG. See "If Serena Times Out" section first.

## MANDATORY: Global Search Decision Gate

**BEFORE adding `--relative_path`, answer:**

```
Pattern contains: Payment, Transaction, Checkout, Order, Invoice,
                 Mollie, Stripe, Provider, Integration, Gateway?

YES/UNSURE → Search globally. NO --relative_path.
NO (and user specified scope) → MAY use --relative_path.
```

30 seconds complete > 0.5s + confusion + 30s retry.
</EXTREMELY-IMPORTANT>

## Red Flags - STOP and Check

- Using grep for PHP class/method lookup → Use Serena
- Using glob to find PHP files → Use Serena
- "Let me search src/ first" → Search globally
- Dispatching Explore agent for code navigation → Use Serena
- Running multiple serena commands in parallel → Run sequentially
- Falling back to grep after one timeout → Follow timeout steps
- Using `find_symbol` for JavaScript → Use `search_for_pattern` (JS not indexed by LSP)
- Using serena for Twig/YAML → Use grep (not indexed)

**Check the "When to Use vs NOT Use" table.**

## Quick Reference

### Finding Code

| Task | Command |
|------|---------|
| Find class | `serena find_symbol --name_path_pattern X` |
| Find method in class | `serena find_symbol --name_path_pattern "Class/method"` |
| Find with source | `serena find_symbol --name_path_pattern X --include_body true` |
| Get class methods | `serena find_symbol --name_path_pattern X --depth 1` |
| Restrict to path | `serena find_symbol --name_path_pattern X --relative_path src/` |
| Substring match | `serena find_symbol --name_path_pattern X --substring_matching true` |

### Finding References

```bash
# Step 1: Find symbol to get exact path
serena find_symbol --name_path_pattern CustomerService

# Step 2: Find who uses it (requires file path)
serena find_referencing_symbols --name_path CustomerService --relative_path src/Service/CustomerService.php
```

### Common Commands

| Task | Command |
|------|---------|
| Check status | `serena get_current_config` |
| Regex search | `serena search_for_pattern --substring_pattern "regex"` |
| File structure | `serena get_symbols_overview --relative_path path.php` |
| List files | `serena list_dir --relative_path src/ --recursive false` |
| Find file | `serena find_file --file_mask "*.php" --relative_path src/` |

## Automatic Triggers

| User Says | You Run |
|-----------|---------|
| "Find class X" / "Where is X defined" | `serena find_symbol --name_path_pattern X --include_body true` |
| "Who calls X" / "Find usages" | `serena find_referencing_symbols --name_path X --relative_path file.php` |
| "What methods does X have" | `serena find_symbol --name_path_pattern X --depth 1` |
| "Search for pattern" | `serena search_for_pattern --substring_pattern "pattern"` |

## When to Use vs NOT Use

| USE `find_symbol` | USE `search_for_pattern` | USE grep |
|-------------------|--------------------------|----------|
| PHP class/method/function | JavaScript files | Twig templates |
| PHP references | Text in AMD modules | HTML files |
| PHP code structure | | YAML/XML config |

**Rule:**
- `find_symbol` = languages in `.serena/project.yml` (semantic LSP search)
- `search_for_pattern` = JS, text patterns (respects ignored_paths)
- grep = templates, config files

**This project:** Only `php` is LSP-configured.

**Check config:** `cat .serena/project.yml | grep -A5 "languages:"`

## Multi-File-Type Searches

When searching across PHP + JS + templates + config:

| File Type | Tool | Why |
|-----------|------|-----|
| PHP classes/methods | `serena find_symbol` | Semantic code navigation |
| JavaScript files | `serena search_for_pattern` | Text search, respects ignored_paths |
| Twig/HTML templates | `grep` | Templates not indexed |
| YAML/XML config | `grep` | Config not indexed |

**JS Search Example:**
```bash
serena search_for_pattern --substring_pattern "ShippingMethodsView" --paths_include_glob "*.js"
```

**Why search_for_pattern over grep for JS?**
- Respects project's `ignored_paths` (skips node_modules, var/, etc.)
- Returns line numbers and context
- Works inside AMD `define()` wrappers (which LSP can't parse)

**Workflow:** Search PHP FIRST (Serena), then JS/templates/config.

**Pattern expansion:** If `ShippingCost` returns nothing, try `shipping_cost` (snake_case) or translation keys.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "No symbols found" | Use `--substring_matching true` or broaden pattern: `CustomerEntity` → `Customer` |
| Empty refs | Use `find_symbol` first to get exact symbol path and file |
| Incomplete results | Remove `--relative_path` - may be missing vendor code |
| Empty results | Run `serena get_current_config` - project not activated |
| Timeout | See "If Serena Times Out" below |

## If Serena Times Out

**DO NOT immediately fall back to grep.** Try in order:

1. Run `serena get_current_config` - verify project is activated
2. Use `--substring_matching true` or broaden pattern: `PaymentMethodProvider` → `PaymentMethod`
3. Add `--relative_path` to reduce scope (only if NOT an integration pattern)
4. Try `serena search_for_pattern` (regex) instead of `find_symbol` (semantic)
5. Check if LSP server needs restart: `serena activate_project --project_name_or_path .`

**Only after all above fail:** Use grep WITH documentation that results may be incomplete.

**Never silently switch to grep** - incomplete results cause more problems than waiting.

## Performance Notes

- **No parallel serena commands** - LSP processes sequentially. Run one at a time.
- Global search: ~20-30s (complete results)
- Path-restricted: ~0.5-3s (may miss vendor code)
- Recipes: ~0.5s (pre-optimized)

## Verification Checklist

Before moving on from a code search task:

- [ ] Used `serena find_symbol` instead of grep for code lookup
- [ ] Used global search for integration patterns (Payment, Order, Mollie, etc.)
- [ ] Ran `serena get_current_config` if results were empty
- [ ] Used `--depth 1` to get class methods

## Project Activation

```bash
serena get_current_config                              # Check current project
serena activate_project --project_name_or_path /path/to/project  # Activate if needed
```

## Deep Reference

Only read if Quick Reference doesn't answer your question:

| File | When to Read |
|------|--------------|
| `references/symbol-kinds.md` | Filter by symbol type (include_kinds/exclude_kinds integers) |
| `references/editing-patterns.md` | Complex code edits with replace_symbol_body |
| `references/session-handoff.md` | Serena memory system for session continuity |

**For most tasks, the Quick Reference above is sufficient.**

**Get full tool help:** `serena help <tool_name>` (e.g., `serena help find_symbol`)
