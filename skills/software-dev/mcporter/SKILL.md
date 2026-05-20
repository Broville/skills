---
name: mcporter
description: Discover, call, and manage MCP (Model Context Protocol) servers and tools from the CLI. List servers, call tools, manage auth, and generate CLI wrappers — all via npx.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User wants to list or call MCP server tools from the command line
  - User needs to connect to an MCP server ad-hoc without configuration
  - User wants to generate a CLI wrapper or TypeScript types for an MCP server
  - User needs to manage MCP server auth (OAuth login, config edits)
related_skills:
  - fastmcp
  - deployment-procedures
---

# mcporter

## Description

Use `mcporter` to discover, call, and manage MCP (Model Context Protocol) servers and tools directly from the terminal. It auto-discovers servers configured by other MCP clients on the machine and supports ad-hoc connections to any HTTP or stdio-based MCP server — no config needed for one-off calls.

## Prerequisites

- Node.js 18+ and npm on PATH (verify with `node -v`)
- `npx` available (bundled with npm)

## Steps

### Step 1: List Configured MCP Servers

```bash
# No install needed — runs via npx
npx mcporter list

# Or install globally for faster invocations
npm install -g mcporter
mcporter list
```

### Step 2: List Tools for a Specific Server

```bash
# Show tools with schema details
npx mcporter list <server> --schema
```

### Step 3: Call a Tool

```bash
# Key=value syntax
npx mcporter call linear.list_issues team=ENG limit:5

# JSON payload
npx mcporter call <server.tool> --args '{"limit": 5}'

# Machine-readable output (recommended for scripting)
npx mcporter call <server.tool> key=value --output json
```

### Step 4: Connect to an Ad-Hoc Server (No Config)

```bash
# HTTP server by URL
npx mcporter list --http-url https://some-mcp-server.com --name my_server

# stdio server on the fly
npx mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

### Step 5: Manage Auth and Config

```bash
# OAuth login for a server
npx mcporter auth <server | url>

# Reset auth and re-login
npx mcporter auth <server | url> --reset

# Manage config
npx mcporter config list
npx mcporter config get <key>
npx mcporter config add <server>
npx mcporter config remove <server>
npx mcporter config import <path>
```

Config file location: `./config/mcporter.json` (override with `--config`).

### Step 6: Code Generation

```bash
# Generate a CLI wrapper for an MCP server
npx mcporter generate-cli --server <name>
npx mcporter generate-cli --command <url>

# Inspect a generated CLI
npx mcporter inspect-cli <path> [--json]

# Generate TypeScript types/client
npx mcporter emit-ts <server> --mode client
npx mcporter emit-ts <server> --mode types
```

## Pitfalls

1. **Missing Node.js.** mcporter requires Node.js 18+ and npm. Verify with `node -v` before use. Without it, `npx` will fail silently or install an incompatible version.
2. **OAuth may require interactive browser flow.** When running `mcporter auth`, a browser window may open for OAuth consent. In headless or SSH-only environments, use a token-based approach or pre-configure auth manually.
3. **Ad-hoc stdio servers can leave zombie processes.** If the MCP stdio server process doesn't clean up on exit, use `pkill` to clean up stale processes after ad-hoc sessions.
4. **Config file location varies.** By default, `mcporter.json` is created in `./config/`. Running from different working directories creates separate configs. Use `--config <path>` for explicit control.

## Verification

1. **Confirm mcporter runs and lists servers:**
   ```bash
   npx mcporter list
   # Should output a list of discovered MCP servers (may be empty if none configured)
   ```
2. **Test an ad-hoc connection:**
   ```bash
   npx mcporter list --http-url https://mock-mcp.example.com --name test_verify
   # Should connect and list available tools, or report a connection error if URL is unreachable
   ```
3. **Verify config management:**
   ```bash
   npx mcporter config list
   # Should show current config entries
   ```