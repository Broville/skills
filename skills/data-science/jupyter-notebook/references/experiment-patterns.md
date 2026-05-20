# Experiment Notebook Patterns

## Structure

A well-structured experiment notebook follows this pattern:

### Cell 1: Title and Hypothesis (Markdown)

```markdown
# Experiment: <Title>

**Hypothesis**: <Clear, testable statement>

**Success Criteria**: <How we measure whether the hypothesis holds>

**Date**: YYYY-MM-DD
```

### Cell 2: Setup and Imports (Code)

```python
import json
import pandas as pd
import numpy as np
# ... other imports

# Configuration
DATA_DIR = "../data/"
RESULTS_DIR = "../results/"
RANDOM_SEED = 42
```

### Cell 3: Data Loading (Code)

```python
# Load data with clear source documentation
# df = pd.read_csv(...)
# Document: shape, columns, any filtering applied
```

### Cell 4+: Exploration and Experimentation

Each code cell should do ONE thing:
- One transformation
- One visualization
- One metric computation

Markdown cells before each code cell explain:
- What we're doing
- Why we're doing it
- What we expect to see

### Final Cells: Results and Conclusions (Markdown)

```markdown
## Results

<Summary of key findings>

## Conclusion

<Was the hypothesis supported? What are the implications?>

## Next Steps

<What to try next based on these results>
```

## Heuristics

- Keep cells small and focused
- Clear all outputs before committing (for clean diffs)
- Use descriptive variable names, not `x`, `y`, `z`
- Print shapes and types after major transformations
- Use `df.head()`, `df.describe()`, `df.info()` for exploration, not full DataFrames
- Set random seeds for reproducibility
- Document data sources and versions