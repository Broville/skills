---
name: "emil-design-eng"
description: "Implement and review polished frontend interactions and animations. Use when UI motion, easing, timing, hover behavior, or component details need Emil Kowalski's design engineering guidance."
license: "MIT"
compatibility: "Open Agent Skills format. Requires access to the target UI source and supported browser tooling; see Prerequisites."
metadata:
  author: "Broville contributors"
  version: "1.0.0"
  platforms: "[\"linux\", \"macos\", \"windows\"]"
  triggers: "[\"UI interactions or animations need implementation or review\", \"A frontend needs polished timing, easing, gesture, hover, or focus behavior\"]"
  inputs: "[{\"name\": \"target_ui\", \"description\": \"UI source, product constraints and requested interaction\", \"required\": true}]"
  outputs: "[{\"name\": \"verified_ui\", \"description\": \"Implemented or reviewed interface with relevant motion and accessibility evidence\"}]"
  tags: "[\"frontend\", \"animation\", \"design-engineering\"]"
  related-skills: "[\"design-taste-frontend\", \"frontend-ui-engineering\", \"web-accessibility\"]"
  source: "emilkowalski/skills@2d228630ba1446365f614a108cb8252f1feda202"
  source-url: "https://github.com/emilkowalski/skills"
---

# Emil Design Engineering

## Description

Apply Emil Kowalski's practical animation and interaction guidance to the requested UI. Preserve the user's brief, existing design system, stack and accessibility requirements. The full, unchanged upstream guidance is in [references/emil-playbook.md](references/emil-playbook.md).

## Prerequisites

- The target source, project instructions and an interaction brief.
- An existing way to run the UI and inspect it through the host's supported browser.
- Read [references/PROVENANCE.md](references/PROVENANCE.md) and [references/UPSTREAM-LICENSE.txt](references/UPSTREAM-LICENSE.txt) when reviewing or redistributing this package.

## Steps

1. Inspect the target's instructions, components, styles and existing motion patterns.

   ```bash
   rg --files | rg '(AGENTS|README|DESIGN|package.json|theme|tokens|css|tsx|jsx)'
   ```

   Expected result: relevant project guidance, styling and component sources are identified.

2. Read the relevant sections of the upstream playbook. Choose motion from the interaction's purpose, frequency and user input. Use the project's existing primitives; dependency examples do not authorize new installations.
3. Implement the requested change. Prefer interruptible transitions for frequent state changes, explicit properties, appropriate transform origin, short purposeful timing and touch-safe hover conditions. Provide reduced motion and visible keyboard focus.
4. Run the project's existing development command and inspect pointer, keyboard and touch behavior at relevant widths. Check rapid reversal, interruption and repeat triggers. Use only the host's supported browser interfaces; don't take over unrelated task tabs.
5. Run the target's established checks and `git diff --check`. Expected result: applicable checks pass and the diff has no whitespace errors.

## Pitfalls

- Treating playbook heuristics as authority over product requirements, accessibility or project policy.
- Adding motion to every interaction, delaying task completion or hiding content behind animations.
- Introducing a new animation library because the source mentions it.
- Claiming visual or device verification from code inspection alone.
- Importing all upstream skills when only the primary design engineering skill is requested.

## Verification

Confirm the intended interaction works at desktop and phone widths, with pointer and keyboard input. Confirm reduced motion, visible focus, rapid interruption and repeated activation. Record the actual checks and any unavailable device coverage.

## Cross-References

- [references/emil-playbook.md](references/emil-playbook.md) — unchanged pinned upstream guidance.
- [references/PROVENANCE.md](references/PROVENANCE.md) and [references/UPSTREAM-LICENSE.txt](references/UPSTREAM-LICENSE.txt) — source and license.
- `design-taste-frontend` — visual direction from a brief.
- `frontend-ui-engineering` — production UI implementation.
- `web-accessibility` — accessibility verification.
