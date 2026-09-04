#!/usr/bin/env python3
"""Cross-platform smoke tests for the Broville skill installer."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_skills.py"
EXPECTED_PATHS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
    "copilot": Path(".agents/skills"),
    "cursor": Path(".cursor/skills"),
    "gemini": Path(".agents/skills"),
    "opencode": Path(".agents/skills"),
    "generic": Path(".agents/skills"),
}


def run(*arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, str(INSTALLER), *arguments],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != expected:
        raise AssertionError(
            f"installer returned {completed.returncode}, expected {expected}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="broville-skills-") as temporary:
        temp_root = Path(temporary)
        for agent, relative_root in EXPECTED_PATHS.items():
            workspace = temp_root / agent
            run("--agent", agent, "--workspace", str(workspace))
            installed = workspace / relative_root
            assert len(list(installed.glob("*/SKILL.md"))) == 85
            assert (installed / "playwright" / "SKILL.md").is_file()
            assert (installed / "playwright" / "references" / "cli.md").is_file()
            assert (installed / "web-accessibility" / "SKILL.md").is_file()

        explicit = temp_root / "explicit"
        run("--target", str(explicit), "--skill", "playwright")
        run("--target", str(explicit), "--skill", "playwright", expected=1)
        run("--target", str(explicit), "--skill", "playwright", "--force")
        assert (explicit / "playwright" / "SKILL.md").is_file()

        dry_run = temp_root / "dry-run"
        run("--target", str(dry_run), "--skill", "playwright", "--dry-run")
        assert not dry_run.exists()

    print("Installer smoke tests passed for all supported discovery adapters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
