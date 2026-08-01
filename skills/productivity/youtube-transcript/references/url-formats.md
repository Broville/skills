# YouTube URL Formats — Parser Contract

The script accepts any of the following 8 forms. The extraction strategy is
in priority order: `urllib.parse.urlparse` with domain check, then
format-specific regex, then raw-ID regex. The raw-ID regex allows 10 OR 11
characters because some legacy IDs are shorter than the modern 11.

| # | Format | Example | Regex / extraction |
|---|--------|---------|---------------------|
| 1 | Standard watch | `https://www.youtube.com/watch?v=dQw4w9WgXcQ` | `urlparse(url).query` → `parse_qs` → `v` |
| 2 | Watch with extra params | `https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s&list=PLabc` | same as #1, ignore other params |
| 3 | Short URL | `https://youtu.be/dQw4w9WgXcQ` | first path segment (after stripping leading `/`) |
| 4 | Short URL with params | `https://youtu.be/dQw4w9WgXcQ?t=42` | first path segment, ignore query |
| 5 | Embed | `https://www.youtube.com/embed/dQw4w9WgXcQ` | `^https?://(?:www\.)?youtube\.com/embed/([A-Za-z0-9_-]{10,11})` |
| 6 | Shorts | `https://www.youtube.com/shorts/dQw4w9WgXcQ` | `^https?://(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]{10,11})` |
| 7 | Mobile | `https://m.youtube.com/watch?v=dQw4w9WgXcQ` | same parsing as #1; host is `m.youtube.com` not `www.youtube.com` |
| 8 | Raw video ID | `dQw4w9WgXcQ` (10 or 11 chars, `[A-Za-z0-9_-]`) | `^[A-Za-z0-9_-]{10,11}$` |

## Combined regex (used as the fallback after URL parsing)

```python
import re

URL_PATTERNS = [
    # youtube.com/watch?v=ID  (any subdomain, with or without www)
    r"(?:^|[^A-Za-z0-9_-])youtube\.com/watch\?.*?v=([A-Za-z0-9_-]{10,11})(?:[&#]|$)",
    # youtu.be/ID
    r"(?:^|[^A-Za-z0-9_-])youtu\.be/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # youtube.com/embed/ID
    r"youtube\.com/embed/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # youtube.com/v/ID  (legacy)
    r"youtube\.com/v/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # youtube.com/shorts/ID
    r"youtube\.com/shorts/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # raw ID
    r"^([A-Za-z0-9_-]{10,11})$",
]
```

## Why 10 or 11 characters?

Modern YouTube video IDs are 11 characters (`[A-Za-z0-9_-]{11}`). Some
legacy IDs in videos uploaded before ~2014 are 10 characters; the
intelligence brief and the kimtaeyoon83 reference implementation both
allow 10 as a defensive measure. There is no observable risk to allowing
10 — if a string matches the regex but is not a real video, the
library's `VideoUnavailable` exception is raised and the script surfaces
`ERROR: VIDEO_UNAVAILABLE`.

## Why not just one regex?

URL parsing is more reliable than regex for `watch?v=...` URLs because
the `v` parameter is a real query string and there are many other
parameters (`t`, `list`, `index`, etc.) that we should not mistake for
the video ID. The hybrid approach — `urlparse` first, regex fallback
for embed/Shorts, raw-ID match for direct input — is the same approach
the kimtaeyoon83 reference uses.
