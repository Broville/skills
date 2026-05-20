---
name: watchers
description: Poll RSS, JSON APIs, and GitHub with watermark dedup. Run watchers on a cron schedule or ad-hoc and react only to new items.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux, macos]
trigger:
  - User wants to watch an RSS/Atom feed and be notified of new entries
  - User wants to poll a JSON endpoint or GitHub repo for new items
  - User asks for "a watcher for X" or "notify me when X changes"
  - Setting up automated monitoring with cron-driven polling
metadata:
  hermes:
    tags: [rss, watcher, monitoring, cron, polling, dedup, github]
    related_skills: [cloudflare-deploy]
---

# Watchers

## Description

Poll external sources on an interval and react only to new items. Three ready-made scripts plus a shared watermark helper — wire them into a cron job or run them ad-hoc from the terminal. Each watcher script fetches data, compares against a watermark of previously-seen IDs, writes the updated watermark back, and prints only new items to stdout (silent on no-change).

## Prerequisites

- Python 3.8+ on PATH
- The watcher scripts installed at `~/.local/share/skills/devops/watchers/scripts/` (or equivalent skill install path)

Optional:
- `GITHUB_TOKEN` environment variable for GitHub API rate limits

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

# Watch a GitHub repo
python3 ~/.local/share/skills/devops/watchers/scripts/watch_github.py \
  --name hermes-issues --repo NousResearch/hermes-agent --scope issues

# Poll an arbitrary JSON API
python3 ~/.local/share/skills/devops/watchers/scripts/watch_http_json.py \
  --name api --url https://api.example.com/events \
  --id-field event_id --items-path data.events
```

### Step 3: Wire into Cron

Create a Hermes cron job that runs the watcher on schedule. If it prints nothing (no new items), stay silent.

### Step 4: Inspect or Reset State Files

```bash
# View current watermark state
cat ~/.local/share/skills/devops/watchers/state/hn.json

# Force a replay (next run treated as first poll)
rm ~/.local/share/skills/devops/watchers/state/hn.json
```

## Pitfalls

1. **Printing "no new items" on every tick.** Callers rely on empty stdout meaning silence. Custom watchers must respect this convention.
2. **Expecting the first run to emit items.** The first run records a baseline — it never replays existing items.
3. **Unbounded watermark growth.** The shared helper caps at 500 IDs by default.
4. **Putting state files where the agent sandbox cannot write.** Always use the standard state directory.

## Verification

1. Run a watcher for the first time and confirm silence (baseline recorded)
2. Delete the state file and re-run — should emit items
3. Confirm state file was created