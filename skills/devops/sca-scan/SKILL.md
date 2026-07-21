---
name: sca-scan
description: Run Software Composition Analysis on project dependencies to surface CVEs, outdated packages, and optional SBOM output.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks to check dependencies for known vulnerabilities
  - User mentions SCA, dependency scanning, npm audit, pip audit, CVE, or SBOM
  - CI pipeline needs a dependency vulnerability scan stage
  - User wants to know if any third-party packages have security issues
inputs:
  - name: scan_path
    description: Path to the project root containing package manifests
    required: true
  - name: ecosystem
    description: "Force a specific ecosystem (python, node, go, java, rust); auto-detected if omitted"
    required: false
  - name: include_transitive
    description: "Include transitive dependencies in the scan (default: true)"
    required: false
  - name: severity_threshold
    description: "Minimum severity to report (critical, high, medium, low)"
    required: false
  - name: generate_sbom
    description: "Emit SBOM in CycloneDX or SPDX format (default: false)"
    required: false
  - name: output_format
    description: "Report format (sarif, json, markdown)"
    required: false
outputs:
  - name: vulnerability_report
    description: SARIF/JSON/Markdown report of dependency vulnerabilities
  - name: sbom_file
    description: "SBOM file (CycloneDX or SPDX) when generate_sbom is true"
  - name: remediation_plan
    description: Prioritized list of safe upgrades
metadata:
  hermes:
    tags: [security, sca, dependencies, cve, sbom, devops]
    related_skills:
      - sast-scan
      - dast-scan
      - secret-scan
      - iac-security-scan
      - vulnerability-triage
      - ci-security-pipeline
      - security-best-practices
---

# sca-scan

## Description

Run Software Composition Analysis (SCA) on a project to find known CVEs in dependencies, flag outdated packages, and optionally produce an SBOM. The skill normalizes output to SARIF 2.1.0 and emits a Markdown report plus a prioritized CSV remediation plan.

## Prerequisites

- Shell access to the project root.
- One of the supported scanners installed: `pip-audit`, `npm`, `govulncheck`, or `trivy`.
- For SBOM generation, `trivy` with CycloneDX/SPDX support.

## Steps

1. Detect the package ecosystem from manifests in `scan_path`:
   - `package.json` → node
   - `requirements.txt` / `pyproject.toml` → python
   - `go.mod` → go
   - `Cargo.toml` → rust
   - `pom.xml` / `build.gradle` → java
   - `Gemfile` → ruby
2. Select a scanner by ecosystem:
   - Python → `pip-audit --format=sarif --output=sca.sarif <scan_path>` (or `safety check` as fallback)
   - Node → `npm audit --json` and convert to SARIF
   - Go → `govulncheck -json ./...`
   - Multi / containers → `trivy fs --scanners vuln <scan_path>`
3. Run the scan with `--format sarif` where supported, or capture tool-native JSON for normalization.
4. Include transitive dependencies unless `include_transitive=false` is explicitly provided.
5. Optionally generate an SBOM:
   ```bash
   trivy fs --format cyclonedx --output sbom.cdx.json <scan_path>
   ```
6. Normalize findings into the common SARIF 2.1.0 shape:
   - `version`: `2.1.0`
   - `runs[0].tool.driver.name`: scanner name and version
   - `results[].ruleId`: CVE or advisory ID
   - `results[].properties`: `{cve, cvss_v4, cvss_v3, epss, severity}`
7. Produce a Markdown report with one row per CVE: package, current version, fixed version, CVSS v4.0 (or v3.1 fallback), EPSS, recommended action.
8. Emit a CSV remediation plan sorted by composite risk (severity × EPSS), descending.

## Pitfalls

- Transitive dependencies often carry the real risk. Do not set `include_transitive=false` unless the user explicitly requests it.
- NVD has a reporting lag; very recent CVEs may be absent. Always note the database timestamp in the report header.
- Some CVEs have no fixed version. Document these as `no-fix-available` rather than suppressing them.
- License compliance is adjacent but out of scope. Do not silently include license findings in the security report.
- CVSS v4.0 may be unavailable; fall back to CVSS v3.1 and record the version used per row.

## Verification

1. SARIF output is valid JSON that loads without error:
   ```bash
   python -c "import json; json.load(open('sca-report.sarif')); print('SARIF ok')"
   ```
2. Every CVE row in the Markdown report has either a `fixed_version` or an explicit `no-fix-available` marker.
3. If an SBOM was requested, `trivy sbom sbom.cdx.json` reports the same package count as the scan, or a manual package count matches within 5%.
4. Running with `severity_threshold=critical` against a clean target exits 0 and reports zero Critical findings.

## Cross-References

- Works with `vulnerability-triage` to prioritize findings.
- Consumed by `ci-security-pipeline` as a PR-stage scanner.
- Complements `security-best-practices` for secure dependency choices.
