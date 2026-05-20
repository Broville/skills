---
name: git-advanced-workflows
description: Advanced Git workflows including interactive rebase, cherry-pick, bisect, worktrees, reflog, autosquash, split commits, and recovery techniques
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Cleaning up commit history before merging
  - Applying specific commits across branches
  - Finding commits that introduced bugs
  - Working on multiple features simultaneously with worktrees
  - Recovering from Git mistakes or lost commits
  - Preparing clean PRs for review
related_skills:
  - systematic-debugging
  - deployment-procedures
  - code-review-checklist
---

# Git Advanced Workflows

## Description

Master advanced Git techniques to maintain clean history, collaborate effectively, and recover from any situation with confidence. This is a reference-style skill covering interactive rebase, cherry-picking, bisect, worktrees, reflog, autosquash, split commits, and recovery.

## Interactive Rebase

The Swiss Army knife of Git history editing.

**Common operations:**
- `pick` — Keep commit as-is
- `reword` — Change commit message
- `edit` — Amend commit content
- `squash` — Combine with previous commit
- `fixup` — Like squash but discard message
- `drop` — Remove commit entirely

```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Rebase all commits on current branch against main
git rebase -i $(git merge-base HEAD main)

# Rebase onto specific commit
git rebase -i abc123
```

## Cherry-Picking

Apply specific commits from one branch to another without merging entire branches.

```bash
# Cherry-pick single commit
git cherry-pick abc123

# Cherry-pick range of commits (exclusive start)
git cherry-pick abc123..def456

# Cherry-pick without committing (stage changes only)
git cherry-pick -n abc123

# Cherry-pick and edit commit message
git cherry-pick -e abc123
```

### Partial Cherry-Pick

Cherry-pick only specific files from a commit:

```bash
# Show files in commit
git show --name-only abc123

# Checkout specific files from commit
git checkout abc123 -- path/to/file1.py path/to/file2.py

# Stage and commit
git commit -m "cherry-pick: apply specific changes from abc123"
```

## Git Bisect

Binary search through commit history to find the commit that introduced a bug.

```bash
# Start bisect
git bisect start
git bisect bad          # Current commit is bad
git bisect good v1.0.0 # Known good commit

# Git checks out middle commit — test it, then mark:
git bisect good    # or git bisect bad

# Continue until bug found
# When done:
git bisect reset
```

### Automated Bisect

```bash
git bisect start HEAD v1.0.0
git bisect run ./test.sh
# test.sh should exit 0 for good, 1-127 (except 125) for bad
```

## Worktrees

Work on multiple branches simultaneously without stashing or switching.

```bash
# List existing worktrees
git worktree list

# Add new worktree for feature branch
git worktree add ../project-feature feature/new-feature

# Add worktree and create new branch
git worktree add -b bugfix/urgent ../project-hotfix main

# Remove worktree
git worktree remove ../project-feature

# Prune stale worktrees
git worktree prune
```

## Reflog

Safety net — tracks all ref movements, even deleted commits (90-day default).

```bash
# View reflog
git reflog

# View reflog for specific branch
git reflog show feature/branch

# Restore deleted commit
git reflog
# Find commit hash, then:
git checkout abc123
git branch recovered-branch

# Restore deleted branch
git reflog
git branch deleted-branch abc123
```

## Practical Workflows

### Clean Up Feature Branch Before PR

```bash
git checkout feature/user-auth
git rebase -i main
# Squash "fix typo" commits, reword messages, reorder logically
git push --force-with-lease origin feature/user-auth
```

### Apply Hotfix to Multiple Releases

```bash
git checkout main
git commit -m "fix: critical security patch"

# Apply to release branches
git checkout release/2.0
git cherry-pick abc123

git checkout release/1.9
git cherry-pick abc123

# Handle conflicts if they arise:
git cherry-pick --continue
# or:
git cherry-pick --abort
```

### Find Bug Introduction with Bisect

```bash
git bisect start
git bisect bad HEAD
git bisect good v2.1.0

# Git checks out middle commit — run tests
npm test

# Mark result:
git bisect bad    # or git bisect good

# Automated version:
git bisect start HEAD v2.1.0
git bisect run npm test
```

### Multi-Branch Development with Worktrees

```bash
# Main project directory
cd ~/projects/myapp

# Create worktree for urgent bugfix
git worktree add ../myapp-hotfix hotfix/critical-bug

# Work on hotfix in separate directory
cd ../myapp-hotfix
# Make changes, commit
git commit -m "fix: resolve critical bug"
git push origin hotfix/critical-bug

# Return to main work without interruption
cd ~/projects/myapp
git fetch origin
git cherry-pick hotfix/critical-bug

# Clean up
git worktree remove ../myapp-hotfix
```

### Recover from Mistakes

```bash
# Accidentally reset to wrong commit
git reset --hard HEAD~5  # Oh no!

# Use reflog to find lost commits
git reflog
# Find the commit hash before the reset

# Recover lost commits
git reset --hard def456

# Or create branch from lost commit
git branch recovery def456
```

## Autosquash Workflow

Automatically squash fixup commits during rebase.

```bash
# Make initial commit
git commit -m "feat: add user authentication"

# Later, fix something in that commit
git commit --fixup HEAD  # or specify commit hash

# Rebase with autosquash
git rebase -i --autosquash main
```

## Split Commit

Break one commit into multiple logical commits.

```bash
git rebase -i HEAD~3
# Mark commit to split with 'edit'
# Git stops at that commit

# Reset commit but keep changes staged
git reset HEAD^

# Stage and commit in logical chunks
git add file1.py
git commit -m "feat: add validation"

git add file2.py
git commit -m "feat: add error handling"

git rebase --continue
```

## Best Practices

1. **Always use `--force-with-lease`** instead of `--force` — safer, prevents overwriting others' work
2. **Rebase only local commits** — don't rebase commits that have been pushed and shared
3. **Descriptive commit messages** — future readers will thank you
4. **Atomic commits** — each commit should be a single logical change
5. **Test before force push** — ensure history rewrite didn't break anything
6. **Keep reflog aware** — it's your 90-day safety net
7. **Branch before risky operations** — create a backup branch before complex rebases

```bash
# Safe force push
git push --force-with-lease origin feature/branch

# Create backup before risky operation
git branch backup-branch
git rebase -i main
# If something goes wrong:
git reset --hard backup-branch
```

## Recovery Commands

```bash
# Abort operations in progress
git rebase --abort
git merge --abort
git cherry-pick --abort
git bisect reset

# Restore file to version from specific commit
git restore --source=abc123 path/to/file

# Undo last commit but keep changes
git reset --soft HEAD^

# Undo last commit and discard changes
git reset --hard HEAD^
```

## Pitfalls

1. **Rebasing public branches** — Causes history conflicts for collaborators. Only rebase local/private branches.
2. **Force pushing without `--force-with-lease`** — Can overwrite teammate's work silently. Always use `--force-with-lease`.
3. **Losing work in rebase** — Resolve conflicts carefully, test after rebase. Create a backup branch first.
4. **Forgetting worktree cleanup** — Orphaned worktrees consume disk space. Run `git worktree prune` after removing directories.
5. **Bisecting on a dirty working directory** — Commit or stash before starting bisect, or results will be unreliable.
6. **Not backing up before risky operations** — Always `git branch backup-branch` before complex rebases or resets.

## Clean Up Merged Branches

Use the provided script to remove local branches that have been merged:

```bash
# See scripts/git-clean-branches.sh
./scripts/git-clean-branches.sh
```

## Verification

1. **After rebase:** Verify history is clean and tests pass
   ```bash
   git log --oneline -10   # Clean history
   npm test                 # All tests pass
   ```
2. **After cherry-pick:** Verify the commit applies cleanly
   ```bash
   git log --oneline -5    # Cherry-picked commit present
   npm test                 # No regressions
   ```
3. **After worktree operations:** Verify worktree state
   ```bash
   git worktree list        # Shows expected worktrees
   git status               # Clean working tree
   ```
4. **After recovery:** Verify the right commit was restored
   ```bash
   git log --oneline -5     # Target commit present
   npm test                 # Tests still pass
   ```

## Cross-References

- **systematic-debugging** — Use `git bisect` to find when a bug was introduced
- **deployment-procedures** — Git workflows for deployment branches
- **code-review-checklist** — Pre-PR cleanup before review