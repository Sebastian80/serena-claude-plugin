# Symfony & Oro Commerce Navigation

Framework-specific patterns for navigating Symfony and Oro Commerce codebases with Serena.

## Prerequisites

For full framework support, use **JetBrains backend** with:
- PhpStorm + Symfony Plugin
- Oro Plugin (for Oro projects)
- Serena JetBrains Plugin

See `references/backends.md` for setup.

## Oro Commerce Patterns

### Finding Oro Classes

```bash
# Bundle classes (in your bundles)
serena find_symbol --name_path_pattern CartManager --relative_path packages/

# Oro core classes (in vendor)
serena find_symbol --name_path_pattern ShoppingListManager
# Note: Requires JetBrains backend or ignore_vendor: false

# By bundle namespace
serena find_symbol --name_path_pattern "OroLab\\Bundle\\CartBundle" --substring_matching true
```

### Extended Entities (Oro 6.1+)

Extended fields moved to `serialized_data` JSON. Use JetBrains backend for autocomplete.

```bash
# Find extended entity
serena find_symbol --name_path_pattern ExtendProduct --include_body true

# Find serialized_data usage
serena search_for_pattern --substring_pattern "serialized_data"
```

### Datagrids

```bash
# Find datagrid configuration
serena search_for_pattern --substring_pattern "datagrid:" --paths_include_glob "*.yml"

# Find datagrid extensions
serena find_symbol --name_path_pattern "DatagridExtension" --include_kinds "[5]"
```

### Oro Services

```bash
# Find service definition
serena search_for_pattern --substring_pattern "oro_cart.manager" --paths_include_glob "*.yml"

# Find service class
serena find_symbol --name_path_pattern CartManager --depth 1
```

## Symfony Patterns

### Service Container Navigation

With JetBrains backend + Symfony plugin:
- Autocomplete works in `services.yml`
- Go to definition from service ID
- Find usages across YAML and PHP

Without JetBrains:
```bash
# Find service by ID
serena search_for_pattern --substring_pattern "app.service.customer" --paths_include_glob "*.yml"

# Find class behind service
serena find_symbol --name_path_pattern CustomerService
```

### Controllers

```bash
# Find controller
serena find_symbol --name_path_pattern CustomerController --depth 1

# Find route usages
serena search_for_pattern --substring_pattern "customer_view" --paths_include_glob "*.yml"
```

### Doctrine Entities

```bash
# Find entity with methods
serena find_symbol --name_path_pattern Customer --depth 1 --include_body true

# Find repository
serena find_symbol --name_path_pattern CustomerRepository

# Find entity usages
serena find_referencing_symbols --name_path Customer --relative_path src/Entity/Customer.php
```

### Event Subscribers

```bash
# Find all subscribers
serena find_symbol --name_path_pattern Subscriber --include_kinds "[5]" --substring_matching true

# Find specific event
serena search_for_pattern --substring_pattern "kernel.request"
```

### Twig Templates

Serena doesn't analyze Twig. Use grep:

```bash
grep -r "customer.name" templates/
grep -r "{% block" templates/
```

## Vendor Navigation (Oro Packages)

Critical for Oro development - most code lives in `vendor/oro/*`.

### JetBrains Backend (Recommended)

Full indexing, fast queries:
```bash
serena find_symbol --name_path_pattern ShoppingList
serena find_symbol --name_path_pattern "Oro\\Bundle\\ShoppingListBundle" --substring_matching true
```

### LSP Backend (Fallback)

Enable vendor indexing (slower):
```yaml
# .serena/project.yml
ls_specific_settings:
  php:
    ignore_vendor: false
```

Expect 2-3 minute initial index, 15s+ per query.

## Common Oro Search Patterns

| Looking For | Command |
|-------------|---------|
| Bundle manager | `find_symbol --name_path_pattern "Manager" --relative_path vendor/oro/` |
| Event listener | `find_symbol --name_path_pattern "Listener" --include_kinds "[5]"` |
| Workflow | `search_for_pattern --substring_pattern "workflows:" --paths_include_glob "*.yml"` |
| API endpoint | `search_for_pattern --substring_pattern "@Route" --relative_path vendor/oro/` |
| Migration | `find_symbol --name_path_pattern "Migration" --substring_matching true` |
| Form type | `find_symbol --name_path_pattern "FormType" --substring_matching true` |

## Oro 6.1 Breaking Changes

Be aware when searching:

1. **Extended entity fields** → `serialized_data` JSON (not real columns)
2. **Enum service** → `oro_entity_extend.enum_options_provider`
3. **Entity aliases** → Use FQCN (`Product::class` not `OroProductBundle:Product`)
4. **Datagrid filters** → `type: enum` with `enum_code`

## Integration with Oro PhpStorm Plugin

When using JetBrains backend with Oro plugin:

- Extended entity methods autocomplete
- YAML config validation
- ACL annotations understood
- Datagrid columns autocomplete

The Serena JetBrains Plugin leverages all of this through PhpStorm's code analysis.

## Workflow: Finding Where Something is Defined

```bash
# 1. Find the class
serena find_symbol --name_path_pattern CustomerManager --include_body true

# 2. If not found in src/, search vendor
serena find_symbol --name_path_pattern CustomerManager  # (JetBrains backend)

# 3. Find who uses it
serena find_referencing_symbols --name_path CustomerManager --relative_path [path from step 1/2]

# 4. Find service definition
serena search_for_pattern --substring_pattern "CustomerManager" --paths_include_glob "*.yml"
```
