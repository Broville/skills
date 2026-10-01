#!/usr/bin/env python3
"""Generate individual plugin metadata from canonical skills, without copying skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_skills import Validation, parse_frontmatter


CATEGORY_LABELS = {
    "creative": "Creative",
    "data": "Data",
    "data-science": "Data Science",
    "devops": "DevOps",
    "finance": "Finance",
    "health": "Health",
    "mlops": "ML Ops",
    "monitoring": "Monitoring",
    "productivity": "Productivity",
    "research": "Research",
    "software-dev": "Software Development",
}


def generated_files(root: Path) -> dict[Path, str]:
    catalog_path = root / ".agents/plugins/marketplace.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    existing = {entry["name"]: entry for entry in catalog["plugins"]}
    entries = []
    files: dict[Path, str] = {}
    for category, label in CATEGORY_LABELS.items():
        bundle = existing[f"broville-{category}"]
        bundle["category"] = label
        entries.append(bundle)
        for skill in sorted((root / "skills" / category).glob("*/SKILL.md")):
            result = Validation()
            parsed = parse_frontmatter(skill, result)
            if parsed is None:
                raise ValueError(f"invalid frontmatter: {skill}: {result.errors}")
            data, _ = parsed
            name = data["name"]
            plugin_name = f"broville-skill-{name}"
            display_name = name.replace("-", " ").title()
            if name == "stable-diffusion-image-generation":
                display_name = "Stable Diffusion Images"
            subtitle_category = "Software Dev" if category == "software-dev" else label
            manifest = {
                "name": plugin_name,
                "version": data["metadata"]["version"],
                "description": data["description"],
                "author": {"name": "Broville", "url": "https://github.com/Broville"},
                "repository": "https://github.com/Broville/skills",
                "license": "MIT",
                "keywords": [category, label, name, "individual-skill"],
                "skills": "./",
                "interface": {
                    "displayName": display_name,
                    "shortDescription": f"{subtitle_category} · single skill",
                    "longDescription": (
                        f"{label}: install only {name}. {data['description']} "
                        "Read the skill's prerequisites before use. "
                        "Choose this individual plugin or its category bundle to avoid overlapping copies."
                    ),
                    "developerName": "Broville",
                    "category": label,
                    "capabilities": [],
                },
            }
            path = skill.parent / ".codex-plugin/plugin.json"
            files[path] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
            entries.append({
                "name": plugin_name,
                "source": {"source": "local", "path": f"./skills/{category}/{name}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": label,
            })
    catalog["plugins"] = entries
    files[catalog_path] = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="fail on stale metadata without writing")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    stale = []
    for path, expected in generated_files(root).items():
        if path.is_file() and path.read_text(encoding="utf-8") == expected:
            continue
        if args.check:
            stale.append(str(path.relative_to(root)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
    if stale:
        parser.exit(1, "Stale marketplace metadata; run python scripts/build_marketplace.py:\n" + "\n".join(stale) + "\n")
    print("Individual plugin metadata and marketplace are up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
