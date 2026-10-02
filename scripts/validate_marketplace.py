#!/usr/bin/env python3
"""Check category bundles and individual plugins without installing or executing them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_skills import NAME_PATTERN, SEMVER_PATTERN, Validation, parse_frontmatter
from build_marketplace import CATEGORY_LABELS


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
    bundles: dict[str, set[Path]] = {}
    individuals: set[Path] = set()
    names: set[str] = set()
    for entry in entries:
        name = entry["name"]
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name) or len(name) > 64 or name in names:
            raise ValueError(f"invalid or duplicate plugin name: {name}")
        names.add(name)
        if entry["source"]["source"] != "local":
            raise ValueError(f"{name}: skill plugins must use local sources")
        root = contained_directory(repo_root, entry["source"]["path"])
        relative = root.relative_to(repo_root).parts
        if len(relative) not in (2, 3) or relative[0] != "skills" or relative[1] not in CATEGORY_LABELS:
            raise ValueError(f"{name}: source must be a canonical category or skill directory")
        category = relative[1]
        is_bundle = len(relative) == 2
        expected_name = f"broville-{category}" if is_bundle else f"broville-skill-{relative[2]}"
        if name != expected_name:
            raise ValueError(f"{name}: expected plugin identity {expected_name}")
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
        if entry["category"] != CATEGORY_LABELS[category]:
            raise ValueError(f"{name}: category label does not match its canonical category")
        if category not in manifest.get("keywords", []):
            raise ValueError(f"{name}: category must be searchable through keywords")
        if not isinstance(interface["capabilities"], list):
            raise ValueError(f"{name}: capabilities must be an array")
        if entry["policy"] != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            raise ValueError(f"{name}: category plugins must remain available for opt-in installation")
        if any(field in manifest for field in ("apps", "hooks")):
            raise ValueError(f"{name}: app bindings and hooks are not supported")
        mcp_path = root / "mcp.json"
        if "mcpServers" in manifest:
            if is_bundle or manifest["mcpServers"] != "./mcp.json" or not mcp_path.is_file():
                raise ValueError(f"{name}: MCP must be a contained individual-package manifest")
            portable = json.loads((root / "plugin.json").read_text())
            for key in ("name", "version", "description", "author", "repository", "license", "keywords"):
                if portable.get(key) != manifest.get(key):
                    raise ValueError(f"{name}: portable and native identity metadata differ")
            if portable.get("extensions", {}).get("com.openai", {}).get("interface") != interface:
                raise ValueError(f"{name}: portable and native presentation differ")
            config = json.loads(mcp_path.read_text())
            servers = config.get("mcpServers")
            if not isinstance(servers, dict) or len(servers) != 1:
                raise ValueError(f"{name}: expected one local MCP server")
            server = next(iter(servers.values()))
            if (server.get("type") != "stdio" or server.get("command") != "python3"
                    or server.get("cwd") != "${PLUGIN_ROOT}"
                    or server.get("args") != ["${PLUGIN_ROOT}/scripts/server.py"]
                    or set(server) != {"type", "command", "args", "cwd"}
                    or not (root / "scripts/server.py").is_file()):
                raise ValueError(f"{name}: unsupported or nonportable local MCP entrypoint")
        elif mcp_path.is_file() and not is_bundle:
            raise ValueError(f"{name}: individual MCP manifest is not connected")
        skills_root = contained_directory(root, manifest["skills"])
        if skills_root != root:
            raise ValueError(f"{name}: discovery must stay at the canonical plugin root")
        # Codex compatibility manifests use recursive discovery, including a root SKILL.md.
        skills = sorted(skills_root.rglob("SKILL.md"))
        if not skills:
            raise ValueError(f"{name}: no discoverable skill packages")
        expected = {path for path in canonical if path.parent.parent.name == category} if is_bundle else {root / "SKILL.md"}
        actual = {skill.resolve() for skill in skills}
        if actual != expected:
            raise ValueError(f"{name}: unexpected skill inventory for {'bundle' if is_bundle else 'individual'} plugin")
        if is_bundle:
            if category in bundles:
                raise ValueError(f"{name}: category bundle is packaged more than once")
            bundles[category] = actual
        for skill in skills:
            path = skill.resolve()
            if path not in canonical or (not is_bundle and path in individuals):
                raise ValueError(f"{name}: non-canonical or duplicate individual skill: {skill}")
            result = Validation()
            parsed = parse_frontmatter(skill, result)
            if parsed is None or parsed[0].get("name") != skill.parent.name:
                raise ValueError(f"{name}: invalid skill discovery metadata: {skill}")
            if not is_bundle:
                individuals.add(path)
        for path in root.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"{name}: symlinks must not be packaged: {path}")
        print(f"{name}: {len(skills)} skills, version {manifest['version']}")
    if set(bundles) != set(CATEGORY_LABELS) or individuals != canonical:
        missing = sorted(str(path.relative_to(repo_root)) for path in canonical - individuals)
        raise ValueError(f"marketplace needs every category bundle and individual skill; missing individuals: {missing}")
    return len(entries), len(individuals)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        plugins, skills = validate(args.repo_root.resolve())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Marketplace validation failed: {exc}\n")
    print(f"Validated {plugins} plugins: {len(CATEGORY_LABELS)} category bundles and {skills} individual skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
