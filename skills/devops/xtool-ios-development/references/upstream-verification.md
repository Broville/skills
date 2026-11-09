# Official xtool verification notes

This reference records the upstream facts used to author the skill. It is intentionally a snapshot of verification evidence, not a version pin for future installs. Re-check the official sources at execution time.

## Sources inspected

- Repository: `https://github.com/xtool-org/xtool`
- Upstream Linux guide in the repository: `Documentation/xtool.docc/Installation-Linux.md`
- Upstream macOS guide in the repository: `Documentation/xtool.docc/Installation-macOS.md`
- Upstream Linux notes: `Linux/README.md`
- Release API: `https://api.github.com/repos/xtool-org/xtool/releases/latest`

At verification time, the upstream repository's latest release API returned tag `1.24.0`, named `v1.24.0`, published `2026-10-26T00:18:19Z`. This is historical evidence captured on November 9, 2026; do not treat it as a permanent latest-release assertion.

## Verified release assets at that time

The GitHub release API reported these architecture-specific CLI assets:

| Asset | Size | API SHA-256 digest |
|---|---:|---|
| `xtool-aarch64.AppImage` | 52,525,576 bytes | `4bc0515fed71efb86e82564f358efa0c4c6d76bf1bcfd4c5f256727b53ec59c8` |
| `xtool-x86_64.AppImage` | 54,135,288 bytes | `dbfd9d7216f077c84c171b688c4173c37c23ca76bf7fd185d1a9ae8a53dab59f` |

The API also listed matching `.zsync` assets and macOS archives. The ARM64 asset confirms that an aarch64 Linux release existed at that point; it does not establish that every ARM64 distribution, kernel, AppImage runtime, or iOS workflow is supported.

## Upstream workflow facts

- xtool describes itself as cross-platform across Linux/WSL/macOS.
- The Linux/Windows guide requires Swift 6.4 for the documented current workflow, `usbmuxd` for Linux device communication, and an Apple-downloaded `Xcode.xip` to generate/install a Darwin Swift SDK through `xtool setup`.
- Windows is documented through WSL, with USB passthrough/USBIPD or the documented relay workaround for device access.
- macOS requires Xcode to be installed and initialized; the guide verifies the iOS SDK with `xcrun -sdk iphoneos -show-sdk-path`.
- The CLI exposes `setup`, `auth`, `sdk`, `new`, `dev`, and device operations. Exact detailed subcommands should be read from the installed release's `xtool --help`.
- The Linux source notes explain that the project builds a native Linux AppImage and uses `uname -m` when selecting the linuxdeploy build asset.

## What was not verified

No claim is made here that a particular user's host can build or deploy an iOS app. A real verification requires running the checks in the skill on that target, with a compatible Swift toolchain, Darwin SDK, Apple authentication state, and— for deployment—a paired device and signing flow. No credentials, Xcode archive, or device data belongs in this repository.
