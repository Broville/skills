---
name: "macos-desktop-distribution"
description: "Sign, notarize, staple, and verify macOS desktop application artifacts distributed outside the Mac App Store."
license: "MIT"
compatibility: "Open Agent Skills format. Requires macOS, Xcode command-line tools, Apple Developer ID credentials, and an already-built application artifact."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"macos\"]"
  triggers: "[\"User asks to sign, notarize, staple, package, or verify a macOS desktop app\",\"A non-App-Store macOS release needs Developer ID and Gatekeeper evidence\",\"Task involves codesign, hardened runtime, entitlements, notarytool, stapler, or spctl\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"macos\",\"codesign\",\"notarization\",\"gatekeeper\",\"release\"]"
  related-skills: "[\"pyinstaller-desktop-release\",\"shipping-and-launch\",\"security-best-practices\",\"verification-before-completion\"]"
  source: "Adapted from openai/plugins@1e285826e604f66f7208f7ac4dba0fe8341d1f57 build-macos-apps (MIT) and Apple Developer documentation"
  source-url: "https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution"
---

# macOS Desktop Distribution

## Description

Prepare a prebuilt macOS application for direct distribution using Developer ID signing, hardened runtime, notarization, ticket stapling, Gatekeeper verification, and clean-machine launch evidence. This skill is build-system neutral and applies to PyInstaller, Swift, Electron, and other valid `.app` producers.

Treat signing and notarization as release transformations of an identified artifact. If approval is tied to an exact source tree or binary, define whether signing changes are part of that approved candidate before mutating it.

## Prerequisites

- macOS with current Xcode command-line tools.
- An Apple Developer ID Application identity and authorized notarization credentials.
- A completed `.app` bundle whose nested code and dependencies are known.
- A project-approved entitlements file and distribution container such as ZIP, DMG, or PKG.

## Steps

1. Record the unsigned artifact identity, source commit/tree, build command, architecture, minimum macOS version, and intended distribution channel. Inspect nested executables, frameworks, plug-ins, helpers, and libraries before signing.

2. Derive the smallest entitlement set from observed runtime needs. Document each entitlement's reason. Hardened-runtime exceptions such as unsigned executable memory, JIT, disabled library validation, or DYLD environment access materially weaken protection and require explicit justification.

3. Sign nested code from the inside out, then sign the outer app with Developer ID, hardened runtime, and a secure timestamp. Use explicit paths and identity variables rather than broad globs.

   ```bash
   codesign --force --options runtime --timestamp --entitlements path/to/entitlements.plist --sign "Developer ID Application: Organization (TEAMID)" path/to/App.app
   codesign --verify --deep --strict --verbose=2 path/to/App.app
   ```

   Expected result: verification exits 0. `--deep` is a verification aid, not a substitute for deliberately signing nested code.

4. Inspect what was actually signed.

   ```bash
   codesign -d --verbose=4 path/to/App.app
   codesign -d --entitlements :- path/to/App.app
   ```

   Expected result: the expected Developer ID identity, Team ID, hardened-runtime flags, and approved entitlements are present.

5. Create the project-approved notarization container without rebuilding the app, submit with `notarytool`, and wait for the final result.

   ```bash
   xcrun notarytool submit path/to/App.zip --keychain-profile PROFILE --wait
   ```

   Expected result: final status is `Accepted`. Retrieve and review the notarization log when status is not accepted or contains actionable diagnostics.

6. Staple and validate the ticket on the distributable artifact.

   ```bash
   xcrun stapler staple path/to/App.app
   xcrun stapler validate path/to/App.app
   spctl --assess --type execute --verbose=4 path/to/App.app
   ```

   Expected result: stapler validation and Gatekeeper assessment both succeed.

7. Verify the distributed container and app on a clean or representative Mac. Test first launch, protected-resource prompts, file access, helpers, plug-ins, updates, and offline Gatekeeper behavior. Record the final container checksum.

## Pitfalls

- Using obsolete `altool`; Apple requires `notarytool` for current notarization submissions.
- Signing only the outer bundle while nested executables remain unsigned or inconsistently signed.
- Using `--deep` for signing as a shortcut instead of controlling nested identities and entitlements.
- Adding broad entitlements until the app launches without identifying the real runtime requirement.
- Including `get-task-allow` in a production distribution.
- Logging or committing Apple credentials, API keys, keychain passwords, or notarization profiles.
- Rebuilding after approval and then presenting the signed artifact as the same binary.
- Treating notarization acceptance as functional application testing.

## Verification

1. `codesign --verify --deep --strict --verbose=2` exits 0.
2. The displayed identity, Team ID, flags, and entitlements match the release record.
3. `notarytool` reports `Accepted`, the ticket staples successfully, and `stapler validate` exits 0.
4. `spctl --assess --type execute` accepts the app.
5. The final container checksum, clean-machine launch result, architecture, and exact source/build identity are recorded.

## Cross-References

- [Apple notarization requirements](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
- [Apple hardened runtime](https://developer.apple.com/documentation/security/hardened-runtime)
- [Pinned OpenAI signing skill](https://github.com/openai/plugins/blob/1e285826e604f66f7208f7ac4dba0fe8341d1f57/plugins/build-macos-apps/skills/signing-entitlements/SKILL.md)
- [Pinned OpenAI packaging skill](https://github.com/openai/plugins/blob/1e285826e604f66f7208f7ac4dba0fe8341d1f57/plugins/build-macos-apps/skills/packaging-notarization/SKILL.md)
- Use `pyinstaller-desktop-release` before signing a PyInstaller application.
