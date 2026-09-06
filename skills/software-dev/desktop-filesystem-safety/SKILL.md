---
name: "desktop-filesystem-safety"
description: "Design and verify safe cross-platform desktop file workflows across local, removable, network, and cloud-backed storage."
license: "MIT"
compatibility: "Open Agent Skills format. Applies to desktop applications on macOS, Windows, and Linux; native edge-case verification requires the target filesystems and operating systems."
metadata:
  author: "Broville"
  version: "1.0.0"
  platforms: "[\"linux\",\"macos\",\"windows\"]"
  triggers: "[\"User asks to implement or review desktop file copy, move, rename, link, import, export, relink, scan, or delete behavior\",\"A workflow touches removable drives, network shares, cloud placeholders, aliases, shortcuts, symlinks, hard links, or case-insensitive filesystems\",\"A file operation must be non-overwriting, transactional, recoverable, or resilient to mid-operation changes\"]"
  inputs: "[]"
  outputs: "[]"
  tags: "[\"filesystem\",\"desktop\",\"safety\",\"cross-platform\",\"files\"]"
  related-skills: "[\"pyside6-desktop-engineering\",\"desktop-media-pipeline\",\"security-best-practices\",\"test-driven-development\",\"verification-before-completion\"]"
  source: "Broville synthesis from Python filesystem documentation and validated cross-platform desktop workflows"
  source-url: "https://docs.python.org/3/library/pathlib.html"
---

# Desktop Filesystem Safety

## Description

Engineer file workflows that preserve user data when paths can disappear, change identity, collide by case, resolve through indirection, or behave differently across operating systems. Apply the smallest policy that fits the operation: reading, linking, copying, moving, renaming, replacing, or deleting have different safety contracts.

Project rules define ownership and overwrite policy. Never turn an ambiguous request such as "import" or "attach" into a copy, move, or deletion without establishing its meaning.

## Prerequisites

- The repository's data-ownership, persistence, recovery, and concurrency rules.
- A written source and destination contract, including allowed file types and indirection policy.
- Representative native filesystems for platform-specific validation.

## Steps

1. Define the operation before coding. State whether it reads, records a link, copies bytes, moves an existing object, renames in place, replaces a destination, or deletes. Identify who owns each path and what must remain unchanged on failure.

2. Separate cheap eligibility from authoritative validation. UI hover and browse filters may inspect names and URL type, but destructive or durable operations must validate immediately before use. Require the intended local-file semantics, regular-file or directory type, readability or writability, extension/content policy, and parent existence.

3. Decide how indirection is handled on each platform.

   - Treat symbolic links, broken links, Finder aliases, Windows shortcuts, and reparse points explicitly.
   - Distinguish path spelling from file identity so hard links, case aliases, and normalized paths do not create accidental duplicates.
   - Accept cloud-backed placeholders only when the operation can open the content at execution time.
   - Do not infer a missing file's replacement from a same-named neighbor.

4. Canonicalize only for the purpose that needs it. Preserve user-facing spelling where useful, but store stable IDs or anchors when objects may move. Reject paths that escape an authorized root after resolution. Account for case-insensitive comparison, reserved Windows names, path-length behavior, Unicode normalization, and files that vanish between checks.

5. Make copy and publication non-overwriting by construction.

   - Write to a private temporary file in the destination directory.
   - Copy incrementally and handle short writes and I/O failures.
   - Flush and sync when durability is part of the contract.
   - Recheck source identity when changing during the copy would be unsafe.
   - Publish atomically or exclusively according to the collision policy.
   - Remove only the operation's own incomplete temporary file after failure.

6. Isolate multiple inputs. Validate and report each source independently unless the user-facing contract promises all-or-nothing behavior. For database-backed batches, use a transaction so a late persistence failure cannot commit an earlier partial result contrary to the reported outcome.

7. Keep slow storage work off the UI thread. Pass immutable paths and policy to the worker, return immutable validated results, and let the owning thread persist them. Define cancellation and close behavior; a worker must not outlive resources it still owns.

8. Design recovery before deletion or replacement. Prefer trash or versioned backup when practical. Resolve exact targets with read-only checks, avoid unresolved globs and broad roots, and report what was removed and whether it can be recovered.

9. Test adversarial changes: source replaced mid-operation, destination collision, permissions lost, volume disconnected, placeholder offline, same file through different paths, locked Windows handle, partial disk, shared directory, and application interruption.

## Pitfalls

- Treating `exists()` followed by use as an atomic guarantee.
- Assuming `resolve()` proves authorization or preserves the identity the user selected.
- Using check-then-write collision handling that can overwrite a file created between those steps.
- Following aliases, shortcuts, or symlinks without an explicit product rule.
- Performing recursive deletion against a broad root, unresolved variable, glob, or user home directory.
- Updating durable state before the filesystem operation is complete and verified.
- Closing or replacing files that remain open on Windows.
- Testing only a fast local, case-sensitive or case-insensitive disk and inferring removable, network, or cloud behavior.

## Verification

1. Focused tests prove the operation's ownership, overwrite, collision, indirection, and transaction contracts.
2. Fault-injection tests leave no unintended destination, orphaned database row, or user-file damage.
3. Native tests cover supported case behavior, removable or network loss, cloud placeholders, and locked handles where applicable.
4. UI responsiveness and close/cancel behavior remain correct during slow I/O.
5. The final evidence names the exact filesystems and platforms observed; untested environments remain pending.

## Cross-References

- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python shutil](https://docs.python.org/3/library/shutil.html)
- [Python os filesystem operations](https://docs.python.org/3/library/os.html#files-and-directories)
- Use `desktop-media-pipeline` when the file is inspected or transformed by an external media process.
- Use `pyside6-desktop-engineering` for worker ownership and responsive Qt integration.
