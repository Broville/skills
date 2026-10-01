#!/usr/bin/env python3
"""Check Broville's category marketplace without installing or executing plugins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_skills import NAME_PATTERN, SEMVER_PATTERN, Validation, parse_frontmatter


def contained_directory(root: Path, value: object) -> Path:
    if (
        not isinstance(value, str)
        or not value.startswith("./")
        or "\\" in value
        or ".." in value.split("/")
    ):
        raise ValueError("directory must use a ./-prefixed path without .. or backslashes")
    path = root / value
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_dir():
        raise ValueError(f"directory is missing or escapes its root: {value}")
    return path.resolve()


def validate(repo_root: Path) -> tuple[int, int]:
    catalog = json.loads((repo_root / ".agents/plugins/marketplace.json").read_text())
    if not NAME_PATTERN.fullmatch(catalog["name"]):
        raise ValueError("marketplace name must be lowercase kebab-case")
    if not catalog["interface"]["displayName"].strip():
        raise ValueError("marketplace displayName is required")
    entries = catalog["plugins"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("marketplace must contain plugin entries")

    canonical = {path.resolve() for path in repo_root.glob("skills/*/*/SKILL.md")}
    discovered: set[Path] = set()
    names: set[str] = set()
    for entry in entries:
        name = entry["name"]
        if not NAME_PATTERN.fullmatch(name) or len(name) > 64 or name in names:
            raise ValueError(f"invalid or duplicate plugin name: {name}")
        names.add(name)
        if entry["source"]["source"] != "local":
            raise ValueError(f"{name}: category plugins must use local sources")
        root = contained_directory(repo_root, entry["source"]["path"])
        manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
        if manifest["name"] != name:
            raise ValueError(f"{name}: catalog and manifest identities differ")
        if not SEMVER_PATTERN.fullmatch(manifest["version"]):
            raise ValueError(f"{name}: plugin version must be SemVer")
        if not manifest["description"].strip() or not manifest["author"]["name"].strip():
            raise ValueError(f"{name}: description and author are required")
        interface = manifest["interface"]
        for field in ("displayName", "shortDescription", "longDescription", "developerName"):
            if not isinstance(interface[field], str) or not interface[field].strip():
                raise ValueError(f"{name}: interface.{field} must be non-empty text")
        for field in ("displayName", "shortDescription"):
            if len(interface[field]) > 30:
                raise ValueError(f"{name}: interface.{field} exceeds 30 characters")
        if interface["category"] != entry["category"]:
            raise ValueError(f"{name}: catalog and listing categories differ")
        if not isinstance(interface["capabilities"], list):
            raise ValueError(f"{name}: capabilities must be an array")
        if entry["policy"] != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            raise ValueError(f"{name}: category plugins must remain available for opt-in installation")
        if any(field in manifest for field in ("apps", "hooks", "mcpServers")):
            raise ValueError(f"{name}: this catalog only wraps existing skill packages")
        skills_root = contained_directory(root, manifest["skills"])
        skills = sorted(skills_root.glob("*/SKILL.md"))
        if not skills:
            raise ValueError(f"{name}: no directly discoverable skill packages")
        for skill in skills:
            path = skill.resolve()
            if path not in canonical or path in discovered:
                raise ValueError(f"{name}: non-canonical or multiply packaged skill: {skill}")
            result = Validation()
            parsed = parse_frontmatter(skill, result)
            if parsed is None or parsed[0].get("name") != skill.parent.name:
                raise ValueError(f"{name}: invalid skill discovery metadata: {skill}")
            discovered.add(path)
        for path in root.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"{name}: symlinks must not be packaged: {path}")
        print(f"{name}: {len(skills)} skills, version {manifest['version']}")
    if discovered != canonical:
        missing = sorted(str(path.relative_to(repo_root)) for path in canonical - discovered)
        raise ValueError(f"marketplace omits canonical skills: {missing}")
    return len(entries), len(discovered)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        plugins, skills = validate(args.repo_root.resolve())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Marketplace validation failed: {exc}\n")
    print(f"Validated {plugins} category plugins covering all {skills} canonical skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
