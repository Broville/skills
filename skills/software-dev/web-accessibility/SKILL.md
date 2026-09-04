---
name: "web-accessibility"
description: "Build and audit web interfaces against WCAG 2.2 with native semantics, manual checks, and assistive-technology evidence."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and compatible hosts. Runtime tools are listed in Prerequisites."
metadata:
  author: "Broville"
  version: "3.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to build, remediate, or audit an accessible web interface\",\"Work involves WCAG, ARIA, keyboard access, focus, screen readers, contrast, zoom, or reduced motion\",\"Accessibility findings or conformance claims need implementation and verification\"]"
  inputs: "[{\"name\":\"target\",\"description\":\"Route, component, workflow, or change set to build or audit\",\"required\":true},{\"name\":\"conformance_target\",\"description\":\"Required standard and level, defaulting to WCAG 2.2 AA when none is specified\",\"required\":false}]"
  outputs: "[{\"name\":\"accessibility_evidence\",\"description\":\"Criterion-mapped automated and manual results with explicit unverified areas\"},{\"name\":\"remediated_interface\",\"description\":\"Project-consistent fixes and regression coverage when changes are requested\"}]"
  tags: "[\"accessibility\",\"wcag-2-2\",\"aria\",\"keyboard\",\"assistive-technology\"]"
  related-skills: "[\"web-design-guidelines\",\"playwright-cli\",\"frontend-ui-engineering\",\"verification-before-completion\"]"
---

# Web Accessibility

## Description

Build and evaluate web interfaces against WCAG 2.2 using native semantics first, ARIA only where necessary, and both automated and human checks. Do not claim conformance from an axe or Lighthouse score: WCAG applies to complete pages and responsive variations, and many success criteria require manual evaluation.

## Prerequisites

- The target routes, states, supported browsers, and conformance requirement.
- A runnable interface for interaction-dependent checks.
- Available project accessibility tooling plus at least keyboard testing; use an assistive technology supported by the target platform when the task requires conformance evidence.

## Steps

1. Define the audit/build matrix before changing code: route, viewport, theme, locale, authentication state, loading/empty/error/success states, input methods, and assistive technology. Read `references/wcag-2.2-aa-checklist.md` and map applicable criteria.

2. Inspect structure before ARIA. Prefer landmarks, headings, lists, links, buttons, labels, tables, details, and dialog/popover primitives with their native behavior. Use ordinary list navigation for site links; `menu` and `menubar` patterns are for application-style composite widgets with their complete keyboard model.

3. Run the repository's existing automated accessibility checks. If the project has no command, use its package manager to add tooling only when dependency changes are authorized; otherwise run an available browser audit without modifying the manifest.

   ```bash
   npm run | rg -i 'a11y|accessib|axe|test|lint'
   ```

   Expected result: the existing applicable commands are identified. Record violations, incomplete results, rules not run, and the exact route/state tested.

4. Test keyboard behavior manually: logical focus order, visible and unobscured focus, activation keys, Escape behavior, focus entry/return for overlays, skip/navigation mechanisms, and no keyboard traps. Custom composite widgets must match the selected ARIA APG pattern rather than an improvised subset.

5. Test names and announcements with the accessibility tree and an appropriate screen reader where available. Confirm name, role, value, state changes, errors, status updates, relationships, landmark structure, heading hierarchy, table semantics, and image alternatives. Avoid duplicate or noisy live-region announcements.

6. Test visual and motor-access requirements: contrast, non-color cues, 200% text zoom, 400% reflow where applicable, orientation, target size or spacing, dragging alternatives, pointer cancellation, hover/focus content, reduced motion, and focus not obscured by sticky or overlay UI.

7. Test forms and authentication: persistent labels, instructions before input, programmatic error association, error summary and focus behavior, autocomplete/purpose tokens, redundant-entry avoidance, paste/password-manager support, and an accessible authentication alternative that does not depend solely on a cognitive-function test.

8. Remediate the smallest root cause in the project's existing primitives. Add a regression test at the lowest useful level, then rerun the affected automated rule and manual scenario. Audit requests are read-only unless the user also requested fixes.

9. Run the focused checks, repository-required suite, build, and:

   ```bash
   git diff --check
   ```

   Expected result: changed states pass, required project checks succeed, and any remaining criteria are explicitly unverified or blocked rather than silently marked compliant.

## Pitfalls

- **ARIA substitution:** Adding a role does not add keyboard behavior, focus management, or accessible state. Prefer native HTML.
- **Menubar misuse:** Do not give ordinary website navigation application-menu semantics.
- **Automated-score confidence:** Automated heuristics catch only a subset of accessibility barriers and cannot establish WCAG conformance.
- **Single-state testing:** Hidden dialogs, validation errors, loading states, responsive variants, and authenticated flows are part of the page experience.
- **Focus by DOM query:** Hand-rolled focus traps often miss shadow DOM, portals, disabled elements, and dynamic content; prefer a proven project primitive or native dialog behavior.
- **Visual-only repair:** A screen-reader-only label can still leave sighted keyboard, speech-input, or cognitive users without a clear control.
- **Unscoped legal claims:** This skill provides engineering evidence, not legal certification.

## Verification

1. The conformance target and route/state/input matrix are recorded.
2. Automated results name the tool, version, route, state, and incomplete checks.
3. Every changed interaction works by keyboard with visible, unobscured focus and correct focus return.
4. Names, roles, values, errors, and dynamic status are verified in the accessibility tree and with assistive technology when required.
5. Contrast, zoom/reflow, reduced motion, target size, and responsive variants are manually checked where applicable.
6. Findings map to WCAG 2.2 criteria or clearly labeled best practices; unsupported conformance claims are not made.
7. Focused regression tests, required repository checks, and `git diff --check` pass after remediation.

## Cross-References

- `web-design-guidelines` — broader interaction, content, responsive, and performance audit.
- `playwright-cli` — browser evidence, screenshots, accessibility snapshots, and interaction diagnostics.
- `frontend-ui-engineering` — implementation architecture and state completeness.
- `verification-before-completion` — evidence before claims.
- `references/wcag-2.2-aa-checklist.md` — criterion-oriented manual and automated check matrix.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — normative standard.
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) — informative widget guidance.
