# Standards and Quality Gates

Read this reference when defining token interchange, component evidence, or release gates for a design system.

## Design tokens

The [Design Tokens Format Module 2025.10](https://www.designtokens.org/TR/2025.10/format/) is a stable Final Community Group Report for exchanging token data. It defines JSON token and group structure, `$value`, `$type`, aliases, group inheritance, deprecation metadata, and the recommended `application/design-tokens+json` media type. It is not a W3C Recommendation; describe it accurately as a stable DTCG community specification.

Use the standard when interoperability matters. Existing project formats remain authoritative when migration cost outweighs the benefit; document any mapping instead of silently rewriting token sources.

## Accessibility

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) is the normative conformance standard. Target A and AA criteria when the project calls for WCAG 2.2 AA.
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) is informative implementation guidance for custom widgets. Native HTML remains the first choice.
- Automated rules catch only a subset of barriers. Treat incomplete or untestable results as manual-review work, not passes.

## Component evidence

[Storybook's UI testing documentation](https://storybook.js.org/docs/writing-tests) treats stories as reusable component states for behavior, accessibility, and visual testing. Storybook is optional: preserve an existing component harness when it can express the same state matrix.

A component's evidence should cover:

1. rendered states and content extremes;
2. user-observable interactions rather than implementation details;
3. automated accessibility heuristics plus keyboard and assistive-technology checks;
4. stable visual comparisons for appearance-sensitive states;
5. at least one consumer integration so package-only success does not hide integration failure.

## Visual regression

[Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) compare screenshots against committed baselines and warn that rendering varies by operating system, browser version, hardware, and settings. Generate and compare baselines in the same controlled environment. Review every changed baseline; `--update-snapshots` is an acceptance action, not a repair.
