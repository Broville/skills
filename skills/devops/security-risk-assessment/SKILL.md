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
    description: "List of paths to scan outputs (SARIF/JSON/CSV) — optional"
    required: false
  - name: repo_path
    description: "Path to the codebase for threat modeling (optional but recommended)"
    required: false
  - name: compliance_frameworks
    description: "List of frameworks to assess against (pci-dss, hipaa, soc2, iso27001)"
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

# security-risk-assessment

## Description

Conduct a structured security risk assessment that combines scan data, threat modeling, business impact, and compliance requirements. Produces an executive-friendly Markdown report with a 5×5 risk matrix, optional FAIR worksheet, and a machine-readable risk register.

## Prerequisites

- Optional scan reports in SARIF, JSON, or CSV format.
- Optional codebase path for threat-model context.
- Business context for impact scoring (data classification, regulatory scope, exposure, blast radius).

## Steps

1. Collect all `scan_reports` and run them through `vulnerability-triage` to get a normalized, prioritized finding list.
2. If `repo_path` is provided, load the `security-threat-model` skill and reference its trust boundaries and assets in the report.
3. For each finding, evaluate business impact on a 4-axis scale (1–5):
   - **Data classification** (public → restricted)
   - **Regulatory scope** (none → PCI/HIPAA)
   - **Blast radius** (single service → organization-wide)
   - **Compensating controls** (none → strong)
4. Build a 5×5 risk matrix (likelihood × impact) using NIST SP 800-30 Rev. 1 terminology. Each cell must contain either a finding reference or the text "no current risk."
5. For each finding, compute composite risk = likelihood × impact and bucket:
   - **Critical** (≥20)
   - **High** (12–19)
   - **Medium** (6–11)
   - **Low** (1–5)
6. Apply `risk_tolerance` to the remediation roadmap:
   - `conservative` → treat High as immediate, include Medium in 90-day plan
   - `moderate` (default) → Critical in 7 days, High in 30 days, Medium in 90 days
   - `aggressive` → Critical in 30 days, High in 90 days, Medium/Low backlogs
7. Optional FAIR worksheet:
   - Loss Event Frequency = Threat Event Frequency × Vulnerability × Loss Event Probability
   - Probable Loss Magnitude = Primary Loss + Secondary Loss
   - Annualized Loss Expectancy = LEF × PLM
   - If quantitative inputs are unavailable, label the section "qualitative, not quantitative" and do not invent numbers.
8. Map findings to `compliance_frameworks` if requested. For each framework, produce a "controls in scope" section mapping findings to control families. Do not claim automatic compliance from a scan.
9. Write the Markdown report with sections: Executive Summary, Risk Matrix, Compliance Mapping, Remediation Roadmap, FAIR Worksheet (optional), Assumptions, Open Questions.
10. Emit a risk register as JSON (and optionally CSV) with one row per risk: `id, description, likelihood, impact, score, owner, due_date, status`.

## Pitfalls

- Risk assessments without business context are just vulnerability lists. Always connect findings to business impact.
- Regulatory compliance may elevate findings that would otherwise be low priority. Document these elevations explicitly.
- Threat modeling and vulnerability scanning are complementary; if `security-threat-model` is not run, mark the threat-model section as "pending" rather than skipping it.
- Risk tolerance varies by organization; the chosen value MUST be visible in the report. Do not silently default to `moderate` without flagging it.
- Executive reports must lead with business impact, not CVE counts. Put the executive summary first; CVE lists belong in the appendix.
- FAIR worksheets require quantitative inputs. If inputs are unavailable, label the section as qualitative and avoid inventing financial figures.

## Verification

1. The risk matrix is a 5×5 grid where every cell is labelled with a finding reference or "no current risk."
2. Every finding has all four business-impact axes scored (data classification, regulatory scope, blast radius, compensating controls).
3. The risk register JSON validates as JSON and contains one row per finding.
4. The compliance mapping section is present when `compliance_frameworks` is set; absent when not set (do not invent).
5. The FAIR section, if present, is labelled either "quantitative" (with explicit input sources) or "qualitative — quantitative inputs not available."

## Cross-References

- Consumes prioritized findings from `vulnerability-triage`.
- Uses `security-threat-model` for trust-boundary context when available.
- Informs `ci-security-pipeline` gate thresholds and executive reporting.
