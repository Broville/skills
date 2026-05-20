# Threat Model Output Template

Use this template when producing the final Markdown threat model report. Sections marked with ★ are required.

---

# <System Name> Threat Model ★

## System Overview ★

[2-3 sentences describing the system, its purpose, and deployment context]

## Trust Boundaries ★

1. **[Boundary Name]**: [Protocol] | Auth: [mechanism] | Encryption: [status] | Validation: [status]
   - From: [component] → To: [component]
   - Notes: [any relevant details]

## Assets ★

1. **[Asset Name]** (sensitivity: [low/medium/high])
   - Type: [data/credentials/config/compute/logs]
   - Location: [where in the system]
   - Access: [who can reach it]

## Entry Points ★

1. **[Entry Point Name]** (reachability: [public/internal/admin])
   - Type: [HTTP endpoint/file upload/parser/webhook/CLI]
   - Input: [what untrusted data enters here]
   - Validation: [what checks exist]

## Threats ★

| ID | Boundary | Asset | Type | Goal | Priority | Description |
|----|----------|-------|------|------|----------|-------------|
| TM-01 | ... | ... | ... | ... | Critical/High/Medium/Low | ... |

## Mitigations

### Existing (with evidence)

- [Mitigation description] — Evidence: [file:line or component reference]

### Recommended

- [Mitigation description] — Location: [boundary/entry point] | Type: [authZ/validation/sandboxing/rate-limit/audit]

## Assumptions ★

- [Confirmed]: [assumption confirmed by user]
- [Unconfirmed]: [assumption not yet validated]

## Open Questions ★

1. [Question that affects threat ranking or scope]