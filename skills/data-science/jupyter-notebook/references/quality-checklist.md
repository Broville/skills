# Quality Checklist for Jupyter Notebooks

Use this checklist before finalizing any notebook.

## Structure

- [ ] Title cell is present and descriptive
- [ ] Every code cell has a preceding markdown cell explaining its purpose
- [ ] No empty or dead cells
- [ ] Imports are in the first code cell(s)
- [ ] Kernel spec is set (Python 3)

## Content

- [ ] Each cell does one thing
- [ ] Variable names are descriptive (not `x`, `y`, `z`)
- [ ] Outputs are cleared for version control
- [ ] Expected outputs are noted (as comments or markdown)
- [ ] Data sources are documented

## Reproducibility

- [ ] Random seeds are set where applicable
- [ ] Package versions are documented or pinned
- [ ] Data paths are configurable (not hardcoded absolute paths)
- [ ] Notebook runs top-to-bottom without errors

## For Experiments

- [ ] Hypothesis is clearly stated
- [ ] Success criteria are defined
- [ ] Results and conclusions are present

## For Tutorials

- [ ] Learning objectives are listed
- [ ] Prerequisites are documented
- [ ] Expected outputs are shown for each step
- [ ] Exercises or checks are included