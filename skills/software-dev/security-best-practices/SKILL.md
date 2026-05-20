---
name: security-best-practices
description: Perform language and framework-specific security best-practice reviews, detect vulnerabilities, and write secure-by-default code for Python, JavaScript/TypeScript, and Go projects.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to review code for security vulnerabilities or weaknesses
  - User asks to check for security issues in existing code
  - User asks to write secure code or apply security best practices
  - User requests a security report or vulnerability audit
  - User mentions OWASP, injection, XSS, CSRF, auth bypass, or similar security terms
inputs:
  - name: language
    description: Primary programming language of the project (python, javascript/typescript, go)
    required: false
  - name: framework
    description: Web framework in use (e.g., flask, django, express, fastapi, gin)
    required: false
  - name: scope
    description: File paths or directories to review (defaults to the whole project)
    required: false
  - name: report_path
    description: Where to write the security report (defaults to security_best_practices_report.md)
    required: false
outputs:
  - name: report
    description: Markdown security report with findings ranked by severity
  - name: fixes
    description: Code changes that address identified vulnerabilities
metadata:
  hermes:
    tags:
      - security
      - code-review
      - vulnerability
      - owasp
      - python
      - javascript
      - go
    related_skills:
      - security-threat-model
      - security-ownership-map
---

# Security Best Practices

## Description

Identify language and framework-specific security vulnerabilities in code and apply secure-by-default patterns. This skill operates in three modes: passive detection while writing code, active review on request, and full security report generation. It covers Python, JavaScript/TypeScript, and Go with framework-specific guidance.

## Prerequisites

- Access to the project source code being reviewed
- Ability to read and modify files in the project (for fix mode)
- Reference docs in `references/` should be consulted for the relevant language/framework combination

## Steps

### 1. Identify languages and frameworks

Inspect the project to determine all languages and frameworks in use. Check for:

- Package manifests: `requirements.txt`, `pyproject.toml`, `package.json`, `go.mod`
- Framework indicators: imports in entry files, middleware patterns, route definitions
- Both frontend and backend stacks for web applications

If the framework is unclear, examine the project structure and report your evidence.

### 2. Load security reference documentation

Check `references/` for language and framework-specific security guidance. File naming convention: `<language>-<framework>-<stack>-security.md`. Also check for `<language>-general-<stack>-security.md` for framework-agnostic guidance.

For web applications with both frontend and backend, load reference docs for both stacks.

If no matching reference exists in `references/`, apply well-known security best practices for the identified language and framework. State explicitly that concrete guidance was not available for the specific combination.

### 3. Operate in the appropriate mode

**Mode A — Secure-by-default coding (passive)**

When writing new code, apply security best practices proactively:
- Use parameterized queries, never string interpolation for SQL
- Validate and sanitize all user input
- Use secure defaults for authentication, session management, and CORS
- Avoid known anti-patterns for the language/framework

**Mode B — Passive vulnerability detection**

While working on the project, flag critical or high-impact vulnerabilities:
- Injected SQL or command execution
- Missing authentication on sensitive endpoints
- Hardcoded credentials or secrets
- Insecure deserialization
- Path traversal or file inclusion vulnerabilities

Notify the user and offer to fix critical findings immediately.

**Mode C — Full security report**

When the user requests a security review or report:

1. Scan the codebase for security anti-patterns matching the loaded reference guidance
2. Document each finding with:
   - Numeric ID for reference (e.g., SBP-01, SBP-02)
   - Severity (Critical / High / Medium / Low)
   - File path and line number(s)
   - One-sentence impact statement for Critical and High findings
   - Recommended fix
3. Write the report to the specified path (default: `security_best_practices_report.md`)
4. Organize findings by severity, Critical first
5. After writing the report, summarize findings to the user and offer to begin fixes

### 4. Check for project-specific overrides

Some projects intentionally deviate from security best practices for valid reasons. Before flagging a finding, check:
- Project documentation and README for stated exceptions
- Code comments explaining intentional bypasses
- Configuration files with documented security decisions

When a best practice is intentionally overridden, note it but do not argue. Suggest documenting the override reason if not already present.

### 5. Apply fixes (when requested)

Fix one finding at a time. For each fix:
- Add concise comments explaining the security rationale
- Consider whether the fix might break existing functionality
- Run any existing test suites before and after the change
- Commit with a message referencing the finding ID (e.g., `fix(SBP-03): parameterize SQL queries`)

## General Security Advice

These rules apply across all languages:

### Avoid incrementing IDs for public resources

Use UUID4 or random hex strings for public-facing resource identifiers. Auto-incrementing IDs leak resource counts and enable enumeration attacks.

### TLS considerations

- Do not flag missing TLS in development environments
- Do not recommend HSTS without understanding the lasting impact (it can cause outages and user lockout)
- Set secure cookies only when the application runs over TLS; use an environment flag to toggle this in dev vs. production

### Input validation

- Validate all input at trust boundaries (API endpoints, form handlers, CLI arguments)
- Use allowlists over denylists where possible
- Enforce schema validation on structured input (JSON, XML, form data)

## Pitfalls

- **Over-reporting in dev environments**: TLS, secure cookies, and strict CORS are often intentionally disabled in local development. Do not flag these as vulnerabilities without confirming the environment is production.
- **Breaking existing functionality**: Security fixes that change authentication flow, session handling, or input validation may regress features. Always test fixes against existing behavior.
- **Framework-specific defaults differ**: A secure default in Django (CSRF tokens) may not exist in Flask. Always check the specific framework's defaults rather than assuming.
- **Secrets in version control**: Scanning only source files misses secrets in config files, `.env` files, Docker Compose files, and CI/CD pipelines. Check these locations too.

## Verification

1. **Report file exists and is non-empty**:
   ```bash
   test -s security_best_practices_report.md && echo "Report created" || echo "No report found"
   ```

2. **Findings reference actual code**: Spot-check 2-3 findings. Confirm the cited file paths exist and the referenced line numbers contain the described vulnerability.

3. **Severity ordering**: Confirm the report lists Critical findings before High, High before Medium, Medium before Low.

4. **Fixes compile/pass tests**: If fixes were applied, run the project's test suite:
   ```bash
   # Python
   python -m pytest
   # Node
   npm test
   # Go
   go test ./...
   ```

## Cross-References

- **security-threat-model** (`software-dev/security-threat-model`) — For systematic threat modeling of a repository's attack surface
- **security-ownership-map** (`software-dev/security-ownership-map`) — For identifying code ownership and bus factor risk in security-sensitive areas