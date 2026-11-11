---
name: "native-desktop-accessibility"
description: "Build and audit semantic keyboard and assistive-technology behavior in native macOS and Windows desktop interfaces."
license: "MIT"
compatibility: "Open Agent Skills format. Native evidence requires the target application plus macOS Accessibility or Windows UI Automation tooling."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"macos\",\"windows\"]"
  triggers: "[\"User asks to implement or audit accessibility in a native desktop application\",\"Task changes keyboard navigation, focus, names, roles, values, states, tables, trees, custom controls, or high-contrast behavior\",\"A macOS or Windows app needs assistive-technology evidence\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"accessibility\",\"desktop\",\"macos\",\"windows\",\"uia\",\"qt\"]"
  related-skills: "[\"pyside6-desktop-engineering\",\"windows-desktop-ui-testing\",\"adversarial-ux-test\",\"web-accessibility\",\"code-review-checklist\"]"
  source: "Broville synthesis from Qt accessibility, Microsoft UI Automation, and Apple accessibility documentation"
  source-url: "https://doc.qt.io/qtforpython-6/overviews/qtdoc-accessible.html"
---

# Native Desktop Accessibility

## Description

Make native desktop software operable and understandable through keyboard navigation, screen readers, magnification, contrast modes, and platform accessibility APIs. This skill covers semantic implementation and platform evidence; it does not substitute a web WCAG scan for native assistive-technology testing.

## Prerequisites

- The target app and source, including custom widgets or controls.
- macOS Accessibility Inspector and VoiceOver for Mac checks, or Windows accessibility/UIA inspection and Narrator for Windows checks.
- The product's supported input methods, display scales, and contrast themes.

## Steps

1. Inventory every interactive and information-bearing surface. Include menus, toolbars, tables, trees, cards, dialogs, notifications, custom-painted controls, drag targets, media controls, system-tray/menu-bar commands, and empty/error/busy states.

2. Define the semantic contract for each control:

   - role and stable identifier;
   - concise accessible name;
   - current value, checked/selected/expanded/busy/invalid state;
   - available actions;
   - parent, label, description, and table relationships;
   - live status changes that need announcement.

   Do not encode changing state only in a name when the platform exposes a state or value property.

3. Make every action keyboard reachable. Establish a predictable focus order, visible focus indicator, standard activation keys, Escape behavior, menu shortcuts, and focus return after dialogs or transient surfaces close. Test without a pointer.

4. Use the framework's built-in semantic support first. For Qt Widgets, set text, labels, buddies, accessible names/descriptions, shortcuts, and stable `objectName` values. Implement `QAccessibleInterface` support only when a custom widget's role, actions, relationships, text, table, or value cannot be represented by built-in widgets.

5. Separate meaning from appearance. Never rely only on color, position, hover, icon shape, animation, or sound. Preserve meaning under high contrast, increased text size, display scaling, reduced motion, muted audio, and monochrome review.

6. Inspect the runtime accessibility tree on each operating system. Verify actual names, roles, values, states, actions, bounds, focus, and hierarchy. A source-code property is not sufficient when the packaged accessibility bridge exposes something different.

7. Exercise representative workflows with the platform screen reader and keyboard. Cover startup, navigation, editing, validation errors, dialogs, long lists, dynamic updates, drag/drop alternatives, playback, and shutdown as applicable.

8. Record findings with the exact platform, app build, control, observed semantic output, expected behavior, severity, and reproduction steps. Keep semantic, visual, and workflow findings distinct.

## Pitfalls

- Equating an automation identifier with an accessible name or with full accessibility.
- Giving every container a name and creating a noisy, deeply nested tree.
- Making a custom-painted control clickable without exposing role, action, state, and keyboard behavior.
- Testing only the source tree instead of the packaged application.
- Assuming macOS and Windows accessibility bridges expose identical semantics.
- Treating drag-and-drop as the only way to complete an operation.
- Reporting color contrast alone as an accessibility audit.

## Verification

1. Complete every changed workflow using only the keyboard.
2. Inspect the packaged app's runtime tree and confirm expected name, role, state, value, action, and focus for every changed control.
3. Complete at least one representative workflow with VoiceOver on macOS and Narrator on Windows when both platforms are supported.
4. Verify high contrast, scaling, and focus visibility visually; record any unavailable platform as pending.
5. Run the repository's accessibility and interaction tests with exit status 0.

## Cross-References

- [Qt accessibility overview](https://doc.qt.io/qtforpython-6/overviews/qtdoc-accessible.html)
- [Qt `QAccessibleInterface`](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QAccessibleInterface.html)
- [Microsoft UI Automation overview](https://learn.microsoft.com/windows/win32/winauto/entry-uiauto-win32)
- [Apple accessibility](https://developer.apple.com/accessibility/)
- Use `windows-desktop-ui-testing` for repeatable UIA evidence and `adversarial-ux-test` for hostile workflow review.
