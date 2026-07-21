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
    description: "URL of the running application (must be staging or test)"
    required: true
  - name: scan_type
    description: baseline, full, or api
    required: false
  - name: auth_config
    description: "Path to authentication config (form, bearer, cookie) for authenticated scans"
    required: false
  - name: output_format
    description: "Report format (sarif, json, markdown)"
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

# dast-scan

## Description

Run Dynamic Application Security Testing (DAST) against a running application to find runtime vulnerabilities such as cross-site scripting, SQL injection, and missing security headers. The skill refuses to scan production URLs without an explicit override, throttles requests, and normalizes output to SARIF 2.1.0.

## Prerequisites

- A running target application reachable at `target_url`.
- `zap-baseline.py` / `zap-full-scan.py` or `nuclei` installed, or available as a Docker image.
- For authenticated scans, a valid `auth_config` file and a sample authenticated request path.

## Steps

1. Validate that `target_url` is reachable:
   ```bash
   curl -fsS -o /dev/null -w "%{http_code}\n" <target_url>
   ```
2. Refuse to scan if the hostname is a known production host unless the user explicitly confirms with a flag (e.g., `--i-know-this-is-production`). Exit with a clear error and no scan output.
3. Choose the scanner by `scan_type`:
   - `baseline` → `zap-baseline.py -t <target_url> -r report.html -J report.json`
   - `full` → `zap-full-scan.py -t <target_url> -r report.html -J report.json`
   - `api` → `nuclei -u <target_url> -t technologies/ -t vulnerabilities/ -json`
4. For authenticated scans, generate the auth context from `auth_config` (ZAP context file or Nuclei `auth.yaml`) and verify that a sample authenticated request returns HTTP 200 before proceeding.
5. Throttle the scan to avoid impacting the target: default 10 requests/sec. Allow override via environment variable (e.g., `DAST_RPS`).
6. Parse and deduplicate results; collapse repeated alerts on the same URL+parameter pair.
7. Normalize to the common SARIF 2.1.0 shape. DAST findings rarely have CVEs; set `properties.cvss_v4` to `null` when unavailable.
8. Write a Markdown report with: finding, URL, evidence, severity, and remediation.

## Pitfalls

- DAST requires a running instance. Do not invoke on unbuildable or un-deployed code.
- Active scans can mutate data in non-test environments. Refuse to scan URLs that resolve to a known production host without explicit confirmation.
- Authenticated scans need careful credential handling. Credentials in `auth_config` MUST be sourced from environment variables or a vault reference, never embedded in plaintext.
- DAST catches runtime issues but misses code-level patterns that SAST catches. Always run both.
- Throttle defaults are a safety mechanism; raising them without need can overwhelm the target.

## Verification

1. SARIF output is valid JSON:
   ```bash
   python -c "import json; json.load(open('dast.sarif')); print('SARIF ok')"
   ```
2. The production-host guard works: scanning a known production hostname without the override flag exits with a clear error and no scan output.
3. Request rate stays at or below 10 rps by default (verifiable from target access logs).
4. For authenticated scans, a sample request to a protected endpoint returns HTTP 200 before the scan proceeds; without auth, the scan produces only unauthenticated findings.

## Cross-References

- Complements `sast-scan` to cover runtime attack surface.
- Works with `api-security-best-practices` for API-specific checks.
- Results feed into `vulnerability-triage` and `ci-security-pipeline` (staging gate).
