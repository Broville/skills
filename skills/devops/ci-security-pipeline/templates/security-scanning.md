# Security Scanning Runbook

This document describes the security scanning pipeline for this repository, how findings are triaged, and how to respond to detected secrets.

## Scan Inventory

| Stage   | Scanner | Trigger | Output |
|---------|---------|---------|--------|
| Pre-commit | Gitleaks | every commit | `secrets.sarif` |
| PR | Gitleaks, Trivy, Semgrep, Checkov | pull request | SARIF files |
| Weekly | Trivy | schedule (`0 6 * * 1`) | `trivy-sca.sarif` |
| Staging deploy | OWASP ZAP | merge to `staging` | `dast-report.json` |

## Severity Gates

- `enforcement_level=advisory`: scans emit annotations but do not block the PR.
- `enforcement_level=blocking`: Critical/High findings fail the PR.
- A 2-week advisory period is recommended before switching to blocking.

## Triage Procedure

1. Feed scan SARIF outputs into the `vulnerability-triage` skill.
2. Prioritize by composite risk (CVSS v4.0 × EPSS) and business context.
3. Create tickets for `Fix Now` and `Fix Soon` items.
4. Mark accepted risks with a written justification.

## Secret Rotation Policy

Any secret detected in git history must be treated as exposed. Rotate the credential immediately, regardless of current repository visibility or whether the commit was reverted.

## Vulnerability Database Lag

SCA tools depend on NVD and vendor advisory databases, which can lag behind public disclosure by hours or days. The weekly schedule refreshes the database; intra-week disclosures may be missed until the next scheduled run or manual trigger.
