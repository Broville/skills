---
name: secret-scan
description: Detect hardcoded secrets, API keys, tokens, and credentials in source and git history using pattern + entropy analysis.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks to scan for leaked secrets, API keys, or credentials
  - User mentions gitleaks, trufflehog, secret scanning, or credential detection
  - CI pipeline needs pre-commit or pre-push secret detection
  - User wants to audit git history for accidentally committed secrets
inputs:
  - name: scan_path
    description: Path to the repository root to scan
    required: true
  - name: scan_depth
    description: "full-history (default) or diff-only (against main)"
    required: false
  - name: custom_rules
    description: Path to a custom Gitleaks/Trufflehog rules file
    required: false
  - name: output_format
    description: "Report format (sarif, json, markdown)"
    required: false
outputs:
  - name: findings
    description: List of detected secrets with file, line, rule, and redacted sample
  - name: report_file
    description: Path to the written report
metadata:
  hermes:
    tags: [security, secrets, credentials, gitleaks, devops]
    related_skills:
      - sast-scan
      - sca-scan
      - ci-security-pipeline
      - security-best-practices
---

# secret-scan

## Description

Detect hardcoded secrets, API keys, tokens, and credentials in source code and git history. Findings are triaged into true positives, false positives, and test fixtures; every true positive receives a rotation recommendation. The skill can also emit a `.pre-commit-config.yaml` snippet to block future commits.

## Prerequisites

- `gitleaks` installed (preferred). `trufflehog` acceptable as a secondary verifier.
- The target path is a git repository or directory.
- For pre-commit hook generation, `pre-commit` is available in the environment.

## Steps

1. Choose the primary tool: **Gitleaks**. Use Trufflehog as a secondary verifier for high-confidence findings if needed.
2. Run a baseline scan against the working tree:
   ```bash
   gitleaks detect --source <scan_path> --report-format sarif --report-path secrets.sarif --no-git
   ```
3. If `scan_depth=full-history`, also scan full git history:
   ```bash
   gitleaks detect --source <scan_path> --report-format sarif --report-path secrets-history.sarif
   ```
4. If `custom_rules` is provided, pass it to the tool:
   ```bash
   gitleaks detect --source <scan_path> --config <custom_rules> --report-format sarif --report-path secrets.sarif
   ```
5. Triage findings: categorize each as **true positive / false positive / test fixture**. Document false positives in `.gitleaksignore` or with a `gitleaks:allow` directive and a reason.
6. For every true positive, emit a "rotate now" recommendation block with secret type, file/commit, and rotation steps.
7. If a pre-commit hook is requested, write `.pre-commit-config.yaml` with the `gitleaks` hook pinned to a specific version.
8. Normalize findings to SARIF 2.1.0 if the tool-native output is JSON, preserving `ruleId`, file, line, and a redacted sample in `properties`.

## Pitfalls

- Test fixtures and documentation contain fake keys that look real. Always review before raising an alert.
- Secrets that have been rebased away are still recoverable from reflog. For thorough audits, use `git log --all --full-history -- <path>`.
- A finding means "rotate immediately" regardless of current repository visibility; exposure window matters, not current reachability.
- Entropy-based detection has a high false-positive rate. Prefer pattern-based rules; use entropy only as a tiebreaker.
- Never commit a plain-text secret while fixing a finding. Rotate via your vault or secret manager, not via `.env` files.

## Verification

1. The SARIF report loads and contains `runs[0].results[]`:
   ```bash
   python -c "import json; d=json.load(open('secrets.sarif')); print(len(d['runs'][0]['results']))"
   ```
2. Every true-positive finding lists a rotation recommendation; no finding is left without remediation text.
3. On a clean repository, `gitleaks detect` exits 0 and reports zero findings.
4. The generated pre-commit hook installs and runs:
   ```bash
   pre-commit run gitleaks --all-files
   ```
   exits 0 on a clean repo and non-zero on a synthetic `.env` containing a fake AWS key like `AKIA...`.

## Cross-References

- Used by `ci-security-pipeline` as the pre-commit and PR-stage scanner.
- Complements `sast-scan` and `sca-scan` in a layered security pipeline.
