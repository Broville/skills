# Threat model

## Assets and trust boundaries

Protect access codes, printer identity, operator intent, physical safety, private
models, local files and camera images. MCP arguments, printer messages, archive
contents, and discovery candidates are untrusted. The operator-controlled launcher,
registry, trust certificates and secret-manager injection form the local trust
boundary. They are not writable through MCP tools.

The threat model includes malicious tool arguments, prompt injection in metadata,
a wrong printer/endpoint, LAN interception, compromised status payloads, archive
bombs, local file traversal, accidental starts and misleading success claims.
A compromised same-user account can replace the registry or launch another
process; deployment under a separate constrained account is an operator decision.
This plugin cannot isolate itself from its own process owner.

## Enforced controls

- **Credential routing:** tools accept an enrolled alias, never a host, port,
  access code, secret reference, serial, CA path or TLS override. RFC1918 IPv4 only,
  port 8883 only, exact serial-bound report topic. Duplicate alias/serial/address/pin/
  secret references refuse enrollment. No DNS-based credential routing.
- **TLS identity:** standard certificate-chain, validity and hostname checks,
  TLS 1.2 minimum, plus exact independently enrolled leaf SHA-256 pin. Access code
  lookup happens only after successful authentication. No automatic certificate
  capture/trust, disabled checks, credential-bearing unverified handshake, proxy,
  cross-service trust reuse, or plaintext fallback. Unverifiable self-signed
  printers stay blocked. MQTT encryption alone is not identity verification.
- **Secrets:** only a trusted launcher-selected environment reference is read;
  no credential input/output tools, extraction logic or literal manifest secrets.
  Secrets are never logged. Exceptions return fixed public messages. Raw status
  payloads, serials, addresses, file names and certificate paths are omitted.
- **Physical actions:** no publish/write/camera adapter exists. Named previews
  require an enrolled ID and exact bounded input; a model cannot self-approve.
  No heater, motion, firmware, private cloud API, or G-code passthrough tool.
- **Files:** operator-chosen root; directory-descriptor traversal, no symlinks,
  nonblocking regular-file check. Snapshot is bounded before hash/inspection.
  128 MiB compressed/file limit; 2048 archive entries; 2 MiB central-directory
  allocation limit checked before ZIP construction; 128 MiB/member, 512 MiB total
  inflation, 100:1 per-member ratio. Reject ZIP64/multidisk, encrypted/linked
  members, unsupported codecs, traversal, duplicate paths and CRC errors.
  Stream validation in 64 KiB chunks, never extract files or parse XML.
- **Protocol:** newline-delimited UTF-8 JSON-RPC; stdout protocol only; bounded
  JSON/MQTT packets (256 KiB), ten-second status deadline and 64-packet cap; no
  broad HTTP/network listener. MQTT CONNECT and QoS 0 SUBSCRIBE only, no PUBLISH.
  Reject retained/stale, wrong-topic, unexpected/QoS>0 messages. Reports can be
  partial; this release does not merge historical state or translate HMS codes.
- **Prompt injection:** no archive text or raw printer string is returned. Tool
  outputs whitelist numeric fields and known state names. Instructions in files,
  model names, status or camera content must never become authorization.

## Residual limits and qualification blockers

A certificate pin is meaningful only if enrollment provenance independently binds
it to the physical device. This release validates the supplied record; it cannot
establish that fact. Certificate authenticity/name availability on actual P2S
firmware remains untested. Shared vendor leaf certificates fail the unique-device
policy. Private IPs can still identify hostile LAN devices; the approved pin and
credential binding are mandatory.

The experimental MQTT subscriber uses an interoperability hypothesis (`bblp`,
port 8883, `device/<serial>/report`, selected `print` fields), not a published P2S
command API guarantee. No actual printer was contacted during development. A
firmware change or unsupported status shape is a blocker, not fallback permission.
Use process/sandbox limits when deploying against untrusted files; bounded input
still consumes bounded CPU and memory. Windows secure file inspection is blocked.

Environment injection does not encrypt secrets in process memory or protect
against debugger access. Do not let an agent read the secret-manager source or
launcher configuration. Public artifacts must exclude enrollment records, model
files, images, access codes and device-specific evidence. Camera and FTPS would
introduce distinct privacy/data-channel trust boundaries and are not implemented.
