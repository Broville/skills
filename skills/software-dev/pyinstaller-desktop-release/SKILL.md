---
name: "pyinstaller-desktop-release"
description: "Build, inspect, and verify reproducible cross-platform desktop release artifacts with PyInstaller."
license: "MIT"
compatibility: "Open Agent Skills format. Requires Python, PyInstaller, the project's build environment, and a native build host for each target operating system."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to package or release a Python desktop application with PyInstaller\",\"A frozen app is missing modules, data, native binaries, icons, or runtime resources\",\"Task involves a PyInstaller spec file, hidden imports, hooks, one-file or one-folder builds, or frozen-runtime paths\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"python\",\"pyinstaller\",\"desktop\",\"packaging\",\"release\"]"
  related-skills: "[\"pyside6-desktop-engineering\",\"macos-desktop-distribution\",\"windows-desktop-ui-testing\",\"shipping-and-launch\",\"sca-scan\",\"verification-before-completion\"]"
  source: "Broville synthesis from PyInstaller 6 documentation"
  source-url: "https://pyinstaller.org/en/stable/spec-files.html"
---

# PyInstaller Desktop Release

## Description

Build and validate frozen Python desktop applications as traceable release artifacts. Use this skill when source-mode behavior is already understood and the remaining work concerns dependency discovery, spec-file control, native resources, cross-platform builds, or packaged execution.

PyInstaller is not a cross-compiler. Build and validate independently on every supported target operating system and architecture.

## Prerequisites

- The repository's release policy, supported targets, dependency lock, entrypoint, and validation commands.
- A clean, controlled native build host for each target.
- The exact source commit or tree approved for the candidate.
- Platform signing credentials only when the release workflow requires them.

## Steps

1. Record the release identity before building: source commit/tree, dirty state, Python version, PyInstaller version, dependency-lock digest, target OS, target architecture, and build command.

   ```bash
   python -m PyInstaller --version
   git status --short
   git rev-parse HEAD
   ```

   Expected result: the intended source is identified and unexplained working-tree changes are absent. Preserve user-owned changes; use an isolated checkout when necessary.

2. Inspect the complete `.spec` file and any hooks as executable Python. Review `Analysis`, `datas`, `binaries`, `hiddenimports`, `excludes`, runtime hooks, bundle metadata, and output paths. Do not execute an untrusted spec merely to learn what it does.

3. Make implicit runtime dependencies explicit.

   - Add lazily imported modules to `hiddenimports` or a narrowly scoped hook.
   - Include data files and native binaries with intentional destination paths.
   - Keep exclusions aligned with real imports; size reduction must not remove runtime capabilities.
   - Bundle native tools needed by the installed app rather than relying on the developer's `PATH`.

4. Resolve resources in both source and frozen execution. Prefer paths derived from the owning module's `__file__`; use `sys.frozen` or `sys._MEIPASS` only where the project actually needs bundle-root behavior. Never embed a developer home directory.

5. Build into a bounded, project-specific output directory using the repository's documented command.

   ```bash
   python -m PyInstaller path/to/App.spec
   ```

   Expected result: the command exits 0 and creates only the intended artifact. Do not combine broad deletion or cleanup with the build command.

6. Inspect the artifact rather than trusting a successful build log. Confirm the entry executable, icons, metadata, expected architecture, native libraries, helper tools, resources, and absence of unintended secrets or developer-only files.

7. Run packaged-mode verification on the native host: launch, startup self-test, database or settings initialization, resource loading, subprocesses, file dialogs, shutdown, and the changed user workflows. Test from a path and account that do not provide the source tree or developer `PATH` as a fallback.

8. Run dependency and security gates required by the repository. Record the artifact checksum and software bill of materials when applicable. Pass the same built candidate to signing and notarization; rebuilding creates a different artifact and invalidates binary-specific approval.

## Pitfalls

- Assuming a source-mode import proves frozen dependency discovery.
- Building Windows on macOS or macOS on Windows and calling the artifact supported.
- Treating a `.spec` file as inert configuration even though PyInstaller executes it as Python.
- Adding broad collection hooks that silently package tests, credentials, caches, or optional ecosystems.
- Using absolute developer paths for icons, media tools, configuration, or data.
- Depending on Homebrew, a system Python, or a globally installed binary from inside the packaged app.
- Rebuilding after validation, signing, or approval without restarting the artifact evidence chain.
- Claiming success from bundle creation without launching the artifact outside the development environment.

## Verification

1. The repository's source tests and packaging command exit 0 on each target host.
2. The packaged app launches without the source checkout, developer Python, or developer `PATH` dependencies.
3. Lazy imports, resources, native binaries, persistence, and shutdown behavior work from the artifact.
4. Architecture and platform metadata match the declared target.
5. Security results, artifact checksum, source identity, toolchain versions, and native-host evidence are recorded.

## Cross-References

- [PyInstaller spec files](https://pyinstaller.org/en/stable/spec-files.html)
- [PyInstaller runtime information](https://pyinstaller.org/en/stable/runtime-information.html)
- Use `macos-desktop-distribution` for Developer ID signing and notarization.
- Use `windows-desktop-ui-testing` for native Windows interaction evidence.
- Use `desktop-media-pipeline` when FFmpeg, ffprobe, or other media binaries ship inside the application.
