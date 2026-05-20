---
name: meme-generation
description: Generate real meme images by picking a template and overlaying text with Pillow — produces actual .png meme files, no external API required
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to make or generate a meme
  - User wants a meme about a specific topic, situation, or frustration
  - User says "meme this" or similar
  - User asks for a humorous image with text overlay
  - User wants to combine an image with caption text
related_skills:
  - stable-diffusion-image-generation
  - searxng-search
---

# Meme Generation

## Description

Generate actual meme images from a topic. Picks a template, writes captions, and renders a real .png file with text overlay using Pillow. Supports 10 curated templates with hand-tuned text positioning and ~100 popular imgflip templates accessible by name or ID. Pure Pillow — no external dependencies or API keys required beyond template image downloads.

## Prerequisites

- Python 3.8+
- Pillow (`pip install Pillow`)
- Internet access for downloading template images on first use (cached locally afterward)

## Steps

### 1. List available templates

```bash
python3 SKILL_DIR/scripts/generate_meme.py --list
```

Shows all curated and dynamic templates with their IDs and field names.

### 2. Generate a meme with a curated template

Pick from 10 hand-tuned templates:

| Template ID | Name | Fields | Best For |
|-------------|------|--------|----------|
| `this-is-fine` | This is Fine | top, bottom | Chaos, denial |
| `drake` | Drake Hotline Bling | reject, approve | Rejecting/preferring |
| `distracted-boyfriend` | Distracted Boyfriend | distraction, current, person | Temptation, shifting priorities |
| `two-buttons` | Two Buttons | left, right, person | Impossible choices |
| `expanding-brain` | Expanding Brain | 4 levels | Escalating irony |
| `change-my-mind` | Change My Mind | statement | Hot takes |
| `woman-yelling-at-cat` | Woman Yelling at Cat | woman, cat | Arguments |
| `one-does-not-simply` | One Does Not Simply | top, bottom | Deceptively hard things |
| `grus-plan` | Gru's Plan | step1-3, realization | Plans that backfire |
| `batman-slapping-robin` | Batman Slapping Robin | robin, batman | Shutting down bad ideas |

```bash
python3 SKILL_DIR/scripts/generate_meme.py drake /tmp/meme.png \
    "Getting 8 hours of sleep" "One more episode at 3 AM"
```

```bash
python3 SKILL_DIR/scripts/generate_meme.py expanding-brain /tmp/meme.png \
    "Setting an alarm" "Setting 5 alarms" "Sleeping through all alarms" "Working from bed"
```

```bash
python3 SKILL_DIR/scripts/generate_meme.py this-is-fine /tmp/meme.png \
    "SERVERS ARE ON FIRE" "This is fine"
```

### 3. Search for a dynamic template

```bash
python3 SKILL_DIR/scripts/generate_meme.py --search "disaster"
```

Returns matching imgflip template names and IDs. Use the name or ID with the generator:

```bash
python3 SKILL_DIR/scripts/generate_meme.py "Disaster Girl" /tmp/meme.png \
    "Top text" "Bottom text"
```

### 4. Custom image with text overlay (overlay mode)

Add text directly on top of any image:

```bash
python3 SKILL_DIR/scripts/generate_meme.py --image /path/to/scene.png /tmp/meme.png \
    "Top text" "Bottom text"
```

White text with black outline for readability on any background.

### 5. Custom image with text bars (bars mode)

Add black bars above and below the image with white text — cleaner and always readable:

```bash
python3 SKILL_DIR/scripts/generate_meme.py --image /path/to/scene.png --bars /tmp/meme.png \
    "Top text" "Bottom text"
```

Use `--bars` when the image is busy/detailed and overlay text would be hard to read.

### 6. Deliver the result

Return the image to the user:

```
MEDIA:/tmp/meme.png
```

## Pitfalls

1. **Keep captions SHORT** — Memes with long text look terrible. Aim for 8-12 words max per field. Shorter is always better.
2. **Match field count to template** — The number of text arguments must match the template's field count. `expanding-brain` takes 4 fields, `drake` takes 2. Check with `--list` if unsure.
3. **Pick the template that fits the joke structure** — Don't pick a template just because it's popular. Pick the one whose structure matches the joke. `drake` is for preference/rejection, `expanding-brain` is for escalation, `this-is-fine` is for denial.
4. **Template images cache on first use** — The script downloads template images to `SKILL_DIR/scripts/.cache/` on first use. Subsequent runs use the cached copy. Ensure network access on first run.
5. **Dynamic templates have default positioning** — Templates not in the curated list get smart default positioning (top/bottom for 2-field, evenly spaced for 3+). Results may need adjustment for complex layouts.

## Verification

1. **Script runs and produces output**: Run `python3 SKILL_DIR/scripts/generate_meme.py drake /tmp/test_meme.png "Option A" "Option B"` and confirm it creates a valid PNG at `/tmp/test_meme.png`.
2. **Text is legible**: Open the generated PNG and confirm text is white with black outline, clearly readable against the template image.
3. **Template list works**: Run `python3 SKILL_DIR/scripts/generate_meme.py --list` and confirm it prints the 10 curated templates with their IDs and field descriptions.