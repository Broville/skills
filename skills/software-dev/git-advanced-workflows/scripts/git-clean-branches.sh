#!/usr/bin/env bash
# Clean up local branches that have been merged into the specified target branch.
# Default target: main
# Usage: ./git-clean-branches.sh [target_branch]
# Example: ./git-clean-branches.sh main
#          ./git-clean-branches.sh develop

set -euo pipefail

TARGET_BRANCH="${1:-main}"

echo "Cleaning up branches merged into '$TARGET_BRANCH'..."

# Fetch latest remote refs
git fetch --prune

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# List merged branches (excluding target and current branch)
MERGED_BRANCHES=$(git branch --merged "$TARGET_BRANCH" | \
  grep -v "^\*\|$TARGET_BRANCH\|develop\|staging" | \
  sed 's/^[ *]*//')

if [ -z "$MERGED_BRANCHES" ]; then
  echo "No merged branches to clean up."
  exit 0
fi

echo "Merged branches found:"
echo "$MERGED_BRANCHES"
echo ""

for BRANCH in $MERGED_BRANCHES; do
  if [ "$BRANCH" = "$CURRENT_BRANCH" ]; then
    echo "Skipping current branch: $BRANCH"
    continue
  fi

  echo "Deleting local branch: $BRANCH"
  git branch -d "$BRANCH"
done

echo ""
echo "Cleanup complete. Remaining local branches:"
git branch