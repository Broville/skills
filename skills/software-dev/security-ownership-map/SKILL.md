---
name: security-ownership-map
description: Analyze git history to build a people-to-files ownership graph, compute bus factor for security-sensitive code, and export CSV/JSON for visualization and risk analysis.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to analyze code ownership or who owns what code
  - User asks to find the bus factor for a repository or code area
  - User asks about orphaned security code or ownership hotspots
  - User wants a security-oriented ownership analysis grounded in git history
  - User mentions CODEOWNERS drift or hidden code owners
inputs:
  - name: repo_path
    description: Absolute path to the git repository to analyze
    required: true
  - name: since
    description: Start date for git history analysis (e.g., "12 months ago", "2024-01-01")
    required: false
  - name: until
    description: End date for git history analysis
    required: false
  - name: sensitive_config
    description: Path to a CSV file defining sensitive file patterns (auth, crypto, secrets)
    required: false
outputs:
  - name: output_dir
    description: Directory containing people.csv, files.csv, edges.csv, summary.json, and optional graph files
metadata:
  hermes:
    tags:
      - security
      - git
      - ownership
      - bus-factor
      - code-analysis
    related_skills:
      - security-threat-model
      - security-best-practices
---

# Security Ownership Map

## Description

Build a bipartite graph of people and files from git history, then compute ownership risk metrics including bus factor and sensitive-code ownership concentration. The analysis identifies orphaned security code, hidden owners, and areas of single-point-of-failure risk. Results are exported as CSV and JSON for graph databases (Neo4j) and visualization tools (Gephi).

## Prerequisites

- Python 3.8+
- `networkx` package for community detection and graph operations
- Git repository with commit history to analyze

Install the Python dependency:

```bash
pip install networkx
```

## Steps

### 1. Verify prerequisites

```bash
python3 --version
# Expected: Python 3.8 or later

pip show networkx 2>/dev/null || pip install networkx
# Expected: networkx version displayed or installed
```

### 2. Scope the analysis

Determine the repository path and time window. Use `--since` to limit analysis to recent history for large repositories:

```bash
git -C /path/to/repo log --oneline --since="12 months ago" | wc -l
# Expected: reasonable commit count (thousands, not millions)
```

If the commit count is extremely large (>100k), narrow the time window with `--since`.

### 3. Run the ownership map analysis

Execute the main analysis script from the skill directory:

```bash
python3 scripts/run_ownership_map.py \
  --repo /path/to/repo \
  --out ownership-map-out \
  --since "12 months ago"
```

Additional options:
- `--emit-commits` — include per-commit details in `commits.jsonl`
- `--identity committer` — attribute to committer instead of author
- `--include-merges` — include merge commits (excluded by default)
- `--no-communities` — skip community detection
- `--graphml` — export GraphML for Neo4j/Gephi import

For custom sensitive file patterns, create a sensitivity CSV:

```
# pattern,tag,weight
**/auth/**,auth,1.0
**/crypto/**,crypto,1.0
**/*.pem,secrets,1.0
```

Then pass it with `--sensitive-config path/to/sensitive.csv`.

### 4. Query the results

Use the query script for bounded JSON slices without loading the full graph:

```bash
# Overview of orphaned sensitive code
python3 scripts/query_ownership.py --data-dir ownership-map-out summary --section orphaned_sensitive_code

# Hidden owners for sensitive tags
python3 scripts/query_ownership.py --data-dir ownership-map-out summary --section hidden_owners

# Auth files with bus factor <= 1
python3 scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 1

# Crypto files with bus factor <= 1
python3 scripts/query_ownership.py --data-dir ownership-map-out files --tag crypto --bus-factor-max 1

# Top contributors to sensitive code
python3 scripts/query_ownership.py --data-dir ownership-map-out people --sort sensitive_touches --limit 10

# Co-change neighbors for a specific file
python3 scripts/query_ownership.py --data-dir ownership-map-out cochange --file path/to/file --min-jaccard 0.05 --limit 20
```

### 5. Export for visualization

For Neo4j import, follow `references/neo4j-import.md` to load the CSVs with proper constraints and indexing.

For Gephi or other graph tools, use the GraphML export:

```bash
python3 scripts/run_ownership_map.py \
  --repo /path/to/repo \
  --out ownership-map-out \
  --since "12 months ago" \
  --graphml
```

The output directory contains:
- `people.csv` — people nodes with commit counts and timezone info
- `files.csv` — file nodes with bus factor and sensitivity tags
- `edges.csv` — person-to-file ownership edges
- `cochange_edges.csv` — file-to-file co-change edges with Jaccard weight
- `summary.json` — security ownership findings (orphaned code, hidden owners, hotspots)
- `communities.json` — community detection results with maintainers per cluster
- `cochange.graph.json` — NetworkX node-link JSON with community annotations
- Optional: `ownership.graphml` / `cochange.graphml` for external graph tools

## Pitfalls

- **Large repositories are slow**: Repositories with >50k commits in the time window can take minutes to analyze. Use `--since` to narrow the window. Use `--no-cochange` to skip the co-change graph if you only need ownership metrics.
- **Bot commits inflate ownership**: Dependabot, Renovate, and other bots create many commits. The script excludes common bots by default. Override with `--no-default-author-excludes` or add custom patterns with `--author-exclude-regex`.
- **Co-change noise from "glue" files**: Lockfiles, CI configs, and `.github/` files create false co-change clusters. The script excludes these by default. Override with `--no-default-cochange-excludes`.
- **Bus factor of 1 does not always mean risk**: A file with bus factor 1 but frequent, routine changes (e.g., changelog) is lower risk than a file with bus factor 1 in a critical auth module. Always cross-reference bus factor with sensitivity tags.

## Verification

1. **Output directory exists and is non-empty**:
   ```bash
   test -d ownership-map-out && ls ownership-map-out/*.csv ownership-map-out/summary.json || echo "Missing output files"
   ```

2. **Summary JSON contains expected sections**:
   ```bash
   python3 -c "import json; d=json.load(open('ownership-map-out/summary.json')); print(list(d.keys()))"
   # Expected: ['orphaned_sensitive_code', 'hidden_owners', 'bus_factor_hotspots']
   ```

3. **People and files are linked**: Verify that `edges.csv` references person IDs from `people.csv` and file paths from `files.csv`:
   ```bash
   head -5 ownership-map-out/people.csv ownership-map-out/files.csv ownership-map-out/edges.csv
   ```

## Cross-References

- **security-threat-model** (`software-dev/security-threat-model`) — Use ownership data to inform trust boundary and asset analysis
- **security-best-practices** (`software-dev/security-best-practices`) — Apply security best practices to files flagged by ownership analysis
- **neo4j-import** guide in `references/neo4j-import.md` for loading results into a graph database