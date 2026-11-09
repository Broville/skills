# Ponytail full — reviewed vendor copy

- Upstream: https://github.com/DietrichGebert/ponytail
- Reviewed release: `v5.3.3`
- Reviewed commit: `7801d061243d7b753bad0e0b3c057cd250b11755`
- License: MIT (see LICENSE-MIT)
- Copied file: `skills/ponytail/SKILL.md`
- Upstream SHA-256: `9badd22a32e19cb884e46dfa8d3aae82bb81dfa5484105b8b4f0262df823a509`

## Review boundary

Only the text skill and license were copied. No plugin manifest, lifecycle hook, Node package, executable, webhook, or networked component was copied or run.

## Findings

- Upstream full mode is the documented default. Dealer deployment must explicitly set `full` for deterministic behavior.
- Lifecycle hooks execute Node.js commands automatically when the full plugin is installed. This vendor copy intentionally excludes hooks.
- The Claude band reads transcript metadata and can POST task metadata to an optional webhook. Keep the band/webhook disabled unless explicitly approved.
- Do not install from mutable `main`; use the reviewed release commit above.
