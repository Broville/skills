# Vendor interface and host feasibility

Evidence checked 2026-10-02. This research establishes scope and limitations;
it does not qualify a particular P2S firmware or permission to change its setup.

## Primary sources

- [Bambu firmware authorization announcement](https://blog.bambulab.com/firmware-update-introducing-new-authorization-control-system-2/)
  describes status pushes separately from critical camera, print and physical
  controls. This announcement initially covers X-series rollout, so it cannot
  certify a P2S command schema or current firmware behavior.
- [Bambu integration clarification](https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/)
  describes supported integration options, including Developer Mode. It does not
  publish a complete P2S MQTT/FTPS/camera command protocol.
- [Third-party integration wiki](https://wiki.bambulab.com/en/software/third-party-integration)
  documents the authorization and mode distinction. Full-page fetch was blocked
  during this research; official indexed excerpts were available. No exact
  private SDK interfaces were inferred from those excerpts.
- [Official Developer Mode setup](https://wiki.bambulab.com/en/knowledge-sharing/enable-developer-mode)
  explicitly includes H2/P2S in indexed material and places Developer Mode after
  LAN Only mode. Full-page fetch was blocked during research. Verify the live
  instructions before approved setup, and explain cloud/Handy/remote feature loss.
- [Official P2S firmware history](https://wiki.bambulab.com/en/p2s/manual/p2s-firmware-release-history)
  is the appropriate source for release requirements. The owner's actual installed
  version is unknown until supplied/read with approval; “updated today” is not a
  compatibility record. Do not downgrade or install firmware for this plugin.
- [Bambu Studio source/license](https://github.com/bambulab/BambuStudio)
  is AGPL-3.0 and identifies its optional network plugin as using non-free
  libraries. This MIT implementation copies no Studio/community code, bundled
  networking binaries, signing keys, or private SDK. A future dependency/snippet
  needs its own compatibility review rather than inheriting this release's license.
- [MQTT 3.1.1 specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)
  governs this original minimal CONNECT/SUBSCRIBE implementation. MQTT framing is
  a standard; vendor usernames/topics/report fields are unqualified integration
  assumptions and are clearly marked experimental.
- [MCP stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
  defines newline-delimited JSON-RPC and protocol-only stdout. The server implements
  the minimal tools lifecycle, not an HTTP service, MCP App, or arbitrary proxy.

## Transport decision

| Candidate | Current conclusion |
|---|---|
| Status MQTT over TLS | Original bounded subscriber implemented; separately enrolled/approved only; fake TLS-tested; actual P2S untested |
| Remote commands | No public P2S schema/ack and exact-action approval contract qualified; blocked |
| FTPS upload | Data-channel address/TLS/identity and firmware path unqualified; blocked |
| P2S camera | Actual stream protocol/service identity/auth unqualified; blocked; do not reuse a P1 camera assumption |
| Official Connect/partner SDK | Legitimate option to investigate; no automation interface/SDK grant established; no impersonation or key extraction |
| Developer Mode | Documented option, separately reviewed security/feature-loss decision; plugin never changes mode |
| Local print preparation | Safe to validate selected artifacts offline; no slicing or physical compatibility claims |

No credential-bearing transport can be activated by a tool-selected endpoint.
The read-only monitor authenticates the supplied trust chain/name and enrolled
pin before it reads the supplied access code. If a valid independently trusted
P2S certificate/name cannot be obtained legitimately, even monitoring stays blocked.

## Host boundaries

The target host has Python and the installed Codex CLI. The standalone process
is tested through actual stdio startup, tool discovery and harmless calls, with
synthetic data. Marketplace discovery and a manifest alone are weaker evidence.
Per-command native Codex app-server verification is recorded in the acceptance
matrix when available. No installed plugin/cache/config is modified during tests.

Delegated/cloud task tool inventories may omit repository-scoped MCP tools even
when the parent desktop has them. Re-check tool availability in the task that
will operate the printer. A stdio server is a local hardware integration; it
cannot supply LAN access to a web/mobile/cloud host by existing in GitHub.

## Provenance

All runtime code and tests are original for this repository under its MIT license.
Runtime dependencies: Python standard library only (PSF licensing). Offline TLS
regressions use the host OpenSSL executable; generated certificates/keys are
synthetic, temporary and never packaged. Marketplace validation uses the
repository's existing PyYAML and skills-ref developer dependencies. No community
printer plugin was installed, vendored, copied or granted credentials.
