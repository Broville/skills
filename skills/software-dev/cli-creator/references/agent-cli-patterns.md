# Composable CLI Patterns

This reference defines the expected shape for CLIs built with this skill. A composable CLI is one that can be called from scripts, piped into other tools, and composed into workflows.

## Command Surface

Every CLI should provide these command groups:

### 1. Help (`--help`)

```
tool-name --help
```

Shows every major capability, subcommand group, and common flags. Must be complete and accurate.

### 2. Doctor (`--json doctor`)

```
tool-name --json doctor
```

Reports:
- CLI version
- Whether auth is available (and from which source: env, config, flag)
- Whether the configured endpoint is reachable
- Any missing setup steps

Output must be stable JSON. Never echo credentials.

### 3. Init (`init`)

```
tool-name init [--org ORG] [--project PROJECT]
```

Stores local configuration when environment-only auth is painful. Writes to `~/.<tool-name>/config.toml` or similar documented path.

### 4. Discovery Commands

```
tool-name list-projects
tool-name list-workspaces
tool-name describe-resource ID
```

Find top-level containers: accounts, projects, workspaces, teams, queues, channels, repos.

### 5. Resolve Commands

```
tool-name resolve --url https://example.com/path/to/resource
tool-name resolve --slug my-project
```

Turn names, URLs, slugs, permalinks, or customer input into stable IDs. Future commands use the ID, not the name.

### 6. Read Commands

```
tool-name get-thing ID
tool-name list-things --limit 20 --json
```

Fetch exact objects and list/search collections. Paginated lists must support bounded `--limit`.

### 7. Write Commands

```
tool-name create-thing --name "..." --dry-run
tool-name update-thing ID --field value
tool-name upload RESOURCE_ID --file data.json
```

One named action per command. Support `--dry-run` or `--preview` when the service allows it. Don't hide writes inside broad commands like `fix` or `debug`.

### 8. Raw Escape Hatch

```
tool-name request GET /api/v1/resources
tool-name api /organizations/ORG/projects
```

For endpoints not covered by dedicated commands. Prefer read-only (`GET`/`HEAD`) first.

## JSON Policy

- Under `--json`, output must be valid, stable JSON
- Success: either raw API response or a CLI envelope `{ "data": ..., "status": "ok" }`
- Error: `{ "error": { "code": "...", "message": "..." } }` — machine-readable, no credentials
- Document which policy the CLI uses in the README

## Naming Conventions

- Commands: `verb-noun` or `noun verb` — pick one convention and stick with it
- Flags: `--long-name` with short aliases where obvious (`-n` for `--name`, `-l` for `--limit`)
- JSON output: always `--json`, never `--format json` or `--output json`

## Installability

The CLI must be installable so `tool-name` works from any directory:

- Python: `pip install -e .` or `make install-local`
- TypeScript: `npm link` or `make install-local`
- Rust: `cargo build --release && cp target/release/tool-name ~/.local/bin/`

Always include a README with install instructions and three copy-pasteable examples.