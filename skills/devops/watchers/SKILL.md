---
name: watchers
description: Poll RSS, JSON APIs, and GitHub with watermark dedup. Run watchers on a cron schedule or ad-hoc and react only to new items.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User wants to watch an RSS/Atom feed and be notified of new entries
  - User wants to poll a JSON endpoint or GitHub repo for new items
  - User asks for "a watcher for X" or "notify me when X changes"
  - Setting up automated monitoring with cron-driven polling
related_skills:
  - deployment-procedures
  - systematic-debugging
---

# Watchers

## Description

Poll external sources on an interval and react only to new items. Three ready-made scripts plus a shared watermark helper — wire them into a cron job or run them ad-hoc from the terminal. Each watcher script fetches data, compares against a watermark of previously-seen IDs, writes the updated watermark back, and prints only new items to stdout (silent on no-change).

## Prerequisites

- Python 3.8+ on PATH
- The watcher scripts installed at `~/.local/share/skills/devops/watchers/scripts/` (or equivalent skill install path)

Optional:
- `GITHUB_TOKEN` environment variable for GitHub API rate limits (avoids the 60 req/hr anonymous cap)

## Steps

### Step 1: Choose the Right Script

| Script | What it watches | Dedup key |
|--------|----------------|-----------|
| `watch_rss.py` | RSS 2.0 or Atom feed URL | `<guid>` / `<id>` |
| `watch_http_json.py` | Any JSON endpoint returning a list of objects | Configurable id field |
| `watch_github.py` | GitHub issues / pulls / releases / commits for a repo | `id` / `sha` |

### Step 2: Run a Watcher Ad-Hoc

```bash
# Watch an RSS feed
python3 ~/.local/share/skills/devops/watchers/scripts/watch_rss.py \
  --name hn --url https://news.ycombinator.com/rss --max 5

# Watch a GitHub repo (set GITHUB_TOKEN for higher rate limits)
python3 ~/.local/share/skills/devops/watchers/scripts/watch_github.py \
  --name hermes-issues --repo NousResearch/hermes-agent --scope issues

# Poll an arbitrary JSON API
python3 ~/.local/share/skills/devops/watchers/scripts/watch_http_json.py \
  --name api --url https://api.example.com/events \
  --id-field event_id --items-path data.events
```

### Step 3: Wire into Cron

Create a cron job that runs the watcher on schedule. If it prints nothing (no new items), stay silent. If it prints new items, process or forward them.

```bash
# Example cron entry: check Hacker News every 15 minutes
*/15 * * * * python3 ~/.local/share/skills/devops/watchers/scripts/watch_rss.py --name hn --url https://news.ycombinator.com/rss
```

### Step 4: Inspect or Reset State Files

```bash
# View current watermark state
cat ~/.local/share/skills/devops/watchers/state/hn.json

# Force a replay (next run treated as first poll)
rm ~/.local/share/skills/devops/watchers/state/hn.json
```

### Step 5: Write a Custom Watcher

Use the shared `_watermark.py` helper for atomic writes, bounded ID sets, and first-run baseline:

```python
# Import the watermark helper from the scripts directory
import sys
sys.path.insert(0, os.path.expanduser("~/.local/share/skills/devops/watchers/scripts"))
from _watermark import Watermark
```

Pattern: load watermark → fetch → diff → save → emit. See any of the three reference scripts for minimal boilerplate.

## Pitfalls

1. **Printing "no new items" on every tick.** Callers rely on empty stdout meaning silence. If you print anything on an empty delta, you spam the channel. Custom watchers must respect this convention.
2. **Expecting the first run to emit items.** The first run records a baseline — it never replays existing items. If you need an initial digest, delete the state file after the first run or add a `--prime-with-latest N` flag.
3. **Unbounded watermark growth.** The shared helper caps at 500 IDs by default. Raise it for high-churn feeds; lower it on constrained filesystems. An unbounded watermark will eventually consume disk.
4. **Putting state files where the agent sandbox cannot write.** Always use the standard state directory (`~/.local/share/skills/devops/watchers/state/`). Paths outside the user's home or skill directory may not be writable in containerized or sandboxed environments.

## Verification

1. **Run a watcher for the first time and confirm silence (baseline recorded):**
   ```bash
   python3 ~/.local/share/skills/devops/watchers/scripts/watch_rss.py \
     --name test-verify --url https://news.ycombinator.com/rss
   # Should produce no output (baseline poll)
   ```
2. **Delete the state file and re-run — should emit items:**
   ```bash
   rm ~/.local/share/skills/devops/watchers/state/test-verify.json
   python3 ~/.local/share/skills/devops/watchers/scripts/watch_rss.py \
     --name test-verify --url https://news.ycombinator.com/rss --max 5
   # Should print new items in "## <title>\n<url>" format
   ```
3. **Confirm state file was created:**
   ```bash
   ls ~/.local/share/skills/devops/watchers/state/test-verify.json
   ```