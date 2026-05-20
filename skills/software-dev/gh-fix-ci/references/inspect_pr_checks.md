# inspect_pr_checks.py Reference

This is the reference documentation for `scripts/inspect_pr_checks.py`.

## Purpose

Inspects failing GitHub Actions checks on a pull request, fetches run logs, and extracts failure snippets. Exits non-zero when failures remain, making it suitable for automation pipelines.

## Requirements

- Python 3.8+ (stdlib only, no external packages)
- `gh` CLI authenticated with `repo` and `workflow` scopes
- Current directory must be inside a git repository

## Usage

```shell
# Basic: inspect failing checks on the current branch's PR
python3 scripts/inspect_pr_checks.py --repo .

# Specify a PR number
python3 scripts/inspect_pr_checks.py --repo . --pr 123

# Specify a PR URL
python3 scripts/inspect_pr_checks.py --repo . --pr https://github.com/org/repo/pull/123

# Machine-readable JSON output
python3 scripts/inspect_pr_checks.py --repo . --pr 123 --json

# Adjust log snippet size
python3 scripts/inspect_pr_checks.py --repo . --max-lines 200 --context 40
```

## Command-line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--repo` | `.` | Path inside the target git repository |
| `--pr` | (current branch PR) | PR number or URL |
| `--max-lines` | `160` | Maximum lines for failure snippet |
| `--context` | `30` | Lines of context around the failure marker |
| `--json` | off | Emit JSON output instead of human-readable text |

## Exit Codes

- `0` — No failing checks detected
- `1` — Failures detected (or an error occurred)

## Output Format (JSON)

```json
{
  "pr": "123",
  "results": [
    {
      "name": "test-unit",
      "detailsUrl": "https://github.com/org/repo/actions/runs/12345",
      "runId": "12345",
      "jobId": "67890",
      "status": "ok",
      "run": {
        "conclusion": "failure",
        "status": "completed",
        "workflowName": "CI",
        "name": "test-unit",
        "event": "pull_request",
        "headBranch": "feat/branch",
        "headSha": "abc123def456",
        "url": "https://github.com/org/repo/actions/runs/12345"
      },
      "logSnippet": "...",
      "logTail": "..."
    }
  ]
}
```

## Failure Detection

A check is considered failing if any of these conditions are true:
- `conclusion` is `failure`, `cancelled`, `timed_out`, or `action_required`
- `state`/`status` is `failure`, `error`, `cancelled`, `timed_out`, or `action_required`
- `bucket` is `fail`

## Field Drift Handling

The script handles `gh` CLI field name changes by trying primary fields first (`name`, `state`, `conclusion`, `detailsUrl`, etc.) and falling back to alternative fields (`bucket`, `link`, `workflow`) if the primary set is rejected.

## External CI Providers

If a check's `detailsUrl` does not point to a GitHub Actions run (e.g., Buildkite, CircleCI), the script labels it as `status: "external"` and reports only the URL — it does not attempt to fetch logs from external providers.