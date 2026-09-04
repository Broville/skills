# Provenance

- Source: `microsoft/playwright-cli`
- Source tag: `v0.1.19`
- Source revision: `397ee39c83a651e1314cfb010b94e8a3aac11261`
- Source path: `skills/playwright-cli`
- Source license: Apache-2.0
- Source URL: https://github.com/microsoft/playwright-cli/tree/v0.1.19/skills/playwright-cli

The upstream `SKILL.md` and its nine Markdown references are vendored under `references/`. The Broville entrypoint removes tool-specific `allowed-tools` frontmatter, pins the fallback invocation, distinguishes this CLI-specific workflow from the existing environment-neutral `playwright` skill, and adds authorization, sensitive-state, session-ownership, and artifact-handling boundaries.

The command content remains pinned to the upstream source. The primary reference has one packaging-only adaptation: links to sibling references are made relative to their vendored location, and a transient snapshot example is rendered as a code path instead of a broken local hyperlink. The new Broville entrypoint is an adaptation and is prominently identified as such here.
