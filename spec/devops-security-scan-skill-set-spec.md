# Blueprint: DevOps Security Scan & Risk Analysis Skill Set

**Spec ID:** spec/devops-security-scan-skill-set
**Status:** Draft for Lens review
**Author:** Cartographer (t_f9474074)
**Source research:** research/devops-security-scan-risk-analysis-research-brief.md (t_29b48c3b)
**Target category:** `devops/`
**Target implementer:** Weaver (one skill = one task per SOP §4)

---

## Overview

This spec converts the research brief into a buildable, testable architectural specification for an 8-skill set that covers automated security scanning and risk analysis in a DevOps context. Every proposed skill is scoped to be independently valuable yet composable into a unified DevSecOps pipeline. The spec defines frontmatter (triggers, inputs, outputs), operational steps with concrete commands, verification criteria, and the risk-analysis protocols (CVSS v4.0, EPSS, NIST SP 800-30, FAIR) that the risk-related skills must integrate.

All skills live under `skills/devops/` per SOP.md §"Repository Layout" and the "devops" category definition. Each skill follows the SKILL-SPEC.md required frontmatter (`name`, `description`, `version`, `author`, `license`) plus the SOP-mandated sections (`trigger`, numbered `Steps`, `Pitfalls`, `Verification`, `related_skills`).

---

## Architecture

### Components

Eight new skill directories under `skills/devops/`:

```
skills/devops/
├── sca-scan/                    # P0 — Software Composition Analysis
├── secret-scan/                 # P0 — Credential / secret detection
├── vulnerability-triage/        # P0 — CVSS + EPSS prioritization
├── ci-security-pipeline/        # P1 — Pipeline integration
├── sast-scan/                   # P1 — Static Application Security Testing
├── iac-security-scan/           # P1 — Infrastructure-as-Code scanning
├── dast-scan/                   # P2 — Dynamic Application Security Testing
└── security-risk-assessment/    # P2 — NIST SP 800-30 / FAIR business risk
```

### Data Flow

```
┌─────────────────┐
│ Source / Build  │
└────────┬────────┘
         │
         ├──► sast-scan ─────────┐
         ├──► sca-scan ──────────┤
         ├──► secret-scan ───────┼──► scan_results (SARIF/JSON/CSV)
         ├──► iac-security-scan ─┤
         └──► dast-scan ─────────┘
                                  │
                                  ▼
                       vulnerability-triage
                       (CVSS v4.0 + EPSS)
                                  │
                                  ▼
                       security-risk-assessment
                       (NIST SP 800-30 + FAIR)
                                  │
                                  ▼
                       ci-security-pipeline
                       (gate / advisory)
```

### Dependencies (external)

| Tool family        | Examples                            | Used by                              |
|--------------------|-------------------------------------|--------------------------------------|
| SAST               | Semgrep, Bandit, CodeQL             | `sast-scan`                          |
| DAST               | OWASP ZAP, Nuclei                   | `dast-scan`                          |
| SCA                | Trivy, OWASP Dependency-Check, `npm audit`, `pip-audit` | `sca-scan`               |
| Secret             | Gitleaks, Trufflehog                | `secret-scan`                        |
| IaC                | Checkov, Trivy (config), KICS       | `iac-security-scan`                  |
| CI/CD              | GitHub Actions, GitLab CI, Jenkins  | `ci-security-pipeline`               |
| Pre-commit         | `pre-commit` framework, Husky       | `ci-security-pipeline`, `secret-scan`|
| Risk APIs          | NVD CVE API, FIRST EPSS API         | `vulnerability-triage`               |
| Reporting          | SARIF (GitHub Security tab)         | `ci-security-pipeline`               |

All recommended tools are open-source-first; commercial alternatives are noted but not required.

### Tech Stack

- **Skill definitions:** YAML frontmatter + Markdown (per `SKILL-SPEC.md`).
- **Execution runtime:** Agent follows steps; tool commands are run via shell. No skill itself ships executable code beyond the `scripts/` subdirectory the skill may declare.
- **Reporting formats:** SARIF 2.1.0 (preferred for scan results), JSON, CSV, Markdown.

---

## Risk-Analysis Protocols (shared reference)

These four protocols underpin the risk-related skills. The spec embeds them so the implementer (Weaver) does not invent scoring rules.

### CVSS v4.0 (Common Vulnerability Scoring System)
- **Source:** FIRST.org — `https://www.first.org/cvss/`
- **Score range:** 0.0 – 10.0 → None / Low / Medium / High / Critical
- **Metric groups:** Base (intrinsic), Threat (exploit characteristics), Environmental (deployment context)
- **Required behavior in skills:**
  - `vulnerability-triage` MUST prefer CVSS v4.0 scores and fall back to CVSS v3.1 only when v4.0 is unavailable. Document the version used per finding.
  - Severity-to-gate mapping: Critical (≥9.0) and High (7.0–8.9) default to "block" in advisory+1 phase; Medium/Low default to "warn" until risk tolerance lowers the bar.

### EPSS (Exploit Prediction Scoring System)
- **Source:** FIRST.org — `https://www.first.org/epss/`
- **Score range:** 0.0 – 1.0 (probability of exploitation in the wild within 30 days)
- **Data source:** Real-world threat intelligence, updated daily.
- **Required behavior in skills:**
  - `vulnerability-triage` MUST look up EPSS for every CVE-bearing finding via the public EPSS API and cache results for at most 24 hours.
  - Composite prioritization rule: a finding with high CVSS but EPSS < 0.1 is auto-tagged "deprioritize" unless business context elevates it.

### NIST SP 800-30 Rev. 1 (Guide for Conducting Risk Assessments)
- **Source:** NIST — `https://csrc.nist.gov/pubs/sp/800/30/r1/upd1/final`
- **Key concepts:** Threat × Vulnerability × Likelihood × Impact → Risk Determination
- **Required behavior in skills:**
  - `security-risk-assessment` MUST produce a risk matrix (likelihood × impact) with at least 5×5 cells and an executive narrative tied to business impact.

### FAIR (Factor Analysis of Information Risk)
- **Source:** The FAIR Institute — `https://www.fairinstitute.org/`
- **Key concepts:** Loss Event Frequency × Probable Loss Magnitude → Quantified Risk
- **Required behavior in skills:**
  - `security-risk-assessment` SHOULD include an optional FAIR worksheet (annualized loss expectancy) when quantitative inputs are available. When inputs are unavailable, the skill MUST fall back to a qualitative scale that is explicitly labelled "qualitative, not quantitative."

---

## Interface Definitions

### Cross-skill input/output contract

All scan-producing skills (`sast-scan`, `dast-scan`, `sca-scan`, `secret-scan`, `iac-security-scan`) MUST emit results in SARIF 2.1.0 with this minimum structure:

```json
{
  "version": "2.1.0",
  "runs": [{
    "tool": { "driver": { "name": "<tool>", "version": "<x.y.z>" } },
    "results": [{
      "ruleId": "<rule-or-CVE-id>",
      "level": "error|warning|note",
      "message": { "text": "<human-readable>" },
      "locations": [{ "physicalLocation": { "artifactLocation": { "uri": "<file>" }, "region": { "startLine": <n> } } }],
      "properties": {
        "cve": ["CVE-..."],
        "cvss_v4": <float|null>,
        "cvss_v3": <float|null>,
        "epss": <float|null>,
        "severity": "critical|high|medium|low"
      }
    }]
  }]
}
```

`vulnerability-triage` accepts SARIF, JSON, or CSV and always re-emits a Markdown triage report plus a CSV remediation plan.

`ci-security-pipeline` consumes nothing (it generates CI configuration) and emits workflow files under `templates/<platform>/`.

### Skill naming rules

- Directory name MUST match the frontmatter `name` field exactly (kebab-case).
- `name` MUST NOT collide with an existing skill. Cross-checked list:
  - Existing devops: `cloudflare-deploy`, `deployment-procedures`, `github-actions-templates`, `pinggy-tunnel`, `watchers` — no collision.
  - Existing software-dev security: `security-best-practices`, `security-threat-model`, `security-ownership-map`, `api-security-best-practices` — no collision; the proposed skills deliberately complement (do not replace) these.

---

## Per-Skill Specifications

Each skill is spec'd below with the frontmatter, purpose, structure, operational steps, pitfalls, and verification. Tasks for Weaver (in the "Task Breakdown" section) are derived from this.

---

### Skill 1: `sca-scan` (P0)

**Directory:** `skills/devops/sca-scan/`
**Purpose:** Scan project dependencies for known CVEs, surface outdated packages, optionally generate an SBOM.

**Frontmatter (YAML):**

```yaml
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
    description: Force a specific ecosystem (python, node, go, java, rust); auto-detected if omitted
    required: false
  - name: include_transitive
    description: Include transitive dependencies in the scan (default: true)
    required: false
  - name: severity_threshold
    description: Minimum severity to report (critical, high, medium, low)
    required: false
  - name: generate_sbom
    description: Emit SBOM in CycloneDX or SPDX format (default: false)
    required: false
  - name: output_format
    description: Report format (sarif, json, markdown)
    required: false
outputs:
  - name: vulnerability_report
    description: SARIF/JSON/Markdown report of dependency vulnerabilities
  - name: sbom_file
    description: SBOM file (CycloneDX or SPDX) when generate_sbom is true
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
```

**Operational Steps:**

1. Detect package ecosystem from manifests (`package.json`, `requirements.txt` / `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`).
2. Select tool by ecosystem:
   - Python → `pip-audit` (or `safety check` as fallback)
   - Node → `npm audit --json` (built-in)
   - Go → `govulncheck ./...`
   - Multi / containers → `trivy fs --scanners vuln <scan_path>`
3. Run scan with `--format sarif` (preferred) or tool-native JSON.
4. Include transitive deps unless `include_transitive=false`.
5. Optionally generate SBOM: `trivy fs --format cyclonedx --output sbom.cdx.json <scan_path>`.
6. Normalize findings into the common SARIF shape defined in this spec's "Interface Definitions" section.
7. Produce a Markdown report (one row per CVE) with: package, current version, fixed version, CVSS v4.0 (or v3.1 fallback), EPSS, recommended action.
8. Emit a remediation plan CSV sorted by composite risk (severity × EPSS).

**Pitfalls:**

- Transitive deps contain the real risk — never set `include_transitive=false` without explicit user instruction.
- NVD has a reporting lag; very recent CVEs may be absent. Note the database timestamp in the report.
- Some CVEs have no fixed version — document these explicitly as "no-fix-available" rather than suppressing.
- License compliance is adjacent but out of scope here. Do not silently include license findings in the security report.

**Verification:**

1. SARIF output validates against the SARIF 2.1.0 schema: `python -c "import json, jsonschema; json.load(open('<report>.sarif')); print('ok')"` (or `trivy convert --format sarif` round-trip if a validator is unavailable).
2. Every CVE row in the Markdown report has either a `fixed_version` or an explicit `no-fix-available` marker.
3. SBOM (if requested) opens in `trivy sbom <file>` and reports the same package count as the scan.
4. Exit code 0 with `severity_threshold=critical` produces zero Critical findings on a clean target.

---

### Skill 2: `secret-scan` (P0)

**Directory:** `skills/devops/secret-scan/`
**Purpose:** Detect hardcoded secrets, API keys, tokens, and credentials in source and git history.

**Frontmatter (YAML):**

```yaml
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
    description: full-history (default) or diff-only (against main)
    required: false
  - name: custom_rules
    description: Path to a custom Gitleaks/Trufflehog rules file
    required: false
  - name: output_format
    description: Report format (sarif, json, markdown)
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
```

**Operational Steps:**

1. Choose primary tool: **Gitleaks** (open-source-first). Trufflehog acceptable as a secondary verifier for high-confidence findings.
2. Run baseline scan against working tree:
   ```bash
   gitleaks detect --source <scan_path> --report-format sarif --report-path secrets.sarif --no-git
   ```
3. For `scan_depth=full-history`, additionally run with full git history:
   ```bash
   gitleaks detect --source <scan_path> --report-format sarif --report-path secrets-history.sarif
   ```
4. Triage findings: categorize each as **true positive / false positive / test fixture**. False positives must be added to a `.gitleaksignore` or `gitleaks:allow` directive with a reason.
5. For every true positive, emit a "rotate now" recommendation block listing the secret type, file/commit, and rotation steps.
6. If a pre-commit hook is requested, write `.pre-commit-config.yaml` with the `gitleaks` hook pinned to a specific version.

**Pitfalls:**

- Test fixtures and docs contain fake keys that look real. Always review before alerting.
- Secrets that have been rebased/squashed away are still recoverable from reflog; use `git log --all --full-history -- <path>` for thorough audits.
- A finding means "rotate immediately" regardless of repo visibility — exposure window is the trigger, not current reachability.
- Entropy-based detection has high false-positive rates. Prefer pattern-based rules; entropy is a tiebreaker, not a primary signal.

**Verification:**

1. SARIF report opens and has at least the required `runs[0].results[]` array.
2. Every finding lists a rotation recommendation; no finding is left without remediation text.
3. On a clean repository, exit code 0 and zero findings.
4. Pre-commit hook (if generated) installs and runs in a sample commit: `pre-commit run gitleaks --all-files` exits 0 on clean and non-zero on a synthetic `.env` containing `AKIA...`.

---

### Skill 3: `vulnerability-triage` (P0)

**Directory:** `skills/devops/vulnerability-triage/`
**Purpose:** Triage scan results using CVSS v4.0 severity, EPSS exploit probability, and business context to produce a prioritized remediation plan.

**Frontmatter (YAML):**

```yaml
---
name: vulnerability-triage
description: Triage vulnerability scan results with CVSS v4.0 + EPSS + business context to produce a prioritized remediation plan.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks to triage or prioritize vulnerability scan results
  - User mentions CVSS, EPSS, vulnerability prioritization, or risk scoring
  - User has a scan report and needs to decide what to fix first
  - User wants to assess whether a finding is actually exploitable in their context
inputs:
  - name: scan_results
    description: Path to a scan output in SARIF, JSON, or CSV (single file or directory)
    required: true
  - name: business_context
    description: Object describing exposure (internet-facing, internal), data classification, and regulatory scope
    required: false
  - name: epss_enabled
    description: Look up EPSS scores (default: true)
    required: false
  - name: cvss_version_preference
    description: Prefer v4.0 (default), fall back to v3.1
    required: false
outputs:
  - name: triage_report
    description: Markdown report grouping findings into Fix Now / Fix Soon / Defer / Accept Risk
  - name: remediation_plan
    description: Ordered CSV of actions (file, package, recommended version, priority)
metadata:
  hermes:
    tags: [security, vulnerability, cvss, epss, triage, prioritization, devops]
    related_skills:
      - sast-scan
      - dast-scan
      - sca-scan
      - secret-scan
      - iac-security-scan
      - security-risk-assessment
      - ci-security-pipeline
---
```

**Operational Steps:**

1. Parse input scan results. Accept SARIF, JSON, or CSV. Normalize into a single internal finding record: `{id, source, file, line, rule, cve, cvss_v4, cvss_v3, epss, message, business_context}`.
2. Deduplicate on `(cve, file)` so the same CVE from multiple tools is counted once.
3. For each CVE, look up CVSS v4.0 from NVD; fall back to CVSS v3.1. Mark the version used per row.
4. For each CVE, look up EPSS from the FIRST EPSS API. Cache results for ≤24h. Mark EPSS as `<unknown>` if the API is unreachable (do not silently zero).
5. Apply business-context multipliers:
   - `internet_facing: true` → ×1.5 on composite score
   - `data_classification: restricted` → ×1.5
   - `regulatory_scope: [pci-dss, hipaa]` → ensure any non-Low finding is at least "Fix Soon"
6. Compute composite priority bucket:
   - **Fix Now** — CVSS ≥ 7.0 AND (EPSS ≥ 0.1 OR business_context elevates)
   - **Fix Soon** — CVSS ≥ 4.0 AND not Fix Now
   - **Defer** — CVSS < 4.0 AND EPSS < 0.1
   - **Accept Risk** — explicitly marked by user (must include justification)
7. Write the Markdown triage report (grouped by bucket, sorted by composite score desc) and a CSV remediation plan.

**Pitfalls:**

- CVSS scores are frequently inflated; EPSS provides the real-world context that prevents alert fatigue.
- A Critical CVSS with EPSS < 0.01 may be lower real risk than a High CVSS with EPSS > 0.5 — do not sort by CVSS alone.
- Business context cannot be fully automated; missing context MUST be flagged as `needs_input` and the report still emitted, but the row marked accordingly.
- Different scan tools may report the same CVE with different identifiers — dedupe on CVE, not on tool-internal ID.

**Verification:**

1. The triage report groups findings into exactly the four named buckets.
2. Every row with a CVE shows both CVSS version used and EPSS value (or `<unknown>`).
3. Deduplication: feeding the same SARIF twice produces the same number of distinct findings; cross-tool merge collapses identical CVEs.
4. EPSS cache TTL is respected — repeated runs within 24h reuse the cache (verifiable via a header log line in the script's stdout when implemented).

---

### Skill 4: `ci-security-pipeline` (P1)

**Directory:** `skills/devops/ci-security-pipeline/`
**Purpose:** Design and emit CI/CD security pipeline configuration (pre-commit, PR checks, deployment gates) that orchestrates the scan skills.

**Frontmatter (YAML):**

```yaml
---
name: ci-security-pipeline
description: Design and emit CI/CD security pipeline stages (pre-commit, PR, deploy gates) chaining SAST, SCA, secret, IaC, and DAST.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks to set up security scanning in a CI/CD pipeline
  - User mentions DevSecOps, shift-left security, or security gates
  - User wants pre-commit or pre-push hooks for secret detection
  - User wants to integrate security scanning into GitHub Actions, GitLab CI, or Jenkins
inputs:
  - name: pipeline_platform
    description: github-actions, gitlab-ci, jenkins, or circleci
    required: true
  - name: scan_types
    description: Subset of [sast, sca, secret, iac, dast] to include (default: all except dast)
    required: false
  - name: enforcement_level
    description: advisory (warn only) or blocking (fail PR)
    required: false
  - name: repo_path
    description: Path to the target repository
    required: true
  - name: compliance_framework
    description: Optional compliance target (cis, nist, pci-dss, hipaa)
    required: false
outputs:
  - name: pipeline_config
    description: CI/CD configuration file(s) written under .github/workflows/, .gitlab-ci.yml, etc.
  - name: pre_commit_config
    description: .pre-commit-config.yaml with secret-scan hook
  - name: security_scanning_doc
    description: security-scanning.md written into the repo root documenting the pipeline
metadata:
  hermes:
    tags: [security, ci-cd, devsecops, github-actions, gitlab, jenkins, pipeline, devops]
    related_skills:
      - sast-scan
      - dast-scan
      - sca-scan
      - secret-scan
      - iac-security-scan
      - vulnerability-triage
      - github-actions-templates
      - deployment-procedures
---
```

**Operational Steps:**

1. Inspect `repo_path` to detect stack (manifests, Dockerfile, IaC files) so the right scan mix is selected.
2. Recommend a default scan mix:
   - Always: `secret-scan` (pre-commit + PR), `sca-scan` (PR), `iac-security-scan` (PR if IaC present)
   - Default on: `sast-scan` (PR) if source code is present
   - Gate: `dast-scan` only on pre-deploy to a staging environment
3. Emit `.pre-commit-config.yaml` with `gitleaks` pinned to a specific version. Stage: pre-commit.
4. Emit platform-specific workflow:
   - **GitHub Actions** → `.github/workflows/security.yml` with jobs: `secrets`, `sca`, `sast`, `iac`, and (optional) `dast` against a deployed preview.
   - **GitLab CI** → `.gitlab-ci.yml` `security` stage with parallel jobs.
   - **Jenkins** → `Jenkinsfile.security` snippet.
5. For `enforcement_level=blocking`, fail the build on Critical/High findings; for `advisory`, emit annotations and `continue-on-error: true`.
6. Configure SARIF upload to GitHub Security tab (when `pipeline_platform=github-actions`): `github/codeql-action/upload-sarif@v3` pinned.
7. Pin all third-party actions to a specific `@vX` or commit SHA. Refuse to emit `@master` or `@main`.
8. Write `security-scanning.md` at the repo root describing: which scans run where, severity gate thresholds, how to triage a finding, and the rotation policy for detected secrets.
9. Add a weekly scheduled run for fresh vulnerability databases (`schedule: cron: '0 6 * * 1'` style).

**Pitfalls:**

- Pre-commit hooks that run heavy scans (SAST on full code) are bypassed. Keep pre-commit to secret-scan only; move SAST/SCA to PR.
- DAST cannot run in PR; gate it on a deployment preview or staging deploy.
- Vulnerability databases update daily; weekly schedules will miss intra-week disclosures. Document the lag.
- `enforcement_level=blocking` on day-1 will cause alert fatigue. Recommend a 2-week advisory period before flipping to blocking — encode this as a comment in the generated workflow.
- Pinning all actions and images is a supply-chain requirement; the skill MUST refuse to emit unpinned actions.

**Verification:**

1. The generated workflow file is syntactically valid: `actionlint <file>` (or platform equivalent).
2. `grep -E '@(master|main)' <generated workflow>` returns zero matches.
3. `pre-commit run --all-files` on a clean repo exits 0.
4. `security-scanning.md` exists in `repo_path` and contains the required sections (scan inventory, severity gates, triage procedure, rotation policy).

---

### Skill 5: `sast-scan` (P1)

**Directory:** `skills/devops/sast-scan/`
**Purpose:** Run Static Application Security Testing on source code for code-level vulnerabilities (injection, XSS, insecure deserialization, etc.).

**Frontmatter (YAML):**

```yaml
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
    description: Force a language (python, javascript, typescript, go, java); auto-detected if omitted
    required: false
  - name: scan_path
    description: Path to scan (file or directory)
    required: true
  - name: ruleset
    description: Semgrep ruleset (p/security-audit, p/owasp-top-ten) or Bandit/CodeQL config
    required: false
  - name: severity_threshold
    description: Minimum severity to report (critical, high, medium, low)
    required: false
  - name: output_format
    description: Report format (sarif, json, markdown)
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
```

**Operational Steps:**

1. Detect language(s) from file extensions and `shebangs`. If multiple languages, run per-language scans and merge results.
2. Select tool by language:
   - **Python** → Bandit (`bandit -r <path> -f sarif -o sast.sarif`)
   - **JS/TS** → Semgrep (`semgrep --config p/javascript --config p/typescript --sarif --output sast.sarif <path>`)
   - **Go** → Semgrep Go ruleset or `gosec ./...`
   - **Multi-language / cross-cutting** → Semgrep with `p/security-audit`
3. If the project mixes languages, prefer Semgrep as the single tool to keep SARIF output uniform.
4. Run with severity threshold filter; default: report all severities.
5. Filter out findings below the threshold; preserve the original count for the report summary.
6. Normalize output to the common SARIF shape (see "Interface Definitions" above). Set `properties.severity` from the tool's native severity; set `properties.cvss_v4` to `null` (SAST findings are not necessarily CVEs).
7. Emit a Markdown report with one row per finding, plus a summary (counts by severity, by language).

**Pitfalls:**

- SAST false positive rates are 30–70%. Always funnel results through `vulnerability-triage` before acting.
- No single SAST tool covers every language. Multi-language repos require multi-tool runs.
- Some tools (e.g., CodeQL) require a buildable codebase; do not silently fail on unbuildable code — note it in the report.
- Long scan times cause developers to bypass the step. Scope to changed files in PR mode; full scan in scheduled job.

**Verification:**

1. SARIF output is valid: `python -c "import json; json.load(open('sast.sarif'))"` exits 0.
2. On a clean target, zero findings and exit 0.
3. Severity counts in the Markdown summary sum to the total finding count in SARIF.
4. Multi-language scan produces findings from each detected language when seeded with known-bad snippets.

---

### Skill 6: `iac-security-scan` (P1)

**Directory:** `skills/devops/iac-security-scan/`
**Purpose:** Scan Infrastructure-as-Code definitions (Terraform, CloudFormation, Kubernetes manifests, Dockerfiles) for misconfigurations and compliance violations.

**Frontmatter (YAML):**

```yaml
---
name: iac-security-scan
description: Scan IaC definitions (Terraform, CloudFormation, K8s, Dockerfiles) for misconfigurations and compliance violations.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks to scan Terraform, CloudFormation, Kubernetes, or Docker configs for security issues
  - User mentions IaC scanning, Checkov, tfsec, KICS, or infrastructure misconfiguration
  - CI pipeline needs IaC security scanning
  - User wants to check cloud resource definitions for compliance violations
inputs:
  - name: scan_path
    description: Path to the IaC files
    required: true
  - name: iac_type
    description: terraform, cloudformation, kubernetes, dockerfile, or all (default: all)
    required: false
  - name: severity_threshold
    description: Minimum severity to report
    required: false
  - name: compliance_framework
    description: cis, nist, pci-dss, or hipaa — applied when the tool supports it
    required: false
outputs:
  - name: findings
    description: Misconfigurations with severity, resource, and remediation
  - name: report_file
    description: Path to the written report (SARIF/JSON/Markdown)
metadata:
  hermes:
    tags: [security, iac, terraform, kubernetes, dockerfile, checkov, misconfiguration, compliance, devops]
    related_skills:
      - sca-scan
      - sast-scan
      - secret-scan
      - vulnerability-triage
      - ci-security-pipeline
---
```

**Operational Steps:**

1. Detect IaC file types in `scan_path` (extensions: `.tf`, `.tfvars`, `cloudformation.yaml|json`, Kubernetes manifests, `Dockerfile*`).
2. Select primary tool: **Checkov** (multi-framework, compliance support). Alternative: Trivy config scan or KICS.
3. Run Checkov with the requested framework filter (`--framework terraform,kubernetes,dockerfile`):
   ```bash
   checkov -d <scan_path> -o sarif --output-file-path iac.sarif --framework <frameworks>
   ```
4. If `compliance_framework` is set, pass `--check` filters that map to it (e.g., `CKV_AWS_xxx` for CIS AWS) and document the mapping in the report.
5. Normalize SARIF output. Set `properties.severity` from Checkov's `BC_RESULT_SEVERITY`; map framework tags to compliance annotations.
6. Emit a Markdown report with: finding ID, resource, file, severity, compliance framework tag, remediation.

**Pitfalls:**

- IaC scanning evaluates declared state, not live cloud state. A clean scan does not guarantee a secure deployed environment. Document this gap in the report footer.
- Some misconfigurations are intentional (public S3 for static hosting). Support a documented exception list and skip with a reason.
- Multi-cloud IaC needs the tool to support both providers; Checkov handles AWS/GCP/Azure but KICS is weaker on GCP.
- Dockerfile scanning catches base image and build-time issues, not runtime configuration drift in K8s deployments.

**Verification:**

1. SARIF output is valid JSON with at least one `runs[].results[]` entry when findings exist.
2. Compliance mapping table is present in the report when `compliance_framework` is set.
3. Exception list (if used) is cited in the report and the `report_file` documents which findings were skipped and why.
4. Exit code 0 on clean IaC; non-zero on Critical/High when enforcement is requested.

---

### Skill 7: `dast-scan` (P2)

**Directory:** `skills/devops/dast-scan/`
**Purpose:** Run Dynamic Application Security Testing against a running application to find runtime vulnerabilities.

**Frontmatter (YAML):**

```yaml
---
name: dast-scan
description: Run Dynamic Application Security Testing on a running app to find runtime issues like XSS, SQLi, and bad headers.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks to scan a running application for security vulnerabilities
  - User mentions DAST, dynamic scanning, OWASP ZAP, or Nuclei
  - CI pipeline needs dynamic security testing
  - User wants to test authentication, session management, or input validation of a live endpoint
inputs:
  - name: target_url
    description: URL of the running application (must be staging or test)
    required: true
  - name: scan_type
    description: baseline, full, or api
    required: false
  - name: auth_config
    description: Path to authentication config (form, bearer, cookie) for authenticated scans
    required: false
  - name: output_format
    description: Report format (sarif, json, markdown)
    required: false
outputs:
  - name: scan_results
    description: SARIF/JSON/Markdown report of dynamic findings
  - name: report_file
    description: Path to the written report
metadata:
  hermes:
    tags: [security, dast, dynamic-analysis, owasp-zap, nuclei, devops]
    related_skills:
      - sast-scan
      - api-security-best-practices
      - vulnerability-triage
      - ci-security-pipeline
---
```

**Operational Steps:**

1. Validate `target_url` is reachable (`curl -fsS -o /dev/null -w "%{http_code}\n" <target_url>`). Refuse to scan if the URL resolves to a known production hostname unless the user explicitly confirms with a `--i-know-this-is-production` flag.
2. Choose tool by `scan_type`:
   - `baseline` → OWASP ZAP baseline: `zap-baseline.py -t <target_url> -r report.html -J report.json`
   - `full` → OWASP ZAP full scan: `zap-full-scan.py -t <target_url> -r report.html -J report.json`
   - `api` → Nuclei with API templates: `nuclei -u <target_url> -t technologies/ -t vulnerabilities/ -json`
3. For authenticated scans, generate the auth context via the `auth_config` (ZAP context file or Nuclei `auth.yaml`) and verify a sample authenticated request returns 200 before proceeding.
4. Throttle scan to avoid impacting the target: default 10 requests/sec; configurable via env var.
5. Parse and deduplicate results; collapse repeated alerts on the same URL+param pair.
6. Normalize to the common SARIF shape. DAST findings rarely have CVEs; `properties.cvss_v4` will usually be `null`.
7. Write Markdown report with: finding, URL, evidence, severity, remediation.

**Pitfalls:**

- DAST requires a running instance; do not invoke on unbuildable or un-deployed code.
- Active scans can mutate data in non-test environments. Refuse to scan URLs that resolve to a known production host without explicit confirmation.
- Authenticated scans need careful credential handling. Credentials in `auth_config` MUST be sourced from environment variables or a vault reference, not embedded in plaintext.
- DAST catches runtime issues but misses code-level patterns SAST catches. Always run both.

**Verification:**

1. SARIF output is valid JSON.
2. Refusal guard: scanning a known production hostname without the override flag exits with a clear error and no scan output.
3. Throttle can be observed (request rate ≤ 10 rps by default) — verifiable from access logs of the target.
4. Authenticated scan: a sample request to a protected endpoint returns 200 before the scan proceeds; without auth, the scan produces unauthenticated-only findings.

---

### Skill 8: `security-risk-assessment` (P2)

**Directory:** `skills/devops/security-risk-assessment/`
**Purpose:** Conduct a structured security risk assessment combining scan data, threat modeling, business impact, and compliance requirements.

**Frontmatter (YAML):**

```yaml
---
name: security-risk-assessment
description: Conduct a structured risk assessment combining scans, threat models, business impact, and compliance for execs.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User asks for a security risk assessment or risk report
  - User wants to evaluate business impact of vulnerabilities
  - User asks about regulatory compliance for security (PCI-DSS, HIPAA, SOC 2, ISO 27001)
  - User wants to combine scan results with business context for prioritization
inputs:
  - name: scan_reports
    description: List of paths to scan outputs (SARIF/JSON/CSV) — optional
    required: false
  - name: repo_path
    description: Path to the codebase for threat modeling (optional but recommended)
    required: false
  - name: compliance_frameworks
    description: List of frameworks to assess against (pci-dss, hipaa, soc2, iso27001)
    required: false
  - name: risk_tolerance
    description: conservative, moderate, or aggressive — used to adjust gates
    required: false
  - name: business_context
    description: Data classification, regulatory scope, exposure, blast radius
    required: false
outputs:
  - name: risk_assessment_report
    description: Markdown risk assessment with risk matrix, executive summary, and remediation roadmap
  - name: risk_register
    description: Structured risk register in JSON/CSV for tracking
metadata:
  hermes:
    tags: [security, risk-assessment, compliance, fair, nist-800-30, executive-report, devops]
    related_skills:
      - vulnerability-triage
      - security-threat-model
      - security-best-practices
      - ci-security-pipeline
      - sast-scan
      - dast-scan
      - sca-scan
      - secret-scan
      - iac-security-scan
---
```

**Operational Steps:**

1. Collect all available `scan_reports` and run them through `vulnerability-triage` (load that skill) to get a normalized, prioritized finding list.
2. If `repo_path` is provided, load the `security-threat-model` skill and reference its trust boundaries and assets in the report.
3. For each finding, evaluate business impact on a 4-axis scale (1–5):
   - **Data classification** (public → restricted)
   - **Regulatory scope** (none → PCI/HIPAA)
   - **Blast radius** (single service → organization-wide)
   - **Compensating controls** (none → strong)
4. Build a **risk matrix** (5×5 likelihood × impact) following NIST SP 800-30 Rev. 1 terminology. Each cell must contain either a finding reference or "no current risk."
5. For each finding, compute composite risk = likelihood × impact. Bucket:
   - **Critical** (≥20)
   - **High** (12–19)
   - **Medium** (6–11)
   - **Low** (1–5)
6. Apply `risk_tolerance` to gate the remediation roadmap:
   - `conservative` → treat High as immediate, include Medium in 90-day plan
   - `moderate` (default) → Critical in 7 days, High in 30 days, Medium in 90 days
   - `aggressive` → Critical in 30 days, High in 90 days, Medium/Low backlogs
7. **Optional FAIR worksheet** (only when quantitative inputs are available):
   - Loss Event Frequency = Threat Event Frequency × Vulnerability × Loss Event Probability
   - Probable Loss Magnitude = Primary Loss + Secondary Loss
   - Annualized Loss Expectancy = LEF × PLM
   - If inputs are unavailable, mark the section "qualitative, not quantitative" and do not invent numbers.
8. Map findings to compliance frameworks if requested. For each framework, produce a "controls in scope" section mapping findings to control families.
9. Write the Markdown report with sections: Executive Summary, Risk Matrix, Compliance Mapping, Remediation Roadmap, FAIR Worksheet (optional), Assumptions, Open Questions.
10. Emit a risk register as JSON (one row per risk with: id, description, likelihood, impact, score, owner, due date, status).

**Pitfalls:**

- Risk assessments without business context are just vulnerability lists. Always connect findings to business impact.
- Regulatory compliance may elevate findings that would otherwise be low priority (e.g., a Medium CVSS finding under PCI-DSS may be a High risk). Document these elevations.
- Threat modeling and vulnerability scanning are complementary; if `security-threat-model` is not run, mark the threat-model section as "pending" rather than skipping it.
- Risk tolerance varies by org; the chosen value MUST be visible in the report and the report MUST NOT silently default to `moderate` without flagging it.
- Executive reports lead with business impact, not CVE counts. The first section is the executive summary; CVE lists live in the appendix.

**Verification:**

1. Risk matrix is 5×5 with every cell labelled (finding or "no current risk").
2. Every finding has all four business-impact axes scored.
3. Risk register JSON validates as JSON and has one row per finding.
4. Compliance mapping section is present when `compliance_frameworks` is set; absent when not set (do not invent).
5. FAIR section, if present, is labelled either "quantitative" (with explicit input sources) or "qualitative — quantitative inputs not available."

---

## Task Breakdown

Each skill is one Weaver task per SOP §4 ("Adding a New Skill"). Priority is preserved from the research brief (P0 first, then P1, then P2). Tasks are independent enough to parallelize, but cross-references require that all 8 land in the same release if cross-references are to validate cleanly. Recommended sequence: implement in priority order; the related_skills references will resolve once the dependent skill lands.

| # | Task | Assignee | Priority | Depends On | Acceptance Criteria |
|---|------|----------|----------|------------|---------------------|
| 1 | Add `sca-scan` skill | weaver | P0 | — | All SKILL-SPEC.md required frontmatter present; `name` matches dir; trigger list ≥1; steps numbered; pitfalls ≥3; verification ≥2 checks; related_skills only reference existing or this-set skills; `test -f skills/devops/sca-scan/SKILL.md` exits 0 |
| 2 | Add `secret-scan` skill | weaver | P0 | — | Same validation as #1, with one Gitleaks-related verification step; `.pre-commit-config.yaml` snippet referenced from SKILL.md and emitted by the steps |
| 3 | Add `vulnerability-triage` skill | weaver | P0 | — | Triage report demonstrates CVSS v4.0 preference and v3.1 fallback; EPSS lookup logic described; dedup behavior described; four-bucket output documented |
| 4 | Add `ci-security-pipeline` skill | weaver | P1 | #1, #2, #3, #5, #6 | Generated GitHub Actions workflow has no `@master`/`@main` actions; pre-commit config includes gitleaks; `security-scanning.md` template present; platform variants covered |
| 5 | Add `sast-scan` skill | weaver | P1 | — | Multi-language tool selection documented; SARIF normalization; language-specific pitfalls enumerated; verification covers multi-language case |
| 6 | Add `iac-security-scan` skill | weaver | P1 | — | Checkov as primary tool; compliance framework mapping documented; exception-list mechanism described; live-vs-declared-state gap noted in pitfalls |
| 7 | Add `dast-scan` skill | weaver | P2 | — | Refusal-to-scan-production guard; throttle default documented; auth credential handling emphasizes env/vault only; baseline/full/api scan types covered |
| 8 | Add `security-risk-assessment` skill | weaver | P2 | #1, #2, #3, #5, #6, #7 | Risk matrix 5×5; FAIR qualitative vs quantitative explicit; executive summary leads; risk register JSON documented; references `security-threat-model` and `vulnerability-triage` correctly |
| 9 | Cross-reference pass | weaver | after #1–#8 | #1–#8 | Every `related_skills` entry in the 8 new SKILL.md files resolves to a directory that exists in `skills/`. Run: `for f in skills/devops/*/SKILL.md; do grep -E 'related_skills' "$f"; done` followed by manual cross-check |

### Per-Task Specifications (concise)

For each row above, the full per-task spec is the corresponding skill section above. Each Weaver task package MUST include:

- A copy of the relevant skill section (frontmatter + steps + pitfalls + verification).
- A pointer to `SKILL-SPEC.md` and `SOP.md` §4 and §10 (Validation Checklist).
- The exact `mkdir -p skills/devops/<name>` and `git checkout -b feat/<name>` commands.
- An explicit reminder: "If you discover new pitfalls or tool quirks while implementing, patch the SKILL.md and update the version per SOP §5."

---

## Acceptance Criteria (top-level, for Lens review)

The spec is acceptable for implementation when all of the following are true. Lens verifies each.

- [ ] All 8 skills are spec'd with complete YAML frontmatter (name, description, version, author, license, trigger, inputs, outputs, metadata.hermes.tags, metadata.hermes.related_skills).
- [ ] Every `description` is a single line under 120 characters.
- [ ] Every `name` matches the proposed directory name and is kebab-case.
- [ ] Every skill lists a `version: 1.0.0`, `author: Broville`, `license: MIT`.
- [ ] Every skill has a `trigger` array with at least one condition that matches the user's request.
- [ ] Every skill documents `inputs` and `outputs` using the YAML object form (per `SKILL-SPEC.md` §"Inputs and Outputs").
- [ ] Every skill has a numbered Steps section, a Pitfalls section with ≥3 entries, and a Verification section with ≥2 concrete checks (commands or assertions).
- [ ] Every skill's `related_skills` lists only skills that exist in the repo OR are part of this 8-skill set.
- [ ] No skill contains hardcoded secrets, tokens, or absolute local paths.
- [ ] All four risk-analysis protocols (CVSS v4.0, EPSS, NIST SP 800-30, FAIR) are explicitly integrated into the relevant skills, with version preference and fallback documented for CVSS.
- [ ] The cross-skill SARIF contract is defined once and referenced by all five scan-producing skills.
- [ ] The P0 / P1 / P2 priority ordering is preserved in the task breakdown.
- [ ] The spec document itself does NOT create skill directories; that is Weaver's job (per SOP §4 and the Cartographer handoff protocol — design only, no implementation).

---

## Constraints, Risks, and Assumptions (what Lens must inspect)

### Constraints

- All 8 skills MUST live in `skills/devops/` (per SOP §3 + category table).
- No new categories may be created (per SOP §3: "Do not create new categories without opening an issue first").
- Each skill is a single `SKILL.md` (plus optional `references/`, `templates/`, `scripts/`, `assets/` per SOP §3) — no executable code is shipped in the skill itself unless it is in `scripts/` and referenced.
- No secrets, tokens, or local paths in any skill file (per SOP §4 "What NOT to do").
- Naming: kebab-case, no collisions with existing skills (verified above).

### Risks

- **EPSS data freshness**: API cache TTL is set to 24h. A run that pulls stale EPSS will mis-prioritize. The skill must surface the EPSS data timestamp in the report. Lens: confirm the SKILL.md for `vulnerability-triage` requires this timestamp in the report header.
- **CVSS v4.0 adoption lag**: many data sources still publish only v3.1. The fallback path is documented, but Lens should confirm the skill flags the version used per row (not silently).
- **DAST in CI**: spinning up a test environment for DAST is stack-dependent. The spec defers this to user-provided deployment context. Lens: confirm the skill refuses to run on production URLs without an override flag.
- **Tool licensing**: several tools (SonarQube, Burp Suite, Checkmarx) are commercial. Spec recommends open-source-first and notes alternatives. Lens: confirm no skill is silently dependent on a commercial tool.
- **Compliance framework mapping**: tools map to benchmarks (e.g., CIS AWS Foundations) but not directly to PCI-DSS/HIPAA controls. The `security-risk-assessment` skill is responsible for the interpretive mapping. Lens: confirm the report documents this gap and does not claim automatic compliance from a scan.
- **CI pinning**: an unpinned GitHub Action is a supply-chain risk. Lens: confirm `ci-security-pipeline` and any emitted workflow refuse `@master`/`@main` and pin to a specific `@vX` or commit SHA.

### Assumptions

- The agent runtime has shell access and can install open-source scanners (Gitleaks, Trivy, Semgrep, Bandit, Checkov, OWASP ZAP, Nuclei) on demand. The skill's `Prerequisites` section must state this.
- The `security-threat-model` skill already exists at `skills/software-dev/security-threat-model/SKILL.md` (verified — yes).
- The `github-actions-templates` skill at `skills/devops/github-actions-templates/SKILL.md` already includes a basic security-scan pattern; `ci-security-pipeline` complements it rather than replaces it. (Verified — yes, Pattern 3 is a basic Trivy scan.)
- The `security-best-practices`, `security-ownership-map`, and `api-security-best-practices` skills exist (verified — yes) and are referenced appropriately in the related_skills lists.
- The CVSS v4.0 → v3.1 fallback hierarchy is acceptable to the user; the brief notes mid-2025 adoption lag and explicitly recommends the v4.0-prefer / v3.1-fallback approach.
- The user accepts the P0/P1/P2 priority as proposed. No reprioritization requested in the task body.

### Information Not Sufficient

None. The research brief is sufficient to produce this spec. Open questions for downstream workers (Weaver, Lens) are called out above in the Risks and Assumptions sections rather than blocking the spec.

---

## Deliverable Summary

- **Spec location:** `spec/devops-security-scan-skill-set-spec.md` (this file).
- **Research source:** `research/devops-security-scan-risk-analysis-research-brief.md`.
- **Number of skills spec'd:** 8.
- **Number of priority tiers:** 3 (P0: 3 skills, P1: 3 skills, P2: 2 skills).
- **Number of cross-cutting protocols documented:** 4 (CVSS v4.0, EPSS, NIST SP 800-30, FAIR).
- **Number of risk-analysis skills:** 2 (`vulnerability-triage`, `security-risk-assessment`); CVSS/EPSS in triage, NIST/FAIR in risk-assessment.
- **No implementation performed:** no skill directories created, no SKILL.md files written under `skills/devops/`. Implementation is Weaver's responsibility per SOP §4.

---

## Cross-References

- **Research brief:** `research/devops-security-scan-risk-analysis-research-brief.md` (t_29b48c3b)
- **SOP — Skill Authoring Process:** `SOP.md` §4 (Adding a New Skill), §10 (Validation Checklist)
- **SOP — Validation Requirements:** `SOP.md` §10 (every frontmatter field, every content rule, every structure rule)
- **SKILL Format:** `SKILL-SPEC.md` (frontmatter schema, body sections, versioning)
- **Existing skills referenced in related_skills:**
  - `software-dev/security-best-practices`
  - `software-dev/security-threat-model`
  - `software-dev/security-ownership-map`
  - `software-dev/api-security-best-practices`
  - `devops/github-actions-templates`
  - `devops/deployment-procedures`
