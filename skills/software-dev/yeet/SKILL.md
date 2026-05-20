---
name: yeet
description: Stage, commit, push, and open or update a GitHub pull request in one flow.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - user says "ship it"
  - user asks to commit and push
  - user asks to create a PR
  - user asks to open a pull request
  - user asks to push changes
metadata:
  hermes:
    tags: [git, github, pr, commit, push, ship]
    related_skills: [git-advanced-workflows, code-review-checklist]
---

# yeet

## Description

Stage, commit, push, and open (or update) a GitHub pull request in one flow. Handles branch creation, committing, pushing, and PR management using `git` and `gh` CLI.

**Do not use this skill** if the user only asks to commit (without pushing) or only asks to push (without creating a PR).

## Prerequisites

- **GitHub CLI (`gh`)** installed and authenticated
- **Git** installed, current directory in a git repo

## Steps

### 1. Authenticate
```shell
gh auth status
```

### 2. Determine the branch
- If on main/master → create a new branch: `git checkout -b "{description}"`
- Otherwise → stay on current branch

### 3. Stage all changes
```shell
git status -sb
git add -A
```

### 4. Commit
```shell
git commit -m "{description}"
```
Use conventional commit format: `<type>(<scope>): <subject>`

### 5. Run checks (if available)
```shell
make lint && make test
# or: npm run lint && npm test
```

### 6. Push
```shell
git push -u origin "$(git branch --show-current)"
```
If push fails due to rejection: `git pull --rebase origin "$(git branch --show-current)"` then retry.

### 7. Discover PR template
Check `.github/pull_request_template.md` and variants. Use template if found.

### 8. Check for existing PR
```shell
gh pr view "$(git branch --show-current)" --json number,isDraft,url
```
If PR exists → update it. Do NOT create a second PR.

### 9. Create or update the PR
Draft PR creation:
```shell
GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head "$(git branch --show-current)"
```

### 10. Write the PR title and body
- **Title**: `<type>(<scope>): <subject>`
- **Body**: Explain WHY, then WHAT changed. Limit to net change. Use `--body-file` to avoid escaping issues.
- Include `## Verification` section only when there's behavioral evidence worth preserving.

### 11. Verify the PR
```shell
gh pr view --json number,url,title
```

## Pitfalls

- **Push failures**: If auth errors from GitHub Actions, add `contents: write` permission. If rejection, pull with `--rebase`.
- **Multiple PR templates**: Do not guess — ask the user which one.
- **Existing PR found**: Never create a second PR. Always update the existing one.
- **Accidentally committing to main**: Always check current branch first.
- **Large diffs**: Consider asking if they want to split the commit.
- **PR body escaping**: Always use `--body-file` instead of string arguments.

## Verification

1. Branch pushed: `git log --oneline origin/$(git branch --show-current) -1`
2. PR exists: `gh pr view --json number,url`
3. PR title and body correct
4. CI checks passing or in progress