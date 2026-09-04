#!/usr/bin/env python3
"""Validate Broville skills against the open Agent Skills contract."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by a missing dependency
    raise SystemExit(
        "PyYAML is required. Install validation dependencies with "
        "`python -m pip install PyYAML skills-ref`."
    ) from exc


ROOT_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
REQUIRED_ROOT_FIELDS = {"name", "description", "license", "compatibility", "metadata"}
REQUIRED_METADATA_FIELDS = {
    "author",
    "version",
    "platforms",
    "triggers",
    "inputs",
    "outputs",
    "tags",
    "related-skills",
}
JSON_ARRAY_FIELDS = {
    "platforms",
    "triggers",
    "inputs",
    "outputs",
    "tags",
    "related-skills",
    "aliases",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
ABSOLUTE_USER_PATHS = (
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"/home/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
)
REQUIRED_HEADINGS = ("Description", "Pitfalls", "Verification")


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: Path, message: str) -> None:
        self.warnings.append(f"{path}: {message}")


def parse_frontmatter(
    path: Path, result: Validation
) -> tuple[dict[str, Any], str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        result.error(path, "must begin with YAML frontmatter")
        return None
    parts = text.split("---", 2)
    if len(parts) != 3:
        result.error(path, "frontmatter closing delimiter is missing")
        return None
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        result.error(path, f"invalid YAML frontmatter: {exc}")
        return None
    if not isinstance(data, dict):
        result.error(path, "frontmatter must be a mapping")
        return None
    return data, parts[2].lstrip("\n")


def decode_array(
    path: Path, metadata: dict[str, str], field: str, result: Validation
) -> list[Any] | None:
    value = metadata.get(field)
    if value is None:
        return None
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError as exc:
        result.error(path, f"metadata.{field} must contain a JSON array string: {exc}")
        return None
    if not isinstance(decoded, list):
        result.error(path, f"metadata.{field} must contain a JSON array string")
        return None
    return decoded


def validate_skill(
    skill_path: Path,
    known_names: set[str],
    seen_names: dict[str, Path],
    result: Validation,
) -> None:
    parsed = parse_frontmatter(skill_path, result)
    if parsed is None:
        return
    frontmatter, body = parsed

    unknown = set(frontmatter) - ROOT_FIELDS
    missing = REQUIRED_ROOT_FIELDS - set(frontmatter)
    if unknown:
        result.error(skill_path, f"non-standard frontmatter fields: {sorted(unknown)}")
    if missing:
        result.error(
            skill_path, f"missing required frontmatter fields: {sorted(missing)}"
        )
        return
    if "allowed-tools" in frontmatter:
        result.error(
            skill_path,
            "allowed-tools is implementation-specific; express runtime tools in Prerequisites",
        )

    name = frontmatter.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        result.error(skill_path, "name must be 1-64 lowercase kebab-case characters")
    elif name != skill_path.parent.name:
        result.error(skill_path, f"name {name!r} does not match its directory")
    elif name in seen_names:
        result.error(skill_path, f"duplicate name also used by {seen_names[name]}")
    else:
        seen_names[name] = skill_path

    description = frontmatter.get("description")
    if not isinstance(description, str) or not (1 <= len(description) <= 1024):
        result.error(skill_path, "description must be a 1-1024 character string")
    compatibility = frontmatter.get("compatibility")
    if not isinstance(compatibility, str) or not (1 <= len(compatibility) <= 500):
        result.error(skill_path, "compatibility must be a 1-500 character string")

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        result.error(skill_path, "metadata must be a string-to-string mapping")
        return
    non_string = [
        key
        for key, value in metadata.items()
        if not isinstance(key, str) or not isinstance(value, str)
    ]
    if non_string:
        result.error(
            skill_path,
            f"metadata values must be strings: {sorted(map(str, non_string))}",
        )
        return
    missing_metadata = REQUIRED_METADATA_FIELDS - set(metadata)
    if missing_metadata:
        result.error(skill_path, f"missing metadata fields: {sorted(missing_metadata)}")

    version = metadata.get("version", "")
    if not SEMVER_PATTERN.fullmatch(version):
        result.error(skill_path, f"metadata.version is not valid SemVer: {version!r}")

    arrays: dict[str, list[Any]] = {}
    for field in JSON_ARRAY_FIELDS & set(metadata):
        decoded = decode_array(skill_path, metadata, field, result)
        if decoded is not None:
            arrays[field] = decoded
    if not arrays.get("triggers") or not all(
        isinstance(item, str) and item.strip() for item in arrays.get("triggers", [])
    ):
        result.error(
            skill_path, "metadata.triggers must contain at least one non-empty string"
        )
    for field in ("platforms", "tags", "related-skills", "aliases"):
        if field in arrays and not all(isinstance(item, str) for item in arrays[field]):
            result.error(skill_path, f"metadata.{field} must contain only strings")
    for field in ("inputs", "outputs"):
        if field in arrays and not all(
            isinstance(item, dict) for item in arrays[field]
        ):
            result.error(skill_path, f"metadata.{field} must contain only objects")
    for related in arrays.get("related-skills", []):
        if isinstance(related, str) and related not in known_names:
            result.error(skill_path, f"related skill does not exist: {related}")

    if not re.search(r"^#\s+\S", body, re.MULTILINE):
        result.error(skill_path, "body must contain an H1 title")
    for heading in REQUIRED_HEADINGS:
        if not re.search(
            rf"^##\s+{re.escape(heading)}\s*$", body, re.MULTILINE | re.IGNORECASE
        ):
            result.error(skill_path, f"body is missing required '## {heading}' section")
    if len(body.splitlines()) > 500:
        result.warn(skill_path, "SKILL.md body exceeds the recommended 500-line limit")

    for pattern in ABSOLUTE_USER_PATHS:
        if pattern.search(body):
            result.error(skill_path, "contains a machine-specific absolute user path")
            break
    if ".hermes/" in body or "~/.hermes" in body:
        result.error(
            skill_path,
            "contains a Hermes-specific path; use a skill-relative or provider-neutral path",
        )

    for child in skill_path.parent.rglob("*"):
        if child.is_symlink():
            result.error(
                child, "symlinks are not portable; include an ordinary file copy"
            )
        if child.is_file() and (
            child.suffix in {".pyc", ".pyo"} or child.name == ".DS_Store"
        ):
            result.error(
                child, "generated platform-specific artifact must not be packaged"
            )


def run_official_validator(skill_paths: list[Path], result: Validation) -> None:
    executable = shutil.which("agentskills")
    if executable is None:
        result.error(
            Path("scripts/validate_skills.py"),
            "official validator not found; install the skills-ref package",
        )
        return
    for skill_path in skill_paths:
        completed = subprocess.run(
            [executable, "validate", str(skill_path.parent)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stdout + completed.stderr).strip().replace("\n", " | ")
            result.error(
                skill_path, f"official Agent Skills validation failed: {detail}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--skip-official", action="store_true", help="skip skills-ref validation"
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    skill_paths = sorted(repo_root.glob("skills/*/*/SKILL.md"))
    result = Validation()
    if not skill_paths:
        result.error(repo_root / "skills", "no skill entrypoints found")
    known_names = {path.parent.name for path in skill_paths}
    seen_names: dict[str, Path] = {}
    for skill_path in skill_paths:
        validate_skill(skill_path, known_names, seen_names, result)
    if not args.skip_official:
        run_official_validator(skill_paths, result)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if result.errors:
        print(
            f"Validation failed: {len(result.errors)} error(s), {len(result.warnings)} warning(s).",
            file=sys.stderr,
        )
        return 1
    print(
        f"Validated {len(skill_paths)} skills: 0 errors, {len(result.warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
