---
name: sentry
description: Inspect Sentry issues and events, summarize production errors, and pull Sentry health data using the read-only Sentry CLI. Focus on understanding, not writing, production incidents.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks about production errors or error monitoring
  - User asks to inspect Sentry issues, events, or projects
  - User mentions Sentry, error tracking, or production incidents
  - User asks to summarize recent errors or health data from Sentry
  - User wants to understand what went wrong in production
inputs:
  - name: org
    description: Sentry organization slug (auto-detected from DSN or config if not specified)
    required: false
  - name: project
    description: Sentry project slug (auto-detected from DSN or config if not specified)
    required: false
  - name: time_range
    description: "Time window for queries (default: 24h)"
    required: false
  - name: environment
    description: "Environment filter (default: production)"
    required: false
  - name: query
    description: 'Sentry search query (e.g., "is:unresolved level:error")'
    required: false
outputs:
  - name: issue_list
    description: List of Sentry issues matching the query
  - name: issue_detail
    description: Detailed information about a specific issue
  - name: event_data
    description: Event details including stack trace context
metadata:
  hermes:
    tags:
      - sentry
      - monitoring
      - error-tracking
      - observability
      - production
    related_skills:
      - security-best-practices
---

# Sentry (Read-only Observability)

## Description

Query Sentry for production error data using the read-only `sentry` CLI. This skill focuses on understanding production incidents: listing issues, examining event details, and getting root-cause explanations. It does not write to Sentry or modify issue state. The Sentry CLI handles authentication, org/project detection, pagination, and retries automatically.

## Prerequisites

- Sentry CLI installed and authenticated

If the CLI is not installed:

```bash
# Install the Sentry CLI
curl https://cli.sentry.dev/install -fsS | bash

# Authenticate (interactive flow)
sentry auth login

# Verify authentication
sentry auth status
# Expected: "Authenticated as <user>" or token details displayed
```

Or set the `SENTRY_AUTH_TOKEN` environment variable for non-interactive auth. **Never paste the full token in chat.** Set it locally and confirm when ready.

The CLI auto-detects org/project from DSNs in `.env` files, source code, config defaults, and directory names. Only specify `<org>/<project>` if auto-detection fails or picks the wrong target.

## Steps

### 1. Verify Sentry CLI is available

```bash
sentry --version
# Expected: Sentry CLI version displayed

sentry auth status
# Expected: Authenticated status with org info
```

### 2. List issues (most recent first)

```bash
sentry issue list \
  --query "is:unresolved environment:production" \
  --period 24h \
  --limit 20 \
  --json --fields shortId,title,priority,level,status
```

If auto-detection doesn't resolve org/project:

```bash
sentry issue list {org}/{project} \
  --query "is:unresolved environment:production" \
  --period 24h \
  --limit 20 \
  --json
```

### 3. Get issue detail

```bash
sentry issue view {SHORT_ID} --json
# Example: sentry issue view PROJ-42F --json
```

Use the short ID format (e.g., `PROJ-123`), not the numeric ID.

### 4. Get issue events

```bash
sentry issue events {SHORT_ID} --limit 20 --json
```

### 5. Get event detail

```bash
sentry event view {org}/{project}/{event_id} --json
```

### 6. Root cause analysis (explain pattern)

When a user asks "what went wrong" or "why is this happening," use the explain pattern:

```bash
sentry issue explain {SHORT_ID}
```

Then synthesize the explanation with context from the codebase:
1. Get the issue details and recent events
2. Examine the stack trace for file paths and line numbers
3. Cross-reference with the project source code
4. Provide a structured explanation following the template:

```
**Issue**: {title} ({short_id})
**Impact**: {count} events in {time_range}, affecting {environment}
**Root Cause**: {synthesis of explain output + code analysis}
**Suggested Fix**: {concrete code change}
```

### 7. Fix planning (plan pattern)

When a user asks for help fixing a Sentry issue, use the plan pattern:

1. List the issue's events to see the pattern
2. View the most recent event for the full stack trace
3. Identify the relevant source files from the stack trace
4. Plan a minimal, targeted fix that addresses the root cause
5. Present the plan before making changes, including:
   - Which files need to change
   - What the change will do
   - Potential side effects
   - How to verify the fix

### 8. Discover API endpoints (fallback)

For endpoints not covered by dedicated CLI commands:

```bash
sentry schema issues
# Lists available API endpoints for the issues resource

sentry api /api/0/organizations/{org}/ --method GET
# Direct API access for unsupported queries
```

## Output Formatting Rules

- **Issue lists**: Show title, short_id, status, first_seen, last_seen, count, environments. Order by most recent.
- **Event details**: Include culprit, timestamp, environment, release, URL.
- **Explicit "no results"**: If a query returns nothing, state it clearly — don't leave the user wondering.
- **Redact PII**: Never print emails, IPs, or credentials in output.
- **Never echo auth tokens** in commands or output.

## Pitfalls

- **Auth token in chat**: Never ask the user to paste their Sentry auth token directly. Direct them to set `SENTRY_AUTH_TOKEN` as an environment variable or use `sentry auth login` interactively.
- **Wrong org/project**: The CLI auto-detects from DSNs and config. If it picks the wrong project, always specify `{org}/{project}` explicitly. Check with `sentry auth status` first.
- **Large result sets**: Default limit is 20. For broad queries, use `--limit` to bound output and `--fields` to select specific columns. Avoid dumping entire event payloads.
- **Rate limiting**: Sentry has API rate limits. If you hit `429` responses, narrow the time range with `--period` or reduce `--limit`.

## Verification

1. **CLI is installed and authenticated**:
   ```bash
   sentry auth status
   # Expected: Authenticated status displayed
   ```

2. **Issue list returns results**:
   ```bash
   sentry issue list --period 24h --limit 5 --json --fields shortId,title
   # Expected: JSON array of issue objects (may be empty if no issues)
   ```

3. **Issue detail is retrievable**:
   ```bash
   sentry issue view {SHORT_ID} --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title','No title'))"
   # Expected: Issue title printed
   ```

4. **Schema discovery works**:
   ```bash
   sentry schema issues
   # Expected: List of available API endpoints
   ```

## Cross-References

- **security-best-practices** (`software-dev/security-best-practices`) — For applying secure coding practices to fix the root cause of Sentry issues
- **security-threat-model** (`software-dev/security-threat-model`) — When production errors may indicate security vulnerabilities worth modeling