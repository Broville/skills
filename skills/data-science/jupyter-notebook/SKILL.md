---
name: jupyter-notebook
description: Create, scaffold, and edit Jupyter notebooks (.ipynb) for experiments, explorations, or tutorials using standardized templates and structure patterns.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to create a Jupyter notebook or .ipynb file
  - User asks to scaffold a notebook for an experiment or analysis
  - User asks to set up a tutorial or teaching notebook
  - User asks to convert scripts or notes into a structured notebook
  - User mentions Jupyter, ipynb, or notebook in the context of creating one
inputs:
  - name: title
    description: Notebook title (used in the first markdown cell)
    required: true
  - name: kind
    description: "Notebook type: experiment or tutorial"
    required: true
  - name: out_path
    description: Output file path for the .ipynb file
    required: true
outputs:
  - name: notebook
    description: A structured .ipynb file following the appropriate template
metadata:
  hermes:
    tags:
      - jupyter
      - notebook
      - data-science
      - experimentation
      - tutorial
    related_skills:
      - cli-creator
---

# Jupyter Notebook

## Description

Create clean, reproducible Jupyter notebooks for two primary modes:

- **Experiments** — exploratory analysis, hypothesis testing, and iterative data work
- **Tutorials** — instructional, step-by-step walkthroughs for a specific audience

Use the bundled templates and the helper script for consistent structure and fewer JSON mistakes in the `.ipynb` format.

## Prerequisites

- Python 3.8+
- (Optional) JupyterLab and ipykernel for running notebooks:

```bash
pip install jupyterlab ipykernel
```

Or with conda:

```bash
conda install jupyterlab ipykernel
```

The scaffold helper script uses only the Python standard library and requires no extra dependencies.

## Steps

### 1. Choose the notebook kind

Identify whether the request is:

- **Experiment** — exploratory, analytical, hypothesis-driven, or iterative
- **Tutorial** — instructional, step-by-step, or audience-specific

If editing an existing notebook, treat it as a refactor: preserve intent and improve structure.

### 2. Scaffold from the template

Use the helper script to generate a properly structured notebook from the template:

```bash
python3 scripts/new_notebook.py \
  --kind experiment \
  --title "Compare prompt variants" \
  --out output/experiment-compare-prompt-variants.ipynb
```

For tutorials:

```bash
python3 scripts/new_notebook.py \
  --kind tutorial \
  --title "Intro to embeddings" \
  --out output/tutorial-intro-to-embeddings.ipynb
```

The script loads the appropriate template from `templates/`, updates the title cell, and writes a valid `.ipynb` file.

### 3. Fill the notebook with content

Add content following the appropriate pattern:

- **Experiment pattern** (see `references/experiment-patterns.md`):
  1. Title and hypothesis
  2. Setup and imports
  3. Data loading
  4. Exploration
  5. Experiment iterations
  6. Results and conclusions

- **Tutorial pattern** (see `references/tutorial-patterns.md`):
  1. Title and learning objectives
  2. Prerequisites
  3. Step-by-step instructions with expected outputs
  4. Exercises or challenges
  5. Summary and next steps

Keep each code cell focused on one step. Add short markdown cells explaining purpose and expected results. Avoid large, noisy outputs when a short summary works.

### 4. Edit existing notebooks safely

When modifying an existing notebook:
- Preserve the cell structure; avoid reordering unless it improves readability
- Prefer targeted edits over full rewrites
- If editing raw JSON, review `references/notebook-structure.md` for the `.ipynb` format
- Keep the top-to-bottom narrative flow intact

### 5. Validate the result

Run the notebook top-to-bottom when the environment allows:

```bash
jupyter nbconvert --to script --stdout output/my-notebook.ipynb > /tmp/test_script.py
python3 /tmp/test_script.py
# Expected: script runs without errors
```

If execution is not possible, state explicitly and describe how to validate locally.

Use the final pass checklist in `references/quality-checklist.md`:
- [ ] Title cell is present and descriptive
- [ ] Every code cell has a preceding markdown cell explaining its purpose
- [ ] No empty or dead cells
- [ ] Imports are in the first code cell
- [ ] Outputs are cleared (for version control)
- [ ] Kernel spec is set (Python 3)

### 6. Save to the output directory

Write final artifacts with stable, descriptive filenames:

```
output/                          ← final notebooks go here
  experiment-ablation-temperature.ipynb
  tutorial-intro-to-embeddings.ipynb
```

Use `tmp/jupyter-notebook/` for intermediate files during work, and delete them when done.

## Template Reference

Templates live in `templates/`:
- `templates/experiment-template.ipynb` — Structured experiment notebook
- `templates/tutorial-template.ipynb` — Structured tutorial notebook

The helper script at `scripts/new_notebook.py` loads a template, updates the title cell, and writes the result. It uses only the Python standard library and requires no external dependencies.

## Reference Documents

- `references/experiment-patterns.md` — Experiment structure and heuristics
- `references/tutorial-patterns.md` — Tutorial structure and teaching flow
- `references/notebook-structure.md` — Notebook JSON shape and safe editing rules
- `references/quality-checklist.md` — Final validation checklist

## Pitfalls

- **Hand-editing notebook JSON**: Jupyter notebooks are JSON files with specific structure requirements. If you must edit raw JSON, validate with `python3 -m json.tool notebook.ipynb > /dev/null` before and after changes. Prefer using the helper script to avoid structural errors.
- **Missing kernel specification**: Notebooks without a `kernelspec` in metadata may fail to open in JupyterLab. Always include `kernelspec` with `language: python` and `display_name: Python 3`. The templates handle this automatically.
- **Stale outputs in version control**: Clear all cell outputs before committing notebooks to git. Stale outputs create noisy diffs. Use `jupyter nbconvert --clear-output --inplace notebook.ipynb` or clear outputs in the Jupyter UI.
- **Large outputs bloating the file**: Avoid printing large DataFrames or raw JSON in cells. Use `.head()`, summaries, or `repr()` instead. Large outputs make notebooks slow to open and hard to diff.

## Verification

1. **Notebook file is valid JSON**:
   ```bash
   python3 -m json.tool output/my-notebook.ipynb > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
   ```

2. **Kernel spec is present**:
   ```bash
   python3 -c "import json; nb=json.load(open('output/my-notebook.ipynb')); print(nb['metadata']['kernelspec']['display_name'])"
   # Expected: "Python 3"
   ```

3. **Title cell exists**:
   ```bash
   python3 -c "import json; nb=json.load(open('output/my-notebook.ipynb')); cells=[c for c in nb['cells'] if c['cell_type']=='markdown']; print('OK' if cells else 'No markdown cells')"
   # Expected: "OK"
   ```

4. **Notebook executes without errors** (if environment available):
   ```bash
   jupyter nbconvert --execute --to notebook --inplace output/my-notebook.ipynb
   # Expected: exit code 0, no execution errors
   ```

## Cross-References

- **cli-creator** (`software-dev/cli-creator`) — For building CLIs that wrap notebook-powered analysis