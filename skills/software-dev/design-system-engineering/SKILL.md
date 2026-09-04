---
name: design-system-engineering
description: Build or evolve governed web design systems with semantic tokens, reusable components, documented states, and tests.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos, windows]
trigger:
  - User asks to create, extend, audit, or migrate a web design system
  - Work involves design tokens, theming, component libraries, Storybook, or reusable UI primitives
  - A product has inconsistent styling or duplicated components that need governed consolidation
inputs:
  - name: target
    description: Repository, package, theme, token set, or component family in scope
    required: true
  - name: consumers
    description: Applications, themes, platforms, or packages that consume the system
    required: false
outputs:
  - name: system_contract
    description: Token layers, component APIs, supported states, and compatibility boundaries
  - name: migration_and_evidence
    description: Incremental adoption plan plus rendered, behavioral, accessibility, and regression evidence
metadata:
  hermes:
    tags: [design-system, tokens, components, storybook, accessibility]
    related_skills: [frontend-ui-engineering, react-composition-patterns, web-accessibility, web-design-guidelines]
---

# Design System Engineering

## Description

Build or evolve a web design system as a governed product: shared decisions become semantic tokens, public component contracts, complete interaction states, documentation, and regression gates. Preserve an existing system unless the user explicitly authorizes replacement; visual consistency alone is not a reason to break consumers.

## Prerequisites

- Repository instructions, package manifests, styling configuration, and consumer applications.
- Existing tokens, themes, components, stories, screenshots, and brand guidance when present.
- A known compatibility target for browsers, frameworks, themes, and product surfaces.

## Steps

1. Inventory the incumbent system and its consumers before proposing a new abstraction.

   ```bash
   rg --files | rg '(tokens?|themes?|styles?|components?|stories|storybook|tailwind|design-system|figma)'
   ```

   Expected result: sources of visual truth, component packages, documentation, and likely consumers are identified. Search imports and CSS-variable usage to confirm actual ownership.

2. Define the system contract and scope:

   - supported products, themes, density modes, locales, and browser range;
   - source of truth and generated artifacts;
   - versioning, ownership, and deprecation policy;
   - which values are global decisions versus component-local implementation details.

3. Model tokens in layers:

   - **primitive tokens** describe raw palette, scale, duration, and typography values;
   - **semantic tokens** express roles such as text, surface, border, action, focus, and status;
   - **component tokens** exist only when a reusable component needs a stable override point.

   Prefer aliases over copied values and validate circular or missing references. When interoperability is required, follow the stable DTCG 2025.10 format described in `references/standards-and-quality-gates.md` rather than inventing a near-standard schema.

4. Define each component as a public contract: anatomy, variants, sizes, content rules, controlled/uncontrolled behavior, slots, events, theming hooks, and deprecation plan. Specify default, hover, focus-visible, active, selected, disabled, loading, empty, error, success, and overflow behavior where applicable.

5. Implement the smallest coherent vertical slice: token source, one representative component family, documentation/story states, and consumer integration. Do not launch a sweeping rewrite before the contract works end to end.

6. Make accessibility structural. Start with native HTML, preserve accessible names and focus order, follow the relevant ARIA APG pattern for custom widgets, support zoom/reflow and reduced motion, and use `web-accessibility` for the detailed WCAG 2.2 workflow.

7. Create executable examples or stories for every supported state and meaningful combination. Test behavior in a real browser, run automated accessibility heuristics, and use deterministic visual comparisons in a consistent rendering environment when baselines are part of the project.

8. Migrate consumers incrementally. Provide compatibility aliases or codemods only when they reduce verified risk; do not maintain two permanent sources of truth. Document breaking changes and remove deprecated tokens/components only through the repository's migration policy.

9. Run package tests, consumer builds, visual and accessibility checks, and:

   ```bash
   git diff --check
   ```

   Expected result: the representative consumer uses the governed source, documented states render, required checks pass, and no unreviewed baseline update hides a regression.

## Pitfalls

- **Tokenizing everything:** Values used once and carrying no reusable decision add indirection rather than governance.
- **Primitive leakage:** Product code that consumes raw palette values bypasses semantic theming and makes future changes expensive.
- **Component explosion:** One component per visual permutation is as hard to maintain as one component with dozens of booleans.
- **Screenshot-only documentation:** A static frame does not prove keyboard, state, content, or responsive behavior.
- **Baseline laundering:** Never accept visual snapshots merely to make CI green; review the rendered change and its intent.
- **Big-bang migration:** Prove a vertical slice and compatibility path before changing every consumer.
- **Framework replacement:** A design-system task does not authorize a new framework, CSS strategy, or component library.

## Verification

1. One authoritative token source is identified, and aliases resolve without cycles.
2. Semantic roles cover both light/dark or other in-scope themes without raw-value leakage in the representative consumer.
3. Public component contracts and all applicable states are documented and exercised.
4. Keyboard, focus, accessible-name, zoom/reflow, reduced-motion, and contrast checks pass for the representative slice.
5. Visual comparisons were reviewed in a stable environment; intentional baseline changes are explicit.
6. Package tests and at least one real consumer build pass.
7. Ownership, versioning, deprecation, and migration responsibilities are recorded.

## Cross-References

- `frontend-ui-engineering` — implementation architecture for product UI.
- `react-composition-patterns` — React-specific public component APIs.
- `web-accessibility` — WCAG 2.2 implementation and audit workflow.
- `web-design-guidelines` — broader web-interface standards audit.
- `references/standards-and-quality-gates.md` — DTCG, WCAG, ARIA, Storybook, and Playwright evidence model.
