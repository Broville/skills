---
name: security-threat-model
description: Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concise Markdown threat model report.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to threat-model a repository or codebase
  - User asks to enumerate threats, abuse paths, or attack surface
  - User asks for AppSec threat modeling or security architecture analysis
  - User mentions STRIDE, trust boundaries, or threat modeling
  - User asks to analyze security risks in a system design
inputs:
  - name: repo_path
    description: Absolute path to the repository or directory to model
    required: true
  - name: scope_paths
    description: Specific subdirectories or files to include (comma-separated)
    required: false
  - name: deployment_context
    description: Known deployment details (internet-facing, internal, cloud provider)
    required: false
outputs:
  - name: report
    description: Markdown threat model file written to <repo-name>-threat-model.md
metadata:
  hermes:
    tags:
      - security
      - threat-modeling
      - appsec
      - trust-boundaries
      - attack-surface
    related_skills:
      - security-best-practices
      - security-ownership-map
---

# Security Threat Model

## Description

Deliver an actionable AppSec-grade threat model specific to a repository or project path. Anchor every architectural claim to evidence in the repo and keep assumptions explicit. Prioritize realistic attacker goals and concrete impacts over generic checklists. The output is a Markdown threat model report filed at `<repo-name>-threat-model.md`.

## Prerequisites

- Read access to the target repository or directory
- Ability to inspect source code, configuration files, and dependency manifests

## Steps

### 1. Scope and extract the system model

Identify primary components, data stores, and external integrations from the repository:

```bash
# Identify project type and main components
find /path/to/repo -maxdepth 2 -name "*.py" -o -name "*.js" -o -name "*.go" -o -name "*.rs" | head -30

# Check configuration and deployment files
find /path/to/repo -maxdepth 2 -name "Dockerfile" -o -name "docker-compose*" -o -name "*.yaml" -o -name "*.toml" | head -20

# Identify dependencies and frameworks
cat /path/to/repo/package.json /path/to/repo/requirements.txt /path/to/repo/go.mod 2>/dev/null | head -50
```

- Identify how the system runs (server, CLI, library, worker) and its entrypoints
- Separate runtime behavior from CI/build/dev tooling and from tests/examples
- Map in-scope locations to components and explicitly exclude out-of-scope items
- Do not claim components, flows, or controls without evidence

### 2. Derive boundaries, assets, and entry points

**Trust boundaries** — Enumerate as concrete edges between components, noting for each:
- Protocol (HTTP, gRPC,IPC, file system)
- Authentication mechanism
- Encryption in transit
- Input validation
- Rate limiting

**Assets** — List what drives risk:
- Data stores (databases, file stores, caches)
- Credentials and secrets
- Configuration and feature flags
- Compute resources
- Audit logs
- User-generated content

**Entry points** — Identify all surfaces where untrusted input enters:
- HTTP endpoints and API routes
- File upload surfaces
- Parsers and decoders
- Job triggers and webhooks
- Admin tooling and management ports
- Logging and error sinks

### 3. Calibrate assets and attacker capabilities

For each asset, describe:
- What value it provides an attacker (exfiltration, modification, availability)
- Who has access (authenticated users, admins, public, internal services)

For attacker capabilities:
- Describe realistic capabilities based on exposure and deployment context
- Explicitly note non-capabilities to avoid inflated severity
- Example: "An attacker can reach the API but cannot access the internal management network"

### 4. Enumerate threats as abuse paths

For each trust boundary and asset pair, consider attacker goals:
- Exfiltration of sensitive data
- Privilege escalation
- Integrity compromise (data modification, code injection)
- Denial of service
- Lateral movement

For each threat:
- Classify the threat type (spoofing, tampering, repudiation, info disclosure, DoS, elevation of privilege)
- Tie it to impacted assets and boundaries
- Keep the number of threats small but high quality — prefer depth over breadth

### 5. Prioritize with explicit likelihood and impact reasoning

Use qualitative ratings with short justifications:

| Rating | Likelihood | Impact |
|--------|-----------|--------|
| Critical | Exploitable with minimal effort | Catastrophic data loss, auth bypass, RCE |
| High | Exploitable with some effort | Significant data exposure, partial system compromise |
| Medium | Requires specific conditions | Limited data exposure, targeted DoS |
| Low | Requires unlikely preconditions | Minor info leak, noisy DoS with easy mitigation |

Set overall priority by combining likelihood × impact, adjusted for existing controls. State which assumptions most influence the ranking.

### 6. Validate service context and assumptions with the user

Present the key assumptions that materially affect threat ranking or scope, then ask the user 1–3 targeted questions to resolve missing context:

- Service owner and operating environment
- Scale and user population
- Deployment model (internet-facing, internal, cloud, on-prem)
- Authentication and authorization mechanisms
- Data sensitivity classification
- Multi-tenancy and isolation requirements

**Pause and wait for user feedback before producing the final report.** If the user declines or cannot answer, state which assumptions remain and how they influence priority.

### 7. Recommend mitigations and focus paths

For each threat:
- Distinguish **existing mitigations** (with evidence from the codebase) from **recommended mitigations**
- Tie mitigations to concrete locations (component, boundary, or entry point)
- Prefer specific implementation hints over generic advice
  - Good: "Enforce schema validation at the API gateway for upload payloads"
  - Vague: "Validate inputs"
- Base recommendations on validated user context; if assumptions remain unresolved, mark recommendations as conditional

Control types to consider:
- Authorization checks (RBAC, ABAC)
- Input validation and schema enforcement
- Sandboxing and isolation
- Rate limiting
- Secrets isolation (vault, env injection)
- Audit logging and monitoring

### 8. Run a quality check and write the report

Before finalizing, verify:
- All discovered entrypoints are covered
- Each trust boundary is represented in threats
- Runtime vs. CI/dev separation is clear
- User clarifications (or explicit non-responses) are reflected
- Assumptions and open questions are explicit
- Format matches the output template in `references/prompt-template.md`

Write the final Markdown to `<repo-name>-threat-model.md` (using the basename of the repo root, or the in-scope directory if modeling a subpath).

## Report Structure

The threat model report should follow this structure:

```markdown
# <System Name> Threat Model

## System Overview
[2-3 sentences describing the system, its purpose, and deployment context]

## Trust Boundaries
[Numbered list of boundaries with protocol, auth, and details]

## Assets
[Numbered list of risk-driving assets with sensitivity classification]

## Entry Points
[Numbered list of attack surfaces with reachability]

## Threats
[Numbered threats with: ID, boundary, asset, type, attacker goal, priority, description]

## Mitigations
[Existing mitigations with evidence, recommended mitigations with implementation hints]

## Assumptions
[Explicit list of assumptions made, marked confirmed/unconfirmed]

## Open Questions
[Unresolved items that affect threat ranking]
```

## Pitfalls

- **Generic checklists instead of grounded threats**: Every threat must reference a specific component, boundary, or code path from the repository. Do not list threats that cannot be supported by evidence in the codebase.
- **Inflated severity**: Do not assume attackers can reach internal services if the code only exposes a public API. Always calibrate capabilities based on actual deployment context.
- **Skipping user validation**: The most impactful assumptions (deployment model, auth requirements, data sensitivity) must be confirmed with the user before finalizing. Unconfirmed assumptions should be explicitly marked.
- **Confusing CI/dev with production**: Build tooling, test code, and development scripts have different threat profiles than production code. Keep them separate in the model.

## Verification

1. **Report file exists and follows the structure**:
   ```bash
   test -f *-threat-model.md && echo "Report exists" || echo "No report found"
   grep -c "^## " *-threat-model.md
   # Expected: at least 4 section headers (System Overview, Trust Boundaries, Assets, Threats)
   ```

2. **Threats reference actual code**: Spot-check 2-3 threats. Confirm the referenced files or components exist in the repository.

3. **Assumptions are explicit**:
   ```bash
   grep -c "^- " *-threat-model.md | head -1
   # Expected: multiple explicit assumptions listed
   ```

4. **User confirmation was requested**: The workflow must pause at step 6 for user input. If this step was skipped, the threat model is incomplete.

## Cross-References

- **security-best-practices** (`software-dev/security-best-practices`) — Apply language-specific security guidance to findings
- **security-ownership-map** (`software-dev/security-ownership-map`) — Use ownership data to identify who maintains critical security code