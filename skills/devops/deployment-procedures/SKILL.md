---
name: deployment-procedures
description: Platform-agnostic deployment framework — pre-deploy checks, deployment strategies, rollback, and verification principles
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - About to deploy code to any environment
  - Setting up deployment pipelines or processes
  - Planning rollback strategies
  - Recovering from a failed deployment
metadata:
  hermes:
    tags: [deployment, devops, rollback, verification]
    related_skills: [github-actions-templates, verification-before-completion]
---

# Deployment Procedures

## Description

Deployment principles and decision-making for safe production releases. This skill teaches how to **think** about deployment, not memorize scripts.

## Platform Selection

| What | Where |
|------|-------|
| Static site / JAMstack | Vercel, Netlify, Cloudflare Pages |
| Simple web app | Railway, Render, Fly.io, VPS + PM2/Docker |
| Microservices | Container orchestration |
| Serverless | Edge functions, Lambda |

## Pre-Deployment Checklist

| Category | What to Check |
|----------|---------------|
| **Code Quality** | Tests passing, linting clean, reviewed |
| **Build** | Production build works, no warnings |
| **Environment** | Env vars set, secrets current |
| **Safety** | Backup done, rollback plan ready |

```bash
# Verify code quality
npm test && npm run lint && echo "Pre-deploy checks pass"

# Verify build
npm run build && echo "Build succeeds"

# Check env vars
for VAR in DATABASE_URL SECRET_KEY; do
  [ -z "${!VAR}" ] && echo "MISSING: $VAR" && exit 1
done
```

## The 5-Phase Process

```
1. PREPARE   → Verify code, build, env vars
2. BACKUP    → Save current state before changing
3. DEPLOY    → Execute with monitoring open
4. VERIFY    → Health check, logs, key flows
5. CONFIRM/ROLLBACK → All good? Confirm. Issues? Rollback.
```

## Post-Deployment Verification

- **First 5 minutes**: Active monitoring
- **15 minutes**: Confirm stable
- **1 hour**: Final verification

```bash
curl -s https://app.example.com/health | jq .
docker logs --since 5m app-container 2>&1 | grep -i error
curl -s -o /dev/null -w "%{http_code}" https://app.example.com/api/status
```

## Rollback Strategies

| Symptom | Action |
|---------|--------|
| Service down | Rollback immediately |
| Critical errors | Rollback |
| Performance >50% degraded | Consider rollback |
| Minor issues | Fix forward if quick |

| Platform | Rollback Method |
|----------|-----------------|
| Vercel/Netlify | Redeploy previous commit |
| Railway/Render | Rollback in dashboard |
| Docker | Previous image tag |
| K8s | `kubectl rollout undo` |

### Rollback Principles
1. **Speed over perfection** — Rollback first, debug later
2. **Don't compound errors** — One rollback, not multiple changes
3. **Communicate** — Tell team what happened
4. **Post-mortem** — Understand why after stable

## Pitfalls

1. **Skipping pre-deploy checks** — Small changes cause big outages. Always verify.
2. **No rollback plan** — Test rollback before you need it.
3. **Deploying multiple changes simultaneously** — One change at a time.
4. **Walking away after deploying** — Monitor for 15+ minutes.
5. **Compounding errors during rollback** — Don't make additional fixes during rollback.