---
name: sast-scan
description: Run Static Application Security Testing on source code to detect injection, deserialization, and other code-level flaws.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks to scan source code for security vulnerabilities
  - User mentions SAST, static analysis, Semgrep, Bandit, or CodeQL
  - CI pipeline needs a static security scan step
  - User wants to find injection flaws, XSS patterns, or insecure deserialization
inputs:
  - name: language
    description: "Force a language (python, javascript, typescript, go, java); auto-detected if omitted"
    required: false
  - name: scan_path
    description: "Path to scan (file or directory)"
    required: true
  - name: ruleset
    description: "Semgrep ruleset (p/security-audit, p/owasp-top-ten) or Bandit/CodeQL config"
    required: false
  - name: severity_threshold
    description: "Minimum severity to report (critical, high, medium, low)"
    required: false
  - name: output_format
    description: "Report format (sarif, json, markdown)"
    required: false
outputs:
  - name: scan_results
    description: SARIF/JSON/Markdown report of static findings
  - name: report_file
    description: Path to the written report
metadata:
  hermes:
    tags: [security, sast, static-analysis, semgrep, bandit, codeql, devops]
    related_skills:
      - dast-scan
      - sca-scan
      - secret-scan
      - iac-security-scan
      - vulnerability-triage
      - ci-security-pipeline
      - security-best-practices
---

# sast-scan

## Description

Run Static Application Security Testing (SAST) on source code to detect code-level vulnerabilities such as injection flaws, cross-site scripting, insecure deserialization, and unsafe cryptographic patterns. The skill normalizes output to SARIF 2.1.0 and emits a Markdown report with per-language summaries.

## Prerequisites

- Source code at `scan_path`.
- One of the supported scanners installed: `bandit` (Python), `semgrep` (JS/TS/Go/multi), `gosec` (Go), or CodeQL (if supported).
- For multi-language repos, `semgrep` is preferred to keep SARIF output uniform.

## Steps

1. Detect language(s) from file extensions and shebangs in `scan_path`.
2. Select the scanner by language:
   - Python → `bandit -r <scan_path> -f sarif -o sast.sarif`
   - JavaScript / TypeScript → `semgrep --config p/javascript --config p/typescript --sarif --output sast.sarif <scan_path>`
   - Go → `gosec -fmt sarif -out sast.sarif ./...` or Semgrep Go ruleset
   - Multi-language / cross-cutting → `semgrep --config p/security-audit --sarif --output sast.sarif <scan_path>`
3. If the project mixes languages, prefer Semgrep as the single tool to keep SARIF output uniform.
4. Run with the requested `severity_threshold` if provided; default to reporting all severities.
5. Filter findings below the threshold while preserving the original count for the report summary.
6. Normalize output to the common SARIF 2.1.0 shape. Set `properties.severity` from the tool's native severity. Set `properties.cvss_v4` to `null` because SAST findings are not necessarily CVEs.
7. Emit a Markdown report with one row per finding plus a summary: counts by severity and by language.

## Pitfalls

- SAST false-positive rates are typically 30–70%. Always funnel results through `vulnerability-triage` before acting.
- No single SAST tool covers every language. Multi-language repos may require multi-tool runs.
- Some tools (e.g., CodeQL) require a buildable codebase. Do not silently fail on unbuildable code; note it in the report.
- Long scan times cause developers to bypass the step. Scope to changed files in PR mode; run a full scan only in scheduled jobs.
- Language auto-detection can miscategorize templated or generated files. Allow `language` override for explicit control.

## Verification

1. SARIF output is valid JSON:
   ```bash
   python -c "import json; json.load(open('sast.sarif')); print('SARIF ok')"
   ```
2. On a clean target, the scan exits 0 and reports zero findings.
3. Severity counts in the Markdown summary sum to the total finding count in SARIF.
4. A multi-language scan seeded with known-bad snippets produces findings from each detected language.

## Cross-References

- Works with `dast-scan` to cover both code-level and runtime vulnerabilities.
- Pairs with `vulnerability-triage` to manage false positives.
- Integrated into `ci-security-pipeline` as a PR-stage scanner.
