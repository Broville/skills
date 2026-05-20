---
name: gh-address-comments
description: Fetch and address review comments on the open PR for the current branch; present a numbered summary, apply selected fixes, and push.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
  - macos
trigger:
  - user asks to address PR review comments
  - user asks to fix review feedback
  - user asks to respond to PR comments
  - user mentions "address comments" in context of a GitHub PR
inputs:
  - name: pr
    description: PR number or URL (optional; defaults to current branch PR)
    required: false
outputs:
  - name: applied_fixes
    description: List of comment IDs that were addressed with code changes
  - name: push_result
    description: Confirmation that changes were pushed to the PR branch
metadata:
  hermes:
    tags: [github, pr, review, comments, feedback]
    related_skills:
      - yeet
      - gh-fix-ci
---

# gh-address-comments

## Description

Use this skill when asked to address review comments or fix feedback on a GitHub pull request. The agent authenticates with `gh`, fetches all comments and review threads on the PR for the current branch, presents a numbered summary of actionable items, applies fixes for the ones the user selects, and pushes the changes.

## Prerequisites

- **GitHub CLI (`gh`)** installed and authenticated. Verify with `gh auth status`. If not authenticated, run `gh auth login` (ensure repo + workflow scopes) before proceeding.
- **Python 3** available on `PATH` for the fetch script.
- Current branch has an associated open PR (or the user provides a PR number/URL).

## Steps

### 1. Verify authentication

```shell
gh auth status
```

If this fails, ask the user to run `gh auth login` and retry. Do not proceed without valid authentication.

### 2. Resolve the PR

If the user provided a PR number or URL, use it directly. Otherwise, resolve the PR for the current branch:

```shell
gh pr view --json number,url
```

If this fails, there is no open PR for the current branch. Ask the user for a PR number or suggest creating one with the `yeet` skill.

### 3. Fetch all comments and review threads

Run the bundled fetch script to collect all conversation comments, reviews, and inline review threads:

```shell
python3 skills/software-dev/gh-address-comments/scripts/fetch_comments.py > pr_comments.json
```

Alternatively, if running from the skill directory:

```shell
python3 scripts/fetch_comments.py > pr_comments.json
```

### 4. Present a numbered summary

Parse `pr_comments.json` and present a numbered list of actionable items:

- **Unresolved review threads** (inline comments that are not yet resolved) — highest priority.
- **Review submissions with "Changes requested"** state — important context.
- **Conversation comments** (top-level PR comments) — review for actionable items.

For each item, show:
- **Number** — sequential index (1, 2, 3, …)
- **Author** — who wrote the comment
- **Location** — file path and line (for inline comments) or "conversation" (for top-level comments)
- **Summary** — brief description of what the comment is asking for
- **Resolved?** — whether the thread is already resolved

Example output format:

```
Comment 1 — @alice at src/main.py:42
  "This function should handle the edge case where input is None."
  Status: unresolved

Comment 2 — @bob (conversation)
  "Can you add a test for the new endpoint?"
  Status: open

Comment 3 — @carol at src/api.py:108
  "Nit: consider using a more descriptive variable name."
  Status: resolved (by @alice)
```

### 5. Ask the user which items to address

Present the summary and ask: "Which numbered comments should I address? (e.g., 1, 3, 5 or 'all')"

### 6. Apply fixes for selected comments

For each selected comment:

1. Read the comment body to understand the requested change.
2. Identify the target file and line range from the review thread metadata.
3. Make the fix — edit the file, add missing error handling, rename variables, add tests, etc.
4. If the fix is ambiguous, ask the user for clarification before proceeding.
5. After applying each fix, consider replying to the review thread confirming the change:

   ```shell
   gh api repos/{owner}/{repo}/pull/comments/{comment_id}/replies \
     --field body="Addressed in {commit_sha}. {brief description of change}."
   ```

### 7. Commit and push

Stage, commit, and push the accumulated fixes:

```shell
git add -A
git commit -m "fix: address PR review comments"
git push
```

Use the `yeet` skill if a more structured commit/PR workflow is desired.

### 8. Verify

Confirm the fixes are visible on the PR:

```shell
gh pr view --json url
```

Open the PR URL and verify the new commits appear and CI checks are passing. If CI is failing, use the `gh-fix-ci` skill.

## Pitfalls

- **Authentication failures mid-run**: If `gh` hits auth or rate-limit errors during the fetch, ask the user to re-authenticate with `gh auth login` and retry from step 3.
- **No PR for current branch**: The branch must have an open PR. If there isn't one, suggest creating one with `yeet` or ask the user for a PR number.
- **Already-resolved threads**: Skip threads marked as `isResolved: true` unless the user explicitly asks to re-examine them.
- **Large PRs with 100+ comments**: The fetch script paginates automatically, but presenting all comments at once can be overwhelming. Group by file and thread status.
- **Cross-repo PRs**: The script handles cross-repo PRs by reading `headRepositoryOwner` and `headRepositoryName` from the PR metadata.
- **GraphQL field changes**: If `gh api graphql` rejects the query, check the GitHub GraphQL schema changelog — field names may have changed. The included script uses stable fields, but GitHub can deprecate them.
- **Replying to comments requires write access**: The `gh api` call to reply to review comments requires write access to the repository. If auth scopes are insufficient, skip the reply step and just note what was done.

## Verification

1. **Fetch succeeded**: The `fetch_comments.py` script exits 0 and produces valid JSON containing a `pull_request` key with `number`, `url`, `title`, and `state` fields.
2. **Changes pushed**: `git log --oneline -1` shows the fix commit on the current branch.
3. **PR updated**: `gh pr view --json url` returns the PR URL, and the new commit is visible on the PR page.
4. **CI green**: `gh pr checks` shows no failing checks (or proceed to `gh-fix-ci` if red).

## Cross-References

- **`yeet`** — Use when you need to commit and push changes, or create/update a PR.
- **`gh-fix-ci`** — Use when CI checks are failing after pushing fixes.