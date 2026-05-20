---
name: github-actions-templates
description: Production-ready GitHub Actions workflow patterns for CI/CD — testing, Docker, K8s deploy, security scanning, and reusable workflows
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Setting up CI/CD with GitHub Actions
  - Creating automated testing workflows
  - Building and pushing Docker images
  - Deploying to Kubernetes from GitHub Actions
  - Running security scans in CI pipelines
  - Creating reusable workflow templates
related_skills:
  - deployment-procedures
  - code-review-checklist
  - git-advanced-workflows
---

# GitHub Actions Templates

## Description

Production-ready GitHub Actions workflow patterns for continuous integration and deployment. All workflows pin actions to specific versions — never use `@master` or `@latest` for security reasons (see Security Note below).

## Security Note: Pin Action Versions

**Always pin GitHub Actions to a specific commit SHA or version tag.** Never use `@master` or `@main` — these mutable references can be changed by action maintainers or compromised to inject malicious code into your workflows.

```yaml
# INCORRECT — vulnerable to supply chain attacks
- uses: actions/checkout@master

# CORRECT — pinned to specific version
- uses: actions/checkout@v4

# MOST SECURE — pinned to specific commit SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a393fba485  # v4.1.1
```

For maximum security, pin to commit SHAs and verify the SHA matches the expected version tag. This prevents tag rotation attacks.

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

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Run tests
      run: npm test

    - name: Upload coverage
      uses: codecov/codecov-action@v4
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

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: Build and push
      uses: docker/build-push-action@v6
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## Pattern 3: Deploy to Kubernetes

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2

    - name: Update kubeconfig
      run: aws eks update-kubeconfig --name production-cluster --region us-west-2

    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/
        kubectl rollout status deployment/my-app -n production
        kubectl get services -n production

    - name: Verify deployment
      run: |
        kubectl get pods -n production
        kubectl describe deployment my-app -n production
```

## Pattern 4: Matrix Build

```yaml
name: Matrix Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest
```

## Pattern 5: Security Scanning

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 06:00 UTC

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@0.28.0
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'

    - name: Run npm audit
      run: npm audit --audit-level=high
      continue-on-error: true

    - name: Run CodeQL analysis
      uses: github/codeql-action/init@v3
      with:
        languages: javascript

    - name: Perform CodeQL analysis
      uses: github/codeql-action/analyze@v3
```

## Pattern 6: Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm ci
    - run: npm test
```

**Call the reusable workflow:**
```yaml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20.x'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Pattern 7: Deployment with Approval Gate

```yaml
name: Deploy to Production

on:
  push:
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com

    steps:
    - uses: actions/checkout@v4

    - name: Deploy application
      run: |
        echo "Deploying to production..."

    - name: Notify Slack
      if: success()
      uses: slackapi/slack-github-action@v1.27.0
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "Deployment to production completed successfully!"
          }
```

## Steps to Create a New Workflow

1. **Identify the workflow type** — test, build, deploy, or scan
2. **Create the YAML file** in `.github/workflows/` with an appropriate name
3. **Pin all action versions** — use specific `@vX` tags (or `@commit-sha` for maximum security), never `@master`
4. **Set required secrets** — configure in repository Settings > Secrets
5. **Test on a branch** — push to a feature branch and verify the workflow runs
6. **Review security** — check permissions, secret handling, and action versions
7. **Merge to main** — only after verifying on the feature branch

## Pitfalls

1. **Using `@master` or `@main` for actions** — Mutable tags can be changed to point to malicious code. Always pin to a specific version tag or commit SHA.
2. **Overly broad permissions** — Default `write` permissions on all scopes is dangerous. Use `permissions:` block to grant minimum required access.
3. **Unpinned Docker image tags** — Use specific image digests in Docker-based workflows: `docker://alpine@sha256:abc...` instead of `docker://alpine:latest`.
4. **Missing `CODECOV_TOKEN`** — Codecov v4+ requires a token. Set `CODECOV_TOKEN` secret in the repository.
5. **Not testing workflow changes** — Push workflow changes to a feature branch first and verify they work before merging.

## Verification

1. **Workflow syntax is valid:**
   ```bash
   # Install actionlint for local validation
   # https://github.com/rhysd/actionlint
   actionlint .github/workflows/your-workflow.yml
   ```
2. **All actions are pinned to versions:**
   ```bash
   grep -r '@master\|@main' .github/workflows/
   # Should return nothing
   ```
3. **Workflow runs successfully:**
   ```bash
   # Trigger manually if workflow_dispatch is configured
   gh workflow run your-workflow.yml
   # Check results
   gh run list --workflow=your-workflow.yml
   ```

## Cross-References

- **deployment-procedures** — Deployment strategies and rollback procedures
- **code-review-checklist** — Checklist for reviewing CI/CD configurations
- **git-advanced-workflows** — Branch management for deployment workflows