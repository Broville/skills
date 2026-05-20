#!/usr/bin/env python3
"""Generate a Jupyter notebook from a template.

Usage:
    python3 scripts/new_notebook.py --kind experiment --title "My Title" --out output/my-notebook.ipynb
    python3 scripts/new_notebook.py --kind tutorial --title "My Tutorial" --out output/my-tutorial.ipynb
"""

import argparse
import json
import os
import uuid

def make_cell(cell_type, source_lines):
    """Create a notebook cell."""
    cell = {
        "cell_type": cell_type,
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": source_lines,
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

def make_notebook(kind, title):
    """Create a notebook from kind and title."""
    cells = []
    
    if kind == "experiment":
        cells.append(make_cell("markdown", [
            f"# Experiment: {title}\n",
            "\n",
            "**Hypothesis**: <clear, testable statement>\n",
            "\n",
            "**Success Criteria**: <how we measure success>\n",
            "\n",
            f"**Date**: <YYYY-MM-DD>\n",
        ]))
        cells.append(make_cell("code", [
            "import json\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "\n",
            "# Configuration\n",
            "DATA_DIR = '../data/'\n",
            "RESULTS_DIR = '../results/'\n",
            "RANDOM_SEED = 42\n",
        ]))
        cells.append(make_cell("markdown", [
            "## Data Loading\n",
        ]))
        cells.append(make_cell("code", [
            "# Load data here\n",
            "# df = pd.read_csv(DATA_DIR + 'data.csv')\n",
            "# df.shape\n",
        ]))
        cells.append(make_cell("markdown", [
            "## Exploration\n",
        ]))
        cells.append(make_cell("code", [
            "# Explore data here\n",
            "# df.describe()\n",
        ]))
        cells.append(make_cell("markdown", [
            "## Results\n",
        ]))
        cells.append(make_cell("code", [
            "# Compute and display results\n",
        ]))
        cells.append(make_cell("markdown", [
            "## Conclusion\n",
            "\n",
            "<Summary of findings and next steps>\n",
        ]))
    
    elif kind == "tutorial":
        cells.append(make_cell("markdown", [
            f"# Tutorial: {title}\n",
            "\n",
            "**Learning Objectives**:\n",
            "1. <Objective 1>\n",
            "2. <Objective 2>\n",
            "\n",
            "**Prerequisites**: <what the learner should know>\n",
            "\n",
            f"**Estimated Time**: <X minutes>\n",
        ]))
        cells.append(make_cell("code", [
            "# Install required packages (uncomment if needed)\n",
            "# !pip install package1 package2\n",
            "\n",
            "import pandas as pd\n",
            "import numpy as np\n",
        ]))
        cells.append(make_cell("markdown", [
            "## Step 1: <Section Title>\n",
            "\n",
            "<Explanation of what we're doing>\n",
        ]))
        cells.append(make_cell("code", [
            "# Step 1 code here\n",
        ]))
        cells.append(make_cell("markdown", [
            "## Summary\n",
            "\n",
            "<What was learned, key takeaways>\n",
            "\n",
            "## Next Steps\n",
            "\n",
            "<Links to further resources>\n",
        ]))
    
    else:
        raise ValueError(f"Unknown kind: {kind}. Use 'experiment' or 'tutorial'.")
    
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0",
            },
        },
        "cells": cells,
    }
    
    return notebook

def main():
    parser = argparse.ArgumentParser(description="Generate a Jupyter notebook from a template")
    parser.add_argument("--kind", required=True, choices=["experiment", "tutorial"],
                        help="Notebook type: experiment or tutorial")
    parser.add_argument("--title", required=True, help="Notebook title")
    parser.add_argument("--out", required=True, help="Output file path (.ipynb)")
    args = parser.parse_args()
    
    notebook = make_notebook(args.kind, args.title)
    
    # Ensure output directory exists
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    
    with open(args.out, "w") as f:
        json.dump(notebook, f, indent=2)
    
    print(f"Created {args.kind} notebook: {args.out}")

if __name__ == "__main__":
    main()