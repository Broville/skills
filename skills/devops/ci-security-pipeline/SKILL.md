---
name: ci-security-pipeline
description: "Design and emit CI/CD security pipeline stages (pre-commit, PR, deploy gates) chaining SAST, SCA, secret, IaC, and DAST."
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
    description: "Subset of [sast, sca, secret, iac, dast] to include (default: all except dast)"
    required: false
  - name: enforcement_level
    description: "advisory (warn only) or blocking (fail PR)"
    required: false
  - name: repo_path
    description: Path to the target repository
    required: true
  - name: compliance_framework
    description: "Optional compliance target (cis, nist, pci-dss, hipaa)"
    required: false
outputs:
  - name: pipeline_config
    description: "CI/CD configuration file(s) written under .github/workflows/, .gitlab-ci.yml, etc."
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

# ci-security-pipeline

## Description

Design and emit a complete CI/CD security pipeline configuration that orchestrates SAST, SCA, secret scanning, IaC scanning, and DAST. The skill inspects the target repository, chooses a sensible scan mix, and writes pinned workflow files, a pre-commit configuration, and a `security-scanning.md` runbook.

## Prerequisites

- Access to the target repository root (`repo_path`).
- One of the supported CI platforms is chosen: `github-actions`, `gitlab-ci`, `jenkins`, or `circleci`.
- The generated workflow assumes the corresponding scanner tools (`gitleaks`, `trivy`, `semgrep`, `bandit`, `checkov`, ZAP, Nuclei) are installed in the CI runners or available as official actions/images.

## Steps

1. Inspect `repo_path` to detect stack and IaC files:
   - Source code → enables `sast-scan`
   - `package.json`, `requirements.txt`, `go.mod`, etc. → enables `sca-scan`
   - `.tf`, `cloudformation.yaml`, Kubernetes manifests, `Dockerfile*` → enables `iac-security-scan`
   - Any repository → enables `secret-scan`
   - A deployed preview/staging URL is required for `dast-scan`
2. Choose the default scan mix:
   - Always: `secret-scan` (pre-commit + PR), `sca-scan` (PR)
   - Default on: `sast-scan` (PR) if source code is present
   - Conditional: `iac-security-scan` (PR) if IaC files are present
   - Gate: `dast-scan` only on pre-deploy to a staging environment
3. Emit `.pre-commit-config.yaml` with `gitleaks` pinned to a specific version. Use the template in `templates/pre-commit-config.yaml`.
4. Emit platform-specific workflow files:
   - **GitHub Actions** → `.github/workflows/security.yml` using `templates/github-actions-security.yml`
   - **GitLab CI** → `.gitlab-ci.yml` using `templates/gitlab-ci-security.yml`
   - **Jenkins** → `Jenkinsfile.security` using `templates/jenkins-security.txt`
5. For `enforcement_level=blocking`, fail the build on Critical/High findings; for `advisory`, emit annotations and use `continue-on-error: true`.
6. For GitHub Actions, add a SARIF upload step using `github/codeql-action/upload-sarif@v3` (or a specific pinned SHA).
7. Pin every third-party action, image, and plugin to a specific `@vX` or commit SHA. Refuse to emit `@master` or `@main`.
8. Write `security-scanning.md` from `templates/security-scanning.md`, filling in: which scans run where, severity gate thresholds, how to triage a finding, and the rotation policy for detected secrets.
9. Add a weekly scheduled run for fresh vulnerability databases (`cron: '0 6 * * 1'`).
10. Validate the generated workflow with a platform linter if available (e.g., `actionlint`).

## Pitfalls

- Pre-commit hooks that run heavy scans (e.g., full SAST) are frequently bypassed. Keep pre-commit limited to `secret-scan`; move SAST and SCA to PR checks.
- DAST cannot run in a PR against static files; gate it on a deployment preview or staging deploy.
- Vulnerability databases update daily; a weekly schedule will miss intra-week disclosures. Document the lag in `security-scanning.md`.
- `enforcement_level=blocking` on day one causes alert fatigue. Encode a 2-week advisory period as a comment before flipping to blocking.
- Unpinned actions are a supply-chain risk. The skill MUST refuse to emit `@master` or `@main`.
- Generated workflows reference the skill set’s scanners. Ensure the target repo has access to the chosen tools or official actions.

## Verification

1. The generated workflow file is syntactically valid:
   ```bash
   actionlint .github/workflows/security.yml
   ```
2. `grep -E '@(master|main)' <generated-workflow>` returns zero matches.
3. `pre-commit run --all-files` on a clean repo exits 0.
4. `security-scanning.md` exists in `repo_path` and contains sections: scan inventory, severity gates, triage procedure, rotation policy.
5. The generated GitLab/Jenkins variant has equivalent stages/jobs for the selected `scan_types`.

## Cross-References

- Emits configs that invoke `sast-scan`, `sca-scan`, `secret-scan`, `iac-security-scan`, and `dast-scan`.
- Complements `github-actions-templates` Pattern 3 and `deployment-procedures`.
- Should be paired with `vulnerability-triage` for finding prioritization.
