#!/usr/bin/env python3
"""Exercise package composition and invalid catalogs using temporary files only."""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from validate_marketplace import validate
from validate_skills import Validation, parse_frontmatter


ROOT = Path(__file__).resolve().parents[1]


def skill_inventory(root: Path) -> dict[str, Path]:
    inventory = {}
    for path in root.rglob("SKILL.md"):
        parsed = parse_frontmatter(path, Validation())
        assert parsed is not None
        name = parsed[0]["name"]
        assert name not in inventory
        inventory[name] = path
    return inventory


def main() -> int:
    catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    originals = {path.relative_to(ROOT): path.read_bytes() for path in ROOT.glob("skills/*/*/SKILL.md")}
    inventories = {}
    with tempfile.TemporaryDirectory(prefix="broville-package-check-") as temporary:
        staging = Path(temporary)
        for entry in catalog["plugins"]:
            source = ROOT / entry["source"]["path"]
            archive = staging / f"{entry['name']}.zip"
            members = {path.relative_to(source).as_posix(): path.read_bytes() for path in source.rglob("*") if path.is_file()}
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
                for name, data in members.items():
                    package.writestr(f"{entry['name']}/{name}", data)
            with zipfile.ZipFile(archive) as package:
                assert package.testzip() is None
                assert all(package.read(f"{entry['name']}/{name}") == data for name, data in members.items())
                package.extractall(staging / "unpacked")
            unpacked = staging / "unpacked" / entry["name"]
            manifest = json.loads((unpacked / ".codex-plugin/plugin.json").read_text())
            assert manifest["name"] == entry["name"]
            # Native compatibility packages use recursive discovery, including root SKILL.md.
            # Installation can rename a plugin root; skill identity comes from frontmatter.
            inventory = skill_inventory(unpacked)
            source_inventory = skill_inventory(source)
            assert set(inventory) == set(source_inventory)
            assert all(path.read_bytes() == source_inventory[name].read_bytes() for name, path in inventory.items())
            inventories[entry["name"]] = inventory

        # Nested individual manifests are metadata inside bundles, with no new skill copies.
        for skill in ROOT.glob("skills/*/*/SKILL.md"):
            bundle = inventories[f"broville-{skill.parent.parent.name}"][skill.parent.name]
            individual = inventories[f"broville-skill-{skill.parent.name}"][skill.parent.name]
            assert bundle != individual
            assert bundle.read_bytes() == individual.read_bytes()
            assert (bundle.parent / ".codex-plugin/plugin.json").is_file()
            # Distinct physical package paths demonstrate overlap; this does not assert host deduplication.

        fixture = staging / "fixture"
        shutil.copytree(ROOT / "skills", fixture / "skills")
        path = fixture / ".agents/plugins/marketplace.json"
        path.parent.mkdir(parents=True)
        cases = {
            "escaping source": lambda data: data["plugins"][1]["source"].update(path="./../outside"),
            "duplicate individual": lambda data: data["plugins"].append(data["plugins"][1]),
            "missing individual": lambda data: data["plugins"].pop(1),
            "missing bundle": lambda data: data["plugins"].pop(0),
            "wrong category": lambda data: data["plugins"][1].update(category="Finance"),
        }
        for label, mutate in cases.items():
            data = json.loads(json.dumps(catalog))
            mutate(data)
            path.write_text(json.dumps(data))
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    validate(fixture)
            except (OSError, ValueError, KeyError, TypeError):
                pass
            else:
                raise AssertionError(f"accepted {label}")

        path.write_text(json.dumps(catalog, indent=2) + "\n")
        stale = fixture / catalog["plugins"][1]["source"]["path"] / ".codex-plugin/plugin.json"
        stale.write_text("{}\n")
        command = [sys.executable, str(ROOT / "scripts/build_marketplace.py"), "--repo-root", str(fixture)]
        assert subprocess.run([*command, "--check"], capture_output=True).returncode == 1
        subprocess.run(command, check=True, capture_output=True)
        subprocess.run([*command, "--check"], check=True, capture_output=True)

    assert all((ROOT / path).read_bytes() == data for path, data in originals.items())
    print(f"Package checks passed for {len(inventories)} plugins; overlap paths, regeneration, and invalid catalogs checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
