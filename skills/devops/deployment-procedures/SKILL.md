---
name: deployment-procedures
description: Platform-agnostic deployment framework — pre-deploy checks, deployment strategies, rollback, and verification principles
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - About to deploy code to any environment
  - Setting up deployment pipelines or processes
  - Planning rollback strategies
  - Recovering from a failed deployment
  - Creating deployment documentation
related_skills:
  - github-actions-templates
  - verification-before-completion
  - git-advanced-workflows
---

# Deployment Procedures

## Description

Deployment principles and decision-making for safe production releases. This skill teaches how to **think** about deployment, not how to memorize scripts. Every deployment is unique — understand the WHY behind each step.

## Platform Selection

### Decision Tree

```
What are you deploying?
│
├── Static site / JAMstack
│   └── Vercel, Netlify, Cloudflare Pages
│
├── Simple web app
│   ├── Managed → Railway, Render, Fly.io
│   └── Control → VPS + PM2/Docker
│
├── Microservices
│   └── Container orchestration
│
└── Serverless
    └── Edge functions, Lambda
```

### Platform Deployment Methods

| Platform | Deployment Method |
|----------|-------------------|
| **Vercel/Netlify** | Git push, auto-deploy |
| **Railway/Render** | Git push or CLI |
| **VPS + PM2** | SSH + manual steps |
| **Docker** | Image push + orchestration |
| **Kubernetes** | kubectl apply |

## Pre-Deployment Checklist

The 4 verification categories:

| Category | What to Check |
|----------|---------------|
| **Code Quality** | Tests passing, linting clean, reviewed |
| **Build** | Production build works, no warnings |
| **Environment** | Env vars set, secrets current |
| **Safety** | Backup done, rollback plan ready |

### Step 1: Verify Code Quality

```bash
# Run full test suite
npm test && echo "Tests pass"

# Run linter
npm run lint && echo "Lint clean"

# Check for any uncommitted changes
git status --porcelain
# Should return nothing
```

### Step 2: Verify Build

```bash
# Production build
npm run build && echo "Build succeeds"
```

### Step 3: Verify Environment

```bash
# Check required env vars are set (example)
for VAR in DATABASE_URL SECRET_KEY AWS_ACCESS_KEY_ID; do
  if [ -z "${!VAR}" ]; then
    echo "MISSING: $VAR"
    exit 1
  fi
done
echo "All env vars present"
```

### Step 4: Verify Safety

- [ ] Database migrations ready (if any)
- [ ] Rollback plan documented
- [ ] Team notified
- [ ] Monitoring dashboards open

## Deployment Workflow: The 5-Phase Process

```
1. PREPARE   → Verify code, build, env vars
2. BACKUP    → Save current state before changing
3. DEPLOY    → Execute with monitoring open
4. VERIFY    → Health check, logs, key flows
5. CONFIRM/ROLLBACK → All good? Confirm. Issues? Rollback.
```

### Phase Principles

| Phase | Principle |
|-------|-----------|
| **Prepare** | Never deploy untested code |
| **Backup** | Can't rollback without backup |
| **Deploy** | Watch it happen, don't walk away |
| **Verify** | Trust but verify |
| **Confirm** | Have rollback trigger ready |

## Post-Deployment Verification

### What to Verify

| Check | Why |
|-------|-----|
| **Health endpoint** | Service is running |
| **Error logs** | No new errors |
| **Key user flows** | Critical features work |
| **Performance** | Response times acceptable |

### Verification Window

- **First 5 minutes**: Active monitoring
- **15 minutes**: Confirm stable
- **1 hour**: Final verification
- **Next day**: Review metrics

```bash
# Check health endpoint
curl -s https://app.example.com/health | jq .

# Check for error logs (example for Docker)
docker logs --since 5m app-container 2>&1 | grep -i error

# Verify key endpoint responds
curl -s -o /dev/null -w "%{http_code}" https://app.example.com/api/status
# Should return 200
```

## Rollback Strategies

### When to Rollback

| Symptom | Action |
|---------|--------|
| Service down | Rollback immediately |
| Critical errors | Rollback |
| Performance >50% degraded | Consider rollback |
| Minor issues | Fix forward if quick |

### Rollback Strategy by Platform

| Platform | Rollback Method |
|----------|-----------------|
| **Vercel/Netlify** | Redeploy previous commit |
| **Railway/Render** | Rollback in dashboard |
| **VPS + PM2** | Restore backup, restart |
| **Docker** | Previous image tag |
| **K8s** | `kubectl rollout undo` |

### Rollback Principles

1. **Speed over perfection** — Rollback first, debug later
2. **Don't compound errors** — One rollback, not multiple changes
3. **Communicate** — Tell team what happened
4. **Post-mortem** — Understand why after stable

## Zero-Downtime Deployment Strategies

| Strategy | How It Works |
|----------|--------------|
| **Rolling** | Replace instances one by one |
| **Blue-Green** | Switch traffic between environments |
| **Canary** | Gradual traffic shift |

### Selection Principles

| Scenario | Strategy |
|----------|----------|
| Standard release | Rolling |
| High-risk change | Blue-green (easy rollback) |
| Need validation | Canary (test with real traffic) |

## Emergency Procedures

### Service Down Priority

1. **Assess** — What's the symptom?
2. **Quick fix** — Restart if unclear
3. **Rollback** — If restart doesn't help
4. **Investigate** — After stable

### Investigation Order

| Check | Common Issues |
|-------|---------------|
| **Logs** | Errors, exceptions |
| **Resources** | Disk full, memory |
| **Network** | DNS, firewall |
| **Dependencies** | Database, APIs |

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Deploy on Friday | Deploy early in the week |
| Rush deployment | Follow the process |
| Skip staging | Always test first |
| Deploy without backup | Backup before deploy |
| Walk away after deploy | Monitor for 15+ minutes |
| Multiple changes at once | One change at a time |

## Pitfalls

1. **Skipping pre-deploy checks because "it's a small change"** — Small changes cause big outages. Always verify.
2. **No rollback plan** — Without a tested rollback path, a failed deployment becomes an emergency. Test rollback before you need it.
3. **Deploying multiple changes simultaneously** — When something breaks, you can't isolate the cause. One change at a time.
4. **Walking away after deploying** — The first 5 minutes are critical. Monitor actively for errors and performance degradation.
5. **Compounding errors during rollback** — Don't make additional "fix" changes during rollback. Rollback to the known-good state first.

## Verification

1. **Pre-deployment: All checks green**
   ```bash
   npm test && npm run build && echo "Pre-deploy checks pass"
   ```
2. **Health endpoint responding:**
   ```bash
   curl -sf https://app.example.com/health && echo "Health check OK"
   ```
3. **No new errors in logs:**
   ```bash
   docker logs --since 5m app 2>&1 | grep -c ERROR
   # Should be 0 or baseline
   ```
4. **Rollback procedure tested:**
   ```bash
   # Verify you can access the previous version
   # Docker: previous image tag exists
   # K8s: kubectl rollout history deployment/my-app
   # PM2: pm2 list shows running processes
   ```