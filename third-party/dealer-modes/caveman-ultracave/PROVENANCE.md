# Caveman ultracave — reviewed vendor copy

- Upstream: https://github.com/JuliusBrussee/caveman
- Reviewed release: `v4.1.0`
- Reviewed commit: `1e91f1306d602d4ca23618701b1185575ae1869b`
- License: Apache-2.0 (Caveman 3.0.0+; see LICENSE-APACHE-2.0 and upstream LICENSING.md)
- Copied file: `skills/ultracave/SKILL.md`
- Upstream SHA-256: `a8da5b0b3501b853e1b98f2ae09fe8dc9c0edf481b1d3fa9529f8557011c1ef8`

## Review boundary

Only the text skill and license were copied. No installer, hook, Node package, executable, MCP server, or networked component was copied or run.

## Findings

- Upstream default-mode configuration is `{"defaultMode":"ultracave"}` in `~/.config/caveman/config.json` or project-local `.caveman.json`.
- Upstream CLI telemetry is enabled by default unless disabled. Any Dealer deployment must set `DO_NOT_TRACK=1` or run the documented telemetry-off action.
- Routing/cloud can transmit prompt, system-prompt, tool-call/result, code, and image context. Keep routing/cloud disabled unless explicitly approved.
- The upstream installer pipes remote code into an interpreter. Do not use that installer blindly.
