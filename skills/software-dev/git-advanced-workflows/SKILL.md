---
name: git-advanced-workflows
description: Advanced Git workflows — branching strategies, versioning, rebase, cherry-pick, bisect, worktrees, reflog, recovery
version: 1.1.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - Cleaning up commit history before merging
  - Applying specific commits across branches
  - Finding commits that introduced bugs
  - Working on multiple features simultaneously with worktrees
  - Recovering from Git mistakes or lost commits
  - Preparing clean PRs for review
  - Choosing a branching strategy or release workflow
  - Cutting a release, choosing a semantic version bump, or writing a changelog
metadata:
  hermes:
    tags: [git, rebase, cherry-pick, bisect, worktree, reflog, recovery, branching, versioning, conventional-commits]
    related_skills: [systematic-debugging, yeet, code-review-checklist, shipping-and-launch]
    aliases: [git-workflow-and-versioning]
    source: addyosmani/agent-skills (MIT)
    source_url: https://github.com/addyosmani/agent-skills/tree/main/skills/git-workflow-and-versioning
---

# Git Advanced Workflows

> This skill absorbs and supersedes the external skill `git-workflow-and-versioning` from addyosmani/agent-skills (MIT).

## Description

Advanced Git workflows for teams and agents: keep history clean, recover from mistakes, work in parallel, and release with consistent versioning. Combines tactical commands with branching strategy and release conventions.

## Steps

### Branching Strategies

Choose a strategy based on release cadence and team size.

### Trunk-Based Development (recommended default)

Keep `main` always deployable. Work in short-lived feature branches that merge back within 1-3 days. Prefer feature flags over long-lived branches.

```
main ──●──●──●──●──●──●──●──●──●──  (always deployable)
        ╲      ╱  ╲    ╱
         ●──●─╱    ●──╱    ← short-lived feature branches (1-3 days)
```

### Gitflow

Use when releases need stabilization branches and parallel hotfix lanes.

```
main    ●────●────●────●────●────●
         ╲         ╲        ╲
develop   ●──●──●──●──●──●──●──●
           ╲      ╱ ╲        ╱
feature     ●──●─╱   ●────●─╱
release          ●──●
hotfix                 ●──●
```

### GitHub Flow

For teams already doing continuous deployment: branch from `main`, open a PR, review, merge, deploy.

## Branch Naming

```
feature/<short-description>   → feature/task-creation
fix/<short-description>       → fix/duplicate-tasks
chore/<short-description>     → chore/update-deps
refactor/<short-description>  → refactor/auth-module
docs/<short-description>      → docs/api-examples
```

## Commit Conventions

### Conventional Commits

```
<type>(<scope>): <short description>

<optional body explaining why, not what>
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `refactor` — Code change that neither fixes a bug nor adds a feature
- `test` — Adding or updating tests
- `docs` — Documentation only
- `chore` — Tooling, dependencies, config
- `perf` — Performance improvement
- `security` — Security fix

### Atomic commits

Each commit does one logical thing:

```
# Good
a1b2c3d feat: add task creation endpoint with validation
d4e5f6g feat: add task creation form component
h7i8j9k test: add task creation unit + integration tests

# Bad
x1y2z3a add task feature, fix sidebar, update deps, refactor utils
```

### Commit hygiene checklist

```bash
# 1. Check what you're about to commit
git diff --staged

# 2. Ensure no secrets
git diff --staged | grep -i "password\|secret\|api_key\|token"

# 3. Run tests, lint, and type checks
npm test
npm run lint
npx tsc --noEmit
```

## Versioning and Releases

### Semantic Versioning

```
MAJOR — breaking change that forces consumers to update
MINOR — new functionality, backward-compatible
PATCH — bug fix, backward-compatible
```

### Tag releases

```bash
git tag -a v1.4.0 -m "Release 1.4.0"
git push origin v1.4.0
```

### Keep a changelog

Write a human-readable entry for each release grouped by impact:

```markdown
## [1.4.0] - 2025-06-12
### Added
- Bulk task import via CSV
### Fixed
- Timezone drift in recurring task due dates
### Security
- Fix SSRF in webhook handler
```

## Interactive Rebase

```bash
git rebase -i HEAD~5
git rebase -i $(git merge-base HEAD main)
```

Operations: `pick`, `reword`, `edit`, `squash`, `fixup`, `drop`

## Cherry-Picking

```bash
git cherry-pick abc123
git cherry-pick abc123..def456   # range (exclusive start)
git cherry-pick -n abc123       # stage only, no commit
```

### Partial Cherry-Pick
```bash
git checkout abc123 -- path/to/file1.py path/to/file2.py
git commit -m "cherry-pick: apply specific changes from abc123"
```

## Git Bisect

```bash
git bisect start
git bisect bad          # current is bad
git bisect good v1.0.0  # known good
# test each commit...
git bisect reset
```

### Automated Bisect
```bash
git bisect start HEAD v1.0.0
git bisect run ./test.sh
```

## Worktrees

```bash
# Create a worktree for a feature branch
git worktree add ../project-feature-a feature/task-creation
git worktree add ../project-feature-b feature/user-settings

# Each worktree is a separate directory with its own branch
ls ../
  project/              ← main branch
  project-feature-a/    ← task-creation branch
  project-feature-b/    ← user-settings branch

# When done, merge and clean up
git worktree remove ../project-feature-a
```

## Reflog (Safety Net)

```bash
git reflog
git reflog show feature/branch
# Restore: checkout the hash, then branch from it
git branch recovered-branch abc123
```

## Autosquash Workflow

```bash
git commit --fixup HEAD          # create fixup commit
git rebase -i --autosquash main  # auto-squash during rebase
```

## Split Commit

```bash
git rebase -i HEAD~3    # mark commit with 'edit'
git reset HEAD^         # unstage
git add file1.py && git commit -m "feat: add validation"
git add file2.py && git commit -m "feat: add error handling"
git rebase --continue
```

## Using Git for Debugging

```bash
# Find which commit introduced a bug
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>

# View what changed recently
git log --oneline -20
git diff HEAD~5..HEAD -- src/

# Find who last changed a specific line
git blame src/services/task.ts

# Search commit messages for a keyword
git log --grep="validation" --oneline
```

## Best Practices

1. Always use `--force-with-lease` instead of `--force`
2. Rebase only local commits
3. Atomic commits — each commit = one logical change
4. Test before force push
5. Keep reflog aware — it's your 90-day safety net
6. Branch before risky operations
7. Separate concerns: refactors, features, and fixes in distinct commits
8. Delete branches after merge

## Recovery Commands

```bash
git rebase --abort / git merge --abort / git cherry-pick --abort
git restore --source=abc123 path/to/file
git reset --soft HEAD^   # undo commit, keep changes
git reset --hard HEAD^   # undo commit, discard changes
```

## Pitfalls

1. **Rebasing public branches** — Only rebase local/private branches
2. **Force pushing without `--force-with-lease`** — Can overwrite teammate's work
3. **Losing work in rebase** — Resolve conflicts carefully, create backup first
4. **Forgetting worktree cleanup** — Run `git worktree prune`
5. **Bisecting on dirty working directory** — Commit or stash first
6. **Not backing up before risky operations** — Always `git branch backup-branch` first
7. **Giant commits** — Changes over ~1000 lines should be split
8. **Mixing concerns in one commit** — Keep refactors, features, and formatting separate
9. **Skipping changelog entry** — Write it when the change is made, not at release time

## Verification

For every commit:
- [ ] Commit does one logical thing
- [ ] Message explains the why, follows type conventions
- [ ] Tests pass before committing
- [ ] No secrets in the diff
- [ ] No formatting-only changes mixed with behavior changes
- [ ] `.gitignore` covers standard exclusions

For every release (anything with consumers):
- [ ] The version bump matches the change: breaking → major, additive → minor, fix → patch
- [ ] The release is tagged, and the version is derived from the tag or a single source of truth
- [ ] The changelog has a curated, human-readable entry grouped by impact for this version

## Cross-References

- **systematic-debugging** — use `git bisect` and recent-history analysis to find which commit introduced a bug
- **code-review-checklist** — review commit history, scope, and hygiene as part of PR review
- **shipping-and-launch** — coordinate tags, changelogs, and release branches with deployment
