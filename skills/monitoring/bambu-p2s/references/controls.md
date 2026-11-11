# Permission and control contract

This release exposes five read-only MCP tools. Annotations are advisory; actual
implementation and the absent write adapter enforce the boundary. No HTTP
listener or arbitrary command dispatcher exists.

| Tool | Inputs | Effect and limits |
|---|---|---|
| `p2s_capabilities` | None | Offline scope/blocker report |
| `p2s_list_devices` | None | Enrolled aliases, model, recorded firmware and approval state; no discovery |
| `p2s_status` | `device_id` | Synthetic demo report, or explicitly enrolled experimental TLS MQTT subscription |
| `p2s_inspect_artifact` | Relative `artifact` | Local container validation and snapshot SHA-256; POSIX only |
| `p2s_preview_action` | `device_id`, `action`, optional `artifact`, `settings` | Non-executable plan; no network, writes, camera or approval issuance |

## Desired operations and present support

| Requested operation | Implemented behavior | Additional gate |
|---|---|---|
| Status, errors, progress, temperatures | Whitelisted partial MQTT report fields; numeric error/HMS codes | Actual P2S firmware/status topic/auth/TLS qualification |
| Camera | Privacy-sensitive blocked preview; pure exact-endpoint validator | Documented P2S stream protocol, per-service TLS identity, explicit stream approval |
| File/3MF upload | Bounded local inspection + snapshot transfer plan; pure passive endpoint validation | Qualified FTPS/other vendor path, data-channel authentication/identity, digest reconciliation |
| Start print | File/identity/settings-bound blocked preview | Qualified vendor command + enforced exact-action owner approval |
| Pause/resume/cancel | Named blocked previews plus fresh job-state gates; pure vendor-shape fixtures and conservative ack correlation | Live command/state/ack qualification, native physical checks and owner approval |
| Preparation settings | Validate intent for plate and Boolean leveling/flow/vibration/timelapse/AMS toggles | P2S/firmware-specific supported settings; no inferred device changes |
| AMS 2 Pro four-slot mapping | Up to four intent slot indices 0–3, requires `use_ams: true` | Verify actual AMS, loaded materials, mapping semantics and firmware support |
| Device enrollment/multiple P2S | Validate explicit local records and select unique approved aliases | Owner checks physical identity, legitimate cert provenance and access mode |
| Automatic network discovery | Excluded | Future discovery must be approved, bounded, secret-free, and separate from enrollment |
| Manual heater/motion control, arbitrary G-code | Excluded | Separate safety design; no broad passthrough planned |
| Firmware, cloud login, LAN/Developer Mode, credentials | Excluded | Separate user-reviewed native setup; never a tool-side workaround |

A `.gcode` file is hashed but never parsed as commands, executed, uploaded, or
claimed safe. A `.3mf` is treated as an untrusted ZIP, not as an instruction
source. Candidate `Metadata/plate_N.gcode` names establish only plate presence,
not slicing compatibility. Settings are plain intent; no arbitrary nested JSON,
URLs, custom G-code, speed, temperature, or network fields are accepted.

## Approval requirements for a future write adapter

A future implementation must show the exact operation and physical consequence
before execution. Approval must bind printer identity/certificate, file snapshot
and digest, selected plate, full settings, current job/state, and expiry. Print
start/resume can cause heat and motion; cancel can irreversibly spoil a job; camera
reveals the surrounding space. Do not treat them as blanket-authorized commands.

The operator approval channel must be independent of model-controlled tool inputs.
An `approved: true` field, an agent's statement, a preview digest, or an MCP tool
annotation is not owner approval. Use single-use authorization with short expiry,
state revalidation and replay protection before effects. Never blindly retry a
start or upload after an ambiguous connection/ack; query state and reconcile first.
Fail closed on identity, file, setting, job or firmware changes. Preserve native
printer physical safety interlocks. The current release has **no execution tool**,
so it grants no authorization token and cannot perform these operations.

## Offline protocol contracts

`protocol_contracts.py` is pure validation: it has no sockets, publisher, SDK,
subprocess or MCP execution endpoint. Public Studio source supports the tested
pause/resume/stop field shapes; it does not establish the installed P2S firmware's
acceptance. Synthetic fixtures are original facts-based examples, not captured
printer packets. Cancel fixtures bind a numeric job ID; pause/resume fixture
shapes have no job field, so any future sender must revalidate the exact job
independently immediately before execution.

Previews use only an internal status observation received within ten seconds,
not caller-supplied status. Unknown job identity, conflicting states, stale or
future timestamps, and incompatible/transitional states fail the precondition.
An attempted status read invalidates earlier evidence even when the read fails.
A precondition marked ready is only eligibility for review; it cannot verify
physical safety, permit a command, or substitute for native printer interlocks.
The opaque job digest is a binding, not anonymization or a secret.

Even a correlated success acknowledgement returns `completed: false` and
`retry_allowed: false`; reported job state must be reconciled separately.
Upload plans forbid overwrite/resume and require independent remote digest
reconciliation. A passive reply may only select the enrolled IP and documented
50000–50100 ports, with separately verified TLS on the data channel. Camera hints
must match an independently approved RTSPS endpoint exactly; authentication,
real stream path and service identity are still unqualified.
