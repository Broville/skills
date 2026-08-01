# Blueprint: YouTube Transcript Skill (`youtube-transcript`)

**Design task**: t_bdadfe40
**Designer**: Cartographer
**Upstream evidence**: `research-youtube-transcript-brief.md` (Compass, 2026-07-31)
**Target deliverable**: `skills/productivity/youtube-transcript/SKILL.md` + `scripts/get_transcript.py`

---

## Overview

A model- and provider-agnostic Hermes skill that extracts the spoken transcript
from a YouTube video given a URL or raw 11-character video ID. The skill is a
thin agent-facing wrapper around the `youtube-transcript-api` Python library
(v1.2.4, MIT), which calls YouTube's internal caption endpoint directly — no
API key, no headless browser, no MCP server runtime. Output is returned as
both a timestamped transcript and a plain text transcript so that downstream
agents can either quote segments with timestamps or feed the cleaned text into
a summarization/QA prompt.

The skill is intentionally **a transcript fetcher, not a summarizer or
chat-with-video tool**. Summarization and question-answering are LLM
responsibilities that the host agent performs after the skill delivers
structured transcript data. Keeping the skill narrow keeps it portable
across model providers and easy to verify.

---

## Architecture

### Components

- **`SKILL.md`** — the agent-facing documentation. Defines triggers, inputs,
  steps, output schema, pitfalls, and verification. Pulled into agent
  context the same way any other skill is pulled.
- **`scripts/get_transcript.py`** — executable Python script. Self-contained:
  declares its own dependency (`youtube-transcript-api==1.2.4`) inline at the
  top via PEP 723 so `uv run --script` installs on demand without polluting
  the host's global Python. The agent shells out to this script rather than
  importing the library directly; this matches the established
  `intellectronica/agent-skills` pattern and avoids requiring the agent's
  Python environment to be pre-configured.
- **`references/url-formats.md`** — canonical list of the seven YouTube URL
  formats the parser handles, with one regex + one example per format.
  Referenced by `SKILL.md` so agents (and reviewers) can verify coverage.
- **`references/error-mapping.md`** — mapping from
  `youtube-transcript-api` exceptions to actionable error messages an agent
  should surface to the user. Keeps the `SKILL.md` body from becoming a wall
  of exception names.

### Data flow

```
agent receives user message with YouTube URL
  ↓
agent loads youtube-transcript skill (matches trigger)
  ↓
agent reads SKILL.md → sees "run scripts/get_transcript.py URL"
  ↓
agent executes:  uv run --script scripts/get_transcript.py <URL> [flags]
  ↓
script (1) normalizes URL → video_id
       (2) calls YouTubeTranscriptApi().fetch(video_id, languages=[...])
       (3) catches library exceptions, maps to one-line stderr message
       (4) prints JSON envelope to stdout, exits 0
  ↓
agent parses JSON envelope
  ↓
agent uses `transcript` (timestamped) and `transcript_plain` fields
       — either quotes a segment to the user, or feeds `transcript_plain`
         into a follow-up prompt for summarization / Q&A
```

### Dependencies

| Layer | Dependency | Why |
|-------|-----------|-----|
| Runtime | `uv` (Astral) | Runs the script with on-the-fly dependency resolution via PEP 723. Already standard tooling for the agent fleet. |
| Runtime | Python 3.10+ | `youtube-transcript-api` v1.2.4 supports 3.8–3.14; 3.10 keeps us comfortably inside the supported range without forcing a downgrade. |
| Library | `youtube-transcript-api == 1.2.4` | MIT-licensed, no API key, no browser. Pinned exact version per task requirement. |
| Network | Outbound HTTPS to `youtube.com` and `youtubei.googleapis.com` | The library calls YouTube's internal `get_transcript` endpoint. No keys, no auth, but rate-limited per IP. |

### Tech stack

- **Language**: Python 3.10+ (script)
- **Script invocation**: `uv run --script` with PEP 723 inline metadata
- **Output format**: JSON envelope on stdout (machine-readable), human error
  on stderr (so the agent can show the user what went wrong)
- **No external services, no API keys, no headless browser, no MCP server**

---

## Interface Definitions

### Script CLI

```
uv run scripts/get_transcript.py <url-or-video-id>
                                  [--languages en,de]
                                  [--format json|text|both]   # default: both
                                  [--list]                    # list available transcripts and exit
```

| Flag | Default | Meaning |
|------|---------|---------|
| `<url-or-video-id>` (positional, required) | — | Any of the 7 supported URL forms, or a bare 10–11 char video ID |
| `--languages` | `en` | Comma-separated, priority-ordered list of ISO 639-1 language codes. The library tries them in order; if none are available it falls back to the first transcript the video exposes. |
| `--format` | `both` | `json` → structured JSON envelope; `text` → plain text only (timestamped or plain depending on `--timestamps`); `both` → JSON envelope containing both formats. |
| `--timestamps` | off | When set, `text` mode emits `[MM:SS] text` lines; default is plain (no timestamps). Ignored when `--format json` or `--format both` because both forms are included in the envelope anyway. |
| `--list` | off | List available transcripts (language, is_generated, is_translatable) and exit 0. Does not return transcript content. |

### Output envelope (JSON, exit 0)

```json
{
  "video_id": "dQw4w9WgXcQ",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "language": "en",
  "language_code": "en",
  "is_generated": false,
  "available_languages": ["en", "de", "fr"],
  "transcript": [
    {"start": 0.0,  "duration": 4.0, "text": "We're no strangers to love"},
    {"start": 4.0,  "duration": 3.5, "text": "You know the rules and so do I"}
  ],
  "transcript_plain": "We're no strangers to love You know the rules and so do I ..."
}
```

The agent can pick `transcript_plain` for LLM input, or iterate over the
timestamped `transcript` array to quote a specific moment.

### Error output (stderr, exit non-zero)

Errors are written as a single line on stderr in the form
`ERROR: <CODE>: <human-readable message>`, plus exit code 1 (or 2 for
usage errors). The agent should surface the message verbatim to the user.

| Library exception | Exit code | stderr prefix | Suggested user message |
|-------------------|-----------|---------------|------------------------|
| `InvalidVideoId` | 1 | `ERROR: INVALID_VIDEO_ID` | "That doesn't look like a valid YouTube video ID or URL. Double-check the link." |
| `VideoUnavailable` | 1 | `ERROR: VIDEO_UNAVAILABLE` | "This video is private, deleted, or region-locked. I can't fetch its transcript." |
| `TranscriptsDisabled` | 1 | `ERROR: TRANSCRIPTS_DISABLED` | "The creator has disabled captions on this video, so there's no transcript to fetch." |
| `NoTranscriptFound` | 1 | `ERROR: NO_TRANSCRIPT_FOUND` | "No captions available in the requested language(s). Try `--list` to see what's offered." |
| `AgeRestricted` | 1 | `ERROR: AGE_RESTRICTED` | "This video is age-restricted. The library can't authenticate to bypass that right now (YouTube cookie auth is broken upstream)." |
| `IpBlocked` / `RequestBlocked` | 1 | `ERROR: RATE_LIMITED` | "YouTube is rate-limiting from this network. Wait a few minutes or try a different network." |
| `PoTokenRequired` | 1 | `ERROR: PO_TOKEN_REQUIRED` | "YouTube is asking for a verification token. Retry in a few hours; nothing we can do client-side." |
| `NotTranslatable` | 1 | `ERROR: NOT_TRANSLATABLE` | "The selected transcript is auto-generated and can't be translated." |
| any other exception | 1 | `ERROR: UNKNOWN: <class name>` | Fallback; agent should report the class name and the original message. |

---

## URL-Format Coverage

The script must accept all of the following. The full regex is in
`references/url-formats.md`; this is the contract.

| # | Format | Example | Extraction |
|---|--------|---------|------------|
| 1 | Standard watch | `https://www.youtube.com/watch?v=VIDEO_ID` | query param `v` |
| 2 | Standard watch with extra params | `https://www.youtube.com/watch?v=VIDEO_ID&t=42s` | query param `v` (ignore `t`) |
| 3 | Short URL | `https://youtu.be/VIDEO_ID` | first path segment |
| 4 | Short URL with params | `https://youtu.be/VIDEO_ID?t=42` | first path segment (ignore query) |
| 5 | Embed | `https://www.youtube.com/embed/VIDEO_ID` | last path segment |
| 6 | Shorts | `https://www.youtube.com/shorts/VIDEO_ID` | segment after `/shorts/` |
| 7 | Mobile | `https://m.youtube.com/watch?v=VIDEO_ID` | query param `v` (same as #1) |
| 8 | Raw ID | `dQw4w9WgXcQ` (10 or 11 chars, `[A-Za-z0-9_-]{10,11}`) | direct |

Implementation strategy: try `urllib.parse.urlparse` + domain check first
(handles #1, #2, #3, #4, #7 cleanly); fall back to regex for embed/Shorts
(#5, #6) where path-based routing is more reliable; finally accept a raw ID
matching the permissive 10–11 char regex (#8). The validation regex allows
10 chars because some legacy IDs are shorter than 11; the research brief
notes this is intentional.

---

## Task Breakdown

This is a single, focused skill, so the breakdown is one design task
(this document) plus three implementation tasks for the human
implementer. The implementer is expected to work sequentially because
the script is the load-bearing artifact and the references can only be
written after the script's behavior is finalized.

| # | Task | Assignee | Depends on | Acceptance criteria |
|---|------|----------|------------|---------------------|
| 1 | Write `scripts/get_transcript.py` with PEP 723 metadata pinning `youtube-transcript-api==1.2.4`, URL normalization for 8 formats, language fallback (`['en']` default, then first available), JSON envelope output, stderr error mapping per the table above. | implementer | — | See task spec below |
| 2 | Write `references/url-formats.md` (one table row per format with regex + example) and `references/error-mapping.md` (the exception → user-message table from above). | implementer | #1 | Both files exist, both referenced from `SKILL.md`, both free of secrets/absolute paths. |
| 3 | Write `SKILL.md` per `SKILL-SPEC.md`: frontmatter (name `youtube-transcript`, description ≤120 chars, version 1.0.0, license MIT, trigger list, related_skills pointing to skills that actually exist), Description, Prerequisites, Steps (numbered, with exact `uv run` commands), Pitfalls, Verification, Cross-References. | implementer | #1, #2 | `SKILL.md` passes the `SOP.md` Validation Checklist. |

---

## Task Specification (per task)

### Task 1: `scripts/get_transcript.py`

#### Objective

A self-contained Python script that takes a YouTube URL or video ID and
prints a JSON envelope with the video's transcript to stdout. Uses
`uv run --script` for zero-install execution. Surfaces library
exceptions as one-line actionable stderr messages.

#### Files to create

- `skills/productivity/youtube-transcript/scripts/get_transcript.py`

#### Acceptance criteria

- [ ] The first two lines are the PEP 723 metadata block pinning
      `youtube-transcript-api==1.2.4` (exact version, per task requirement).
- [ ] `uv run scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"`
      exits 0, prints a JSON envelope on stdout, prints nothing on stderr,
      and the envelope contains `video_id == "dQw4w9WgXcQ"`,
      a non-empty `transcript` array, and a non-empty `transcript_plain`
      string.
- [ ] The same command with
      `"https://youtu.be/dQw4w9WgXcQ"`, an embed URL, a Shorts URL, a
      `m.youtube.com` URL, a watch URL with `&t=` params, and the bare
      `dQw4w9WgXcQ` all exit 0 and produce an envelope with
      `video_id == "dQw4w9WgXcQ"`.
- [ ] An invalid input like `"not a url"` exits 1 with
      `ERROR: INVALID_VIDEO_ID:` on stderr and no stdout.
- [ ] `uv run scripts/get_transcript.py dQw4w9WgXcQ --list` exits 0 and
      prints a JSON list of available transcripts (each with
      `language_code`, `is_generated`, `is_translatable`) to stdout.
- [ ] `uv run scripts/get_transcript.py dQw4w9WgXcQ --format text --timestamps`
      exits 0 and prints lines of the form `[MM:SS] text` to stdout.
- [ ] `uv run scripts/get_transcript.py dQw4w9WgXcQ --languages de,en`
      exits 0 and returns the German transcript if available, otherwise
      English.
- [ ] The library exceptions listed in the error-mapping table each
      produce the documented `ERROR: <CODE>:` prefix on stderr and
      the corresponding non-zero exit code. (Manually verified against
      a private video for `VideoUnavailable`; others can be verified
      by mocking in a unit test if no real-world trigger is available.)
- [ ] The script does NOT modify or paraphrase any transcript text —
      it returns exactly what the library returns. (The
      `intellectronica` skill's hard rule.)
- [ ] No hardcoded API keys, no absolute paths, no `os.chdir` calls,
      no global state mutation.

#### Deliverable location

`/home/echo/repos/skills/skills/productivity/youtube-transcript/scripts/get_transcript.py`

#### Expected effort

~45 min for an implementer who has the library's exception list in front of
them; the URL parser is the only non-trivial piece.

---

### Task 2: `references/url-formats.md` + `references/error-mapping.md`

#### Objective

Two short reference files that `SKILL.md` can link to instead of inlining
long tables. Keeps the skill body scannable while preserving the precise
spec.

#### Files to create

- `skills/productivity/youtube-transcript/references/url-formats.md`
- `skills/productivity/youtube-transcript/references/error-mapping.md`

#### Acceptance criteria (url-formats.md)

- [ ] One row per URL format (8 rows: standard, watch+params, short,
      short+params, embed, Shorts, mobile, raw ID).
- [ ] Each row has: format name, example URL, regex pattern, parsing
      note.
- [ ] The combined regex list is the same one used in
      `scripts/get_transcript.py` (copy-paste match).

#### Acceptance criteria (error-mapping.md)

- [ ] One row per documented exception (`VideoUnavailable`,
      `NoTranscriptFound`, `TranscriptsDisabled`, `AgeRestricted`,
      `IpBlocked`, `RequestBlocked`, `PoTokenRequired`, `InvalidVideoId`,
      `NotTranslatable`).
- [ ] Each row has: exception class, stderr prefix, exit code,
      suggested user-facing message.

#### Deliverable location

`/home/echo/repos/skills/skills/productivity/youtube-transcript/references/`

#### Expected effort

~15 min.

---

### Task 3: `SKILL.md`

#### Objective

The agent-facing entry point. Follows the `SKILL-SPEC.md` format and the
`SOP.md` Validation Checklist exactly.

#### Files to create

- `skills/productivity/youtube-transcript/SKILL.md`

#### Acceptance criteria

**Frontmatter**

- [ ] `name: youtube-transcript` (matches directory name, kebab-case)
- [ ] `description:` is a single line, ≤120 chars, names the trigger
      ("extract the transcript of a YouTube video given a URL or video ID")
- [ ] `version: 1.0.0`
- [ ] `author: Broville`
- [ ] `license: MIT`
- [ ] `platforms: [linux, macos]` (Windows unverified — library works but
      `uv run --script` ergonomics differ; mark linux+macos safe)
- [ ] `trigger:` lists at least three concrete conditions
      (e.g., "user shares a `youtube.com` URL and asks for a transcript /
      summary", "user shares a `youtu.be` short URL", "user pastes an
      11-char video ID")
- [ ] `inputs:` array with `name=url_or_video_id` (required) plus the
      optional `languages` and `format` controls
- [ ] `outputs:` array documenting the JSON envelope
- [ ] `related_skills:` points only at skills that exist in this repo.
      Confirmed candidates at design time: `mcp-builder` (relevant if
      someone later wraps this in MCP), `systematic-debugging` (for
      error triage on blocked fetches), `rest-graphql-debug` (debugging
      HTTP-level failures — possibly relevant for IP-block diagnosis),
      `pdf` (if the transcript is later turned into a study document).
      Each must be verified to exist in the repo before publishing.

**Body**

- [ ] `# Youtube Transcript` H1 title
- [ ] `## Description` (2–3 sentences)
- [ ] `## Prerequisites` — `uv` on PATH, Python 3.10+, outbound HTTPS
      to `youtube.com`. No API key.
- [ ] `## Steps` — numbered, each step a single `uv run` command with
      expected output, plus one step showing `--list`, one showing
      `--format text --timestamps`, and one showing `--languages`.
- [ ] `## Pitfalls` — at minimum: rate limiting / IP block on bulk
      fetches, `AgeRestricted` videos un-fetchable until upstream
      cookie auth is fixed, `PoTokenRequired` is a YouTube A/B test
      with no client-side workaround, `FetchedTranscriptSnippet.duration`
      is on-screen duration (segments may overlap — do not assume
      strict contiguous timing), script is not thread-safe (one process
      per concurrent fetch).
- [ ] `## Verification` — at least one concrete check: run the script
      against a known-public video, confirm exit 0 and non-empty
      `transcript_plain`.
- [ ] `## Cross-References` — links to `references/url-formats.md`
      and `references/error-mapping.md`, plus the `related_skills`
      frontmatter entries.
- [ ] No hardcoded secrets, no absolute local paths, no fabricated
      commands.

**Category**

- [ ] Lives at `skills/productivity/youtube-transcript/` per the task
      requirement that this is a productivity tool.

#### Deliverable location

`/home/echo/repos/skills/skills/productivity/youtube-transcript/SKILL.md`

#### Expected effort

~30 min after Tasks 1 and 2 land.

---

## Constraints, Risks, and Assumptions (Lens must inspect)

### Constraints

- **Exact library version pin**: `youtube-transcript-api==1.2.4` is
  required by the task body. The script must declare this in PEP 723
  metadata; Lens should reject any `>=` or unbounded range.
- **Model/provider agnostic**: no prompt templates, no model-specific
  tokens, no tool-calling scaffolding that assumes a particular agent
  runtime. The script is a plain CLI; the agent invokes it the same
  way regardless of the underlying LLM.
- **Six+ URL formats**: task says "6+", design covers 8. Lens should
  confirm all 8 are reachable and tested, not just the minimum 6.
- **Structured output**: both timestamped and plain forms are
  produced in the JSON envelope; both are independently consumable.

### Risks

- **YouTube rate limiting**: `IpBlocked` is the dominant operational
  failure mode. Mitigated by surfacing a clear error message, not by
  any client-side retry (retries belong at the orchestration layer and
  would just make a block last longer). Lens should verify the error
  message names the *cause* (IP rate limit) and the *next action*
  (wait, or use a different network), not just "transcript fetch
  failed".
- **`youtube-transcript-api` upstream churn**: the library is the
  single point of failure. If the library breaks against YouTube's
  internal API (e.g., a new poToken rollout), the skill breaks with
  no fallback. Acceptable for v1.0.0; v1.1.0 should consider
  surfacing a `--help-me-find-an-alternative` flag.
- **Cookie auth is broken upstream**: `AgeRestricted` videos
  cannot currently be fetched. The skill surfaces this honestly
  rather than pretending. Lens should not accept any "fix" that
  papers over it.
- **`PoTokenRequired` is opaque**: when YouTube A/B-tests a
  verification requirement, there is no client-side workaround.
  The skill's only correct behavior is to surface the error.
  Lens should flag any attempt to "retry forever" or
  "auto-solve challenge" as a non-starter.

### Assumptions

- **`uv` is on PATH on every agent host.** This holds for the Broville
  fleet per the established pattern (intellectronica, scrapling,
  pinggy-tunnel skills all rely on it). Lens should confirm
  `uv --version` works on a fresh host as a sanity check.
- **Outbound HTTPS to YouTube is not blocked.** Cloud VMs (AWS/GCP/Azure)
  are frequently pre-blocked; this is the same constraint as
  `research-youtube-transcript-brief.md` notes. The skill does not
  attempt proxy configuration in v1.0.0 — proxy support is
  documented as a v1.1.0 follow-on.
- **The transcript text is treated as user-provided content.** The
  skill is a content fetcher; the host agent is responsible for
  fair-use disclaimers and copyright handling. The skill itself
  does not add a "this text is copyrighted" notice, because
  transcript text is no different from the video itself in that
  regard and adding such a notice in the tool output would be
  performative.
- **English (`en`) is the default fallback language.** The brief
  recommends this. The fallback chain is
  `requested → en → first available` — same as the intellectronica
  reference implementation.
- **The skill's deliverable is a transcript, not a summary.** Per
  the brief's recommendation #7: keep summarization at the LLM layer.

---

## Verification (Blueprint-Level)

Once all three tasks land, the following blueprint-level checks must pass
before this design is considered implemented:

1. **Pull test**: An agent (any model) loads the skill via standard
   pull procedure, reads `SKILL.md`, runs the script against a
   known-public video, and gets a non-empty `transcript_plain`.
2. **URL coverage test**: All 8 URL formats in `references/url-formats.md`
   resolve to the same `video_id` when fed to the script. Confirmed
   by Lens running each form as a separate test case.
3. **Error mapping test**: Lens mocks each library exception
   (or finds a real video that triggers it) and confirms the
   documented `ERROR: <CODE>:` prefix and non-zero exit code
   appear on stderr.
4. **Validation checklist**: `SOP.md` § Validation Checklist passes
   for the new skill. No item skipped, no item hand-waved.

---

## Out of Scope (Explicitly)

The following are intentionally NOT in v1.0.0 and should be tracked as
follow-on issues, not scope-creep into this design:

- Video metadata (title, author, view count) — would require YouTube
  Data API v3 (key-gated) or HTML scraping. Out of scope per brief
  recommendation #7.
- Auto-generated chapter markers / ad stripping — only the MCP server
  does this and it's fragile. Out of scope.
- Concurrent / threaded fetching — `YouTubeTranscriptApi()` instances
  are not thread-safe; document the limitation, do not engineer around
  it.
- Proxy rotation — `youtube-transcript-api` supports `ProxyConfig`,
  but wiring it requires a proxy source. Out of scope for v1.0.0.
- Summarization, Q&A, "chat with this video" — LLM concerns, not
  transcript concerns.
- MCP server wrapping — see the related `mcp-builder` skill if
  someone wants to expose this over MCP later.
