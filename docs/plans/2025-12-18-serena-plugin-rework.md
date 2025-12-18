# Serena Plugin Rework Specification

**Date:** 2025-12-18
**Status:** Draft
**Author:** Claude (senior analysis)

## Executive Summary

The serena-integration plugin has evolved organically and needs restructuring to match the established bridge/jira plugin architecture. This will improve maintainability, reduce code duplication, enable proper testing, and provide consistent UX across all CLI tools.

---

## Current State Analysis

### Directory Structure (Current)

```
serena-integration/
├── agents/                    # ✓ Keep - Claude agent definitions
├── bin/
│   └── serena                 # ⚠ Needs rework - bash dispatcher
├── .claude-plugin/
│   └── plugin.json            # ✓ Keep - plugin metadata
├── commands/                  # ✓ Keep - slash commands
├── docs/plans/                # ✓ Keep - planning docs
├── hooks/                     # ✓ Keep - Claude hooks
├── skills/serena/
│   ├── scripts/
│   │   ├── connector.py       # ⚠ Should be in serena/ package
│   │   ├── plugin.py          # ⚠ Should be in serena/ package
│   │   ├── routes/            # ⚠ Should be in serena/ package
│   │   └── serena_cli/        # ⚠ Nested package - awkward
│   └── references/            # ✓ Keep - skill docs
└── README.md
```

### Problems Identified

| Issue | Impact | Severity |
|-------|--------|----------|
| Python code buried in `skills/serena/scripts/` | Hard to find, test, package | High |
| No `pyproject.toml` | Can't pip install, no dependency management | High |
| No `.venv/` isolation | Uses bridge's venv implicitly | Medium |
| `bin/serena` is bash dispatcher | Complex routing logic, no setup command | Medium |
| `serena_cli/` nested awkwardly | Import path confusion | Medium |
| No tests directory | Zero test coverage | High |
| Duplicate permission logic needed | If we add setup, duplicates bridge | Low |

---

## Target State (Benchmark: jira plugin)

### Directory Structure (Target)

```
serena-integration/
├── agents/                    # Claude agent definitions
├── bin/
│   └── serena                 # Thin wrapper with setup command
├── .claude-plugin/
│   └── plugin.json            # Plugin metadata
├── commands/                  # Slash commands
├── docs/                      # Documentation
├── hooks/                     # Claude hooks
├── pyproject.toml             # NEW: Package definition
├── pytest.ini                 # NEW: Test config
├── README.md
├── serena/                    # NEW: Main Python package
│   ├── __init__.py
│   ├── connector.py           # Moved from scripts/
│   ├── plugin.py              # Moved from scripts/
│   ├── response.py            # Moved from scripts/
│   ├── deps.py                # Moved from scripts/
│   ├── cli/                   # NEW: CLI subpackage
│   │   ├── __init__.py
│   │   ├── client.py          # From serena_cli/
│   │   ├── commands.py        # CLI command definitions
│   │   ├── formatters.py      # From serena_cli/
│   │   ├── main.py            # Entry point
│   │   └── session.py         # From serena_cli/
│   ├── routes/                # Moved from scripts/routes/
│   │   ├── __init__.py
│   │   ├── edit.py
│   │   ├── find.py
│   │   ├── memory.py
│   │   ├── onboarding.py
│   │   ├── search.py
│   │   └── status.py
│   └── lib/                   # NEW: Shared utilities
│       ├── __init__.py
│       └── lsp.py             # LSP protocol helpers
├── skills/serena/             # Skill definition only
│   ├── SKILL.md
│   ├── manifest.json
│   └── references/            # Skill reference docs
└── tests/                     # NEW: Test suite
    ├── __init__.py
    ├── conftest.py
    ├── test_connector.py
    ├── test_routes.py
    └── test_cli.py
```

---

## Implementation Plan

### Phase 1: Package Foundation

**Goal:** Create proper Python package structure without breaking existing functionality.

1. **Create `pyproject.toml`**
   ```toml
   [project]
   name = "serena"
   version = "1.1.0"
   description = "Semantic code intelligence via LSP for AI agents"
   requires-python = ">=3.11"
   dependencies = [
       "httpx>=0.25.0",
       "structlog>=23.2.0",
   ]

   [project.scripts]
   serena = "serena.cli.main:main"

   [project.optional-dependencies]
   dev = ["pytest>=7.4.0", "pytest-asyncio>=0.21.0", "ruff>=0.1.0"]

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"
   ```

2. **Create `serena/` package directory**
   - Move `scripts/*.py` → `serena/`
   - Move `scripts/routes/` → `serena/routes/`
   - Move `scripts/serena_cli/` → `serena/cli/`
   - Update all imports

3. **Create pytest.ini**
   ```ini
   [pytest]
   asyncio_mode = auto
   testpaths = tests
   ```

### Phase 2: CLI Rework

**Goal:** Unified CLI with setup command, matching bridge/jira pattern.

1. **New `bin/serena` wrapper**
   ```bash
   #!/bin/bash
   # Serena CLI wrapper with auto-setup

   set -e

   PLUGIN_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
   VENV_DIR="$PLUGIN_DIR/.venv"
   SERENA_BIN="$VENV_DIR/bin/serena"
   CLAUDE_SETTINGS="$HOME/.claude/settings.local.json"

   # [add_claude_permission function - same as bridge]

   setup_venv() {
       echo "Setting up Serena..." >&2

       if [[ ! -d "$VENV_DIR" ]]; then
           python3 -m venv "$VENV_DIR"
       fi

       "$VENV_DIR/bin/pip" install --quiet --upgrade pip
       "$VENV_DIR/bin/pip" install --quiet -e "$PLUGIN_DIR"

       # Symlink
       LOCAL_BIN="$HOME/.local/bin"
       ln -sf "$SERENA_BIN" "$LOCAL_BIN/serena"

       # Permission
       add_claude_permission 'Bash(serena:*)'

       echo "Setup complete." >&2
   }

   if [[ ! -x "$SERENA_BIN" ]]; then
       setup_venv
   fi

   if [[ "$1" == "setup" ]]; then
       setup_venv
       echo "Serena is ready."
       exit 0
   fi

   exec "$SERENA_BIN" "$@"
   ```

2. **New `serena/cli/main.py`**
   - Consolidate command routing (currently in bash)
   - Use Click or argparse for proper CLI
   - Commands: find, refs, overview, status, search, recipe, memory, edit, tools, activate, setup

### Phase 3: Test Suite

**Goal:** Basic test coverage for critical paths.

```python
# tests/test_connector.py
async def test_connector_connect():
    """Test SerenaConnector connection lifecycle."""

# tests/test_routes.py
async def test_find_symbol():
    """Test symbol search route."""

# tests/test_cli.py
def test_cli_help():
    """Test CLI help output."""
```

### Phase 4: Cleanup

1. Remove old `scripts/` directory
2. Update skill references to new paths
3. Update README with new structure
4. Bump version to 1.1.0

---

## Migration Path

```
Week 1: Phase 1 (Package Foundation)
  - Create pyproject.toml
  - Move files, fix imports
  - Verify bridge still loads plugin

Week 2: Phase 2 (CLI Rework)
  - New bin/serena wrapper
  - Python CLI entry point
  - Test setup command

Week 3: Phase 3 + 4 (Tests & Cleanup)
  - Add test suite
  - Remove old structure
  - Documentation update
```

---

## Shared Utilities Consideration

Both bridge and plugins duplicate:
- `add_claude_permission()` function
- Setup logic patterns
- Permission patterns

**Future consideration:** Extract to shared `claude-plugin-utils` package:
```python
from claude_plugin_utils import add_permission, setup_cli_link
```

Not in scope for this rework, but worth noting for future DRY improvement.

---

## Success Criteria

- [ ] `serena setup` creates symlink and adds permission
- [ ] `pip install -e .` works in plugin directory
- [ ] `pytest` runs with >80% coverage on critical paths
- [ ] Bridge loads serena plugin without changes
- [ ] All existing CLI commands work identically
- [ ] No bash command routing (all in Python)

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking bridge plugin loading | Test plugin.py interface unchanged |
| Import path breaks | Careful import updates, test each move |
| Bash→Python CLI parity | Document all commands, test each |
| Downstream skill breakage | Keep skill paths stable, symlink if needed |

---

## Appendix: File Mapping

| Current Location | Target Location |
|------------------|-----------------|
| `skills/serena/scripts/connector.py` | `serena/connector.py` |
| `skills/serena/scripts/plugin.py` | `serena/plugin.py` |
| `skills/serena/scripts/response.py` | `serena/response.py` |
| `skills/serena/scripts/deps.py` | `serena/deps.py` |
| `skills/serena/scripts/routes/*.py` | `serena/routes/*.py` |
| `skills/serena/scripts/serena_cli/*.py` | `serena/cli/*.py` |
| `skills/serena/scripts/serena` (bash) | DELETED (logic in bin/serena) |
| `skills/serena/scripts/serena-fast` (bash) | DELETED (commands in Python) |
