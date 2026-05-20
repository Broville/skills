# Tutorial Notebook Patterns

## Structure

A tutorial notebook should be self-contained and walk a learner through a topic step by step.

### Cell 1: Title and Learning Objectives (Markdown)

```markdown
# Tutorial: <Title>

**Learning Objectives**:
1. <Objective 1>
2. <Objective 2>
3. <Objective 3>

**Prerequisites**: <What the learner should already know>

**Estimated Time**: <X minutes>
```

### Cell 2: Setup (Code)

```python
# Install required packages (commented out for learners)
# !pip install package1 package2

import pandas as pd
import numpy as np
# ... other imports with brief comments
```

### Cell 3+: Step-by-Step Instruction

Each section follows this pattern:

```markdown
## Step N: <Section Title>

<Explanation of what we're doing and why>

<Code cell with example>

<Expected output shown as a comment>
```

### Mid-Point: Quick Check (Markdown)

```markdown
### Quick Check

Before moving on, verify:
- <Check 1>
- <Check 2>
```

### Final Sections

```markdown
## Exercises

1. <Exercise 1>
2. <Exercise 2>

## Summary

<What was learned, key takeaways>

## Next Steps

<Links to further resources or related tutorials>
```

## Heuristics

- Start from zero assumed knowledge
- Each step should be runnable independently (idempotent where possible)
- Show expected outputs as comments so learners can compare
- Keep code cells short — one concept per cell
- Use clear, descriptive variable names
- Include visualizations when they aid understanding
- Test the notebook top-to-bottom before sharing