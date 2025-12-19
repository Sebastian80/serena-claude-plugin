# Symbol Editing Patterns

When to use Serena's symbol-based editing vs. standard Edit tool.

## Decision Matrix

| Scenario | Serena | Standard Edit |
|----------|--------|---------------|
| Replace entire method body | `replace_symbol_body` | - |
| Add new method to class | `insert_after_symbol` | - |
| Add import statement | `insert_before_symbol` | - |
| Rename method/class | `rename_symbol` | - |
| Change few lines in method | - | Edit tool |
| Fix typo in string | - | Edit tool |
| Modify config files | - | Edit tool |
| Non-PHP files | - | Edit tool |

## Symbol Editing Operations

### replace_symbol_body

Replaces the entire body of a symbol (method, function, class).

```bash
serena replace_symbol_body \
  --name_path "Customer/calculateTotal" \
  --relative_path src/Entity/Customer.php \
  --body "public function calculateTotal(): int
{
    \$total = 0;
    foreach (\$this->items as \$item) {
        \$total += \$item->getPrice();
    }
    return \$total;
}"
```

**Best for**: Rewriting methods, updating function logic.

### insert_after_symbol

Inserts code after a symbol. Useful for adding methods.

```bash
serena insert_after_symbol \
  --name_path "Customer/getName" \
  --relative_path src/Entity/Customer.php \
  --body "
    public function getFullName(): string
    {
        return \$this->firstName . ' ' . \$this->lastName;
    }"
```

**Best for**: Adding new methods, appending to class.

### insert_before_symbol

Inserts code before a symbol. Useful for imports.

```bash
serena insert_before_symbol \
  --name_path "Customer" \
  --relative_path src/Entity/Customer.php \
  --body "use App\\Service\\Calculator;"
```

**Best for**: Adding imports, docblocks, annotations.

### rename_symbol

Renames a symbol and updates all references.

```bash
serena rename_symbol \
  --name_path "Customer/getName" \
  --relative_path src/Entity/Customer.php \
  --new_name "getCustomerName"
```

**Best for**: Refactoring, renaming methods/classes.

## When NOT to Use Symbol Editing

1. **Small changes within a method**: Use standard Edit
2. **Non-code files**: JSON, YAML, MD - use standard Edit
3. **Config files**: Use standard Edit
4. **When you need line-level precision**: Use standard Edit

## Workflow: Adding a New Feature

```bash
# 1. Find where to add
serena get_symbols_overview --relative_path src/Entity/Customer.php

# 2. Check existing code
serena find_symbol --name_path_pattern "Customer/getName" --include_body true

# 3. Insert new code
serena insert_after_symbol \
  --name_path "Customer/getName" \
  --relative_path src/Entity/Customer.php \
  --body "public function newMethod() {}"

# 4. Add imports if needed
serena insert_before_symbol \
  --name_path "Customer" \
  --relative_path src/Entity/Customer.php \
  --body "use App\\Service\\NewService;"

# 5. Check references if needed
serena find_referencing_symbols \
  --name_path "Customer/getName" \
  --relative_path src/Entity/Customer.php
```

## Error Handling

Symbol operations fail if:
- Symbol not found (check name_path spelling)
- File not in project (check relative_path)
- Syntax error in body (validate PHP syntax)

Always verify symbol exists before editing:

```bash
# Check symbol exists first
serena find_symbol --name_path_pattern "Customer/getName" --relative_path src/Entity/Customer.php

# Then edit if found
serena replace_symbol_body \
  --name_path "Customer/getName" \
  --relative_path src/Entity/Customer.php \
  --body "public function getName(): string { return \$this->name; }"
```
