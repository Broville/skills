# Dealer coding modes — reviewed staging bundle

This directory stages reviewed, text-only copies for Dealer:

- `caveman-ultracave/`: Caveman `ultracave`, Apache-2.0, upstream `v4.1.0` at `1e91f1306d602d4ca23618701b1185575ae1869b`.
- `ponytail-full/`: Ponytail `full`, MIT, upstream `v5.3.3` at `7801d061243d7b753bad0e0b3c057cd250b11755`.

No third-party executable, installer, hook, dependency, MCP server, or network component is included.

## Review verification

The reviewed deployment used local skill discovery and confirmed both modes were enabled. A real chat probe produced terse Caveman output, preserved a security warning, and ended with Ponytail's skipped-checks/risk lines. No upstream installer, hook, telemetry, webhook, MCP server, or cloud-routing component was installed or activated. Repeat this verification in the target environment without copying deployment credentials or machine-specific paths into the repository.
