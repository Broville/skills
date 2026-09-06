---
name: "windows-desktop-ui-testing"
description: "Create repeatable Windows UI Automation tests and visual evidence for packaged desktop applications, with an explicit framework-compatibility pilot."
license: "MIT"
compatibility: "Open Agent Skills format. Requires Windows, an interactive desktop for input injection, and Microsoft WinApp CLI with its UI Automation commands."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"windows\"]"
  triggers: "[\"User asks to automate or validate a Windows desktop application\",\"A packaged Windows beta needs repeatable UI Automation assertions or screenshots\",\"Task involves Windows dialogs, keyboard shortcuts, drag and drop, accessibility-tree selectors, or native UI evidence\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"windows\",\"desktop\",\"testing\",\"uia\",\"automation\",\"visual-qa\"]"
  related-skills: "[\"native-desktop-accessibility\",\"pyside6-desktop-engineering\",\"pyinstaller-desktop-release\",\"test-driven-development\",\"verification-before-completion\"]"
  source: "Adapted from microsoft/win-dev-skills@68ae65d5c65ee87c3265a7f5abe3aaf97c7e6932 winui-ui-testing (MIT)"
  source-url: "https://github.com/microsoft/win-dev-skills/tree/68ae65d5c65ee87c3265a7f5abe3aaf97c7e6932/plugins/winui/agent-plugin/skills/winui-ui-testing"
---

# Windows Desktop UI Testing

## Description

Build a deterministic Windows UI Automation smoke or acceptance suite around an exact packaged desktop build. Use semantic assertions for behavior and screenshots for visual state; neither evidence type replaces the other.

Microsoft documents WinApp UI automation for WPF, WinForms, Win32, Electron, and WinUI 3. Treat any unlisted framework—including Qt/PySide6—as unproven until a bounded pilot demonstrates a usable UIA tree and stable actions on the real packaged application.

## Prerequisites

- A Windows host with the exact application build and a disposable test profile/database.
- WinApp CLI installed and pinned according to the project tool policy.
- An unlocked interactive desktop for real keyboard, pointer, touch, or pen injection.
- Stable accessible identifiers or a documented selector strategy.

## Steps

1. Record the test identity: source commit/tree, packaged artifact checksum, application version/channel, Windows version, WinApp version, display scale, and test-data location.

2. Confirm the tool and inspect its live command schema.

   ```powershell
   winapp --version
   winapp ui --cli-schema
   ```

   Expected result: both commands exit 0 and the schema lists the UI commands used by the suite.

3. Run a framework-compatibility pilot before authoring a broad suite.

   ```powershell
   winapp ui list-windows -a $AppPid --json
   winapp ui inspect -a $AppPid --interactive --json
   ```

   Expected result: the real application window and meaningful controls expose stable names, identifiers, roles, bounds, states, and supported actions. If the tree is empty, flattened, or unstable, stop and report the accessibility bridge gap.

4. Write one batch PowerShell test that accepts a mandatory application PID. Do not name the parameter `$PID`, which PowerShell reserves. Isolate every case, collect structured pass/fail details, and return nonzero when any required assertion fails.

5. Cover only requirements in scope. Prefer `wait-for` value/state assertions and stable identifiers. Include startup, navigation, editing, keyboard shortcuts, dialogs, file pickers, menus, persistence, drag/drop, and shutdown only where the product contract requires them.

6. Keep semantic and injected-input paths distinct. UIA pattern actions can run in more environments than foreground input injection. Tests using real keyboard, pointer, touch, or pen require the correct visible foreground session and must declare that dependency.

7. Capture screenshots after meaningful state transitions. Inspect clipping, overlap, scaling, focus, hover, error, selected, disabled, high-contrast, and dialog states. UIA success does not detect visual breakage.

8. Rerun the suite enough times to measure selector stability and flake rate. Preserve logs, structured results, and only the screenshots needed to support the conclusion. Keep native human acceptance as the final gate when the product requires it.

## Pitfalls

- Claiming support for an unlisted UI framework before inspecting the packaged app's real UIA tree.
- Relaunching a different build than the one whose PID and checksum were recorded.
- Using visible text as the sole selector when names are translated or dynamic.
- Treating AutomationId coverage as an accessibility audit.
- Running input-injection tests in a locked, disconnected, minimized, or non-interactive session.
- Reusing user data instead of a disposable profile.
- Letting OS dialogs, popup hosts, or stale windows contaminate application-only assertions.
- Accepting screenshot evidence without semantic assertions, or semantic assertions without visual review.

## Verification

1. `winapp ui --cli-schema` exits 0 on the test host.
2. The pilot records a usable tree and completes one read assertion plus one reversible action on the exact packaged build.
3. The batch suite exits 0, reports zero required failures, and emits parseable structured results.
4. Relevant screenshots are visually reviewed at every supported scale/theme.
5. The report distinguishes directly observed automation, visual review, and remaining human validation.

## Cross-References

- [Microsoft WinApp UI automation](https://github.com/microsoft/winappCli/blob/main/docs/ui-automation.md)
- [Pinned upstream testing skill](https://github.com/microsoft/win-dev-skills/blob/68ae65d5c65ee87c3265a7f5abe3aaf97c7e6932/plugins/winui/agent-plugin/skills/winui-ui-testing/SKILL.md)
- Use `native-desktop-accessibility` for accessibility semantics and `pyinstaller-desktop-release` for packaged artifact identity.
