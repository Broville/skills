# Security Controls and Assets Reference

This document provides a reference list of common security controls and asset categories to consult when performing threat modeling.

## Control Types

- **Authentication (AuthN)**: Verifying identity (passwords, MFA, certificates, tokens)
- **Authorization (AuthZ)**: Enforcing access rules (RBAC, ABAC, ACLs, policy engines)
- **Input Validation**: Checking data at trust boundaries (schema validation, type checking, allowlists)
- **Output Encoding**: Preventing injection in output (HTML escaping, JSON serialization, parameterized queries)
- **Encryption at Rest**: Protecting stored data (AES-256, envelope encryption, KMS)
- **Encryption in Transit**: Protecting data in motion (TLS, mTLS, WireGuard)
- **Rate Limiting**: Controlling request frequency (per-user, per-IP, per-endpoint)
- **Audit Logging**: Recording security-relevant events (access, changes, errors)
- **Sandboxing**: Isolating untrusted code (containers, VMs, seccomp, chroot)
- **Secrets Management**: Storing credentials securely (vault, env injection, secret mounts)

## Asset Categories

- **Data Stores**: Databases, caches, file stores, object storage
- **Credentials**: API keys, tokens, certificates, passwords
- **Configuration**: Feature flags, environment variables, deployment configs
- **Compute Resources**: Servers, containers, serverless functions, job runners
- **Audit Logs**: Access logs, change logs, error logs
- **User Content**: Uploads, posts, messages, generated content
- **Models and Algorithms**: ML models, rule engines, scoring systems

## Risk Categories

| Priority | Examples |
|----------|---------|
| Critical | Pre-auth RCE, auth bypass, cross-tenant access, sensitive data exfiltration, key/token theft |
| High | Authenticated RCE, privilege escalation, targeted data exposure, DoS of critical component |
| Medium | Targeted DoS with workaround, partial data exposure, rate-limit bypass with measurable impact |
| Low | Low-sensitivity info leak, noisy DoS with easy mitigation, issues requiring unlikely preconditions |