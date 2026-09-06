---
name: "desktop-media-pipeline"
description: "Build and verify safe FFmpeg-based media inspection, conversion, preview, and publication workflows in desktop applications."
license: "MIT"
compatibility: "Open Agent Skills format. Requires the project's supported FFmpeg and ffprobe binaries plus native verification on each target platform."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to add audio or video inspection, preview, conversion, transcoding, waveform, metadata, or export to a desktop app\",\"Task invokes FFmpeg or ffprobe from Python or a native desktop UI\",\"A packaged app must bundle and safely execute media binaries across macOS and Windows\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"ffmpeg\",\"ffprobe\",\"audio\",\"video\",\"desktop\",\"media\"]"
  related-skills: "[\"pyside6-desktop-engineering\",\"desktop-filesystem-safety\",\"pyinstaller-desktop-release\",\"performance-optimization\",\"security-best-practices\",\"verification-before-completion\"]"
  source: "Broville synthesis from FFmpeg and ffprobe documentation"
  source-url: "https://ffmpeg.org/ffmpeg.html"
---

# Desktop Media Pipeline

## Description

Implement media workflows that are deterministic, responsive, safe for user files, and functional after packaging. This skill covers probing, preview preparation, transcoding, progress, cancellation, caching, publication, and bundled tool execution; it does not choose creative output settings without a product requirement.

## Prerequisites

- Supported input and output formats, codecs, quality targets, metadata policy, and overwrite rules.
- An approved FFmpeg distribution and an understood licensing posture for its configured codecs.
- Exact FFmpeg and ffprobe binaries for every target platform and architecture.
- The repository's worker, packaging, filesystem, and release conventions.

## Steps

1. Define an immutable media job before starting a subprocess: canonical input identity, selected streams, operation, output container and codecs, quality or bitrate settings, metadata policy, destination, overwrite behavior, and cancellation semantics.

2. Resolve the project's pinned binary explicitly. Installed applications must not depend on a developer shell, Homebrew, system Python, or an arbitrary executable found first on `PATH`. Record binary version and build configuration.

   ```bash
   path/to/ffmpeg -version
   path/to/ffprobe -version
   ```

3. Probe before transforming. Request machine-readable JSON with only the fields needed for the decision.

   ```bash
   path/to/ffprobe -v error -show_format -show_streams -of json path/to/input
   ```

   Expected result: valid JSON is parsed with explicit handling for missing duration, tags, streams, or unknown codecs. Treat probe output and media metadata as untrusted data.

4. Build subprocess arguments as a list and invoke without a shell. Keep paths as individual arguments, define timeouts where appropriate, bound captured output, and redact sensitive paths or metadata from logs when the product requires it. Never concatenate a filename into a shell command.

5. Run probe and transform work outside the GUI thread. Stream progress from a supported machine-readable channel, throttle UI updates, and preserve the main event loop. Cancellation should terminate the process tree, wait for exit, and remove only the job's own incomplete output.

6. Protect originals and destinations.

   - Never transform the input in place.
   - Encode to a private temporary path in the destination directory.
   - Refuse an existing destination unless replacement was explicitly authorized.
   - Verify the completed output, then publish it using the filesystem policy.
   - Keep database updates transactional with publication.

7. Verify the output independently with ffprobe. Check container, selected streams, codecs, duration tolerance, channel or pixel properties, sample or frame rate, and required metadata. For perceptual requirements, include representative listening or viewing evidence rather than inferring quality from exit status.

8. Cache only when the key captures source identity and every output-affecting setting, including tool version where relevant. Invalidate on source replacement, option change, or incompatible binary upgrade. Bound cache size and expose a safe recovery path.

9. Package the exact binaries, licenses, and required runtime libraries. Test from the frozen application on clean macOS and Windows hosts, including paths with spaces and Unicode, long jobs, malformed files, unsupported codecs, cancellation, low disk space, and app shutdown.

## Pitfalls

- Trusting an extension instead of probing the actual container and streams.
- Passing user-controlled paths through a shell.
- Blocking the UI while waiting for a process or reading full stderr after its pipe fills.
- Treating FFmpeg exit status 0 as proof that the output meets the product contract.
- Overwriting an existing export or publishing a partial file under its final name.
- Selecting the first stream without accounting for cover art, alternate audio, or multiple video streams.
- Parsing human-oriented console text when a structured probe or progress channel exists.
- Shipping binaries without verifying target architecture, redistribution terms, and clean-machine execution.

## Verification

1. Unit tests cover job construction, stream selection, path handling, progress parsing, cache keys, and error mapping.
2. Integration fixtures cover valid, malformed, truncated, unsupported, multi-stream, Unicode-path, and cancellation cases.
3. Published outputs pass an independent ffprobe contract check and preserve or omit metadata as specified.
4. Originals and pre-existing destinations remain byte-for-byte unchanged unless replacement was explicitly authorized.
5. Packaged macOS and Windows builds invoke their bundled binaries successfully without developer-environment fallbacks.

## Cross-References

- [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html)
- [ffprobe documentation](https://ffmpeg.org/ffprobe.html)
- Use `desktop-filesystem-safety` for publication, collision, and removable-drive behavior.
- Use `pyinstaller-desktop-release` to include binaries and licenses in frozen Python applications.
- Use `pyside6-desktop-engineering` for Qt worker and shutdown integration.
