#!/usr/bin/env python3
"""Install complete Broville skill packages into an agent discovery directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

AGENT_PATHS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
    "copilot": Path(".agents/skills"),
    "cursor": Path(".cursor/skills"),
    "gemini": Path(".agents/skills"),
    "opencode": Path(".agents/skills"),
    "generic": Path(".agents/skills"),
}


def discover(source_root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for entrypoint in sorted(source_root.glob("*/*/SKILL.md")):
        name = entrypoint.parent.name
        if name in found:
            raise SystemExit(
                f"Duplicate skill name {name!r}: {found[name]} and {entrypoint.parent}"
            )
        found[name] = entrypoint.parent
    if not found:
        raise SystemExit(f"No skills found under {source_root}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=sorted(AGENT_PATHS), default="generic")
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument(
        "--workspace",
        type=Path,
        help="project root; the agent's standard discovery path is appended",
    )
    destination.add_argument(
        "--target",
        type=Path,
        help="explicit skills directory for any standard-compatible host",
    )
    parser.add_argument(
        "--skill", action="append", default=[], help="skill name; repeat as needed"
    )
    parser.add_argument(
        "--force", action="store_true", help="replace existing skill directories"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="print actions without copying"
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "skills",
    )
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    available = discover(source_root)
    requested = args.skill or sorted(available)
    unknown = sorted(set(requested) - set(available))
    if unknown:
        raise SystemExit(f"Unknown skill name(s): {', '.join(unknown)}")
    if len(requested) != len(set(requested)):
        raise SystemExit("A skill was selected more than once")

    target_root = (
        args.target.resolve()
        if args.target
        else args.workspace.resolve() / AGENT_PATHS[args.agent]
    )
    actions: list[tuple[Path, Path]] = []
    for name in requested:
        source = available[name]
        target = target_root / name
        if target.exists() and not args.force:
            raise SystemExit(f"Target exists: {target} (use --force to replace it)")
        actions.append((source, target))

    for source, target in actions:
        print(f"{source} -> {target}")
        if args.dry_run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.copytree(source, target, symlinks=False)

    mode = "Would install" if args.dry_run else "Installed"
    print(f"{mode} {len(actions)} skill(s) for {args.agent} in {target_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
