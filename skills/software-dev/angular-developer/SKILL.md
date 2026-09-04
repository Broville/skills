---
name: "angular-developer"
description: "Build, review, test, and modernize Angular applications using version-aware official framework guidance."
license: "MIT"
compatibility: "Open Agent Skills format for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot, and compatible hosts. Runtime tools are listed in Prerequisites."
metadata:
  author: "Broville contributors"
  version: "2.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to create, review, debug, test, or modernize an Angular application\",\"Work involves Angular components, Signals, forms, dependency injection, routing, SSR, styling, or CLI tooling\",\"An Angular change needs current framework-specific architecture or API guidance\"]"
  inputs: "[{\"name\":\"target\",\"description\":\"Angular workspace, application, library, route, component, or change set in scope\",\"required\":true},{\"name\":\"requested_outcome\",\"description\":\"Feature, defect, migration, review, or architecture outcome to deliver\",\"required\":true}]"
  outputs: "[{\"name\":\"angular_change\",\"description\":\"Version-compatible implementation or evidence-backed guidance\"},{\"name\":\"verification_evidence\",\"description\":\"Focused tests, build results, and applicable browser evidence\"}]"
  tags: "[\"angular\",\"typescript\",\"signals\",\"routing\",\"forms\"]"
  related-skills: "[\"frontend-ui-engineering\",\"web-accessibility\",\"performance-optimization\",\"test-driven-development\",\"verification-before-completion\"]"
  source: "angular/angular@81c3f3a6aab30a0e9ca3a8b511100afea4d07003 (MIT)"
  source-url: "https://github.com/angular/angular/tree/81c3f3a6aab30a0e9ca3a8b511100afea4d07003/skills/dev-skills/angular-developer"
---

# Angular Developer

## Description

Build, review, test, and modernize Angular applications using task-routed guidance maintained by the Angular team. Inspect the installed Angular version and project conventions first; use only APIs supported by that version and preserve the workspace's established architecture unless the user authorized a migration.

## Prerequisites

- An Angular workspace or explicit authorization to create one.
- The repository instructions, package manifest, lockfile, and existing quality commands.
- Node.js plus the package manager selected by the workspace.

## Steps

1. Inspect the workspace, policy, installed versions, and existing commands before generating or editing code.

   ```bash
   node -e "const p=require('./package.json'); console.log({angular:p.dependencies?.['@angular/core']||p.devDependencies?.['@angular/core'], cli:p.devDependencies?.['@angular/cli'], scripts:p.scripts})"
   ```

   Expected result: the declared Angular/CLI range and project-provided build, test, lint, and serve commands are visible. Resolve the installed version from the lockfile when a range is ambiguous.

2. Read only the task-relevant official references in the routing table below. Treat their examples as version-bounded patterns, not permission to replace local conventions or dependencies.

3. Define the behavior and compatibility boundary before implementation: affected application/library, browser and rendering mode, public component/service contract, data and error states, accessibility behavior, and migration impact.

4. Use the workspace's installed Angular CLI and package manager for supported generators and migrations. For a user-requested new project, use an explicitly requested Angular version when given; otherwise use the current stable CLI without a global installation requirement.

   ```bash
   npx --yes @angular/cli@<requested-version-or-latest> new <app-name> --interactive=false
   ```

   Expected result: the CLI creates a buildable workspace using the selected version. Choose routing, SSR, styles, tests, and AI configuration from the user's requirements rather than adding every option.

5. Implement the smallest coherent change. Prefer Angular's supported primitives, preserve Signals/Observable and forms strategies already used by the surrounding feature, keep server/client boundaries explicit, and use `web-accessibility` for criterion-level accessibility work.

6. Add or update tests at the lowest useful level: pure logic, component behavior, router harness, HTTP boundary, or end-to-end flow. Exercise loading, empty, error, success, permission, and hydration states that can affect the requested behavior.

7. Run the workspace's focused tests, required lint/type checks, production build, and:

   ```bash
   git diff --check
   ```

   Expected result: the exact changed behavior passes, the production build succeeds, and `git diff --check` exits with status 0. Run browser checks for rendered or interactive changes and report any environment-dependent verification left unrun.

## Reference Routing

### Components

- [Components](references/components.md) — anatomy, metadata, templates, and control flow.
- [Inputs](references/inputs.md) — signal inputs, transforms, and model inputs.
- [Outputs](references/outputs.md) — signal outputs and event contracts.
- [Host elements](references/host-elements.md) — host bindings and attributes.
- [Naming conventions](references/naming-conventions.md) — current intent-oriented naming guidance.

### Reactivity and data

- [Signals overview](references/signals-overview.md) — `signal`, `computed`, reactive contexts, and `untracked`.
- [Linked signal](references/linked-signal.md) — writable state derived from a source.
- [Resource](references/resource.md) — asynchronous signal state.
- [Effects](references/effects.md) — effects, render effects, and misuse boundaries.
- [HTTP client](references/http-client.md) — providers, clients, interceptors, and `httpResource`.

### Forms and dependency injection

- [Signal forms](references/signal-forms.md) — version-gated Signal Forms guidance.
- [Template-driven forms](references/template-driven-forms.md) — simple form workflows.
- [Reactive forms](references/reactive-forms.md) — explicit, complex form state.
- [DI fundamentals](references/di-fundamentals.md), [creating services](references/creating-services.md), [defining providers](references/defining-providers.md), [injection context](references/injection-context.md), and [hierarchical injectors](references/hierarchical-injectors.md) — dependency ownership and resolution.
- [Pipes](references/pipes.md) — template formatting and reusable transformation boundaries.

### Accessibility and routing

- [Angular Aria](references/angular-aria.md) — headless accessible composite widgets; confirm package/version support and still verify the rendered result.
- [Define routes](references/define-routes.md), [loading strategies](references/loading-strategies.md), [route outlets](references/show-routes-with-outlets.md), and [navigation](references/navigate-to-routes.md) — route structure and activation.
- [Route guards](references/route-guards.md), [data resolvers](references/data-resolvers.md), and [router lifecycle](references/router-lifecycle.md) — navigation policy, data, and diagnostics.
- [Rendering strategies](references/rendering-strategies.md) and [route animations](references/route-animations.md) — CSR, SSR, prerendering, hydration, and view transitions.

### Styling, testing, and tooling

- [Component styling](references/component-styling.md), [Tailwind CSS](references/tailwind-css.md), and [Angular animations](references/angular-animations.md) — encapsulation, utility integration, and current animation choices.
- [Testing fundamentals](references/testing-fundamentals.md), [component harnesses](references/component-harnesses.md), [router testing](references/router-testing.md), and [end-to-end testing](references/e2e-testing.md) — behavior-focused verification.
- [Angular CLI](references/cli.md), [migrations](references/migrations.md), [environment configuration](references/environment-configuration.md), and [Angular MCP](references/mcp.md) — generation, modernization, configuration, and optional tool-assisted guidance.

## Pitfalls

- **Version fantasy:** Do not use Signal Forms, Angular Aria, current control flow, or another recent API before confirming the installed framework supports it.
- **Unpinned migration:** Never run broad `ng update` migrations as an incidental feature step; migration scope and compatibility require explicit authorization and evidence.
- **CLI replacement:** Generators accelerate consistent setup but do not override repository naming, layout, tests, or architecture.
- **Guard as security boundary:** Client route guards improve navigation UX but cannot replace server-side authorization.
- **Reactive-style churn:** Do not rewrite functioning Observable, Signals, or forms architecture solely to match a newer preference.
- **Hydration blindness:** Browser-only code, nondeterministic output, DOM mutation, and duplicate fetching can break SSR or hydration even when client navigation works.
- **Framework-only confidence:** A successful `ng build` does not prove accessibility, interaction, responsive behavior, or end-to-end correctness.

## Verification

1. The installed Angular and CLI versions are recorded, and every selected API is supported by them.
2. Each material choice maps to the repository's conventions or an applicable pinned reference.
3. Focused tests cover the requested behavior and relevant failure/state transitions.
4. The workspace's required checks and production build pass with fresh output.
5. Rendered changes receive keyboard, responsive, accessibility, console, and network verification as applicable.
6. Migrations, dependency changes, and public API changes are intentional and have a compatibility or rollback path.

## Cross-References

- `frontend-ui-engineering` — framework-neutral UI architecture and state completeness.
- `web-accessibility` — WCAG 2.2 implementation and evidence workflow.
- `performance-optimization` — measured cross-stack performance diagnosis.
- `test-driven-development` — behavior-first implementation and regression coverage.
- `verification-before-completion` — fresh evidence before completion claims.
- `references/PROVENANCE.md` — source pin and adaptation notes.
- `references/UPSTREAM-LICENSE.txt` — upstream MIT license.
