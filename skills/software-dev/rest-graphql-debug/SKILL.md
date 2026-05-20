---
name: rest-graphql-debug
description: Debug REST and GraphQL APIs through layered diagnosis — connectivity, timeouts, TLS, auth, request format, response parsing, and semantics. Isolate the failing layer before guessing at the fix.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - API returns unexpected status code or response body
  - Authentication failing (401/403) after token refresh
  - Works in one tool but fails in code
  - Need to debug webhook or callback integrations
  - Building or reviewing API integration tests
  - Rate limiting or pagination issues
related_skills:
  - systematic-debugging
  - verification-before-completion
  - concise-planning
---

# REST/GraphQL Debug

## Description

A methodology for debugging REST and GraphQL APIs by walking the chain in order: connectivity → timeouts → TLS → auth → request format → response parsing → semantics. Isolate the failing layer before guessing at the fix. A 200 OK can hide broken data. A 500 can mask a one-character auth typo. This skill ensures you never skip diagnostic steps.

Uses standard HTTP client patterns (`curl` via terminal, Python `requests` via scripting) — no external dependencies beyond what ships with a typical Linux environment.

## Prerequisites

- `curl` available on the system
- Python 3.x with `requests` library (for multi-step debugging flows)
- Access to the target API and any required authentication credentials

```bash
# Verify curl is available
curl --version

# Verify Python and requests
python3 -c "import requests; print(requests.__version__)"
```

## Steps

### Step 1: Connectivity Check

Verify the host is reachable at all.

```bash
# DNS resolution
nslookup api.example.com

# Basic connectivity
curl -v --connect-timeout 5 https://api.example.com/health
```

If DNS doesn't resolve or the connection times out: firewall, VPN, or proxy issue. Stop here and fix connectivity first.

### Step 2: Timeout Diagnosis

Distinguish *can't reach* from *reaches but slow*:

```bash
curl -w "dns:%{time_namelookup}s connect:%{time_connect}s tls:%{time_appconnect}s ttfb:%{time_starttransfer}s total:%{time_total}s\n" \
  -o /dev/null -s https://api.example.com/endpoint
```

- High `time_connect` → network/firewall issue
- High `time_starttransfer` with low `time_connect` → slow server

In Python, always use a tuple timeout to prevent hanging:

```python
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout
try:
    requests.get(url, timeout=(3.05, 30))
except ConnectTimeout:
    print("Cannot reach host — DNS, firewall, VPN")
except ReadTimeout:
    print("Connected but server is slow")
```

### Step 3: TLS/SSL Check

```bash
curl -vI https://api.example.com 2>&1 | grep -E "SSL|subject|expire|issuer"
```

Common failures: expired cert, self-signed, hostname mismatch, missing CA bundle. Use `-k` only for ad-hoc debugging, never in production code.

### Step 4: Authentication Check

```bash
# Check token validity
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $TOKEN" https://api.example.com/me
```

For JWT tokens, decode and check expiration:

```python
import json, base64, os
tok = os.environ["TOKEN"]
payload = tok.split(".")[1]
payload += "=" * (-len(payload) % 4)
print(json.dumps(json.loads(base64.urlsafe_b64decode(payload)), indent=2))
```

Checklist:
- Token expired? (check `exp` claim in JWT)
- Right scheme? Bearer vs Basic vs Token vs `X-Api-Key`
- Right environment? Staging key on prod is a classic mistake
- API key in header vs query param (`?api_key=…`)?

### Step 5: Request Format Validation

```bash
curl -v -X POST https://api.example.com/endpoint \
  -H 'Content-Type: application/json' \
  -d '{"key":"value"}' 2>&1
```

Content-Type / body mismatch is a common silent failure:

```python
# WRONG — data= sends form-encoded, header says JSON
requests.post(url, data='{"k":"v"}', headers={"Content-Type": "application/json"})

# RIGHT — json= auto-sets header AND serializes
requests.post(url, json={"k": "v"})

# WRONG — Accept says XML, code calls .json()
requests.get(url, headers={"Accept": "text/xml"})

# RIGHT — let requests build multipart with boundary
requests.post(url, files={"file": open("doc.pdf", "rb")})
```

Common issues: form-encoded vs JSON, missing required fields, wrong HTTP method, unencoded query params.

**GraphQL gotcha:** servers often return HTTP 200 even when the query failed. Always check the `errors` field:

```python
import requests
resp = requests.post(
    "https://api.example.com/graphql",
    json={"query": "{ user(id: 1) { name email } }"},
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
data = resp.json()
if data.get("errors"):
    for err in data["errors"]:
        print(f"GraphQL error: {err['message']} (path: {err.get('path')})")
```

### Step 6: Response Parsing

Always inspect content-type before calling `.json()`:

```python
import requests
resp = requests.post(url, json=payload, timeout=10)
print(f"status={resp.status_code}")
print(f"headers={dict(resp.headers)}")
ct = resp.headers.get("Content-Type", "")
if "application/json" in ct:
    print(resp.json())
else:
    print(f"unexpected content-type {ct!r}, body={resp.text[:500]!r}")
```

Common failures: HTML error page where JSON expected, empty body, wrong charset.

### Step 7: Semantic Validation

Parsed cleanly — but is the data correct?

- Does `"status": "active"` mean what your code thinks?
- ID in response matches the one requested?
- Timestamps in expected timezone?
- Pagination returning all results, or just page 1?

### Step 8: Report and Create Repro

Document the finding in a standard format:

```markdown
## Finding
Endpoint: POST /api/v1/users
Status:   422 Unprocessable Entity
Req ID:   req_abc123xyz

## Repro
curl -X POST https://api.example.com/api/v1/users \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <REDACTED>' \
  -d '{"name":"test"}'

## Root Cause
Missing required field `email`. Server validation rejects before processing.

## Fix
-d '{"name":"test","email":"test@example.com"}'
```

Always capture the provider's request ID for vendor support:

```python
request_id = (
    resp.headers.get("X-Request-Id")
    or resp.headers.get("X-Trace-Id")
    or resp.headers.get("CF-Ray")  # Cloudflare
)
```

## HTTP Status Playbook

- **401** — Credentials missing or invalid. Check header, token, scheme.
- **403** — Authenticated but not authorized. Check scopes, resource ownership, IP allowlist, CORS.
- **404** — Resource doesn't exist or URL is wrong. Check path, trailing slash, API version, base URL.
- **409** — State collision. Duplicate create, stale ETag, concurrent modification.
- **422** — Valid JSON, invalid data. Check field types, required vs optional, enum values.
- **429** — Rate limited. Check `Retry-After` and `X-RateLimit-*` headers. Use exponential backoff.
- **5xx** — Server-side. Capture correlation ID, backoff with jitter, alert on persistence.

## Security

- Never log full tokens. Redact: `Bearer <REDACTED>`
- Never hardcode tokens. Read from env: `os.environ["API_TOKEN"]`
- Rotate immediately if a token surfaces in logs, error messages, or git history
- API keys in query strings end up in server logs and browser history — use headers instead

```python
def redact_auth(headers: dict) -> dict:
    sensitive = {"authorization", "x-api-key", "cookie", "set-cookie"}
    return {k: ("<REDACTED>" if k.lower() in sensitive else v) for k, v in headers.items()}
```

## Pitfalls

1. **Skipping layers** — A 200 response doesn't mean the data is correct. A 500 might be a one-character auth typo. Walk the chain in order, never leap to conclusions.
2. **Forgetting tuple timeouts in Python `requests`** — `requests.get(url)` hangs forever with no default timeout. Always pass `timeout=(3.05, 30)`.
3. **GraphQL 200-with-errors** — GraphQL servers often return HTTP 200 even on query failure. Always check `data.get("errors")` regardless of status code.
4. **Content-Type / body mismatches** — `data=` sends form-encoded while `json=` auto-sets the header and serializes. Mixing these up causes silent 415/400 errors.
5. **Testing with admin accounts** — If it works with a pre-seeded admin but fails for new users, you're masking the cold-start experience. Test with a fresh account.
6. **Not capturing correlation IDs** — When reporting bugs to API providers, the request ID (`X-Request-Id`, `X-Trace-Id`, `CF-Ray`) is the fastest path to resolution.

## Verification

1. **Identified the failing layer** — at least one step produced a failed check
2. **Repro command works** — the `curl` repro in the report reproduces the issue
3. **Report saved with standard format:**
   ```bash
   ls .hermes/debug/api-*.md
   ```
4. **Auth token redacted** — no full tokens in the report
5. **Correlation ID captured** — report includes X-Request-Id or equivalent