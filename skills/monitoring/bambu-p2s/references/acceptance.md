# Acceptance matrix — 0.2.0 draft

Evidence date: 2026-10-02. “Implemented” describes code, “offline-tested” describes
synthetic tests, and “live-untested” describes external compatibility. No printer
was contacted; no credentials were supplied and no model was sent or changed.

| Outcome | Implementation | Evidence | Remaining limit |
|---|---|---|---|
| Local stdio startup/discovery/call | Five tools, bounded MCP tools lifecycle | Real Python subprocess initialize/list/capabilities/demo call; native host proof below | Desktop installed-plugin/chat availability separate |
| Status/errors/progress | Experimental TLS MQTT subscription, numeric/enum normalization, numeric job binding and modern job-state fields | Real TLS socketpair fake printer; CONNECT/SUBSCRIBE only | Actual P2S auth/topic/report/firmware untested; partial reports only |
| TLS identity/credential isolation | Chain, hostname, pin before credential lookup | Synthetic trusted TLS succeeds; wrong pin/name/CA fails without credentials | Legitimate P2S certificate enrollment path unestablished |
| Multiple printer identity | Explicit aliases; unique serial/address/pin/secret | Synthetic two-device selection and enrollment collision tests | No real printers enrolled; no discovery scan |
| Local 3MF/G-code preparation | Snapshot digest; bounded ZIP/plate presence inspection | Traversal/symlink/FIFO, inflated archives, duplicate paths and limits tested | POSIX only; no slicing, compatibility or physical safety certification |
| Upload/start settings | Strict non-executable intent previews, snapshot-bound transfer contract | File/printer digest binding, plate/toggle/AMS bounds; passive endpoint/port/TLS policy fixtures | FTPS/start adapter and firmware semantics blocked |
| Pause/resume/cancel | Non-executable named previews | Pinned vendor request shapes; fresh/internal job-state gates; ack correlation without completion/retry claims | Offline contract implemented; actual command/ack/live state compatibility and physical safety unqualified |
| Camera | Blocked privacy-sensitive preview | Exact operator-selected RTSPS endpoint validation; no credentials in URIs; redirect/plaintext refusal | P2S protocol/auth/service TLS identity unqualified |
| Exact-action approval | Enforced absence of execution path | `approved` argument refused; no write tool or MQTT PUBLISH | Future independent single-use approval channel required |
| Firmware/mode/security setup | Documented separate approval boundary | No setup mutation implementation | User approval, actual firmware and feature-loss review required |
| Marketplace | Individual native MCP overlay; bundles skills-only | Generator/validator/composition/installer checks | Draft PR must be reviewed and merged before main listing exists |

## Native host proof

The installed Codex CLI 0.159.2 is used with temporary per-command MCP
configuration, an offline synthetic server, and a nonpersistent protocol test
session. No model turn, plugin installation, persistent host configuration change,
cache edit or printer call is performed. Startup, `tools/list`, and a
`p2s_capabilities` call must succeed through native `mcpServerStatus/list` and
`mcpServer/tool/call`; raw private host logs are not published.

Native marketplace listing also discovered `broville-skill-bambu-p2s` version
`0.2.0` through a local per-command catalog override, with `installed: false`
and `enabled: false`. No other marketplace entry was installed or changed.

Native discovery initially found a standard `_meta` field in `tools/list` which
the server refused. The implementation and regression now accept that metadata;
this is why mock/subprocess success alone was insufficient. Final native result: startup succeeded, all five tools were discovered with
`toolsError: null`, and the host called `p2s_capabilities` with `isError: false`.
Its result confirmed demo mode, no startup network and blocked live controls.

This proof does not establish installed-plugin discovery in the desktop UI,
availability in a delegated/cloud task, or a live P2S connection. Those require
separately authorized setup and tests in the actual operating task.

## Repeatable offline verification

From this skill directory:

```bash
python3 scripts/test_plugin.py
```

From the repository root, using the existing validation dependencies:

```bash
python scripts/validate_skills.py
python scripts/test_install_skills.py
python scripts/validate_marketplace.py
python scripts/build_marketplace.py --check
python scripts/test_marketplace.py
```

The suite contains 22 security regressions. Security regressions also run in the repository's Linux/macOS/Windows CI matrix.
Windows explicitly skips POSIX artifact and TLS socketpair fixtures; Windows
secure file access is blocked at runtime rather than silently falling back.

## Release decision

Reviewable foundation, not full interaction complete. Before enabling live status:
follow the [next qualification bundle](qualification.md), obtain exact-printer read-only approval, record firmware/mode, establish legitimate
certificate provenance and name, inject the operator-supplied code privately, and
perform a single qualified status test. Keep write/camera controls unavailable
until their separate protocol/security/approval/physical acceptance gates pass.
