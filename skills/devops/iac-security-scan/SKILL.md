---
name: iac-security-scan
description: "Scan IaC definitions (Terraform, CloudFormation, K8s, Dockerfiles) for misconfigurations and compliance violations."
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
    description: "terraform, cloudformation, kubernetes, dockerfile, or all (default: all)"
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
    description: "Path to the written report (SARIF/JSON/Markdown)"
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

# iac-security-scan

## Description

Scan Infrastructure-as-Code definitions (Terraform, CloudFormation, Kubernetes manifests, Dockerfiles) for security misconfigurations and compliance violations. The skill normalizes findings to SARIF 2.1.0 and includes a compliance mapping table when a framework is requested.

## Prerequisites

- IaC files present at `scan_path`.
- `checkov` installed (primary). `trivy config` or `kics` may be used as alternatives.
- For `compliance_framework`, the chosen tool must support a benchmark mapping to that framework.

## Steps

1. Detect IaC file types in `scan_path`:
   - `.tf`, `.tfvars` → terraform
   - `*.cloudformation.json|yaml`, `cloudformation.yaml|json` → cloudformation
   - Kubernetes manifests → kubernetes
   - `Dockerfile*` → dockerfile
2. Select the framework filter for Checkov, e.g.:
   ```bash
   checkov -d <scan_path> --framework terraform,kubernetes,dockerfile -o sarif --output-file-path iac.sarif
   ```
3. If `compliance_framework` is set, pass `--check` filters that map to the framework and document the mapping in the report. Example: CIS AWS mappings use `CKV_AWS_*` checks.
4. Run Checkov and capture SARIF output.
5. Normalize SARIF. Set `properties.severity` from Checkov's `BC_RESULT_SEVERITY`. Map framework tags to compliance annotations in `properties.compliance`.
6. Apply `severity_threshold` if provided, preserving suppressed counts in the report summary.
7. Emit a Markdown report with: finding ID, resource, file, severity, compliance framework tag, and remediation.
8. If an exception list is provided, skip those findings and document the skipped IDs with reasons.

## Pitfalls

- IaC scanning evaluates declared state, not live cloud state. A clean scan does not guarantee a secure deployed environment. Document this gap in the report footer.
- Some misconfigurations are intentional (e.g., a public S3 bucket for static hosting). Support a documented exception list with reasons for each skip.
- Multi-cloud IaC needs a tool that supports both providers. Checkov handles AWS/GCP/Azure; KICS is weaker on GCP.
- Dockerfile scanning catches base-image and build-time issues, not runtime configuration drift in Kubernetes deployments.
- Compliance framework mapping is interpretive. The report must not claim automatic compliance from a scan; document the gap.

## Verification

1. SARIF output is valid JSON and contains `runs[].results[]` when findings exist.
2. The Markdown report includes a compliance mapping table when `compliance_framework` is set.
3. Any exception list is cited in the report, and the `report_file` documents which findings were skipped and why.
4. On clean IaC, the scan exits 0; on Critical/High with enforcement requested, it exits non-zero.

## Cross-References

- Pairs with `sast-scan` and `sca-scan` for a layered PR security check.
- Consumed by `ci-security-pipeline` when IaC files are detected.
- Feed findings into `vulnerability-triage` alongside CVE-based results.
