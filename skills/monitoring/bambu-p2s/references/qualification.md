# Next live qualification bundle

Offline development is authorized independently of live setup. Collect this
bundle before proposing one read-only test; missing technical evidence cannot
be replaced by permission alone.

| Dependency | Required private evidence or decision |
|---|---|
| Actual printer | Owner-verified P2S identity, fixed private address, serial, installed firmware version, current LAN/cloud and Developer Mode state; record AMS configuration separately |
| Firmware access requirements | Current vendor instructions for that exact firmware; distinguish status push access from write/camera authorization |
| Legitimate TLS enrollment | Independently authentic CA/chain, SAN/server name and device-bound leaf pin through a supported vendor or physically trusted process; provenance recorded before any connection |
| Credential entry | Owner inputs access code into their secret manager; trusted launcher injects the dedicated environment variable privately; no chat, manifest literal, CLI argument, shell history, extraction or displayed value |
| First network permission | One explicit subscription to that enrolled printer on TLS MQTT 8883, ten-second limit, CONNECT/SUBSCRIBE only; no PUBLISH, discovery, camera, transfer or mode change |
| Observation handling | Whitelisted status only; private compatibility notes; no raw reports/device identifiers in public artifacts; stop on mismatch, timeout or unsupported shape |

There is currently no established vendor-supported P2S certificate export and
name-enrollment procedure in this research. Do not capture and trust the presented
certificate automatically. A physically obtained certificate still needs an
independent identity/provenance check. If that legitimate path is unavailable,
live monitoring remains blocked and a supported vendor integration must be
investigated instead.

If the installed firmware requires LAN Only or Developer Mode, make that a
separate concrete decision after reviewing current vendor instructions and the
features lost or altered, including cloud/Handy/remote use and authorization
protections. Never change mode as a hidden prerequisite to a status test.
The plugin implements no security-setting mutation or downgrade.

The smallest approval request is: authorize one bounded read-only status
subscription to the privately identified, enrolled printer, with its verified
certificate identity and secret-manager injection. This approval permits no
configuration changes, printing, transfer or camera access. It becomes actionable
only after the technical dependencies above are satisfied.

Later camera, upload and job-control acceptance each require a qualified interface,
per-service verified identity, an independent exact-action approval mechanism,
firmware-specific state reconciliation, and explicit live scope. Existing prepared
jobs must remain unchanged and unsent until their own approval. Offline command
fixtures or a ready precondition cannot authorize effects.

## Actual operating host

First verify startup, discovery and a harmless capability call in the task that
will operate the printer. Native per-command CLI proof does not make this plugin
installed, enabled or callable in a desktop/dot/delegated task. A cloud task may
lack the local printer's network and MCP inventory. Treat that as an architecture
dependency rather than asking the model to invent a tool path.
