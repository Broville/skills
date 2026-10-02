---
name: bambu-p2s
description: Prepare and inspect Bambu Lab P2S jobs, validate explicit printer enrollment, report capabilities, and preview operator-approved actions with a local MCP server; use when a user asks about P2S monitoring, printing, or secure printer integration. Live controls are blocked in this draft.
license: MIT
compatibility: Python 3.12+ stdlib; stdio MCP host. Secure artifact inspection requires macOS or Linux. Experimental LAN status needs separately approved enrollment and verified TLS identity. No startup network access.
metadata:
  author: Broville
  version: "0.1.0"
  platforms: '["linux","macos","windows"]'
  triggers: '["User asks to prepare, monitor, or operate a Bambu Lab P2S", "Task involves P2S enrollment or printer control feasibility"]'
  inputs: '[{"name":"device_id","description":"Explicit local enrolled alias; never a caller-selected host","required":false},{"name":"artifact","description":"Relative 3MF or G-code under an operator-selected root","required":false}]'
  outputs: '[{"name":"capabilities","description":"Implemented controls, blocked actions, and qualification limits"},{"name":"inspection","description":"Bounded container inspection and exact snapshot digest"},{"name":"action_preview","description":"Non-executable device/file/settings-bound plan requiring owner review"}]'
  tags: '["bambu-lab","p2s","printer","mcp","security","monitoring"]'
  related-skills: '["security-best-practices","systematic-debugging"]'
---

# Bambu Lab P2S

## Description

Original local plugin and portable workflow for security-conscious P2S preparation
and monitoring. This is a **0.1.0 draft, not a full-control printer integration**.
The five MCP tools expose capabilities, enrolled aliases, experimental status,
bounded artifact inspection, and action previews. Upload, print start, pause,
resume, cancel, and camera requests return non-executable previews. No write
adapter, arbitrary G-code, heater control, or motion control is present.

## Prerequisites

- Python 3.12+; no runtime dependencies. macOS/Linux for secure file inspection.
- Read [setup](references/setup.md), [controls](references/controls.md),
  [threat model](references/security.md), [protocol evidence](references/protocols.md),
  and [acceptance matrix](references/acceptance.md) before printer integration.
- Plugin identity [plugin.json](plugin.json) and local individual-plugin manifest [.codex-plugin/plugin.json](.codex-plugin/plugin.json)
  connects [mcp.json](mcp.json) to [server.py](scripts/server.py), with security
  logic in [core.py](scripts/core.py). Bundles carry the workflow only.
- No installation, credential entry, network enrollment, or mode changes are
  implied by source review or offline tests. Obtain specific approval first.

## Steps

1. Establish the requested operation and explicit device alias. Call
   `p2s_capabilities` and `p2s_list_devices` before any printer operation. If tools
   are absent, report that host integration is unavailable; reading this skill
   or a manifest does not make MCP tools callable in delegated tasks.
2. Verify offline behavior from the skill directory:
   ```bash
   python3 scripts/test_plugin.py
   ```
   Expected: security tests pass; TLS fixtures use synthetic socketpairs. The
   Windows fixture skips POSIX file access and TLS socketpair tests explicitly.
3. For a standalone offline demo, launch:
   ```bash
   python3 scripts/server.py --demo
   ```
   This waits for newline-delimited MCP messages on stdin. It has two synthetic
   aliases and never connects to a printer. Actual user artifacts require a
   separately selected `BAMBUP2S_FILE_ROOT`; never select an entire home folder.
4. If live monitoring is requested, follow the separate approval/enrollment
   process in [setup](references/setup.md). Start with the empty
   [registry template](templates/devices.example.json) outside the public plugin.
   Validate without any network access:
   ```bash
   python3 scripts/server.py --check-registry ./private-state/devices.json
   ```
   Expected: `valid: true`, device count, and `network_access: false`. The
   example registry is empty intentionally; do not fabricate a printer identity,
   firmware, access code, or certificate fingerprint to make validation pass.
5. Inspect a user-selected artifact with `p2s_inspect_artifact`. Explain that a
   valid ZIP and hash cannot establish printer compatibility or physical safety.
   Never modify, slice, upload, or start an existing job without authorization.
6. Use `p2s_preview_action` for the requested action. Select a sliced candidate
   plate explicitly for a 3MF start preview. Present the device, artifact digest,
   settings, and blockers. These settings record intent, not validated firmware
   controls. An approval statement cannot unlock this release's blocked actions.
7. Report observed status with its source and receipt time. A single report can
   be partial; absent fields are unknown. Demo reports are synthetic. A timeout,
   certificate mismatch, firmware change, or unknown device is a blocker, never
   a reason to relax validation or reuse another printer's access code.

## Pitfalls

- “Full interaction” is an objective, not a firmware API guarantee. See the
  exact [control contract](references/controls.md) and live qualification gaps.
- LAN Only/Developer Mode can change cloud features and printer security. Do not
  change modes, downgrade firmware, or extract credentials to unlock functions.
- Self-signed TLS requires an independently trusted certificate/name and pin;
  no `CERT_NONE`, hostname-disable flag, automatic trust-on-first-use, or fallback.
- Discovery candidates must not receive credentials. This draft does not scan
  networks or automatically enroll devices; manual enrollment is explicit.
- Installing a category bundle supplies the skill but does not launch a nested
  MCP manifest. Use the individual plugin after separately authorized installation.
- Never echo raw reports, file names, serials, IPs, access codes, or network errors
  into public issues/PRs. Camera images and model content are private user data.
- The MCP process shares the operator's local trust boundary. A malicious same-user
  process can change the private registry or environment; this plugin is not an
  isolation boundary against a compromised operator account.

## Verification

Run `python3 scripts/test_plugin.py` and inspect the acceptance matrix. Verify
an actual host initializes the process, discovers five tools, and calls
`p2s_capabilities` before claiming host availability. Require separately approved,
identity-verified P2S tests before claiming live compatibility. Repository-wide
validation commands are documented in the root README.

## Related skills

- [Security Best Practices](../../software-dev/security-best-practices/SKILL.md)
- [Systematic Debugging](../../software-dev/systematic-debugging/SKILL.md)
