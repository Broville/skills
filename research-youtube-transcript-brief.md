# Intelligence Brief: YouTube Transcript Skill Requirements

**Date**: 2026-07-31  
**Researcher**: Compass  
**Task**: t_a61f4316  

---

## Summary

Three reference sources were analyzed for a model-agnostic YouTube Transcript skill, plus the underlying `youtube-transcript-api` Python library (v1.2.4). The skill should extract video transcripts, generate structured summaries, and answer questions about YouTube URLs. The recommended implementation uses the `youtube-transcript-api` Python library (MIT license, v1.2.4) as the extraction engine, with a companion Python script invoked via `uv run`. The MCP server approach from kimtaeyoon83 is valuable for reference but adds unnecessary runtime complexity for a Hermes skill. The intellectronica skill provides a clean minimal template. Video ID extraction must handle 6+ URL formats. Rate-limiting and IP blocking are the primary operational risks.

---

## Evidence

| Claim | Source | Confidence |
|-------|--------|------------|
| `youtube-transcript-api` v1.2.4 is MIT-licensed, supports Python 3.8–3.14, no headless browser needed | PyPI, github.com/jdepoix/youtube-transcript-api | **Certain** |
| Library provides `YouTubeTranscriptApi().fetch(video_id)` and `.list(video_id)` APIs with language priority, translation, and auto-generated caption fallback | github.com/jdepoix/youtube-transcript-api source (README + `_api.py`) | **Certain** |
| Library raises specific exceptions: `VideoUnavailable`, `NoTranscriptFound`, `TranscriptsDisabled`, `AgeRestricted`, `RequestBlocked`, `IpBlocked`, `InvalidVideoId`, `NotTranslatable`, `PoTokenRequired` | github.com/jdepoix/youtube-transcript-api `_errors.py` | **Certain** |
| IP blocking (HTTP 429 → `IpBlocked`) occurs under high request volume; library supports `ProxyConfig` for rotating proxies | github.com/jdepoix/youtube-transcript-api `_errors.py`, `_api.py` | **Certain** |
| Cookie auth is currently disabled ("temporarily unsupported") due to YouTube API changes; `AgeRestricted` videos cannot be fetched without auth | github.com/jdepoix/youtube-transcript-api `_errors.py` L93-99 | **Certain** |
| intellectronica/agent-skills skill uses `uv run --script` with inline dependency declaration, regex-based URL parsing, simple `FetchedTranscript` consumption | github.com/intellectronica/agent-skills `skills/youtube-transcript/SKILL.md` + `scripts/get_transcript.py` | **Certain** |
| kimtaeyoon83/mcp-server-youtube-transcript (579 stars) is a TypeScript MCP server that calls YouTube's internal API directly via protobuf-encoded params, bypasses poToken enforcement using ANDROID client, strips ad chapters, and extracts video metadata | github.com/kimtaeyoon83 source (`index.ts`, `youtube-fetcher.ts`) | **Certain** |
| The MCP server handles URL formats: standard watch URLs, shortened youtu.be, Shorts `/shorts/{id}`, embed URLs, and raw video IDs (10-11 char regex: `^-?[a-zA-Z0-9_-]{10,11}$`) | github.com/kimtaeyoon83 `index.ts` `extractYoutubeId()` | **Certain** |
| ericgandrade/claude-superskills has 18 skills (none are YouTube-related); it is a meta/orchestration skill pack, not relevant to YouTube transcript extraction | github.com/ericgandrade/claude-superskills | **Likely** |

---

## Detailed Analysis

### 1. Library Evaluation: `youtube-transcript-api`

**Recommendation: Use this library.** It is the de facto standard for Python-based YouTube transcript extraction.

**Strengths:**
- Pure Python, no headless browser or Selenium required
- Active maintenance (v1.2.4, Jan 2026), MIT license
- Supports language priority lists (`languages=['de', 'en']`), auto-generated caption fallback, translation
- Returns structured `FetchedTranscript` objects with `FetchedTranscriptSnippet(text, start, duration)` per segment
- `FetchedTranscript` is iterable, indexable, has `len()`, and `.to_raw_data()` for dict output
- `list(video_id)` API exposes all available transcripts with metadata (language, is_generated, is_translatable)
- Proxy support via `ProxyConfig` for IP-block circumvention
- CLI interface available: `python -m youtube_transcript_api <video_id>`

**Weaknesses:**
- Cookie authentication is currently broken (disabled in code), so age-restricted videos cannot be fetched
- YouTube can return `PoTokenRequired` errors requiring bot-verification tokens
- `RequestBlocked` / `IpBlocked` exceptions indicate rate limiting or cloud IP detection
- The `FetchedTranscriptSnippet.duration` field measures on-screen duration, not speech duration — segments can overlap
- The library is NOT thread-safe (creates `requests.Session` per instance; one instance per thread)

**Key API surface for the skill:**

```python
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()

# Simple fetch
transcript = api.fetch(video_id, languages=['en'])

# List available transcripts first
transcript_list = api.list(video_id)
for t in transcript_list:
    print(t.language_code, t.is_generated, t.is_translatable)

# Find specific transcript type
transcript = transcript_list.find_transcript(['en'])
# or find_manually_created_transcript / find_generated_transcript

# Translate
translated = transcript.translate('de').fetch()
```

### 2. Video ID Extraction

**URL formats that MUST be handled:**

| Format | Example | Extraction Method |
|--------|---------|-------------------|
| Standard watch | `https://www.youtube.com/watch?v=VIDEO_ID` | `URL.searchParams.get('v')` or regex |
| Shortened | `https://youtu.be/VIDEO_ID` | `URL.pathname.slice(1)` or regex |
| Embed | `https://www.youtube.com/embed/VIDEO_ID` | regex or URL parsing |
| Shorts | `https://www.youtube.com/shorts/VIDEO_ID` | `URL.pathname.split('/shorts/')[1]` or regex |
| Mobile | `https://m.youtube.com/watch?v=VIDEO_ID` | same as standard |
| Raw ID | `VIDEO_ID` (11 chars, `[a-zA-Z0-9_-]`) | regex: `^[a-zA-Z0-9_-]{11}$` |
| With params | `https://youtube.com/watch?v=VIDEO_ID&t=123s` | strip params, extract `v` |

**The intellectronica skill uses this regex:**
```python
patterns = [
    r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
    r'^([a-zA-Z0-9_-]{11})$'
]
```

**The MCP server uses `new URL()` parsing** with explicit Shorts handling and a more permissive raw-ID regex (`^-?[a-zA-Z0-9_-]{10,11}$`). The MCP approach is more robust because:
- It handles edge cases in URL parsing (e.g., `youtu.be` without regex brittleness)
- It validates the domain (`youtube.com` or `youtu.be`)
- It handles Shorts explicitly
- The 10-11 char regex allows for short video IDs (some legacy IDs may be shorter than 11 chars)

**Recommended approach:** Combine both — use `URL` parsing first, fall back to regex, then validate with `[a-zA-Z0-9_-]{10,11}`.

### 3. Security Considerations and Rate-Limiting Pitfalls

**Security:**
- The `youtube-transcript-api` library makes HTTP requests to YouTube's internal `youtubei/v1/get_transcript` endpoint. No API key is needed.
- The MCP server approach (TypeScript) constructs raw protobuf-encoded params and uses ANDROID client impersonation to bypass poToken enforcement. This is more fragile and may break with YouTube API changes.
- No user authentication is involved — transcript fetching is anonymous.
- Video IDs should be validated before use to prevent injection into URL construction (standard regex validation suffices).

**Rate-limiting and blocking:**
- YouTube enforces rate limits at the IP level. The library raises `IpBlocked` (HTTP 429) when blocked.
- Cloud provider IPs (AWS, GCP, Azure) are frequently pre-blocked.
- The library supports `ProxyConfig` with retry logic: `retries_when_blocked` parameter on `GenericProxyConfig`.
- **For a skill running on a home server or local machine:** Occasional use (1-5 videos/day) is fine. Bulk processing (10+ videos in rapid succession) risks IP blocking.
- **Mitigation strategy:** Add a configurable delay between requests (2-5 seconds) and catch `IpBlocked` / `RequestBlocked` with actionable error messages.
- The MCP server uses a 30-second request timeout, which is a reasonable default.

**Privacy:**
- The library sends the video ID and language preference to YouTube. No personal data is transmitted beyond what YouTube already collects.
- Transcript text is subject to the video creator's copyright. The skill should include a disclaimer about fair use.

### 4. Structured Output Format Proposal

Based on analysis of all three sources, here is a proposed structured output format:

```yaml
# Transcript extraction output
video_id: "dQw4w9WgXcQ"
url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
title: "Rick Astley - Never Gonna Give You Up"  # from MCP server metadata
author: "Rick Astley"                             # from MCP server metadata
language: "en"
language_code: "en"
is_generated: false
available_languages: ["en", "de", "fr"]            # from .list()
transcript: |
   [0:00] We're no strangers to love
   [0:04] You know the rules and so do I
   ...
transcript_plain: |
   We're no strangers to love You know the rules and so do I ...
summary: |                                          # LLM-generated
   The video is the official music video for "Never Gonna Give You Up" by Rick Astley...
```

**Key design decisions:**
1. **Two transcript formats:** Timestamped (`[MM:SS] text`) and plain (continuous text). The intellectronica skill provides both via `--timestamps` flag. Both should be available.
2. **Metadata enrichment:** The MCP server fetches title, author, subscriber count, view count, and publish date. The Python library does NOT provide this metadata — it only returns transcript data. If metadata is desired, a secondary YouTube Data API call or page scrape would be needed.
3. **Language fallback:** Both the Python library and the MCP server implement language fallback (try requested → English → first available). This should be a feature.
4. **Summary generation:** This is an LLM concern, not a transcript extraction concern. The skill should focus on providing clean transcript data; summarization can be delegated to the agent.

---

## Gaps

- **No video metadata from Python library:** The `youtube-transcript-api` only returns transcript snippets. Video title, author, view count, etc. are not included. The skill would need a separate mechanism (YouTube Data API v3 with an API key, or scraping) for metadata. The MCP server handles this by scraping the watch page HTML.
- **No chapter/ad-stripping in Python library:** The MCP server extracts chapter markers and strips ad segments. The Python library does not provide this. This is a nice-to-have, not a must.
- **Cookie auth currently broken:** Age-restricted videos cannot be fetched until the library re-enables cookie authentication.
- **PoToken enforcement:** YouTube is A/B testing a `poToken` requirement. The Python library will raise `PoTokenRequired` when this happens. The MCP server works around this by impersonating the ANDROID client, but this is fragile.
- **Thread safety:** `YouTubeTranscriptApi()` instances are NOT thread-safe (internal `requests.Session`). For concurrent use, create one instance per thread.

---

## Recommendations for Implementation

1. **Use `youtube-transcript-api` (Python, v1.2.4)** as the extraction engine. It's the most mature, actively maintained, and Python-native solution.
2. **Implement as a Hermes skill** with a `scripts/get_transcript.py` using `uv run --script` inline dependency declaration (matching the intellectronica pattern). This avoids requiring a pre-installed environment.
3. **Video ID extraction** should handle all 6+ URL formats using a combination of URL parsing and regex validation, with Shorts support.
4. **Output two formats:** timestamped (`[MM:SS] text`) and plain text, controlled by a `--timestamps` flag.
5. **Language fallback:** Default to `['en']`, with automatic fallback to first available language if English is not available.
6. **Rate-limiting mitigation:** Add a note in the Pitfalls section about IP blocking risks. The skill should not add artificial delays (those belong at the orchestration level), but should catch and surface `RequestBlocked` / `IpBlocked` exceptions with actionable error messages.
7. **Metadata:** Do NOT add YouTube Data API v3 dependency for metadata — it requires an API key. Instead, surface only what the transcript library provides (language, is_generated, snippet text/timing). If metadata is needed, that's a separate skill.
8. **Error handling:** Surface all library exceptions as actionable error messages. The key exceptions to handle:
   - `VideoUnavailable` — video doesn't exist or is private
   - `NoTranscriptFound` — no captions in requested language
   - `TranscriptsDisabled` — creator disabled captions
   - `IpBlocked` / `RequestBlocked` — rate limited; suggest waiting or using proxy
   - `AgeRestricted` — cookie auth currently broken; inform user
   - `PoTokenRequired` — YouTube A/B test; suggest retry later
9. **Category:** `productivity` (transcript extraction is a productivity/research tool)
10. **Related skills:** `systematic-debugging` (for error triage), `mcp-builder` (if someone wants to build an MCP server wrapper later)

---

## Source Code References

### intellectronica/agent-skills — SKILL.md (full)
```
name: youtube-transcript
description: Extract transcripts from YouTube videos. Use when the user asks for a transcript, subtitles, or captions of a YouTube video and provides a YouTube URL (youtube.com/watch?v=, youtu.be/, or similar). Supports output with or without timestamps.
```
- Uses `uv run --script` with `youtube-transcript-api>=1.0.0` as inline dependency
- Script at `scripts/get_transcript.py` (71 lines)
- Supports `--timestamps` flag
- URL formats: watch, youtu.be, embed, /v/, raw ID
- CRITICAL rule: "NEVER MODIFY THE RETURNED TRANSCRIPT" — agent should only clean up paragraph formatting, not alter content

### kimtaeyoon83/mcp-server-youtube-transcript — Key features
- TypeScript MCP server (579 stars, MIT license)
- Two tools: `get_transcript` and `analyze_video` (TwelveLabs Pegasus)
- ANDROID client impersonation to bypass poToken
- Video metadata extraction via HTML scraping
- Ad chapter stripping based on chapter markers
- Language fallback with `enableFallback` flag
- Structured output with `meta` (title | author | subs | views | date) and `content` fields
- 30-second request timeout

### ericgandrade/claude-superskills
- 18 skills total, none YouTube-related
- Not relevant to this skill's implementation
- Focus is on meta/orchestration, planning, research, and content