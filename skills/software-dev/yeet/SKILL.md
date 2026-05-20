---
name: yeet
description: Stage, commit, push, and open or update a GitHub pull request in one flow.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
  - macos
trigger:
  - user says "ship it"
  - user asks to commit and push
  - user asks to create a PR
  - user asks to open a pull request
  - user asks to push changes
inputs:
  - name: description
    description: Brief description of the change (used for branch name, commit message, and PR title)
    required: true
outputs:
  - name: pr_url
    description: URL of the created or updated pull request
  - name: pr_number
    description: Number of the created or updated pull request
metadata:
  hermes:
    tags: [git, github, pr, commit, push, ship]
    related_skills:
      - gh-address-comments
      - gh-fix-ci
---

# yeet

## Description

Use this skill when the user explicitly asks to stage, commit, push, and open (or update) a GitHub pull request in one flow. The agent handles branch creation, committing, pushing, and PR management using standard `git` and `gh` CLI commands.

**Do not use this skill** if the user only asks to commit (without pushing) or only asks to push (without creating a PR). This skill is for the full ship-it flow.

## Prerequisites

- **GitHub CLI (`gh`)** installed. Verify with `gh --version`. If missing, ask the user to install it and stop.
- **Authenticated `gh` session**. Run `gh auth status`. If not authenticated, ask the user to run `gh auth login` (with repo + workflow scopes) before continuing.
- **Git** installed and the current directory is inside a git repository.

## Steps

### 1. Authenticate

```shell
gh auth status
```

If not authenticated, ask the user to run `gh auth login` and then re-run `gh auth status` before proceeding.

### 2. Determine the branch

Check the current branch:

```shell
git branch --show-current
```

- If on `main`, `master`, or the default branch, create a new branch:

  ```shell
  git checkout -b "{description}"
  ```

  Where `{description}` is a short, hyphenated summary of the change (e.g., `feat/add-hat-wobble`).

- Otherwise, stay on the current branch.

### 3. Stage all changes

```shell
git status -sb
git add -A
```

Review `git status -sb` output to confirm what will be committed. If there are unexpected files, ask the user before proceeding.

### 4. Commit

```shell
git commit -m "{description}"
```

The commit message should be terse and follow conventional commit format:

```
<type>(<scope>): <subject>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

Examples:
- `feat: add hat wobble`
- `fix(api): handle null input in user endpoint`
- `docs: update README with setup instructions`

### 5. Run checks (if available)

If the project has lint, test, or build commands, run them once:

```shell
# Adapt these to the project's actual tooling
make lint && make test
# or: npm run lint && npm test
# or: pip install -e . && pytest
```

If checks fail due to missing dependencies, install them and rerun once. If checks still fail, report the failure and ask the user whether to proceed anyway.

### 6. Push

```shell
git push -u origin "$(git branch --show-current)"
```

If the push fails due to remote rejection (e.g., remote has diverged), pull and retry:

```shell
git pull --rebase origin "$(git branch --show-current)"
git push -u origin "$(git branch --show-current)"
```

If the push fails due to GitHub Actions workflow auth errors, follow GitHub's instructions (usually adding `contents: write` permission to the workflow).

### 7. Discover the PR template

Before creating the PR, check for an existing PR template:

```shell
repo_root="$(git rev-parse --show-toplevel)"
```

Template candidates, in order:
- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- One `*.md` file under `.github/pull_request_template/`
- One `*.md` file under `.github/PULL_REQUEST_TEMPLATE/`

Use paths relative to the repository root (e.g., `.github/pull_request_template.md`).

If exactly one template is found, read it and use it to structure the PR body.
If multiple template files are found, stop and ask which template to use.
If no template exists, use the fallback body shape below.

### 8. Check for an existing PR

```shell
gh pr view "$(git branch --show-current)" --json number,isDraft,url
```

- If a PR already exists, **update it in place**. Do not create a new PR. Do not change the draft/ready-for-review status.
- If no PR exists, create a new draft PR.

### 9. Create or update the PR

**Creating a new draft PR:**

With a template:

```shell
GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create \
  --draft \
  --fill \
  --template "$template" \
  --head "$(git branch --show-current)"
```

Without a template:

```shell
GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create \
  --draft \
  --fill \
  --head "$(git branch --show-current)"
```

**Updating an existing PR:**

```shell
pr_number="$(gh pr view --json number --jq '.number')"
```

Then edit the title and body (see next step).

### 10. Write the PR title and body

Write the PR description to a temp file and pass it via `--body-file` to avoid `\n`-escaped markdown:

```shell
gh pr edit "$pr_number" --title "{type}: {description}" --body-file /tmp/pr_body.md
```

**PR title format**: `<type>(<scope>): <subject>`

**PR body contents:**

- **Explain _why_** the change is being made. Capture motivation from the current conversation.
- **Explain _what_ changed** after the why. Focus on the net change.
- **Limit discussion to the net change** — do not discuss changes that were attempted but undone.
- **Avoid absolute local paths** — use repo-relative paths.
- **Preserve existing images and sections** — never remove images from an existing PR body; the author may have no way to recover them.
- **If a repo template exists**, adapt the body to that template. Replace placeholder text with net-diff content or `N/A`. Do not discard template sections.

**Fallback PR body shape** (when no template exists):

```markdown
## Why

Describe the user-facing or maintainer-facing problem, including cause and effect where useful.

## What Changed

Describe the net implementation change in concise prose.
```

**Verification section:** Include a `## Verification` section only when there is behavioral evidence worth preserving — a reproduced bug, a before/after check, a targeted test that exercises the changed behavior. Do not use it for generic commands or automation results (package tests, type checks, linters, formatters).

### 11. Verify the PR

```shell
gh pr view --json number,url,title
```

Confirm:
- The PR number, URL, and title are correct.
- The PR is visible on GitHub.
- CI checks have started (or are passing).

If CI checks are failing, use the `gh-fix-ci` skill.

## Pitfalls

- **Push failures**: If `git push` fails with auth errors related to GitHub Actions, the repository workflow may need `contents: write` permission. If it fails with rejection, pull with `--rebase` and retry.
- **Multiple PR templates**: If more than one template file exists, do not guess — ask the user which one to use.
- **Existing PR found**: Never create a second PR for the same branch. Always update the existing one. Never convert an existing ready-for-review PR back to draft.
- **Accidentally committing to main**: Always check the current branch before committing. If on the default branch, create a feature branch first.
- **Large diffs**: If the staged changes are very large, consider asking the user if they want to split the commit. A single monolithic commit is hard to review.
- **gh auth scopes**: Some operations require `repo` and `workflow` scopes. If `gh` auth errors occur during PR creation, ask the user to re-authenticate with `gh auth login` and ensure those scopes are selected.
- **PR body escaping**: Always use `--body-file` instead of passing the body as a string argument. Shell escaping of markdown newlines is unreliable.

## Verification

1. **Branch pushed**: `git log --oneline origin/$(git branch --show-current) -1` shows the commit.
2. **PR exists**: `gh pr view --json number,url` returns a valid PR number and URL.
3. **PR title and body correct**: Open the PR URL and verify the title and body reflect the net change.
4. **CI checks**: `gh pr checks` shows all checks passing or in progress. If failing, proceed to `gh-fix-ci`.

## Cross-References

- **`gh-address-comments`** — Use when there are review comments on the PR that need addressing.
- **`gh-fix-ci`** — Use when CI checks are failing on the PR after pushing.