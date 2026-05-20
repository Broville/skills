---
name: github-actions-templates
description: Production-ready GitHub Actions workflow patterns for CI/CD — testing, Docker, K8s deploy, security scanning, and reusable workflows
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - Setting up CI/CD with GitHub Actions
  - Creating automated testing workflows
  - Building and pushing Docker images
  - Deploying from GitHub Actions
  - Running security scans in CI pipelines
metadata:
  hermes:
    tags: [github-actions, ci-cd, workflow, testing, docker, security]
    related_skills: [deployment-procedures, code-review-checklist]
---

# GitHub Actions Templates

## Security Note: Pin Action Versions

**Always pin GitHub Actions to a specific version tag or commit SHA.** Never use `@master` or `@main`.

```yaml
# INCORRECT — vulnerable to supply chain attacks
- uses: actions/checkout@master

# CORRECT — pinned to specific version
- uses: actions/checkout@v4

# MOST SECURE — pinned to commit SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a393fba485  # v4.1.1
```

## Pattern 1: Test Workflow

```yaml
name: Test
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    - run: npm ci
    - run: npm run lint
    - run: npm test
    - uses: codecov/codecov-action@v4
      with:
        files: ./coverage/lcov.info
        token: ${{ secrets.CODECOV_TOKEN }}
```

## Pattern 2: Build and Push Docker Image

```yaml
name: Build and Push
on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
    - uses: actions/checkout@v4
    - uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - uses: docker/metadata-action@v5
      id: meta
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
    - uses: docker/build-push-action@v6
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## Pattern 3: Security Scanning

```yaml
name: Security Scan
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@0.28.0
      with:
        scan-type: 'fs'
        scan-ref: '.'
    - run: npm audit --audit-level=high
      continue-on-error: true
```

## Steps to Create a New Workflow

1. Identify the workflow type — test, build, deploy, or scan
2. Create the YAML file in `.github/workflows/`
3. Pin all action versions — use specific `@vX` tags
4. Set required secrets in repo Settings > Secrets
5. Test on a feature branch first
6. Review security — check permissions and secret handling
7. Merge to main only after verifying on feature branch

## Pitfalls

1. **Using `@master` for actions** — Mutable tags can be changed. Always pin versions.
2. **Overly broad permissions** — Use `permissions:` block for minimum required access.
3. **Unpinned Docker image tags** — Use specific digests: `docker://alpine@sha256:abc...`
4. **Missing `CODECOV_TOKEN`** — Codecov v4+ requires a token.
5. **Not testing workflow changes** — Push to feature branch first.

## Verification

1. **Workflow syntax valid**: `actionlint .github/workflows/your-workflow.yml`
2. **All actions pinned**: `grep -r '@master\|@main' .github/workflows/` returns nothing
3. **Workflow runs**: `gh workflow run your-workflow.yml && gh run list --workflow=your-workflow.yml`