---
name: xtool-ios-development
description: Set up, validate, and use xtool for SwiftPM-based iOS development across supported Linux, WSL, and macOS environments. Use when installing xtool, preparing a Darwin Swift SDK, authenticating with Apple Developer Services, building, signing, deploying, or troubleshooting an xtool workflow.
license: MIT
compatibility: Open Agent Skills format. Requires a supported host, Swift toolchain, xtool release or source build, network access, and Apple-provided SDK or Xcode prerequisites appropriate to the host. Device deployment additionally requires a compatible iOS device, USB/network access, pairing, and Apple account capabilities.
metadata:
  author: Broville
  version: "1.0.0"
  platforms: '["linux","macos","windows"]'
  triggers: '["User asks to install or configure xtool","User asks to build or deploy a SwiftPM iOS app without Xcode project workflows","User mentions xtool, xtool setup, xtool sdk, or xtool dev","User needs to diagnose xtool, Swift SDK, Apple Developer Services, or iOS device setup"]'
  inputs: '[{"name":"host","description":"Current operating system, architecture, distribution, and shell","required":true},{"name":"project","description":"SwiftPM project and xtool.yml when building or deploying","required":false},{"name":"apple-prerequisites","description":"User-supplied Apple credentials and Xcode.xip or macOS Xcode installation when required","required":false}]'
  outputs: '[{"name":"validated-environment","description":"Observed host, toolchain, SDK, authentication, and device status"},{"name":"xtool-workflow","description":"Install, configure, build, deploy, or troubleshooting result with unverified boundaries called out"}]'
  tags: '["xtool","ios","swift","swiftpm","apple","linux","macos","wsl","mobile-development"]'
  related-skills: '[]'
  aliases: '["xtool","xtool-ios"]'
  source: "Official xtool documentation and repository"
  source-url: "https://github.com/xtool-org/xtool"
---

# xtool iOS Development

## Description

Use this skill for a device-agnostic xtool workflow. Discover the actual host and architecture first; never assume Ubuntu, ARM64, a fixed install directory, a fixed release, or a working Apple environment. The workflow covers the officially documented Linux/WSL and macOS paths. ARM64 is a verified release-asset example, not a restriction or default.

## Prerequisites

- A supported host: xtool documents Linux, Windows through WSL, and macOS. Windows users must run the Linux workflow inside WSL; USB device access needs USB passthrough or another documented relay.
- Internet access to the official Swift, xtool, Apple Developer, and libimobiledevice sources as applicable.
- Swift 6.4 for the current Linux/WSL documentation; discover the current required toolchain from the official docs rather than hardcoding it.
- Linux/WSL: `usbmuxd` for device communication. `libimobiledevice-utils`/`ideviceinfo` is useful for discovery and diagnostics.
- Linux/WSL SDK path: an Apple-provided `Xcode.xip`, downloaded by the user through Apple Developer authentication. The file is consumed by `xtool setup` to generate/install a Darwin Swift SDK.
- macOS: Xcode installed and launched once, with an iOS SDK available through `xcrun -sdk iphoneos -show-sdk-path`.
- For signing/deployment: Apple Developer Services access, a compatible iOS device, pairing/trust, and Developer Mode where required. Never request, record, or paste passwords, API keys, private keys, recovery codes, or 2FA codes into skill output.

## Steps

### 1. Discover the target and preserve evidence

Run read-only checks before changing the system:

```bash
uname -srm
uname -m
[ -f /etc/os-release ] && cat /etc/os-release
command -v swift || true
command -v xtool || true
command -v usbmuxd || true
command -v ideviceinfo || true
swift --version 2>/dev/null || true
xtool --version 2>/dev/null || true
```

Record the exact outputs, host architecture, distribution/version, shell, and whether the host is WSL, a container, or native Linux. Check available disk and memory when installing a toolchain or extracting Xcode:

```bash
df -h .
free -h 2>/dev/null || vm_stat 2>/dev/null || true
```

Do not infer support from architecture alone. Match the observed `uname -m` to an actual official release asset or build path.

### 2. Choose the official host path

- **Linux:** follow the official Linux installation guide and select the release asset for the observed architecture. The upstream command derives the asset suffix from `uname -m`; verify that the resulting name exists before downloading.
- **Windows:** use WSL and follow the Linux workflow. Configure USB passthrough with Microsoft's USBIPD guidance or use the relay documented by xtool when USBIPD is unsuitable.
- **macOS:** use the macOS app/Homebrew path documented by xtool. This path uses the installed Xcode iOS SDK rather than importing `Xcode.xip` into a Linux Swift SDK.
- **Other systems:** stop and report that the official documentation does not establish support. Do not present an unverified port or compatibility guess as supported.

### 3. Install and verify Swift

Install Swift from the official Swift Linux page for the observed distribution/architecture, or use the official macOS toolchain. Then verify:

```bash
swift --version
swift package --version
```

For Linux/WSL, the official current documentation calls for Swift 6.4. If the observed toolchain differs, report it and consult the current xtool documentation/release requirements before proceeding. Do not silently replace a user's toolchain.

### 4. Install xtool from an official release

Prefer the official GitHub release asset over an unverified mirror. Discover the latest release and asset names from the GitHub API or release page, then select the asset matching the observed architecture. On Linux, the documented pattern is:

```bash
arch="$(uname -m)"
asset="xtool-${arch}.AppImage"
url="https://github.com/xtool-org/xtool/releases/latest/download/${asset}"
curl -fL "$url" -o "${asset}"
chmod +x "${asset}"
./"${asset}" --help
```

Before installing system-wide, verify the release API's asset `digest` against a local `sha256sum`. Prefer a user-local directory on `PATH`; use `/usr/local/bin` only with explicit user authorization and appropriate permissions. Do not overwrite an existing binary without recording its path and version.

On macOS, use the documented Homebrew cask/tap path or the official release app, then verify `xtool --help` and `xtool --version`.

### 5. Install device communication dependencies where applicable

On Linux/WSL, verify `usbmuxd --help`. If absent, install it using the host distribution's package manager; the official docs give Ubuntu/Debian as an example:

```bash
sudo apt-get install usbmuxd
sudo apt-get install libimobiledevice-utils
```

Do not apply Debian commands to another distribution without checking its package names and package manager. On macOS, xtool's upstream Linux README notes that `usbmuxd` is preinstalled; still verify the actual host rather than assuming it.

For a connected device, use a non-secret diagnostic such as:

```bash
idevice_id -l 2>/dev/null || ideviceinfo 2>/dev/null || true
```

An empty result means no device was observed; it is not proof that xtool is broken.

### 6. Configure Apple authentication and the Darwin SDK safely

Run the interactive setup only when the user is present and has independently obtained the required Apple prerequisites:

```bash
xtool setup
```

The documented setup offers API Key authentication for paid Apple Developer Program members and password authentication using private Apple APIs. Prefer the public API-key route when appropriate, but never collect credentials in chat, files, logs, shell history, or a skill. Stop before credential prompts if the user has not explicitly authorized and supplied a safe credential flow.

On Linux/WSL, provide the user-selected path to their Apple-downloaded `Xcode.xip` only through the interactive local prompt. `xtool setup` extracts it and installs a Darwin Swift SDK. Verify without exposing secrets:

```bash
swift sdk list
xtool sdk --help
xtool auth --help
```

The exact SDK/auth subcommands can vary by release; inspect `xtool --help` and the current official docs instead of inventing a command. On macOS, verify the native SDK first:

```bash
xcrun -sdk iphoneos -show-sdk-path
```

### 7. Create or inspect a project

For a new project, use the official template command:

```bash
xtool new
```

For an existing project, inspect `Package.swift`, `xtool.yml`, and optionally `.bsp/xtool.json`. Confirm the bundle identifier and deployment settings are appropriate before building. Avoid modifying project files until their current state is recorded.

### 8. Build, sign, and deploy only after prerequisites pass

From the SwiftPM project directory:

```bash
xtool dev
```

The first build may be slow while SwiftPM builds modules for the iOS SDK. Device deployment requires USB/network visibility, pairing/trust, Developer Mode when prompted, and Apple Developer Services operations for registration/signing/provisioning. If a trust or Developer Mode prompt appears, follow the device's local instructions and rerun `xtool dev` as directed by the official tutorial.

If only a build artifact is needed, use the release's documented help to select the supported non-device workflow; do not claim a successful iOS build until a real Darwin SDK and tool output confirm it.

### 9. Troubleshoot by boundary

Classify the failure before changing anything:

1. **Host/runtime:** wrong OS/architecture, missing permissions, insufficient disk/RAM, WSL USB boundary, or unsupported distribution.
2. **Swift:** missing or incompatible toolchain; verify `swift --version` and package resolution.
3. **xtool binary:** wrong asset, missing execute permission, AppImage runtime issue, or stale version; rerun `xtool --help` and check the official release digest.
4. **SDK:** `Xcode.xip` missing/invalid, SDK not installed/listed, or macOS Xcode not initialized.
5. **Authentication/signing:** Apple account/API-key/2FA, team membership, device registration, provisioning, or Developer Mode. Never debug by asking for secrets.
6. **Device transport:** `usbmuxd`, USBIPD/WSL, pairing, cable, trust, or device visibility.

Capture exact error text and rerun the smallest read-only diagnostic that distinguishes these boundaries.

## Pitfalls

- **Hardcoding ARM64 or Ubuntu:** xtool publishes architecture-specific assets and documents multiple host paths. Discover `uname -m` and the distribution first.
- **Assuming the latest release name:** resolve the current release and asset digest at execution time; the verified ARM64 example in the companion reference is historical evidence, not a permanent pin.
- **Using `xtool` before a Darwin SDK exists:** the CLI can install/run without a usable iOS SDK. Separate CLI verification from iOS build verification.
- **Treating `swift sdk list` as authentication proof:** SDK presence and Apple Developer Services authentication are separate checks.
- **Downloading Xcode.xip with curl:** Apple Developer downloads require browser authentication and license acceptance; the user must obtain the file through Apple.
- **Copying credentials into commands or logs:** never handle passwords, API keys, private keys, or 2FA codes through the skill.
- **Applying `apt-get` everywhere:** Ubuntu/Debian is only an example; use the observed distribution's supported package manager.
- **Calling Windows native support verified:** upstream documents Windows via WSL, not a separate native Windows CLI workflow.
- **Claiming device success from a tool install:** device pairing, trust, Developer Mode, signing, and Apple account state must be observed separately.
- **Overwriting an existing install:** record the current path/version and use an explicit user-approved destination.

## Verification

A valid report includes exact observed evidence, not assumptions:

- Host OS, release/distribution, architecture, and whether WSL/containerized.
- Swift version and package-manager availability.
- xtool path, version, `xtool --help`, selected release/asset, and SHA-256 verification source/result.
- Device dependency status (`usbmuxd`, optional `ideviceinfo`/`idevice_id`) and whether a device was actually detected.
- SDK evidence: `swift sdk list` on Linux/WSL or `xcrun -sdk iphoneos -show-sdk-path` on macOS.
- Authentication status only as a redacted state; never include credentials.
- Project/build/deploy command output and exact failure boundary if any.
- Explicit distinction between **verified**, **not attempted**, and **blocked/unverified** capabilities.

Minimum CLI smoke check after installation:

```bash
xtool --help
xtool --version
xtool sdk --help
xtool auth --help
```

Do not mark iOS build or deployment verified unless the target host produced successful xtool output using a real Darwin Swift SDK and, for deployment, a real device/signing flow.

## Cross-References

- Official upstream repository and release assets: `https://github.com/xtool-org/xtool`
- Official xtool documentation: `https://xtool.sh/documentation/xtooldocs/installation-linux` and `https://xtool.sh/documentation/xtooldocs/installation-macos`
- Release verification notes and the ARM64 example: [references/upstream-verification.md](references/upstream-verification.md)
- Swift Linux installation: `https://swift.org/install/linux`
- Apple Xcode downloads: `https://developer.apple.com/download/all/?q=Xcode`
- Apple App Store Connect API keys: `https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api`
- Microsoft WSL USB guidance: `https://learn.microsoft.com/en-us/windows/wsl/connect-usb`
- libimobiledevice/usbmuxd: `https://github.com/libimobiledevice/usbmuxd`
