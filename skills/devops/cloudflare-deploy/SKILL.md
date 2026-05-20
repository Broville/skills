---
name: cloudflare-deploy
description: Deploy applications and infrastructure to Cloudflare using MCP tools (primary) or Wrangler CLI (fallback). Covers Workers, Pages, KV, D1, R2, Queues, Vectorize, and AI Gateway.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to deploy to Cloudflare or set up Cloudflare infrastructure
  - User asks to create, update, or manage Cloudflare Workers, Pages, KV, D1, R2, Queues, Vectorize, or AI Gateway
  - User mentions Cloudflare Workers, Pages Functions, or edge deployment
  - User asks to configure Cloudflare routing, CORS, environment variables, or bindings
  - User wants to manage Cloudflare account resources via API
inputs:
  - name: account_id
    description: Cloudflare account ID (pre-configured for MCP tools; required for Wrangler CLI)
    required: false
  - name: resource_type
    description: Type of Cloudflare resource (worker, page, kv, d1, r2, queue, vectorize, ai-gateway)
    required: true
  - name: action
    description: Action to perform (deploy, create, update, delete, list, get)
    required: true
outputs:
  - name: resource_id
    description: ID of the created or deployed resource
  - name: deploy_url
    description: URL where the deployed resource is accessible
metadata:
  hermes:
    tags:
      - cloudflare
      - workers
      - pages
      - deployment
      - edge-computing
      - serverless
      - devops
      - mcp
    related_skills:
      - pdf
---

# Cloudflare Deploy

Deploy applications and manage infrastructure on the Cloudflare platform. This skill supports two paths for interacting with Cloudflare:

1. **MCP Tools (Primary)** — Use `mcp_cloudflare_api_search` and `mcp_cloudflare_api_execute` when available. These tools provide direct API access with pre-configured authentication. No additional setup required.

2. **Wrangler CLI (Fallback)** — Use `npx wrangler` when MCP tools are not available. Requires `CLOUDFLARE_API_TOKEN` or `wrangler login`.

## Prerequisites

### Path 1: MCP Tools (Primary)

- MCP tools `mcp_cloudflare_api_search` and `mcp_cloudflare_api_execute` must be configured in your agent environment
- Account ID is pre-configured in the MCP tools and accessible directly

No additional installation or authentication steps are needed.

### Path 2: Wrangler CLI (Fallback)

```bash
# Install or use via npx
npx wrangler --version

# Authenticate (interactive)
npx wrangler login

# Or set API token for CI/CD
export CLOUDFLARE_API_TOKEN="your-api-token"
```

Verify authentication:
```bash
npx wrangler whoami
# Expected: account name, account ID displayed
```

## Quick Decision Tree

### "I need to run code"

- **Serverless functions at the edge** → Workers
- **Full-stack web app with Git deploys** → Pages
- **Stateful coordination/real-time** → Durable Objects
- **Scheduled tasks (cron)** → Cron Triggers on Workers

### "I need to store data"

- **Key-value store (config, sessions, cache)** → KV
- **Relational SQL (SQLite)** → D1
- **Object/file storage (S3-compatible)** → R2
- **Message queue (async processing)** → Queues
- **Vector embeddings (AI/semantic search)** → Vectorize

### "I need AI"

- **Run inference (LLMs, embeddings)** → Workers AI
- **Gateway for any AI provider** → AI Gateway

## Steps

### 1. Choose your interaction path

**If MCP tools are available** (check for `mcp_cloudflare_api_search` and `mcp_cloudflare_api_execute` in your tool list):
- Proceed with **MCP path** steps below

**If MCP tools are NOT available**:
- Proceed with **Wrangler CLI path** steps below

### 2. Deploy a Worker

#### MCP Path (Primary)

```python
# Search for the Workers deployment endpoint
result = mcp_cloudflare_api_search("Workers scripts deployment")

# Deploy a Worker script
mcp_cloudflare_api_execute({
    "method": "PUT",
    "path": f"/accounts/{account_id}/workers/scripts/my-worker",
    "body": "addEventListener('fetch', e => e.respondWith(new Response('Hello!')))",
    "contentType": "application/javascript"
})
```

The `account_id` is pre-configured in MCP tools and accessible directly — you do not need to look it up.

For Workers with bindings (KV, D1, R2, etc.), use multipart/form-data:

```python
import json, time

code = """
addEventListener('fetch', e => e.respondWith(
  MY_KV.get('key').then(v => new Response(v || 'none'))
));
"""
metadata = {
    "body_part": "script",
    "bindings": [{"type": "kv_namespace", "name": "MY_KV", "namespace_id": "your-kv-id"}]
}

boundary = f"--F{int(time.time())}"
body_parts = [
    f"--{boundary}", 'Content-Disposition: form-data; name="metadata"',
    "Content-Type: application/json", "", json.dumps(metadata),
    f"--{boundary}", 'Content-Disposition: form-data; name="script"',
    "Content-Type: application/javascript", "", code,
    f"--{boundary}--"
]
body = "\r\n".join(body_parts)

mcp_cloudflare_api_execute({
    "method": "PUT",
    "path": f"/accounts/{account_id}/workers/scripts/my-worker",
    "body": body,
    "contentType": f"multipart/form-data; boundary={boundary}",
    "rawBody": True
})
```

#### Wrangler CLI Path (Fallback)

```bash
# Create a new Worker project
npx wrangler init my-worker
cd my-worker

# Or deploy an existing Worker
npx wrangler deploy

# Set secrets (environment variables)
npx wrangler secret put MY_SECRET
```

### 3. Deploy a Pages project

#### MCP Path

```python
# Create a Pages project
mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/pages/projects",
    "body": {"name": "my-site", "production_branch": "main"}
})

# Deploy to Pages (requires multipart upload of static assets)
mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/pages/projects/my-site/deployments",
    # ... multipart body with asset files
})
```

#### Wrangler CLI Path

```bash
# Deploy a directory of static files
npx wrangler pages deploy ./dist --project-name=my-site

# Or connect to a Git repository for automatic deployments
npx wrangler pages project create my-site --production-branch=main
```

### 4. Create and use KV namespace

#### MCP Path

```python
# Create a KV namespace
result = mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/storage/kv/namespaces",
    "body": {"title": "my-kv-namespace"}
})
namespace_id = result["result"]["id"]

# Write a key-value pair
mcp_cloudflare_api_execute({
    "method": "PUT",
    "path": f"/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/my-key",
    "body": "my-value",
    "contentType": "text/plain"
})

# Read a key
mcp_cloudflare_api_execute({
    "method": "GET",
    "path": f"/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/my-key"
})
```

#### Wrangler CLI Path

```bash
# Create a KV namespace
npx wrangler kv namespace create "my-kv-namespace"

# Write a key-value pair
npx wrangler kv key put --namespace-id=<NAMESPACE_ID> "my-key" "my-value"

# Read a key
npx wrangler kv key get --namespace-id=<NAMESPACE_ID> "my-key"
```

### 5. Create a D1 database

#### MCP Path

```python
# Create a D1 database
result = mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/d1/database",
    "body": {"name": "my-d1-db"}
})
database_id = result["result"]["uuid"]

# Execute a query
mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/d1/database/{database_id}/query",
    "body": {"sql": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"}
})
```

#### Wrangler CLI Path

```bash
# Create a D1 database
npx wrangler d1 create my-d1-db

# Execute a query
npx wrangler d1 execute my-d1-db --command="SELECT * FROM users"

# Execute from a SQL file
npx wrangler d1 execute my-d1-db --file=schema.sql
```

### 6. Create an R2 bucket

#### MCP Path

```python
# Create an R2 bucket
mcp_cloudflare_api_execute({
    "method": "PUT",
    "path": f"/accounts/{account_id}/r2/buckets/my-bucket"
})

# Upload an object
mcp_cloudflare_api_execute({
    "method": "PUT",
    "path": f"/accounts/{account_id}/r2/buckets/my-bucket/objects/my-file.txt",
    "body": "file contents here",
    "contentType": "text/plain"
})
```

#### Wrangler CLI Path

```bash
# Create an R2 bucket
npx wrangler r2 bucket create my-bucket

# Upload an object
npx wrangler r2 object put my-bucket/my-file.txt --file=./local-file.txt
```

### 7. Create a Queue

#### MCP Path

```python
# Create a Queue
mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/queues",
    "body": {"name": "my-queue"}
})
```

#### Wrangler CLI Path

```bash
npx wrangler queues create my-queue
```

### 8. Create a Vectorize index

#### MCP Path

```python
# Create a Vectorize index
mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/vectorize/indexes",
    "body": {
        "name": "my-vector-index",
        "dimensions": 768,
        "metric": "cosine"
    }
})
```

#### Wrangler CLI Path

```bash
npx wrangler vectorize create my-vector-index --dimensions=768 --metric=cosine
```

### 9. Create an AI Gateway

#### MCP Path

```python
# Create an AI Gateway
mcp_cloudflare_api_execute({
    "method": "POST",
    "path": f"/accounts/{account_id}/ai-gateway/gateways",
    "body": {"name": "my-ai-gateway"}
})
```

#### Wrangler CLI Path

```bash
# AI Gateway is configured via dashboard or API (no dedicated wrangler subcommand yet)
# Use the API directly with curl or MCP tools
```

### 10. Discover API endpoints with MCP

When you need an endpoint not listed above, use the search tool to find it:

```python
# Search for any Cloudflare product endpoint
result = mcp_cloudflare_api_search({
    "code": """async () => {
        const results = [];
        for (const [path, methods] of Object.entries(spec.paths)) {
            if (path.includes('durable-objects')) {
                for (const [method, op] of Object.entries(methods)) {
                    results.push({ method: method.toUpperCase(), path, summary: op?.summary });
                }
            }
        }
        return results;
    }"""
})
```

## Pitfalls

- **CORS errors on Workers**: Add appropriate CORS headers to all Worker responses. Failure to do so causes browser requests to be blocked:
  ```javascript
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
  // Handle OPTIONS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }
  ```
- **Environment variables vs secrets**: Use `wrangler secret put` for sensitive values (API keys, tokens). Use `[vars]` in `wrangler.toml` for non-sensitive config. Secrets are encrypted at rest; vars are not.
- **KV eventual consistency**: KV reads may be stale for up to 60 seconds globally. Do not use KV for data that requires immediate consistency. Use D1 or Durable Objects for strongly consistent state.
- **Worker script size limits**: Free plan Workers have a 1MB script size limit (10MB paid). Large dependencies may need bundling with esbuild or webpack.
- **R2 bucket names must be globally unique**: Like S3, R2 bucket names share a global namespace across all accounts. Choose descriptive, prefixed names.
- **D1 is in beta**: D1 databases have size and throughput limits. Check current limits before using in production.
- **MCP multipart uploads**: When deploying Workers with bindings via MCP, the request must be `multipart/form-data` with a `metadata` JSON part and a `script` part. See Step 2 for the exact format.
- **Wrangler version mismatch**: Always use `npx wrangler` to get the latest version. Global installations may be outdated. Check with `npx wrangler --version`.
- **Missing bindings in Worker**: If a Worker references a binding (KV, D1, R2, etc.) that isn't declared in `wrangler.toml` or the MCP deployment metadata, it will fail at runtime with a ReferenceError.
- **Queue consumer configuration**: A Worker must be configured as a consumer for a Queue. The binding name in `wrangler.toml` must match the Worker code.
- **Vectorize index dimensions**: The `dimensions` parameter must match the output dimensions of the embedding model you use. Mismatched dimensions cause insert/query failures.

## Verification

### MCP Path Verification

1. **Verify Worker deployment**:
   ```python
   result = mcp_cloudflare_api_execute({
       "method": "GET",
       "path": f"/accounts/{account_id}/workers/scripts/my-worker"
   })
   # Expected: result.success == True
   ```

2. **Verify KV namespace**:
   ```python
   result = mcp_cloudflare_api_execute({
       "method": "GET",
       "path": f"/accounts/{account_id}/storage/kv/namespaces"
   })
   # Expected: Your namespace appears in the result list
   ```

3. **Check Worker is responding**:
   ```bash
   curl -s https://my-worker.<subdomain>.workers.dev | head -5
   # Expected: Your Worker's response body
   ```

### Wrangler CLI Verification

1. **Verify authentication**:
   ```bash
   npx wrangler whoami
   # Expected: Account name and ID displayed
   ```

2. **Verify Worker deployment**:
   ```bash
   npx wrangler deployments list --name=my-worker
   # Expected: At least one successful deployment listed
   ```

3. **Check Worker is responding**:
   ```bash
   curl -s https://my-worker.<subdomain>.workers.dev | head -5
   # Expected: Your Worker's response body
   ```

4. **List KV namespaces**:
   ```bash
   npx wrangler kv namespace list
   # Expected: Your namespace appears in the JSON output
   ```

## Cross-References

- **pdf** (`productivity/pdf`) — For generating deployment documentation or reports