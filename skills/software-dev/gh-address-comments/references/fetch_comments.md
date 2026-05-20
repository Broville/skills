# fetch_comments.py Reference

This is the reference documentation for `scripts/fetch_comments.py`.

## Purpose

Fetches all PR conversation comments, reviews, and inline review threads for the PR associated with the current git branch. Uses the GitHub GraphQL API via `gh api graphql`.

## Requirements

- Python 3.8+
- `gh` CLI authenticated (`gh auth login`)
- Current branch must have an associated open PR

## Usage

```shell
# Basic: fetch comments for the current branch's PR
python3 scripts/fetch_comments.py > pr_comments.json

# Pipe through jq for inspection
python3 scripts/fetch_comments.py | jq '.pull_request'
python3 scripts/fetch_comments.py | jq '.review_threads[] | select(.isResolved == false)'
```

## Output Format

The script outputs JSON with this structure:

```json
{
  "pull_request": {
    "number": 42,
    "url": "https://github.com/org/repo/pull/42",
    "title": "Add feature X",
    "state": "OPEN",
    "owner": "org",
    "repo": "repo"
  },
  "conversation_comments": [...],
  "reviews": [...],
  "review_threads": [
    {
      "id": "...",
      "isResolved": false,
      "isOutdated": false,
      "path": "src/main.py",
      "line": 42,
      "diffSide": "RIGHT",
      "startLine": 40,
      "startDiffSide": "RIGHT",
      "originalLine": 42,
      "originalStartLine": 40,
      "resolvedBy": null,
      "comments": [
        {
          "id": "...",
          "body": "Consider handling the edge case...",
          "createdAt": "...",
          "updatedAt": "...",
          "author": { "login": "alice" }
        }
      ]
    }
  ]
}
```

## Pagination

The script handles GraphQL pagination automatically — it will fetch all pages of comments, reviews, and threads (up to 100 per page).

## Error Handling

- If `gh auth status` fails, the script prints an error message and exits.
- If the current branch has no PR, `gh pr view --json` will fail and the script will propagate the error.
- If GitHub GraphQL returns errors, the script prints them and exits.