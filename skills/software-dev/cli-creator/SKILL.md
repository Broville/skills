---
name: cli-creator
description: Build composable command-line tools from API docs, OpenAPI specs, curl examples, SDKs, or existing scripts. Produces durable, installable CLIs in Python, TypeScript, or Rust.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to create a CLI or command-line tool
  - User asks to wrap an API with a command-line interface
  - User wants to build a tool from an OpenAPI spec, curl examples, or SDK
  - User asks to make a script installable as a proper command
  - User mentions argparse, typer, commander, clap, or CLI frameworks
inputs:
  - name: tool_name
    description: Short binary name for the CLI (e.g., "ci-logs", "slack-cli")
    required: true
  - name: source
    description: API docs, OpenAPI spec, curl examples, SDK, or existing script
    required: true
  - name: runtime
    description: "Language choice: python, typescript, or rust (auto-detected if not specified)"
    required: false
outputs:
  - name: cli_binary
    description: Installable CLI tool available on PATH
  - name: readme
    description: README with usage examples and installation instructions
metadata:
  hermes:
    tags:
      - cli
      - command-line
      - api-wrapper
      - tooling
      - developer-tools
    related_skills:
      - jupyter-notebook
---

# CLI Creator

## Description

Create a real, durable CLI tool that can run from any working directory. This skill is for tools meant to live on `$PATH` and be composed into workflows — not for one-off scripts that stay in a single repo. The CLI should be installable, self-documenting, and produce stable JSON output.

## Prerequisites

Depends on the chosen runtime. Check what is available:

```bash
command -v python3 node cargo rustc || true
```

## Steps

### 1. Define the tool

Name the target tool, its source, and its first real jobs:

- **Source**: API docs, OpenAPI JSON, SDK docs, curl examples, a web app, an existing internal script, or shell history
- **Jobs**: concrete reads/writes such as `list drafts`, `download failed job logs`, `search messages`, `upload media`
- **Install name**: a short binary name such as `ci-logs`, `slack-cli`, `sentry-cli`, or `buildkite-logs`

Check if the name is already taken:

```bash
command -v <tool-name> || echo "Name available"
```

If it exists, choose a clearer name or ask the user.

### 2. Choose the runtime

Inspect the user's machine and source material, then choose the least surprising toolchain:

- **Python** — for data science, local file transforms, notebooks, SQLite/CSV/JSON analysis, or Python-heavy admin tooling. Use `argparse` for simple CLIs or `typer` when subcommands would otherwise get messy.
- **TypeScript/Node** — when the official SDK, auth helper, or existing repo tooling is JavaScript/TypeScript. Use `commander` or `cac` for commands and help; `zod` for payload validation; `package.json` `bin` entry for the installed command.
- **Rust** — for a durable, fast CLI that should run from any repo with no runtime dependency. Use `clap` for commands, `reqwest` for HTTP, `serde`/`serde_json` for payloads, `anyhow` for errors.

If the best language is not installed, either install the toolchain with the user's approval or choose the next-best installed option.

State the choice in one sentence before scaffolding, including the reason and the installed toolchain.

### 3. Sketch the command surface

Define the full command surface in chat before coding:

- `tool-name --help` — shows every major capability
- `tool-name --json doctor` — verifies config, auth, version, endpoint reachability, and missing setup
- `tool-name init ...` — stores local config when env-only auth is painful
- Discovery commands — find accounts, projects, workspaces, teams, repos, or other top-level containers
- Resolve commands — turn names, URLs, slugs, or permalinks into stable IDs
- Read commands — fetch exact objects and list/search collections. Paginated lists support `--limit`
- Write commands — one named action each: create, update, delete, upload, retry. Support `--dry-run` when the service allows it
- `--json` — returns stable machine-readable output
- Raw escape hatch — `request`, `api`, or nearest honest name for direct API access

Do not expose only a generic `request` command. Give high-level verbs for the repeated jobs.

See `references/agent-cli-patterns.md` for the expected composable CLI shape.

### 4. Scaffold the project

Create the project with a README and install instructions:

```bash
# Python example
mkdir -p ~/code/clis/<tool-name> && cd ~/code/clis/<tool-name>
# Create pyproject.toml, src/ module, README.md

# TypeScript example
mkdir -p ~/code/clis/<tool-name> && cd ~/code/clis/<tool-name>
npm init -y
# Create src/ files, package.json bin entry

# Rust example
cargo init --name <tool-name> ~/code/clis/<tool-name>
cd ~/code/clis/<tool-name>
# Edit Cargo.toml, src/main.rs
```

### 5. Implement core commands

Implement in this order:
1. `doctor` — config check, auth probe, version report
2. Discovery — list top-level resources
3. Resolve — name-to-ID lookups
4. Read — fetch and list resources
5. One narrow write path (if requested) with `--dry-run`
6. Raw escape hatch

### 6. Install on PATH

```bash
# Python
pip install -e .
# Or: add Makefile target: make install-local

# TypeScript
npm run build && npm link
# Or: make install-local

# Rust
cargo build --release && cp target/release/<tool-name> ~/.local/bin/
# Or: make install-local
```

Add a `Makefile` target such as `make install-local` that builds release and installs the binary.

### 7. Smoke test from outside the source

```bash
cd /tmp
command -v <tool-name>            # Expected: path to binary
<tool-name> --help                # Expected: usage information
<tool-name> --json doctor          # Expected: config/auth/version status
```

Test from `/tmp` or another directory, not from inside the source folder. This catches binaries that only work in-tree.

### 8. Add tests

Write tests for:
- Request builders and pagination logic
- No-auth `doctor` output
- Help output completeness
- At least one fixture or dry-run call

```bash
# Python
python -m pytest

# TypeScript
npm test

# Rust
cargo test
```

## Auth and Config

Support the boring paths first, in this precedence order:

1. **Environment variable** using the service's standard name (e.g., `GITHUB_TOKEN`, `SENTRY_AUTH_TOKEN`)
2. **User config** under `~/.<tool-name>/config.toml` or another documented path
3. **Flag** — `--api-key` or tool-specific token flag only for explicit one-off tests

Never print full tokens in output. `doctor --json` should report whether a token is available, the auth source category (`env`, `config`, `flag`), and what setup step is missing. It should not echo the token value.

## JSON Policy

Document in the CLI README:
- Whether output is API pass-through or a CLI envelope
- Success shape: `{ "data": ..., "status": "ok" }` or raw API response
- Error shape: `{ "error": { "code": ..., "message": ... } }` or equivalent
- One example for each command family

Under `--json`, errors must be machine-readable and must not contain credentials.

## Runtime Defaults

### Python

- `argparse` for commands and help, or `typer` for subcommands
- `urllib.request` / `urllib.parse`, `requests`, or `httpx` for HTTP
- `json`, `csv`, `sqlite3`, `pathlib`, `subprocess` for local operations
- `pyproject.toml` console script entry point for the installed command
- Virtualenv only when external dependencies are actually needed

### TypeScript/Node

- `commander` or `cac` for commands and help
- Native `fetch`, the official SDK, or an existing HTTP helper
- `zod` only where external payload validation prevents real breakage
- `package.json` `bin` entry for the installed command
- `tsup`, `tsx`, or `tsc` using the repo's existing convention

### Rust

- `clap` for commands and help
- `reqwest` for HTTP
- `serde` / `serde_json` for payloads
- `toml` for small config files
- `anyhow` for CLI-shaped error context
- `Makefile` with `make install-local` target

### For web app source from DevTools

When building a CLI from a web app's DevTools network activity:
1. Create sanitized endpoint notes: resource name, method/path, required headers, auth mechanism, CSRF behavior, request body shape, response ID fields, pagination, errors
2. Never commit copied cookies, bearer tokens, or customer secrets
3. Use screenshots to infer workflow and fields, not as API evidence

## Pitfalls

- **Binary only works in the source directory**: Always smoke-test from `/tmp` or another directory. Hardcoded relative paths, missing assets, or incorrect `bin` entries cause this. Verify with `command -v <tool-name>` and run `--json doctor` from outside the source tree.
- **Auth token leaks**: Never echo tokens in `--json` output. The `doctor` command should report auth status (present/missing/source) without displaying the token value. Warn if a token is provided via command-line flag (visible in process listings and shell history).
- **Pagination that doesn't terminate**: Pagination loops that miss the "last page" signal can run forever. Always set a `--limit` cap, and document the default. Test with `--limit 1` to verify the loop terminates.
- **Generic `request` command only**: A CLI with only a raw `request` command is no better than `curl`. Always provide high-level verbs for the top jobs the user described. The raw escape hatch is for exploration, not primary use.

## Verification

1. **Binary is on PATH**:
   ```bash
   command -v <tool-name>
   # Expected: full path to the binary
   ```

2. **Help output is complete**:
   ```bash
   <tool-name> --help
   # Expected: lists all major commands and flags
   ```

3. **Doctor command works**:
   ```bash
   <tool-name> --json doctor
   # Expected: JSON with version, auth status, and config check
   ```

4. **Runs from outside source**:
   ```bash
   cd /tmp && <tool-name> --json doctor
   # Expected: same output as running from source directory
   ```

5. **Tests pass**:
   ```bash
   # Python
   python -m pytest
   # TypeScript
   npm test
   # Rust
   cargo test
   # All should exit 0
   ```

## Cross-References

- **jupyter-notebook** (`data-science/jupyter-notebook`) — For creating notebooks that analyze CLI output data
- CLI pattern reference: `references/agent-cli-patterns.md`