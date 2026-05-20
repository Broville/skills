---
name: screenshot
description: Capture desktop screenshots on Linux (X11 and Wayland) for visual verification, debugging, and documentation.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to take a screenshot or capture the screen
  - User asks to verify what is displayed on screen
  - Visual verification of a GUI application is needed
  - User asks to document or record the current desktop state
inputs:
  - name: path
    description: Output file path for the screenshot (defaults to auto-generated in ~/Pictures/Screenshots or /tmp)
    required: false
  - name: region
    description: Crop region as x,y,width,height in pixels
    required: false
  - name: active_window
    description: Capture only the currently focused window
    required: false
outputs:
  - name: screenshot_path
    description: Absolute path to the saved screenshot file
metadata:
  hermes:
    tags:
      - screenshot
      - capture
      - desktop
      - x11
      - wayland
      - visual-verification
    related_skills:
      - pdf
---

# Screenshot Capture

Capture desktop screenshots on Linux systems. Automatically detects whether the session runs on X11 or Wayland and selects the appropriate tool.

## When to Use

- User explicitly asks for a screenshot
- Visual verification of a running application is needed
- Debugging UI layout or rendering issues
- Documenting the current desktop state

## Prerequisites

### X11 sessions

Install at least one of:

```bash
# scrot (recommended — lightweight, supports regions and active window)
sudo apt-get install -y scrot        # Debian/Ubuntu
sudo dnf install -y scrot             # Fedora
sudo pacman -S scrot                  # Arch Linux

# gnome-screenshot (fallback — GNOME desktops)
sudo apt-get install -y gnome-screenshot   # Debian/Ubuntu
sudo dnf install -y gnome-screenshot       # Fedora

# ImageMagick import (fallback — most versatile)
sudo apt-get install -y imagemagick    # Debian/Ubuntu
sudo dnf install -y ImageMagick       # Fedora
sudo pacman -S imagemagick            # Arch Linux
```

### Wayland sessions

```bash
# grim (standard Wayland screenshot tool)
sudo apt-get install -y grim           # Debian/Ubuntu
sudo dnf install -y grim               # Fedora
sudo pacman -S grim                    # Arch Linux

# For active window capture on Wayland, also install slurp and jq:
sudo apt-get install -y slurp jq       # Debian/Ubuntu
sudo dnf install -y slurp jq          # Fedora
sudo pacman -S slurp jq               # Arch Linux
```

## Steps

### 1. Detect the display server

Use the helper script to auto-detect and capture:

```bash
python3 scripts/take_screenshot.py
```

Or check manually:

```bash
echo $XDG_SESSION_TYPE
# "x11"  → use X11 tools (scrot, gnome-screenshot, import)
# "wayland" → use grim

# Alternative check:
loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type
```

### 2. Take a full-screen screenshot

**Using the helper script (recommended):**

```bash
# Default location (~/Pictures/Screenshots/ or /tmp)
python3 scripts/take_screenshot.py

# Explicit output path
python3 scripts/take_screenshot.py --path output/screen.png

# Temp location (for agent inspection, not user-facing)
python3 scripts/take_screenshot.py --mode temp
```

**Direct X11 commands:**

```bash
# scrot (preferred)
scrot output/screen.png

# gnome-screenshot (fallback)
gnome-screenshot -f output/screen.png

# ImageMagick import (fallback)
import -window root output/screen.png
```

**Direct Wayland commands:**

```bash
grim output/screen.png
```

### 3. Capture a specific region

```bash
# Using the helper
python3 scripts/take_screenshot.py --region 100,200,800,600

# scrot (X11)
scrot -a 100,200,800,600 output/region.png

# ImageMagick import (X11)
import -window root -crop 800x600+100+200 output/region.png

# grim + slurp (Wayland — interactive region selection)
grim -g "$(slurp)" output/region.png
```

### 4. Capture the active window

```bash
# Using the helper
python3 scripts/take_screenshot.py --active-window

# scrot (X11)
scrot -u output/window.png

# gnome-screenshot (X11)
gnome-screenshot -w -f output/window.png

# grim + hyprctl (Wayland — Hyprland)
grim -g "$(hyprctl activewindow -j | jq -r '.at[0]+\",\"+.at[1]+\" \"+.size[0]+\"x\"+.size[1]')" output/window.png
```

### 5. Verify the screenshot was taken

```bash
test -f "output/screen.png" && echo "Screenshot saved" || echo "Screenshot failed"
file output/screen.png
# Expected: "output/screen.png: PNG image data, ..."
```

## Save Location Rules

1. If the user specifies a path → save there
2. If the user asks for a screenshot without a path → save to `~/Pictures/Screenshots/`
3. If the agent needs a screenshot for its own inspection → save to `/tmp/`

## Pitfalls

- **No display server (headless environment)**: Screenshot tools require a running display server. In SSH sessions, containers, or CI environments without a display, screenshots will fail. Use Xvfb as a virtual display if needed:
  ```bash
  Xvfb :99 -screen 0 1920x1080x24 &
  export DISPLAY=:99
  ```
- **Wayland compatibility**: Many X11 screenshot tools (`scrot`, `import`) do not work on Wayland. Always check `$XDG_SESSION_TYPE` before selecting a tool. The helper script handles this automatically.
- **Permission denied on save**: Ensure the output directory exists and is writable. The helper script creates parent directories automatically.
- **grim not found on Wayland**: Install `grim` (and `slurp` for interactive regions). Without grim, Wayland screenshots are not possible from the CLI.
- **scrot region format**: `scrot -a` takes `x,y,width,height` — not `x,y,x2,y2`. Confusing coordinates is the most common mistake.
- **Blank screenshots**: A compositor may block screen capture for security. Check that the screenshot is not a blank/zero-byte file after capture.
- **Multiple monitors**: On X11, `scrot` captures the entire virtual desktop spanning all monitors. On Wayland, `grim` captures all outputs by default. Use region capture to isolate a single display.
- **Timing issues**: If capturing an app that animates or loads, add a brief delay:
  ```bash
  sleep 2 && scrot output/screen.png
  ```

## Verification

1. Confirm the file exists and is a valid image:
   ```bash
   file output/screen.png
   # Expected: "PNG image data, ..."
   ```
2. Confirm the file is non-empty (not a blank screenshot):
   ```bash
   python3 -c "from PIL import Image; img=Image.open('output/screen.png'); print(f'Size: {img.size}, Mode: {img.mode}')"
   ```
3. Confirm display server detection works:
   ```bash
   python3 scripts/take_screenshot.py --detect-only
   # Expected: "Display server: X11" or "Display server: Wayland"
   ```

## Cross-References

- **pdf** (`productivity/pdf`) — For incorporating screenshots into PDF documents