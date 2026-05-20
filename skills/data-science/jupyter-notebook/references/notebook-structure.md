# Notebook Structure Reference

## .ipynb JSON Format

A Jupyter notebook (`.ipynb`) is a JSON file with this top-level structure:

```json
{
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.12.0"
    }
  },
  "cells": [...]
}
```

## Cell Types

### Markdown Cell

```json
{
  "cell_type": "markdown",
  "id": "unique-id",
  "metadata": {},
  "source": ["# Title\n", "Description text"]
}
```

### Code Cell

```json
{
  "cell_type": "code",
  "id": "unique-id",
  "metadata": {},
  "source": ["import pandas as pd\n", "df = pd.read_csv('data.csv')"],
  "execution_count": null,
  "outputs": []
}
```

## Safe Editing Rules

1. **Always validate JSON after editing**: `python3 -m json.tool notebook.ipynb > /dev/null`
2. **Preserve cell IDs**: Each cell needs a unique `id` field. When adding cells, generate new IDs.
3. **Clear outputs before committing**: Set `execution_count` to `null` and `outputs` to `[]` for version control.
4. **Keep kernelspec intact**: Never remove the `kernelspec` from metadata.
5. **Source is an array of strings**: Each element represents a line. Lines ending with `\n` include the newline.
6. **Don't mix cell types**: A markdown cell must have `cell_type: "markdown"`, not `"code"`.

## Generating Valid IDs

Use UUIDs or short random strings:

```python
import uuid
cell_id = uuid.uuid4().hex[:8]  # e.g., "a3f7b2c1"
```