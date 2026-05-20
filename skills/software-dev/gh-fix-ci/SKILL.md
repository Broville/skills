---
name: gh-fix-ci
description: Inspect failing GitHub Actions PR checks, summarize failure context, draft a fix plan, and implement after approval.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
  - macos
trigger:
  - user says CI is failing
  - user asks to fix failing checks
  - user says a PR has red checks
  - user mentions build failure or test failure on a PR
inputs:
  - name: pr
    description: PR number or URL (optional; defaults to current branch PR)
    required: false
  - name: repo
    description: Path inside the repository (default: current directory)
    required: false
outputs:
  - name: fix_plan
    description: Summary of failures and proposed fix steps
  - name: changes_applied
    description: List of files modified to fix the failures
metadata:
  hermes:
    tags: [github, ci, actions, debugging, pr]
    related_skills:
      - gh-address-comments
      - yeet
---

# gh-fix-ci

## Description

Use this skill when CI checks are failing on a GitHub pull request. The agent authenticates with `gh`, inspects failing checks using the bundled Python script, summarizes the failure context, drafts a fix plan, and implements changes only after explicit user approval. External CI providers (e.g., Buildkite) are treated as out of scope — only the details URL is reported.

## Prerequisites

- **GitHub CLI (`gh`)** installed and authenticated. Verify with `gh auth status`. Ensure `repo` and `workflow` scopes are included.
- **Python 3** available on `PATH` for the inspection script.
- Current directory is inside a git repository with a PR (or the user provides a PR number/URL).

## Steps

### 1. Verify authentication

```shell
gh auth status
```

If unauthenticated, ask the user to run `gh auth login` (ensuring repo + workflow scopes) before proceeding.

### 2. Resolve the PR

If the user provided a PR number or URL, use it directly. Otherwise, resolve the PR for the current branch:

```shell
gh pr view --json number,url
```

If this fails, there is no open PR for the current branch. Ask the user for a PR number or suggest creating one with the `yeet` skill.

### 3. Inspect failing checks

Run the bundled inspection script to analyze failing GitHub Actions checks:

```shell
python3 skills/software-dev/gh-fix-ci/scripts/inspect_pr_checks.py --repo . --pr "<number-or-url>"
```

Add `--json` for machine-friendly output:

```shell
python3 skills/software-dev/gh-fix-ci/scripts/inspect_pr_checks.py --repo . --pr "<number-or-url>" --json
```

The script:
- Fetches all PR checks via `gh pr checks`
- Handles `gh` field drift by falling back to available fields
- For each failing check, extracts the GitHub Actions run ID and fetches logs
- Extracts a failure snippet from the log (the most relevant lines around the error)
- Exits non-zero when failures remain (usable in automation)

**Manual fallback** (if the script is unavailable):

```shell
gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow
```

If a field is rejected, rerun with the available fields reported by `gh`.

For each failing check, extract the run ID from `detailsUrl` and fetch logs:

```shell
gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha
gh run view <run_id> --log
```

If the run log says it is still in progress, fetch job logs directly:

```shell
gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs"
```

### 4. Scope non-GitHub Actions checks

If a check's `detailsUrl` is not a GitHub Actions run (e.g., Buildkite, CircleCI), label it as **external** and report only the URL. Do not attempt to integrate with external CI providers — this skill only handles GitHub Actions.

### 5. Summarize failures

Present the user with a concise summary of each failing check:

- **Check name** — e.g., `test-unit`
- **Run URL** — link to the GitHub Actions run
- **Failure snippet** — the most relevant log lines (use the `logSnippet` from the script output, or the last ~30 lines from manual `gh run view --log`)
- **Missing logs** — call out explicitly when logs are not available

Example summary format:

```
Check: test-unit
URL: https://github.com/org/repo/actions/runs/12345
Failure snippet:
  > AssertionError: expected 200 but got 404
  > at test_api.py:42
  > at runner.py:108

Check: lint
URL: https://github.com/org/repo/actions/runs/12346
Note: External provider (Buildkite) — see details URL
```

### 6. Create a fix plan

Draft a concise fix plan based on the failure analysis. Present the plan to the user and request explicit approval before making any changes. The plan should include:

- Root cause for each failure
- Files to modify
- Specific changes to make
- Whether to add or update tests

**Do not implement changes without explicit user approval.**

### 7. Implement after approval

Once the user approves the plan:

1. Make the identified changes in the relevant files.
2. Run relevant tests locally to verify the fix (if the project has a test command).
3. Summarize the diffs for the user.
4. Ask whether to push the changes and open/update the PR (use `yeet` skill).

### 8. Recheck CI status

After pushing changes, monitor CI:

```shell
gh pr checks
```

If all checks pass, report success. If new failures appear, loop back to step 3.

## Pitfalls

- **Authentication failures**: `gh` may lose auth mid-run. If commands start failing with auth errors, ask the user to re-authenticate with `gh auth login` and retry.
- **GraphQL field drift**: GitHub can deprecate or rename fields. The inspection script handles this by falling back to available fields, but manual `gh pr checks` commands may also need field adjustments.
- **Log availability**: GitHub Actions logs may not be available immediately after a run completes (pending state). If logs are unavailable, wait and retry, or use the job-level log API as a fallback (the script does this automatically).
- **External CI providers**: Buildkite, CircleCI, and other external providers have their own log systems. This skill only reports their details URLs and does not attempt to fetch logs from them.
- **Rate limiting**: The GitHub API has rate limits. The script makes multiple API calls per failing check — for PRs with many failures, this can hit secondary rate limits. Add delays between checks if needed.
- **Zip-archived logs**: Some job log endpoints return zip archives instead of text. The script detects this (`PK` magic bytes) and reports an error rather than trying to decompress.
- **No PR for current branch**: If `gh pr view` fails because there's no PR, suggest creating one with the `yeet` skill or ask for a PR number.

## Verification

1. **All checks passing**: `gh pr checks` shows no failing checks.
2. **Fix committed and pushed**: `git log --oneline -1` shows the fix commit on the branch.
3. **PR updated**: `gh pr view --json url` returns the PR URL with the new commit visible.

## Cross-References

- **`yeet`** — Use when ready to commit CI fixes and push/update the PR.
- **`gh-address-comments`** — Use when CI failures are related to review feedback that needs addressing.