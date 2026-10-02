# Setup and enrollment

## Offline review

Python 3.12+ is the only runtime requirement. No runtime downloads, SDK import,
network scan, or printer contact happens on startup. From the skill root:

```bash
python3 scripts/test_plugin.py
python3 scripts/server.py --demo
```

The second command waits for MCP JSON-RPC on stdin; it is not a chat CLI.
Use `initialize`, `notifications/initialized`, `tools/list`, and `tools/call`.
The regression test exercises this exact subprocess path with a harmless
capability call and synthetic status call.

`mcp.json` launches `python3 ${PLUGIN_ROOT}/scripts/server.py` over stdio.
The Codex compatibility manifest connects this file with `mcpServers`.
Use the **individual** `broville-skill-bambu-p2s` package after source review
and separately authorized installation. Category bundles remain skills-only.

An installer copying only the skill is a valid workflow adapter, but it does
not register a new MCP server. Likewise, a delegated task can read the package
and run offline scripts even if it cannot call the parent host's MCP tools.
Report that boundary; do not claim tool availability from a manifest validator.
The root `plugin.json` is an Agent Plugins identity/presentation manifest;
Codex's overlay discovers the canonical root SKILL.md. Hosts requiring a fixed
`skills/` subdirectory must adapt discovery when packaging; this source layout
does not promise that every host loads its skill automatically.

## Operator-selected local files

Set `BAMBUP2S_FILE_ROOT` in the server launcher environment to a private, dedicated
artifact directory you have authorized the agent to inspect. Tool paths are
relative to this root. Do not use a home directory or filesystem root. No default
artifact root is inferred. No file contents or archive member names are returned.
Secure file access uses POSIX directory descriptors and `O_NOFOLLOW`; Windows
file inspection is refused until an equally strong native implementation exists.

## Separately approved live monitoring

This draft implements a minimal experimental MQTT 3.1.1 subscriber. It does not
claim P2S firmware compatibility. It never publishes a status request or control
message; if the firmware supplies no fresh QoS 0 status push, it times out.

Before enabling it, the owner must explicitly approve **read-only network access
to a specific printer** and supply/verify the following privately:

1. Actual printer model, serial, firmware, current network mode, and fixed private
   IPv4 address. Do not infer a current firmware version from the latest release.
2. The required mode for this firmware's status interface. LAN Only and Developer
   Mode changes require separate approval after reviewing vendor instructions and
   feature loss. This plugin neither detects nor changes those settings.
3. A legitimate locally supplied trust certificate and its independently verified
   TLS server name and leaf SHA-256 fingerprint. A printer certificate must be
   obtained through a vendor-supported or physically/out-of-band trusted process.
   Do not trust a certificate solely because the target address presented it.
   This repository has **not established that P2S offers such an enrollment path**.
   If no trustworthy certificate/name is available, integration is blocked.
4. An operator-provided eight-character access code. Do not extract Studio/Handy
   credentials, call private cloud endpoints, or impersonate official clients.

Keep an enrollment directory outside the installed plugin and repository, under
operator-only write control. Copy `templates/devices.example.json` there. Each
entry has exactly these fields (values below describe the contract, not an
actual printer record):

| Field | Contract |
|---|---|
| `id` | Unique lowercase operator alias, up to 48 characters |
| `model` | `P2S` only |
| `serial` | Independently approved serial, alphanumeric 6–32 characters |
| `address` | Fixed RFC1918 IPv4; no DNS, loopback, link-local, public IP, or URLs |
| `tls_name` | Independently approved certificate SAN/hostname |
| `ca_file` | Contained basename ending `.crt`, in the enrollment directory |
| `certificate_sha256` | Independently verified lowercase 64-digit leaf fingerprint |
| `secret_env` | Dedicated variable named `BAMBUP2S_SECRET_` plus uppercase suffix |
| `firmware` | Actual recorded four-component, two-digit version |
| `monitor_approved` | `false` initially; owner sets `true` only after exact read-only approval |

The registry contains `version: 1` and at most 32 `devices`. Alias, serial,
address, certificate pin and secret reference must all be unique. A printer
sharing a vendor certificate with another device cannot satisfy this release's
individual identity requirement; stop rather than weakening the binding.

Validate offline:

```bash
python3 scripts/server.py --check-registry ./private-state/devices.json
```

Validation checks schema and local certificate-file presence only, not ownership,
certificate authenticity, trust provenance, mode, firmware compatibility, or
printer reachability. An empty registry validates but enrolls no device.

Only after approval, select `BAMBUP2S_REGISTRY` in the trusted launcher's environment
and supply each access code through its configured secret environment variable.
Use an operator-controlled secret manager to inject it without placing literal
codes in manifests, command arguments, shell history, source, or logs. This draft
has no keychain-extraction logic. Environment variables are private to the process
trust boundary, not protected against a compromised same-user process or debugger.
Host environment forwarding is host-specific; verify it without printing secrets.

TLS requires the certificate chain, hostname, validity interval and enrolled pin.
Credentials are read and sent only after these checks. Connections go to the
registry's fixed address on port 8883. There is no endpoint override in any tool.
A DHCP or certificate change requires reviewed re-enrollment; no auto-rebinding.

## Next qualification gates

The first live test requires separate permission, trusted TLS identity, and the
actual firmware/mode. Limit it to one status subscription with no publish or mode
change. Record the outcome privately. Camera, FTPS upload, remote start and other
controls need their own documented interface and identity review, approval
mechanism, tests, and explicit live acceptance. Do not install/enable this draft,
stream a camera, upload the prepared model, or change the printer as part of an
offline code review.
