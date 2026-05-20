---
name: cloudflare-deploy
description: Deploy applications and infrastructure to Cloudflare using MCP tools (primary) or Wrangler CLI (fallback). Covers Workers, Pages, KV, D1, R2, Queues, Vectorize, and AI Gateway.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
  - macos
trigger:
  - User asks to deploy to Cloudflare or set up Cloudflare infrastructure
  - User asks to create, update, or manage Cloudflare Workers, Pages, KV, D1, R2, Queues, Vectorize, or AI Gateway
  - User mentions Cloudflare Workers, Pages Functions, or edge deployment
  - User asks to configure Cloudflare routing, CORS, environment variables, or bindings
  - User wants to manage Cloudflare account resources via API
metadata:
  hermes:
    tags: [cloudflare, workers, pages, deployment, edge-computing, serverless, devops, mcp]
    related_skills: [kaleb-one-sites]
---

# Cloudflare Deploy

Deploy applications and manage infrastructure on the Cloudflare platform. This skill supports two paths for interacting with Cloudflare:

1. **MCP Tools (Primary)** — Use `mcp_cloudflare_api_search` and `mcp_cloudflare_api_execute` when available. These tools provide direct API access with pre-configured authentication. No additional setup required.

2. **Wrangler CLI (Fallback)** — Use `npx wrangler` when MCP tools are not available. Requires `CLOUDFLARE_API_TOKEN` or `wrangler login`.

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
- Proceed with **MCP path**

**If MCP tools are NOT available**:
- Proceed with **Wrangler CLI path** (`npx wrangler`)

### 2. Deploy a Worker

#### Wrangler CLI Path
```bash
npx wrangler init my-worker
cd my-worker
npx wrangler deploy
npx wrangler secret put MY_SECRET
```

### 3. Deploy a Pages project
```bash
npx wrangler pages deploy ./dist --project-name=my-site
npx wrangler pages project create my-site --production-branch=main
```

### 4. Create and use KV namespace
```bash
npx wrangler kv namespace create "my-kv-namespace"
npx wrangler kv key put --namespace-id=<NAMESPACE_ID> "my-key" "my-value"
npx wrangler kv key get --namespace-id=<NAMESPACE_ID> "my-key"
```

### 5. Create a D1 database
```bash
npx wrangler d1 create my-d1-db
npx wrangler d1 execute my-d1-db --command="SELECT * FROM users"
npx wrangler d1 execute my-d1-db --file=schema.sql
```

### 6. Create an R2 bucket
```bash
npx wrangler r2 bucket create my-bucket
npx wrangler r2 object put my-bucket/my-file.txt --file=./local-file.txt
```

### 7. Create a Queue
```bash
npx wrangler queues create my-queue
```

### 8. Create a Vectorize index
```bash
npx wrangler vectorize create my-vector-index --dimensions=768 --metric=cosine
```

## Pitfalls

- **CORS errors on Workers**: Add appropriate CORS headers to all Worker responses
- **Environment variables vs secrets**: Use `wrangler secret put` for sensitive values. Use `[vars]` in `wrangler.toml` for non-sensitive config
- **KV eventual consistency**: KV reads may be stale for up to 60 seconds globally. Use D1 for strongly consistent state
- **Worker script size limits**: Free plan Workers have a 1MB script size limit (10MB paid)
- **R2 bucket names must be globally unique**: Like S3, R2 bucket names share a global namespace
- **Wrangler version mismatch**: Always use `npx wrangler` to get the latest version
- **Missing bindings in Worker**: If a Worker references a binding not in `wrangler.toml`, it will fail at runtime with ReferenceError
- **Vectorize index dimensions**: Must match the output dimensions of the embedding model used

## Verification

1. **Verify authentication**: `npx wrangler whoami`
2. **Verify Worker**: `npx wrangler deployments list --name=my-worker`
3. **Check Worker responding**: `curl -s https://my-worker.<subdomain>.workers.dev | head -5`
4. **List KV namespaces**: `npx wrangler kv namespace list`