---
name: api-security-best-practices
description: OWASP-aligned API security patterns — authentication, input validation, rate limiting, CORS, security headers, and error handling
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Designing new API endpoints
  - Securing existing APIs
  - Implementing authentication and authorization
  - Protecting against API attacks (injection, DDoS)
  - Conducting API security reviews
  - Setting up rate limiting or CORS policies
related_skills:
  - code-review-checklist
  - systematic-debugging
  - postgresql
---

# API Security Best Practices

## Description

OWASP-aligned API security patterns for building secure APIs. Covers authentication, authorization, input validation, rate limiting, CORS, security headers, and error handling with concrete code examples. All patterns are provider-agnostic and applicable to any API framework.

## When to Use

- Designing new API endpoints
- Securing existing APIs
- Implementing authentication and authorization
- Protecting against injection, DDoS, and other API attacks
- Conducting API security reviews
- Setting up rate limiting or CORS policies

## 1. Authentication and Authorization

### Token-Based Authentication

```python
# Python example — JWT authentication
import jwt
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

JWT_SECRET = os.environ["JWT_SECRET"]  # 256-bit minimum
JWT_REFRESH_SECRET = os.environ["JWT_REFRESH_SECRET"]

def create_access_token(user_id: str, role: str) -> str:
    """Create short-lived access token (1 hour)."""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iss": "your-app",
        "aud": "your-app-users",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def authenticate_token(f):
    """Middleware to verify JWT tokens."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Access token required"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token, JWT_SECRET,
                algorithms=["HS256"],
                issuer="your-app",
                audience="your-app-users",
            )
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated
```

### Authorization — Verify Ownership

```python
# BAD: Only checks authentication
@app.delete("/api/posts/<post_id>")
@authenticate_token
def delete_post(post_id):
    db.posts.delete(id=post_id)
    return jsonify({"success": True})

# GOOD: Checks both authentication AND authorization
@app.delete("/api/posts/<post_id>")
@authenticate_token
def delete_post(post_id):
    post = db.posts.find_unique(where={"id": post_id})
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post.user_id != request.user["user_id"] and request.user["role"] != "admin":
        return jsonify({"error": "Not authorized to delete this post"}), 403

    db.posts.delete(where={"id": post_id})
    return jsonify({"success": True})
```

### Security Best Practices

- Use strong JWT secrets (256-bit minimum, stored in environment variables)
- Set short expiration times (1 hour for access tokens)
- Implement refresh tokens for long-lived sessions (stored in database, revocable)
- Use HTTPS for all API traffic
- Don't store sensitive data in JWT payloads (they're not encrypted)
- Validate token issuer and audience
- Implement token blacklisting for logout

## 2. Input Validation and Sanitization

### Never Trust User Input

```python
# BAD: SQL injection vulnerability
@app.get("/api/users/<user_id>")
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    result = db.execute(query)
    return jsonify(result)

# GOOD: Parameterized query + input validation
@app.get("/api/users/<user_id>")
def get_user(user_id):
    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Invalid user ID"}), 400

    result = db.execute(
        "SELECT id, email, name FROM users WHERE id = %s",
        [user_id]  # Parameterized — safe
    )
    if not result:
        return jsonify({"error": "User not found"}), 404
    return jsonify(result)
```

### Request Schema Validation

```python
from pydantic import BaseModel, EmailStr, field_validator

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a number")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain a special character")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        v = v.strip()  # Sanitize whitespace
        if len(v) < 2 or len(v) > 100:
            raise ValueError("Name must be 2-100 characters")
        return v
```

### Validation Checklist

- [ ] Validate all user inputs (type, range, format)
- [ ] Use parameterized queries or ORM — never string interpolation
- [ ] Sanitize HTML content (use allowlists, not blocklists)
- [ ] Validate file uploads (type, size, content)
- [ ] Use schema validation middleware for all endpoints

## 3. Rate Limiting and Throttling

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="redis://localhost:6379",
)

# Standard rate limit
@app.route("/api/")
@limiter.limit("100 per hour")
def api_root():
    pass

# Strict limit for authentication endpoints
@app.route("/api/auth/login", methods=["POST"])
@limiter.limit("5 per 15 minutes")
def login():
    pass

# Per-user limit for expensive operations
@app.route("/api/reports/generate", methods=["POST"])
@authenticate_token
@limiter.limit("10 per hour", key_func=lambda: request.user["user_id"])
def generate_report():
    pass
```

### Rate Limit Response Headers

Always include these headers in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640000000
Retry-After: 900
```

## 4. CORS Configuration

```python
from flask_cors import CORS

# GOOD: Explicit origin allowlist
CORS(app, origins=[
    "https://app.example.com",
    "https://admin.example.com",
], supports_credentials=True)

# BAD: Allow all origins
# CORS(app, origins="*")  # NEVER do this in production

# BAD: Allow all origins with credentials
# CORS(app, origins="*", supports_credentials=True)  # Browser blocks this anyway
```

### CORS Best Practices

- Use an explicit allowlist of trusted origins
- Never use `*` with `supports_credentials=True` (browsers block this)
- Restrict methods to only what each endpoint needs
- Restrict headers to only what's needed
- Set appropriate `max_age` to reduce preflight requests

## 5. Security Headers

```python
# Apply security headers to all responses
@app.after_request
def add_security_headers(response):
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Enable HSTS (1 year, include subdomains)
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains; preload"
    )

    # XSS protection
    response.headers["X-XSS-Protection"] = "0"  # Modern: disable legacy filter, use CSP

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:"
    )

    # Referrer policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response
```

## 6. Error Handling — Don't Leak Information

```python
# BAD: Exposes database details
@app.post("/api/users")
def create_user():
    try:
        user = db.users.create(data=request.json)
        return jsonify(user), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 500
        # Might leak: "Unique constraint failed on the fields: (email)"

# GOOD: Generic error message to client, full error in logs
import logging
logger = logging.getLogger(__name__)

@app.post("/api/users")
def create_user():
    try:
        user = db.users.create(data=request.json)
        return jsonify(user), 201
    except Exception as error:
        logger.error("User creation error: %s", error, exc_info=True)

        # Map known errors to safe responses
        if "unique constraint" in str(error).lower():
            return jsonify({"error": "Email already exists"}), 400

        return jsonify({"error": "An error occurred while creating user"}), 500
```

### Error Handling Rules

- Log full errors server-side (with context)
- Return generic error messages to clients
- Map known error types to appropriate HTTP status codes
- Never expose stack traces, database details, or internal paths
- Include a correlation ID for troubleshooting

## 7. OWASP API Security Top 10

1. **Broken Object Level Authorization** — Always verify user can access resource
2. **Broken Authentication** — Implement strong authentication mechanisms
3. **Broken Object Property Level Authorization** — Validate which properties user can access
4. **Unrestricted Resource Consumption** — Implement rate limiting and quotas
5. **Broken Function Level Authorization** — Verify user role for each function
6. **Unrestricted Access to Sensitive Business Flows** — Protect critical workflows
7. **Server Side Request Forgery (SSRF)** — Validate and sanitize URLs
8. **Security Misconfiguration** — Use security headers and best practices
9. **Improper Inventory Management** — Document and secure all API endpoints
10. **Unsafe Consumption of APIs** — Validate data from third-party APIs

## Pitfalls

1. **Hardcoding secrets** — Never put API keys, JWT secrets, or database credentials in source code. Use environment variables or secret managers.
   ```python
   # BAD
   JWT_SECRET = "my-secret-key"
   # GOOD
   JWT_SECRET = os.environ["JWT_SECRET"]
   if not JWT_SECRET:
       raise RuntimeError("JWT_SECRET environment variable is required")
   ```

2. **Using `*` for CORS origins** — In production, always specify exact origins. `Access-Control-Allow-Origin: *` with credentials is blocked by browsers anyway, and without credentials it still allows any site to call your API.

3. **Missing authorization checks** — Authentication (who are you?) is not authorization (what can you do?). Every protected endpoint needs both. Check ownership or role for every resource access.

4. **Verbose error messages** — Returning stack traces or database error details to clients gives attackers useful information. Log full errors server-side, return generic messages to clients.

5. **No rate limiting on auth endpoints** — Login endpoints without rate limiting are vulnerable to brute force attacks. Apply strict limits (5-10 attempts per 15 minutes per IP).

## Verification

1. **No hardcoded secrets in codebase:**
   ```bash
   grep -rn "SECRET\|API_KEY\|PASSWORD\|TOKEN" --include="*.py" --include="*.js" --include="*.ts" src/
   # Should only find environment variable references
   ```
2. **All endpoints have authentication:**
   ```bash
   # Verify each route has auth middleware
   grep -n "@authenticate" src/routes.py  # or equivalent
   ```
3. **Rate limiting configured:**
   ```bash
   # Test rate limit response
   curl -s -o /dev/null -w "%{http_code}" -X POST https://api.example.com/api/auth/login
   # After exceeding limit, should return 429
   ```
4. **Security headers present:**
   ```bash
   curl -sI https://api.example.com/ | grep -i "x-frame\|x-content-type\|strict-transport"
   # Should show all three headers
   ```