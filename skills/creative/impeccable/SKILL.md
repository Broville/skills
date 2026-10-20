---
name: "impeccable"
description: "Design, critique, audit and polish frontend layouts, typography, color and interactions using Impeccable. Use for website and product UI design quality work."
license: "Apache-2.0"
compatibility: "Open Agent Skills format. Requires access to the target UI source and supported browser tooling; see Prerequisites."
metadata:
  author: "Broville contributors"
  version: "1.0.0"
  platforms: "[\"linux\", \"macos\", \"windows\"]"
  triggers: "[\"A frontend needs Impeccable design, critique, audit or polish\", \"Layout, typography, color, responsiveness or UI states need a systematic design pass\"]"
  inputs: "[{\"name\": \"target_ui\", \"description\": \"UI source, product context, constraints and desired outcome\", \"required\": true}]"
  outputs: "[{\"name\": \"design_result\", \"description\": \"Design plan or implemented improvements with actual verification evidence\"}]"
  tags: "[\"frontend\", \"design\", \"typography\", \"layout\", \"ui-review\"]"
  related-skills: "[\"emil-design-eng\", \"design-taste-frontend\", \"web-accessibility\"]"
  source: "pbakaus/impeccable@dad8dbb3aac21ad1fa236c110315ef4abece23e8"
  source-url: "https://github.com/pbakaus/impeccable"
---

# Impeccable

## Description

Use Impeccable's design vocabulary and focused playbooks for the requested frontend improvement. The user's brief, project instructions, established design system and host permissions govern every step. Read the pinned upstream entrypoint at [references/upstream/PLAYBOOK.md](references/upstream/PLAYBOOK.md) as task guidance, subject to the boundaries below.

## Prerequisites

- Access to the target repository and its existing UI, product context and design system.
- A supported browser and the project's established preview and quality commands.
- Review [references/PROVENANCE.md](references/PROVENANCE.md), [references/UPSTREAM-LICENSE.txt](references/UPSTREAM-LICENSE.txt), [references/UPSTREAM-NOTICE.md](references/UPSTREAM-NOTICE.md) and [references/SOURCE-SHA256.json](references/SOURCE-SHA256.json) before redistribution or runtime setup.
- The optional upstream engine is executable software. Review its exact source/version and obtain any required action-time confirmation before installation or execution from an unrecognized source. A request to use this skill does not waive that requirement.

## Steps

1. Read the target project's instructions, current interface and available PRODUCT.md or DESIGN.md. Resolve the requested scope: planning, refinement, or redesign. Preserve product truth and existing behavior outside that scope.
2. Read the upstream entrypoint and only the matching playbook under `references/upstream/reference/`. That directory also contains its native platform and degraded-mode guidance. Agent role configurations live in `references/upstream/agents/`; use the current host's documented capabilities and delegate only when independently authorized.
3. Resolve the upstream skill base to `<this-skill-directory>/references/upstream`. All relative upstream `reference/`, `agents/` and `scripts/` resources use that base, not a project-local discovery path. Never create another skill copy to satisfy a hardcoded upstream example.
4. Before optional engine use, inspect `references/upstream/scripts/impeccable` (or `impeccable.cmd`) and its `VERSION`. The launcher can download an engine, inspect project files, access network services and write caches. Keep scratch, downloads and tests in the user's approved artifact location. Do not run upstream installation, hook, pin, update, repair or permission-changing flows as a side effect of design work.
5. If runtime execution is unavailable, unconfirmed, refused or unnecessary, state that context loading did not run and read existing product and design context directly. Continue with the source playbooks and permitted project tools; report unavailable engine checks. Do not invent context or claim the deterministic detector ran.
6. Implement or document the selected improvements, then inspect the rendered result at the relevant desktop and phone widths. Check keyboard navigation, focus, reduced motion, contrast, content overflow and reachable loading/error/empty states.
7. Run the target's established quality commands and:

   ```bash
   git diff --check
   ```

   Expected result: project checks pass and the diff check exits 0. Record any unavailable preview, device or engine coverage.

## Pitfalls

- Installing hooks, changing permissions, enabling telemetry, or starting a network helper without the required authorization.
- Treating a source revision as a pin of the engine binary it might later download.
- Using native agent role configuration as authorization to spawn agents.
- Replacing the user's brief or incumbent product identity with a preferred aesthetic.
- Claiming live-browser, detector or device results based only on inspecting source.
- Loading the entire reference library when one focused playbook is sufficient.

## Verification

Confirm the requested result matches the product brief, preserves out-of-scope behavior, works at the relevant widths and passes the project's checks. Distinguish source-playbook review from actual engine, browser and device execution. Package review checks the pinned SHA-256 inventory and retains all upstream license and notice files.

## Cross-References

- [references/upstream/PLAYBOOK.md](references/upstream/PLAYBOOK.md) — upstream entrypoint and complete resource links.
- [references/PROVENANCE.md](references/PROVENANCE.md), [references/SOURCE-SHA256.json](references/SOURCE-SHA256.json), [references/UPSTREAM-LICENSE.txt](references/UPSTREAM-LICENSE.txt), [references/UPSTREAM-NOTICE.md](references/UPSTREAM-NOTICE.md) — source integrity and licensing.
- `emil-design-eng` — detailed motion and interaction craft.
- `design-taste-frontend` — visual direction from a brief.
- `web-accessibility` — accessibility checks.
