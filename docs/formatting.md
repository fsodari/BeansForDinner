### Formatting Guidelines

- If a name is not specified, the filename will be used.

- If a top-level 'variants' field is supplied, then the recipe will be considered a 'Collection'. If a top-level 'ingredients' field is supplied, then the recipe will be considered a 'Composite'. If neither is supplied, the recipe will be considered an 'Atomic'. A recipe should not include both fields.

- If a 'source' field is used, that source file will be loaded as the default config, then any extra fields are applied as overrides.
