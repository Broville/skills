---
name: react-composition-patterns
description: Design scalable React component APIs with composition, explicit variants, clear state ownership, and React 19 awareness.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos, windows]
trigger:
  - User asks to design or refactor reusable React component APIs
  - React components have boolean-prop proliferation or tangled state ownership
  - Work involves compound components, providers, variants, render props, or React 19 ref APIs
inputs:
  - name: target
    description: Components or component-library API to design, review, or refactor
    required: true
outputs:
  - name: component_contract
    description: Explicit public API, ownership model, and supported variants
  - name: verified_refactor
    description: Behavior-preserving implementation and tests when changes are requested
metadata:
  hermes:
    source: vercel-labs/agent-skills@063bee94c3f4df8453406c830b0a7df0f2860278 (MIT)
    source_url: https://github.com/vercel-labs/agent-skills/tree/063bee94c3f4df8453406c830b0a7df0f2860278/skills/composition-patterns
    tags: [react, components, composition, context, api-design]
    related_skills: [react-best-practices, frontend-ui-engineering, design-system-engineering, test-driven-development]
---

# React Composition Patterns

## Description

Design and refactor React component APIs that scale without boolean-prop matrices or state-coupled markup. The skill preserves existing behavior and applies only the composition pattern justified by the component's real variants and consumers.

## Prerequisites

- A React codebase and the installed React version.
- The component's current public API, consumers, tests, and intended reuse boundary.

## Steps

1. Inventory the component contract and consumers before changing it.

   ```bash
   rg -n "<ComponentName|ComponentName\(" src test tests stories 2>/dev/null
   ```

   Expected result: call sites, stories, tests, and variants that constrain the public API are identified.

2. Record the actual problem: boolean-prop combinations, duplicated variants, trapped state, prop drilling, implementation-coupled context, or an unsupported React-version pattern. Do not refactor merely because composition is fashionable.

3. Read the applicable file under `references/rules/`:

   ```bash
   rg --files "<skill-dir>/references/rules" | sort
   ```

   Expected result: eight vendored rules covering architecture, state ownership, implementation patterns, and React 19.

4. Define the proposed contract before implementation:

   - which component owns state and which may control it;
   - the context interface of state, actions, and metadata;
   - which variants are explicit components;
   - which children are composable slots;
   - migration behavior for existing consumers.

5. Choose the smallest fitting pattern. Prefer ordinary props for simple components, explicit variants when modes have different structure, compound components for coordinated subparts, and a provider only when descendants genuinely share state or actions.

6. Implement incrementally. Preserve accessible names, keyboard behavior, refs, server/client boundaries, and styling hooks. If the change is breaking, follow `deprecation-and-migration` rather than silently rewriting consumers.

7. Add or update tests for each supported variant and interaction, including controlled and uncontrolled behavior when both are public. Run focused tests, the repository's required suite, and:

   ```bash
   git diff --check
   ```

   Expected result: existing consumers remain valid or have an explicit migration path, and all required checks pass.

## Pitfalls

- **Premature abstraction:** A one-off component does not need a compound-component API.
- **Context as a dumping ground:** Keep the interface narrow; unrelated frequently changing state causes broad rerenders and hidden coupling.
- **Boolean relocation:** Moving flags into context does not eliminate an incoherent variant model.
- **Breaking consumers silently:** Public component contracts require migration planning and compatibility evidence.
- **React 19 assumptions:** Do not remove `forwardRef` or use React 19 APIs until the installed version and framework support are confirmed.
- **Accessibility regression:** Visual composition must not fragment labels, focus order, or semantic ownership.

## Verification

1. The original consumers and public contract were inventoried before editing.
2. The chosen pattern maps to a specific observed scaling problem and vendored rule.
3. Supported variants and state ownership are explicit and tested.
4. Accessibility, refs, server/client boundaries, and existing styling hooks remain correct.
5. Breaking changes have an intentional migration path; otherwise existing consumers pass unchanged.

## Cross-References

- `react-best-practices` — React and Next.js performance guidance.
- `frontend-ui-engineering` — general UI architecture and implementation.
- `design-system-engineering` — governed reusable component systems.
- `test-driven-development` — behavior-preserving refactors.
- `references/rules/` — eight pinned Vercel rule files.
- `references/PROVENANCE.md` — source pin and adaptation notes.
- `references/UPSTREAM-LICENSE.txt` — upstream MIT license.
