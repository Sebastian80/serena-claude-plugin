# Serena Backends: JetBrains vs LSP

Serena supports two language analysis backends. Choose based on your project needs.

## Quick Comparison

| Feature | JetBrains Plugin | LSP (Intelephense) |
|---------|-----------------|-------------------|
| **Cost** | $15/year | Free |
| **IDE Required** | PhpStorm must be running | No |
| **Symfony Support** | Full (via Symfony plugin) | None |
| **Oro Support** | Full (via Oro plugin) | None |
| **Vendor Indexing** | Full, fast | Excluded or slow |
| **Query Speed** | ~0.5s (IDE cached) | 0.5s (no vendor) / 15s (vendor) |
| **Setup** | Install plugin, configure | Docker + auto-download |
| **Polyglot** | All JetBrains languages | PHP only |

## When to Use JetBrains Backend

**Use for Oro Commerce / Symfony projects:**
- PhpStorm's Symfony plugin understands service containers, routes, forms
- Oro PhpStorm plugin understands extended entities, ACLs, datagrids
- Full `vendor/oro/*` package navigation without performance penalty
- IDE-level accuracy for framework magic methods

**Requirements:**
- PhpStorm 2022.3+ with project open and indexed
- Serena JetBrains Plugin from [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/28946-serena)
- Symfony Plugin for PhpStorm (recommended)
- Oro Plugin for PhpStorm (for Oro projects)

## When to Use LSP Backend

**Use for Laravel / Plain PHP / Quick analysis:**
- No IDE dependency
- Lighter weight for simple projects
- CI/CD environments
- Remote servers

**Limitations:**
- No framework awareness (Symfony services, Doctrine magic)
- Vendor excluded by default (enable with `ignore_vendor: false`)
- 15s+ query times with vendor enabled

## JetBrains Backend Setup

### 1. Install Plugin

Install from [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/28946-serena).

### 2. Configure Serena

**Global (all projects):**
```yaml
# ~/.serena/serena_config.yml
language_backend: JetBrains
```

**Per-session:**
```bash
serena start-mcp-server --language-backend JetBrains
```

### 3. Verify

Dashboard should show: "Languages: Using JetBrains backend"

```bash
serena get_current_config
```

### 4. Keep PhpStorm Running

The JetBrains plugin exposes HTTP on ports 24226-24246. PhpStorm must have the project open and indexed.

## LSP Backend Setup

### 1. Start Serena

```bash
# Via Docker
cd ~/workspace/KI_Tools/serena
docker compose up -d

# Or via uvx
uvx --from git+https://github.com/oraios/serena serena start-mcp-server
```

### 2. Configure (Optional)

**Enable vendor (slower but complete):**
```yaml
# .serena/project.yml
ls_specific_settings:
  php:
    ignore_vendor: false
```

**Premium Intelephense features:**
```bash
export INTELEPHENSE_LICENSE_KEY=your_key
```

## Tool Name Differences

| Operation | LSP Backend | JetBrains Backend |
|-----------|------------|-------------------|
| Find symbol | `find_symbol` | `jet_brains_find_symbol` |
| Find refs | `find_referencing_symbols` | `jet_brains_find_referencing_symbols` |
| Get overview | `get_symbols_overview` | `jet_brains_get_symbols_overview` |

Serena CLI abstracts this - use `serena find_symbol` regardless of backend.

## Switching Backends

```yaml
# ~/.serena/serena_config.yml
language_backend: JetBrains  # or LSP
```

Then restart Serena:
```bash
serena activate_project --project_name_or_path .
```

## Troubleshooting

### JetBrains Backend

| Problem | Solution |
|---------|----------|
| "Connection refused" | Ensure PhpStorm is running with project open |
| "Plugin not responding" | Check plugin is enabled in PhpStorm settings |
| "Wrong project" | Open correct project in PhpStorm |
| Slow queries | Wait for IDE indexing to complete |

### LSP Backend

| Problem | Solution |
|---------|----------|
| "No symbols in vendor" | Set `ignore_vendor: false` or use JetBrains |
| 15s+ query times | Normal with vendor; use JetBrains for performance |
| Missing framework magic | LSP has no framework awareness; use JetBrains |

## Recommendation for Oro Commerce

**Use JetBrains backend with:**
1. PhpStorm + Symfony Plugin + Oro Plugin
2. Serena JetBrains Plugin
3. Global config: `language_backend: JetBrains`

This gives you:
- Full `vendor/oro/*` navigation
- Symfony service container awareness
- Oro extended entity autocomplete
- Fast queries (~0.5s)
