# Symbol Kinds Reference

LSP Symbol Kinds used by Serena/Intelephense.

## Symbol Path Convention

When using `--name_path` with `find_referencing_symbols` or edit commands:

| Type | Format | Example |
|------|--------|---------|
| Class | `ClassName` | `Customer` |
| Method | `Class/method` | `Customer/getName` |
| Constructor | `Class/__construct` | `Customer/__construct` |
| Property | `Class/$property` | `Customer/$name` |
| Nested | `Outer/Inner/method` | `OrderService/Handler/process` |

## Common Kinds

| Kind | Name | Description | Example |
|------|------|-------------|---------|
| 1 | File | Source file | `Customer.php` |
| 2 | Module | Module/Package | - |
| 3 | Namespace | PHP Namespace | `Meyer\Bundle\ImportBundle` |
| 4 | Package | Package | - |
| 5 | Class | PHP Class | `Customer`, `OrderService` |
| 6 | Method | Class method | `getName`, `__construct` |
| 7 | Property | Class property | `$name`, `$id` |
| 8 | Field | Field | - |
| 9 | Constructor | Constructor | `__construct` |
| 10 | Enum | Enumeration | `OrderStatus` |
| 11 | Interface | PHP Interface | `CustomerInterface` |
| 12 | Function | Standalone function | `helper_function` |
| 13 | Variable | Variable | `$customer` |
| 14 | Constant | Constant | `MAX_ITEMS` |
| 15 | String | String literal | - |
| 16 | Number | Number literal | - |
| 17 | Boolean | Boolean | - |
| 18 | Array | Array | - |

## Filtering by Kind

Use `--include_kinds` or `--exclude_kinds` with JSON arrays:

```bash
# Find only classes (kind 5)
serena find_symbol --name_path_pattern Customer --include_kinds "[5]"

# Find only methods (kind 6)
serena find_symbol --name_path_pattern get --include_kinds "[6]"

# Find only interfaces (kind 11)
serena find_symbol --name_path_pattern Interface --include_kinds "[11]"

# Find classes and interfaces
serena find_symbol --name_path_pattern Service --include_kinds "[5, 11]"

# Exclude methods (find everything except methods)
serena find_symbol --name_path_pattern Customer --exclude_kinds "[6]"
```

## Kind Filter Quick Reference

| To Find | Kind Number | Flag |
|---------|-------------|------|
| Classes | 5 | `--include_kinds "[5]"` |
| Methods | 6 | `--include_kinds "[6]"` |
| Properties | 7 | `--include_kinds "[7]"` |
| Interfaces | 11 | `--include_kinds "[11]"` |
| Functions | 12 | `--include_kinds "[12]"` |
| Namespaces | 3 | `--include_kinds "[3]"` |

## PHP-Specific Notes

- **Traits**: Kind 5 (Class)
- **Abstract classes**: Kind 5 (Class)
- **Static methods**: Kind 6 (Method)
- **Magic methods**: Kind 6 (Method) - `__construct`, `__toString`, etc.

## Common Patterns

```bash
# Find all classes containing "Service"
serena find_symbol --name_path_pattern Service --include_kinds "[5]"

# Find all methods starting with "get"
serena find_symbol --name_path_pattern get --include_kinds "[6]" --substring_matching true

# Find all interfaces
serena find_symbol --name_path_pattern Interface --include_kinds "[11]" --substring_matching true

# Get class with its methods (depth 1)
serena find_symbol --name_path_pattern CustomerService --depth 1
```
