---
name: "pyside6-desktop-engineering"
description: "Build or review production PySide6 and Qt Widgets desktop applications without replacing the product's architecture or design system."
license: "MIT"
compatibility: "Open Agent Skills format. Requires Python 3.10+ and PySide6 for implementation; platform-native verification requires macOS or Windows."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to build, modify, or review a PySide6 or Qt Widgets application\",\"Task involves Qt models, delegates, signals, slots, threads, QSS, palettes, or native desktop behavior\",\"A Python desktop UI needs cross-platform engineering or visual quality work\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"python\",\"pyside6\",\"qt\",\"qt-widgets\",\"desktop\",\"ui\"]"
  related-skills: "[\"native-desktop-accessibility\",\"desktop-filesystem-safety\",\"desktop-media-pipeline\",\"pyinstaller-desktop-release\",\"frontend-ui-engineering\",\"design-taste-frontend\",\"test-driven-development\",\"performance-optimization\"]"
  source: "Broville synthesis; ejacques11/pyside6-fluent-ui@4538e312ee9abde4b77d041d59a5392aa7d43188 (MIT); Qt for Python documentation"
  source-url: "https://doc.qt.io/qtforpython-6/"
---

# PySide6 Desktop Engineering

## Description

Engineer maintainable native desktop interfaces with PySide6 and Qt Widgets. Apply this skill to implementation and review where Qt object lifetime, model/view behavior, event ordering, styling, worker isolation, or macOS/Windows parity materially affects correctness.

Project instructions, existing architecture, and established visual language remain authoritative. Use external design systems as evidence, not as permission to migrate frameworks or reproduce another product's identity.

## Prerequisites

- Read access to the repository instructions, dependency files, UI modules, tests, and packaging configuration.
- The project's supported Python and PySide6 environment for implementation checks.
- A native host for platform behavior that headless Qt tests cannot prove.

## Steps

1. Discover the application contract before editing.

   ```bash
   rg --files | rg '(AGENTS|CLAUDE|pyproject|requirements|\.spec$|ui/|core/|tests/)'
   ```

   Expected result: the repository policy, Qt entrypoint, state owners, theme, packaging rules, and validation commands are identified. Record which behaviors are testable headlessly and which require a native host.

2. Preserve state ownership and put decisions at the narrowest testable layer. Keep filesystem, database, filtering, sorting, validation, and state-transition decisions in Qt-free functions when practical. Let widgets coordinate presentation, signals, and lifecycle rather than becoming a second domain model.

3. Implement model/view behavior with stable identity.

   - Carry durable IDs in model roles; resolve proxy indexes back to source data at action time.
   - Treat selection, current index, focus, hover, and expanded state as different concepts.
   - Keep delegates deterministic: share geometry between paint and hit testing.
   - Expect model resets and filtering to invalidate indexes and transient widget references.
   - Use explicit accessible names and stable `objectName` values where automation needs identifiers.

4. Use Qt's event and lifetime model deliberately.

   - Parent `QObject` instances or retain explicit ownership for objects that must outlive a callback.
   - Connect signals once; disconnect or dispose temporary controllers and workers intentionally.
   - Use event filters only when the target and accepted event types are bounded.
   - Account for focus-in, focus-out, drag, drop, wheel, activation, and close ordering on both supported desktop platforms.

5. Keep blocking work outside the GUI thread. A worker receives immutable inputs, touches no widgets, and returns immutable results through signals. The main thread owns widgets and ordinary UI-bound database connections. Define concurrency limits, close behavior, cancellation semantics, and stale-result rejection before starting the worker.

6. Apply the product's own visual system through semantic tokens, `QPalette`, shared QSS, and reusable widgets. Cover enabled, disabled, hover, pressed, focus, selected, checked, invalid, empty, busy, and high-contrast states. Package every icon or stylesheet resource and resolve it in both source and frozen execution.

7. Verify in layers.

   - Test pure decisions without Qt.
   - Run headless widget/model tests for signal, selection, geometry, and lifecycle behavior.
   - Exercise the changed interface with keyboard and pointer input.
   - Validate scaling, multiple displays, platform dialogs, menu/tray behavior, and shutdown on each supported native host.
   - Build and launch the packaged application; source-mode success is not packaging evidence.

## Pitfalls

- Calling a generic frontend a "Qt design system" without covering widget states, focus, palette roles, and packaged resources.
- Moving a Widgets application to QML, web technology, WinUI, or SwiftUI only to imitate a reference design.
- Performing file I/O, scans, subprocess waits, or media inspection on the GUI thread.
- Updating widgets from worker threads or sharing a UI-thread database connection with a worker.
- Treating `currentIndex()` as the complete multi-selection or retaining a proxy index across model refresh.
- Styling only the happy path; native controls can expose unreadable disabled, focused, checked, or high-contrast states.
- Claiming platform parity from an offscreen test or from only one operating system.

## Verification

1. Run the repository's focused pure-logic and Qt tests with its documented command; require exit status 0.
2. Run the complete relevant test and packaging gates; require exit status 0 and a launchable artifact.
3. Confirm changed controls expose stable identity, keyboard focus, accessible text, and all relevant visual states.
4. Record native macOS and Windows checks separately. Mark unobserved native behavior as pending rather than inferred.

## Cross-References

- [Qt for Python documentation](https://doc.qt.io/qtforpython-6/)
- [Qt accessibility for QWidget applications](https://doc.qt.io/qtforpython-6/overviews/qtdoc-accessible.html)
- Use `native-desktop-accessibility` for assistive-technology evidence.
- Use `pyinstaller-desktop-release` for frozen artifacts and `windows-desktop-ui-testing` for Windows UI Automation.
- Use `design-taste-frontend` and `frontend-ui-engineering` only for principles that transfer to the existing native stack.
