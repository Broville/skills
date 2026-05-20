---
name: git-advanced-workflows
description: Advanced Git workflows including interactive rebase, cherry-pick, bisect, worktrees, reflog, autosquash, split commits, and recovery techniques
version: 1.0.0
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
metadata:
  hermes:
    tags: [git, rebase, cherry-pick, bisect, worktree, reflog, recovery]
    related_skills: [systematic-debugging, yeet, code-review-checklist]
---

# Git Advanced Workflows

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
git worktree add ../project-feature feature/new-feature
git worktree add -b bugfix/urgent ../project-hotfix main
git worktree remove ../project-feature
git worktree prune
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

## Best Practices

1. Always use `--force-with-lease` instead of `--force`
2. Rebase only local commits
3. Atomic commits — each commit = one logical change
4. Test before force push
5. Keep reflog aware — it's your 90-day safety net
6. Branch before risky operations

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