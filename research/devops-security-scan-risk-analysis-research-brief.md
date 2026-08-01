# Intelligence Brief: DevOps Security Scan & Risk Analysis Skill Set

## Summary

This research identifies 8 modular skill definitions needed to cover the DevOps security scanning and risk analysis landscape. The skills span four scanning categories (SAST, DAST, SCA, Secret Scanning), three risk analysis dimensions (vulnerability severity, exploit prediction, business impact), and one integration skill (CI/CD pipeline wiring). Four existing skills in the repo partially overlap (security-best-practices, security-threat-model, security-ownership-map, api-security-best-practices) but none cover automated scanning tool operation, CI/CD integration, or quantitative risk scoring. All proposed skills should live in the `devops` category per SOP.md conventions.

---

## Evidence

| # | Claim | Source | Confidence |
|---|-------|--------|------------|
| 1 | SAST analyzes source/compiled code for security flaws without executing it; high false positive rate; language-specific tooling required | OWASP Source Code Analysis Tools page (https://owasp.org/www-community/Source_Code_Analysis_Tools) | Certain |
| 2 | DAST tests running applications from the outside for vulnerabilities like XSS, SQL Injection, Path Traversal; requires a deployed or testable instance | OWASP Vulnerability Scanning Tools page (https://owasp.org/www-community/Vulnerability_Scanning_Tools) | Certain |
| 3 | SCA (Software Composition Analysis) identifies known vulnerabilities in third-party dependencies; operates on package manifests and lockfiles | OWASP Dependency-Check project (https://owasp.org/www-project-dependency-check/); NVD/CVE databases | Certain |
| 4 | Secret scanning detects hardcoded credentials, API keys, tokens, and private keys in git history and working tree | Gitleaks project (https://github.com/gitleaks/gitleaks, 28.2k stars); GitHub Secret Scanning docs | Certain |
| 5 | Trivy is a comprehensive open-source scanner covering vulnerabilities, misconfigurations, secrets, and SBOM for containers, Kubernetes, code repos, and clouds | Aqua Security Trivy project (https://github.com/aquasecurity/trivy, 37k stars) | Certain |
| 6 | CVSS v4.0 (Common Vulnerability Scoring System) provides a standardized framework for assessing vulnerability severity across Base, Threat, and Environmental metric groups | FIRST CVSS SIG (https://www.first.org/cvss/) | Certain |
| 7 | EPSS (Exploit Prediction Scoring System) estimates the probability that a vulnerability will be exploited in the wild within 30 days, using real-world threat data | FIRST EPSS SIG (https://www.first.org/epss/) | Certain |
| 8 | Business Impact Assessment (BIA) for vulnerabilities requires evaluating data classification, regulatory requirements, blast radius, and compensating controls — no single standardized framework exists, but NIST SP 800-30 and FAIR provide structured approaches | NIST SP 800-30 Rev. 1; FAIR framework (factoranalysis.org) | Likely |
| 9 | The repo already has `software-dev/security-best-practices`, `software-dev/security-threat-model`, `software-dev/security-ownership-map`, and `software-dev/api-security-best-practices` — none of which cover automated scanning tool operation or CI/CD integration | Direct repo inspection | Certain |
| 10 | SOP.md defines 8 categories: devops, software-dev, mlops, data, research, creative, productivity, monitoring — security scanning skills map to `devops`; risk analysis maps to `devops` or `research` | SOP.md (lines 66-78) | Certain |
| 11 | SKILL-SPEC.md requires frontmatter fields: name, description, version, author, license; optional: platforms, metadata (hermes tags, related_skills), trigger, inputs, outputs | SKILL-SPEC.md | Certain |
| 12 | Pre-commit hooks for security scanning are a well-established pattern (pre-commit framework, husky + lint-staged) and should be included as a scenario | pre-commit.com docs; Husky (https://typicode.github.io/husky/) | Certain |
| 13 | Infrastructure-as-Code (IaC) scanning is a distinct subcategory: Terraform, CloudFormation, Kubernetes manifests can be scanned for misconfigurations by tools like Checkov, tfsec (now merged into Trivy), and KICS | Checkov (bridgecrew/checkov); Trivy IaC scanning; KICS (https://kics.io) | Certain |

---

## Proposed Skill Definitions

### Category: `devops`

All 8 proposed skills go under `skills/devops/` per SOP.md.

---

### Skill 1: `sast-scan`

**Directory**: `skills/devops/sast-scan/`

| Field | Value |
|-------|-------|
| name | sast-scan |
| description | Run Static Application Security Testing on source code to detect injection flaws, buffer overflows, and other code-level vulnerabilities before runtime |
| version | 1.0.0 |
| trigger | User asks to scan source code for security vulnerabilities; User mentions SAST, static analysis, code scanning, or Semgrep/Bandit/CodeQL; CI pipeline needs a static security scan step; User wants to find injection flaws, XSS patterns, or insecure deserialization in code |
| inputs | language (required: python, javascript, typescript, go, java, etc.), scan_path (required: path to scan), severity_threshold (optional: critical, high, medium, low), output_format (optional: sarif, json, markdown) |
| outputs | scan_results (findings with file, line, severity, rule ID), report_file (path to written report) |
| related_skills | dast-scan, sca-scan, secret-scan, vulnerability-triage, security-best-practices |

**Steps outline**:
1. Identify language(s) and select appropriate SAST tool(s)
2. Install/configure the SAST tool (Semgrep, Bandit for Python, CodeQL, etc.)
3. Run the scan with appropriate severity thresholds
4. Parse and normalize results (SARIF preferred)
5. Generate a prioritized findings report
6. Optionally integrate with CI/CD pipeline

**Pitfalls**:
- SAST tools have high false positive rates (30-70%); always triage before acting
- Language-specific tools required; no single SAST tool covers all languages well
- Some SAST tools require buildable code (e.g., CodeQL)
- Scanning large codebases can be slow; scope appropriately

---

### Skill 2: `dast-scan`

**Directory**: `skills/devops/dast-scan/`

| Field | Value |
|-------|-------|
| name | dast-scan |
| description | Run Dynamic Application Security Testing against a live or staging application to find runtime vulnerabilities like XSS, SQL Injection, and misconfigured headers |
| version | 1.0.0 |
| trigger | User asks to scan a running application for security vulnerabilities; User mentions DAST, dynamic scanning, OWASP ZAP, or Burp Suite; CI pipeline needs dynamic security testing; User wants to test authentication, session management, or input validation of a live endpoint |
| inputs | target_url (required: URL of the running application), scan_type (optional: baseline, full, api), auth_config (optional: auth mechanism for authenticated scans), output_format (optional: sarif, json, markdown) |
| outputs | scan_results (findings with URL, severity, evidence), report_file (path to written report) |
| related_skills | sast-scan, api-security-best-practices, vulnerability-triage |

**Steps outline**:
1. Verify target URL is accessible and determine scan scope
2. Select DAST tool (OWASP ZAP for web apps, Nuclei for API/URL-based scans)
3. Configure authentication if needed for deeper scans
4. Execute the scan (baseline or full)
5. Parse and deduplicate results
6. Generate prioritized findings report

**Pitfalls**:
- DAST requires a running instance; cannot scan source code alone
- Active scans can damage data in non-test environments
- Authenticated scanning needs careful credential management
- DAST finds runtime issues but misses code-level patterns that SAST catches

---

### Skill 3: `sca-scan`

**Directory**: `skills/devops/sca-scan/`

| Field | Value |
|-------|-------|
| name | sca-scan |
| description | Scan project dependencies for known vulnerabilities (CVEs) using Software Composition Analysis, identify outdated packages, and generate SBOMs |
| version | 1.0.0 |
| trigger | User asks to check dependencies for known vulnerabilities; User mentions SCA, dependency scanning, npm audit, pip audit, CVE, or SBOM; CI pipeline needs dependency vulnerability scanning; User wants to know if any third-party packages have security issues |
| inputs | scan_path (required: path to project), ecosystem (optional: python, node, go, java, rust), include_transitive (optional: default true), severity_threshold (optional), generate_sbom (optional: default false) |
| outputs | vulnerability_report (CVEs with severity, affected package, fixed version), sbom_file (if requested), remediation_plan (prioritized upgrade suggestions) |
| related_skills | sast-scan, vulnerability-triage, iac-security-scan |

**Steps outline**:
1. Identify package ecosystem from manifest files (package.json, requirements.txt, go.mod, etc.)
2. Select and run SCA tool (OWASP Dependency-Check, Trivy fs, npm audit, pip-audit, cargo audit)
3. Parse vulnerability results including transitive dependencies
4. Generate SBOM if requested (CycloneDX or SPDX format)
5. Produce remediation plan with prioritized upgrades
6. Optionally integrate with CI/CD pipeline

**Pitfalls**:
- Transitive dependencies often contain the real risk; always include them
- Vulnerability databases (NVD) have reporting lag; recently disclosed CVEs may not appear
- Some CVEs have no fix available; document these explicitly
- License compliance (not just security) is part of SCA; consider adding license scanning

---

### Skill 4: `secret-scan`

**Directory**: `skills/devops/secret-scan/`

| Field | Value |
|-------|-------|
| name | secret-scan |
| description | Detect hardcoded secrets, API keys, tokens, and credentials in source code and git history using pattern-matching and entropy analysis |
| version | 1.0.0 |
| trigger | User asks to scan for leaked secrets, API keys, or credentials; User mentions gitleaks, trufflehog, secret scanning, or credential detection; CI pipeline needs pre-commit or pre-push secret detection; User wants to audit git history for accidentally committed secrets |
| inputs | scan_path (required: path to repo), scan_depth (optional: full history or diff-only), custom_rules (optional: path to custom detection rules), output_format (optional: sarif, json, markdown) |
| outputs | findings (list of detected secrets with file, line, rule type), report_file (path to written report) |
| related_skills | sast-scan, ci-security-pipeline, security-best-practices |

**Steps outline**:
1. Install/configure secret scanning tool (Gitleaks recommended, Trufflehog as alternative)
2. Run scan against working directory and/or git history
3. Review findings for false positives (test fixtures, documented example keys, etc.)
4. Generate findings report with remediation guidance (rotate exposed secrets)
5. Set up pre-commit hook if requested for ongoing prevention
6. Document any secrets that need rotation

**Pitfalls**:
- Many findings in test fixtures or documentation are false positives
- Secret scanning cannot find secrets that have been rebased/squashed away; use git log --all --full-history for thorough scans
- Finding a secret means it should be rotated immediately, even if it was in a public repo briefly
- Entropy-based detection has high false positive rates; prefer pattern-based rules

---

### Skill 5: `iac-security-scan`

**Directory**: `skills/devops/iac-security-scan/`

| Field | Value |
|-------|-------|
| name | iac-security-scan |
| description | Scan Infrastructure-as-Code definitions (Terraform, CloudFormation, Kubernetes manifests, Dockerfiles) for misconfigurations, compliance violations, and security anti-patterns |
| version | 1.0.0 |
| trigger | User asks to scan Terraform, CloudFormation, Kubernetes, or Docker configs for security issues; User mentions IaC scanning, Checkov, tfsec, KICS, or infrastructure misconfiguration; CI pipeline needs IaC security scanning; User wants to check cloud resource definitions for compliance violations |
| inputs | scan_path (required: path to IaC files), iac_type (optional: terraform, cloudformation, kubernetes, dockerfile, all), severity_threshold (optional), compliance_framework (optional: cis, nist, pci-dss, hipaa) |
| outputs | findings (misconfigurations with severity, resource, and remediation), report_file (path to written report) |
| related_skills | sca-scan, vulnerability-triage, ci-security-pipeline |

**Steps outline**:
1. Identify IaC file types present in the project
2. Select and configure scanning tool (Checkov for multi-framework, Trivy config for Docker/K8s, KICS for broad coverage)
3. Run the scan against all IaC definitions
4. Parse results and map to compliance frameworks if specified
5. Generate prioritized remediation report
6. Optionally integrate with CI/CD pipeline

**Pitfalls**:
- IaC tools report against the resource definition, not the live cloud state; a passing scan doesn't mean the deployed state is secure
- Some misconfigurations are intentional (e.g., public S3 buckets for static hosting); document exceptions
- Multi-cloud IaC (Terraform for AWS + GCP) needs tool support for both providers
- Dockerfile scanning catches base image issues but not runtime configuration drift

---

### Skill 6: `vulnerability-triage`

**Directory**: `skills/devops/vulnerability-triage/`

| Field | Value |
|-------|-------|
| name | vulnerability-triage |
| description | Triage vulnerability scan results using CVSS severity, EPSS exploit probability, and business context to produce a prioritized remediation plan |
| version | 1.0.0 |
| trigger | User asks to triage vulnerability scan results or prioritize CVEs; User mentions CVSS, EPSS, vulnerability prioritization, or risk scoring; User has a scan report and needs to decide what to fix first; User wants to assess whether a vulnerability is actually exploitable in their context |
| inputs | scan_results (required: path to scan output in SARIF, JSON, or CSV), business_context (optional: data classification, regulatory requirements, exposure level), epss_enabled (optional: default true — look up EPSS scores) |
| outputs | triage_report (prioritized findings with CVSS, EPSS, business impact, and action recommendation), remediation_plan (ordered list of what to fix, defer, or accept) |
| related_skills | sast-scan, dast-scan, sca-scan, secret-scan, iac-security-scan |

**Steps outline**:
1. Parse scan results from standard formats (SARIF, JSON, CSV)
2. Normalize severity using CVSS v4.0 scores (fall back to CVSS v3.1 if v4.0 unavailable)
3. Enrich with EPSS scores for each CVE to estimate exploitation probability
4. Apply business context filters (internet-facing, privileged access, data sensitivity)
5. Calculate composite risk score (CVSS severity × EPSS probability × business impact)
6. Generate triaged remediation plan: Fix Now, Fix Soon, Defer, Accept Risk
7. Document accepted risks with justification

**Pitfalls**:
- CVSS scores are often inflated; EPSS provides better exploit likelihood context
- A Critical CVSS score with near-zero EPSS probability means low real-world risk
- Business impact cannot be fully automated; require human input for data classification and regulatory context
- Scan results from different tools may report the same CVE multiple times; deduplicate before triage

---

### Skill 7: `ci-security-pipeline`

**Directory**: `skills/devops/ci-security-pipeline/`

| Field | Value |
|-------|-------|
| name | ci-security-pipeline |
| description | Design and implement CI/CD security pipeline stages — pre-commit hooks, PR checks, and deployment gates — that chain SAST, DAST, SCA, secret scanning, and IaC scanning into automated workflows |
| version | 1.0.0 |
| trigger | User asks to set up security scanning in a CI/CD pipeline; User mentions DevSecOps, shift-left security, or security gates; User wants pre-commit or pre-push hooks for secret detection; User wants to integrate security scanning into GitHub Actions, GitLab CI, or similar |
| inputs | pipeline_platform (required: github-actions, gitlab-ci, jenkins, circleci), scan_types (optional: list of scan types to include), enforcement_level (optional: advisory, blocking), repo_path (required: path to the repo) |
| outputs | pipeline_config (CI/CD configuration files for security scanning), pre_commit_config (pre-commit hook configuration) |
| related_skills | sast-scan, dast-scan, sca-scan, secret-scan, iac-security-scan, github-actions-templates, deployment-procedures |

**Steps outline**:
1. Assess the repository's tech stack, languages, and deployment workflow
2. Select scan types appropriate for the stack (SAST for all, SCA for dependencies, secret scanning for all, DAST if web app, IaC if infrastructure)
3. Design the pipeline stages:
   - **Pre-commit**: Secret scanning (fast, local)
   - **PR/MR check**: SAST + SCA + IaC (automated, advisory or blocking)
   - **Pre-deployment gate**: Full scan suite including DAST (blocking for production)
   - **Scheduled**: Weekly full scans with updated vulnerability databases
4. Generate CI/CD configuration files for the target platform
5. Generate pre-commit hook configuration for local secret scanning
6. Configure SARIF output for GitHub Security tab integration (if applicable)
7. Set up failure thresholds (block on Critical/High, warn on Medium/Low)
8. Document the pipeline in a security-scanning.md file in the repo

**Pitfalls**:
- Pre-commit hooks that are too slow (SAST on every commit) will be bypassed by developers
- DAST requires a deployed environment; it cannot run in pre-commit or PR stages without a test deployment
- Vulnerability databases update daily; ensure the CI pipeline pulls fresh databases
- Blocking pipelines on all findings will cause alert fatigue; start advisory and tighten over time
- Ensure scan tools are pinned to specific versions in CI (supply chain risk)

---

### Skill 8: `security-risk-assessment`

**Directory**: `skills/devops/security-risk-assessment/`

| Field | Value |
|-------|-------|
| name | security-risk-assessment |
| description | Conduct a structured security risk assessment combining vulnerability data, threat modeling, business impact analysis, and compliance requirements into an executive risk report |
| version | 1.0.0 |
| trigger | User asks for a security risk assessment or risk report; User wants to evaluate business impact of vulnerabilities; User asks about regulatory compliance for security (PCI-DSS, HIPAA, SOC 2); User wants to combine vulnerability scan results with business context for prioritization |
| inputs | scan_reports (optional: paths to scan outputs), repo_path (optional: path to codebase for threat modeling), compliance_frameworks (optional: pci-dss, hipaa, soc2, iso27001), risk_tolerance (optional: conservative, moderate, aggressive) |
| outputs | risk_assessment_report (Markdown report with risk matrix, executive summary, and remediation roadmap), risk_register (structured risk data in JSON/CSV) |
| related_skills | vulnerability-triage, security-threat-model, security-best-practices, ci-security-pipeline |

**Steps outline**:
1. Collect all available scan results (SAST, DAST, SCA, secret, IaC)
2. Run or reference threat model for the system (use security-threat-model skill)
3. Apply vulnerability triage (use vulnerability-triage skill)
4. Evaluate business impact for each finding:
   - Data classification (public, internal, confidential, restricted)
   - Regulatory requirements (PCI-DSS, HIPAA, SOC 2, ISO 27001)
   - Blast radius (single service, multi-service, organization-wide)
   - Compensating controls already in place
5. Build a risk matrix (likelihood × impact) for executive communication
6. Create a remediation roadmap with timelines based on risk scores
7. Generate risk register for tracking
8. Write executive summary with key risk indicators

**Pitfalls**:
- Risk assessments without business context are just vulnerability lists; always connect findings to business impact
- Regulatory compliance requirements may elevate findings that would otherwise be low priority
- Threat modeling and vulnerability scanning are complementary; don't skip either
- Risk tolerance varies by organization; document assumptions about what is acceptable
- Executive reports should lead with business impact, not CVE counts

---

## Gap Analysis: Existing Skills vs. Proposed Skills

| Existing Skill | Category | Overlap | Proposed Skill | Key Difference |
|---------------|----------|---------|----------------|----------------|
| security-best-practices | software-dev | Low | sast-scan | security-best-practices is manual code review guidance; sast-scan runs automated tools |
| security-threat-model | software-dev | Moderate | security-risk-assessment | threat-model focuses on architectural analysis; risk-assessment combines scan data + business impact |
| security-ownership-map | software-dev | Low | vulnerability-triage | ownership-map is about code ownership; triage is about vulnerability prioritization |
| api-security-best-practices | software-dev | Low | dast-scan | api-security is design guidance; dast-scan runs automated dynamic testing |
| github-actions-templates | devops | Moderate | ci-security-pipeline | github-actions-templates includes a basic security scan step; ci-security-pipeline is a comprehensive multi-stage security pipeline design |

**Recommendation**: No existing skills should be removed. The proposed skills complement, not replace, existing ones. Cross-references should be added in `related_skills` frontmatter.

---

## Scenario Coverage Matrix

| Scenario | Skill(s) |
|----------|-----------|
| CI/CD pipeline integration | ci-security-pipeline (primary), all scan skills as stages |
| Pre-commit hooks | secret-scan (primary), ci-security-pipeline (configuration) |
| PR/MR security checks | sast-scan, sca-scan, iac-security-scan, ci-security-pipeline (orchestration) |
| Cloud infrastructure auditing | iac-security-scan |
| Dependency vulnerability management | sca-scan, vulnerability-triage |
| Runtime application testing | dast-scan |
| Source code vulnerability detection | sast-scan |
| Credential leak detection | secret-scan |
| Vulnerability prioritization and remediation planning | vulnerability-triage |
| Executive risk reporting | security-risk-assessment |
| Regulatory compliance assessment | security-risk-assessment |
| Supply chain security | sca-scan (dependencies), secret-scan (leaked tokens), ci-security-pipeline (pipeline integrity) |

---

## Key Risk Analysis Protocols

### CVSS v4.0 (Common Vulnerability Scoring System)
- **Source**: FIRST.org (https://www.first.org/cvss/)
- **Purpose**: Standardized vulnerability severity scoring
- **Metric groups**: Base (intrinsic qualities), Threat (exploit characteristics), Environmental (deployment context)
- **Score range**: 0.0–10.0 (None → Low → Medium → High → Critical)
- **Use in skills**: vulnerability-triage uses CVSS as the base severity input

### EPSS (Exploit Prediction Scoring System)
- **Source**: FIRST.org (https://www.first.org/epss/)
- **Purpose**: Estimate probability of vulnerability exploitation in the wild within 30 days
- **Data source**: Real-world threat intelligence (CVEs observed being exploited)
- **Score range**: 0.0–1.0 (probability)
- **Use in skills**: vulnerability-triage uses EPSS to deprioritize high-CVSS but low-exploit-probability findings

### NIST SP 800-30 Rev. 1 (Risk Assessment)
- **Purpose**: Structured approach to risk assessment for information systems
- **Key concepts**: Likelihood of occurrence, magnitude of impact, risk determination
- **Use in skills**: security-risk-assessment uses this framework for business impact evaluation

### FAIR (Factor Analysis of Information Risk)
- **Purpose**: Quantitative risk analysis framework
- **Key concepts**: Loss Event Frequency, Probable Loss Magnitude
- **Use in skills**: security-risk-assessment references FAIR for quantitative risk scoring

---

## Recommended Tool Stack (per skill)

| Skill | Primary Tool(s) | Alternatives |
|-------|----------------|--------------|
| sast-scan | Semgrep, Bandit (Python) | CodeQL, SonarQube, Checkmarx |
| dast-scan | OWASP ZAP, Nuclei | Burp Suite (commercial), Nikto |
| sca-scan | Trivy, OWASP Dependency-Check | Snyk, Grype, npm audit, pip-audit |
| secret-scan | Gitleaks | Trufflehog, detect-secrets, GitHub Secret Scanning |
| iac-security-scan | Checkov, Trivy (config) | tfsec (merged into Trivy), KICS, Terrascan |
| vulnerability-triage | NVD API, EPSS API, custom script | Grype (has built-in matching) |
| ci-security-pipeline | GitHub Actions, pre-commit framework | GitLab CI, Jenkins, CircleCI |
| security-risk-assessment | Custom template + NVD/EPSS APIs | OneTrust, RiskLens (commercial FAIR tools) |

---

## Implementation Priority

| Priority | Skill | Rationale |
|----------|-------|-----------|
| P0 (First) | sca-scan | Highest ROI — dependency vulnerabilities are the most common and easiest to fix |
| P0 (First) | secret-scan | Fastest to implement, highest immediate security value (credential leaks) |
| P0 (First) | vulnerability-triage | Required to make all other scan outputs actionable |
| P1 (Second) | ci-security-pipeline | Integrates P0 scans into automated workflows |
| P1 (Second) | sast-scan | Broader coverage but more false positives; needs triage |
| P1 (Second) | iac-security-scan | Critical for cloud-native deployments |
| P2 (Third) | dast-scan | Requires deployed application; highest setup cost |
| P2 (Third) | security-risk-assessment | Consumes output from all other skills; depends on mature scanning practices |

---

## Gaps and Unknowns

- **No standard for DAST automation in CI**: DAST requires a running instance; best practices for spinning up ephemeral test environments vary significantly by stack. The dast-scan skill will need template configurations for common setups.
- **EPSS data freshness**: EPSS scores are updated daily; CI pipelines must pull fresh data. Caching strategies need documentation.
- **CVSS v4.0 adoption**: As of mid-2025, many vulnerability databases still use CVSS v3.1. The vulnerability-triage skill should handle both and prefer v4.0 when available.
- **Compliance framework mapping**: IaC scanning tools (Checkov) support specific compliance benchmarks, but mapping scan results to specific regulatory requirements (PCI-DSS, HIPAA) requires manual interpretation. The security-risk-assessment skill should document this gap.
- **Tool licensing**: Several recommended tools (SonarQube, Checkmarx, Burp Suite) have commercial licensing. The skills should recommend open-source-first tools and document commercial alternatives as options.