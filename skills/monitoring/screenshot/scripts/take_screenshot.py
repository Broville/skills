#!/usr/bin/env python3
"""Linux screenshot helper with automatic X11/Wayland detection.

Detects the display server type and selects the appropriate capture tool.
On X11: prefers scrot, then gnome-screenshot, then ImageMagick import.
On Wayland: uses grim (with slurp for interactive region selection).

Usage:
    python3 take_screenshot.py                          # Full screen, default location
    python3 take_screenshot.py --path output/screen.png # Full screen, explicit path
    python3 take_screenshot.py --mode temp              # Full screen, /tmp directory
    python3 take_screenshot.py --region 100,200,800,600 # Region capture
    python3 take_screenshot.py --active-window          # Active window capture
    python3 take_screenshot.py --detect-only            # Print display server and exit
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def detect_display_server() -> str:
    """Detect whether the session is X11 or Wayland."""
    session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if session_type == "wayland":
        return "wayland"
    if session_type == "x11":
        return "x11"
    # Fallback: check for Wayland-specific env vars
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    return "unknown"


def find_tool(candidates: list[str]) -> str | None:
    """Return the first candidate that exists on PATH."""
    for cmd in candidates:
        if shutil.which(cmd):
            return cmd
    return None


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def default_output_path(mode: str) -> Path:
    if mode == "temp":
        return Path(f"/tmp/screenshot-{timestamp()}.png")
    # Default save location
    pictures = Path.home() / "Pictures" / "Screenshots"
    pictures.mkdir(parents=True, exist_ok=True)
    return pictures / f"screenshot-{timestamp()}.png"


def parse_region(value: str) -> tuple[int, int, int, int]:
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("region must be x,y,w,h")
    try:
        x, y, w, h = (int(p) for p in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("region values must be integers") from exc
    if w <= 0 or h <= 0:
        raise argparse.ArgumentTypeError("region width and height must be positive")
    return x, y, w, h


def capture_x11(output: Path, args: argparse.Namespace) -> None:
    """Capture a screenshot on X11."""
    scrot = shutil.which("scrot")
    gnome = shutil.which("gnome-screenshot")
    imagemagick = shutil.which("import")
    xdotool = shutil.which("xdotool")

    output.parent.mkdir(parents=True, exist_ok=True)

    if args.region is not None:
        x, y, w, h = args.region
        if scrot:
            subprocess.run(["scrot", "-a", f"{x},{y},{w},{h}", str(output)], check=True)
            return
        if imagemagick:
            subprocess.run(
                ["import", "-window", "root", "-crop", f"{w}x{h}+{x}+{y}", str(output)],
                check=True,
            )
            return
        sys.exit("region capture requires scrot or ImageMagick (import)")

    if args.active_window:
        if scrot:
            subprocess.run(["scrot", "-u", str(output)], check=True)
            return
        if gnome:
            subprocess.run(["gnome-screenshot", "-w", "-f", str(output)], check=True)
            return
        if imagemagick and xdotool:
            win_id = subprocess.check_output(["xdotool", "getactivewindow"], text=True).strip()
            subprocess.run(["import", "-window", win_id, str(output)], check=True)
            return
        sys.exit("active-window capture requires scrot, gnome-screenshot, or import+xdotool")

    # Full screen
    if scrot:
        subprocess.run(["scrot", str(output)], check=True)
        return
    if gnome:
        subprocess.run(["gnome-screenshot", "-f", str(output)], check=True)
        return
    if imagemagick:
        subprocess.run(["import", "-window", "root", str(output)], check=True)
        return
    sys.exit("no supported screenshot tool found. Install scrot, gnome-screenshot, or imagemagick.")


def capture_wayland(output: Path, args: argparse.Namespace) -> None:
    """Capture a screenshot on Wayland."""
    grim = shutil.which("grim")
    if not grim:
        sys.exit("grim is required for Wayland screenshots. Install it and retry.")

    output.parent.mkdir(parents=True, exist_ok=True)

    if args.region is not None:
        x, y, w, h = args.region
        # grim uses geometry format: x,y WxH
        subprocess.run(["grim", "-g", f"{x},{y} {w}x{h}", str(output)], check=True)
        return

    if args.active_window:
        slurp = shutil.which("slurp")
        hyprctl = shutil.which("hyprctl")
        jq = shutil.which("jq")
        if hyprctl and jq:
            # Hyprland: get active window geometry
            try:
                result = subprocess.check_output(
                    ["hyprctl", "activewindow", "-j"], text=True
                )

                win = json.loads(result)
                at = win.get("at", [0, 0])
                size = win.get("size", [0, 0])
                geometry = f"{at[0]},{at[1]} {size[0]}x{size[1]}"
                subprocess.run(["grim", "-g", geometry, str(output)], check=True)
                return
            except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
                pass
        # Fallback: interactive selection with slurp
        if slurp:
            geometry = subprocess.check_output(["slurp"], text=True).strip()
            subprocess.run(["grim", "-g", geometry, str(output)], check=True)
            return
        sys.exit(
            "active-window capture on Wayland requires hyprctl+jq or slurp. "
            "Install one of these combinations and retry."
        )

    # Full screen
    subprocess.run(["grim", str(output)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        help="output file path; overrides --mode",
    )
    parser.add_argument(
        "--mode",
        choices=("default", "temp"),
        default="default",
        help="default saves to ~/Pictures/Screenshots; temp saves to /tmp",
    )
    parser.add_argument(
        "--region",
        type=parse_region,
        help="capture region as x,y,w,h (pixel coordinates)",
    )
    parser.add_argument(
        "--active-window",
        action="store_true",
        help="capture only the focused/active window",
    )
    parser.add_argument(
        "--detect-only",
        action="store_true",
        help="print detected display server type and exit",
    )
    args = parser.parse_args()

    display_server = detect_display_server()

    if args.detect_only:
        print(f"Display server: {display_server}")
        if display_server == "x11":
            tool = find_tool(["scrot", "gnome-screenshot", "import"])
            print(f"Available tool: {tool or 'none'}")
        elif display_server == "wayland":
            tool = find_tool(["grim"])
            print(f"Available tool: {tool or 'none'}")
        else:
            print("No display server detected. Screenshots require X11 or Wayland.")
        return

    # Resolve output path
    if args.path:
        output = Path(args.path)
        if output.suffix == "":
            output = output.with_suffix(".png")
        output.parent.mkdir(parents=True, exist_ok=True)
    else:
        output = default_output_path(args.mode)

    # Dispatch to display-server-specific capture
    if display_server == "wayland":
        capture_wayland(output, args)
    elif display_server == "x11":
        capture_x11(output, args)
    else:
        sys.exit(
            "No display server detected. Set DISPLAY (X11) or WAYLAND_DISPLAY (Wayland) "
            "environment variable, or use Xvfb for headless capture."
        )

    # Verify output
    if output.exists() and output.stat().st_size > 0:
        print(str(output))
    else:
        sys.exit(f"screenshot capture failed: {output} is empty or missing")


if __name__ == "__main__":
    main()