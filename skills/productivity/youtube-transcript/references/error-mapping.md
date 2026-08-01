# Error Mapping — `youtube-transcript-api` Exceptions to User Messages

Every exception the library can raise is mapped below to a stable
`ERROR: <CODE>:` stderr prefix, an exit code, and a suggested
user-facing message the agent can show verbatim. The script is the
source of truth; this file is the documentation the agent reads.

|| Library exception | stderr prefix | exit code | Suggested user-facing message |
|-------------------|---------------|-----------|------------------------------|
|| `InvalidVideoId` | `ERROR: INVALID_VIDEO_ID` | 1 | "That doesn't look like a valid YouTube video ID or URL. Double-check the link." |
|| `VideoUnavailable` | `ERROR: VIDEO_UNAVAILABLE` | 1 | "This video is private, deleted, or region-locked. I can't fetch its transcript." |
|| `TranscriptsDisabled` | `ERROR: TRANSCRIPTS_DISABLED` | 1 | "The creator has disabled captions on this video, so there's no transcript to fetch." |
|| `NoTranscriptFound` | `ERROR: NO_TRANSCRIPT_FOUND` | 1 | "No captions available in the requested language(s). Try --list to see what's offered." |
|| `AgeRestricted` | `ERROR: AGE_RESTRICTED` | 1 | "This video is age-restricted. The library can't authenticate to bypass that right now (YouTube cookie auth is broken upstream)." |
|| `IpBlocked` | `ERROR: RATE_LIMITED` | 1 | "YouTube is rate-limiting from this network. Wait a few minutes, or try from a different network." |
|| `RequestBlocked` | `ERROR: RATE_LIMITED` | 1 | "YouTube is blocking requests from this network. Wait a few minutes, or try a different network." |
|| `PoTokenRequired` | `ERROR: PO_TOKEN_REQUIRED` | 1 | "YouTube is asking for a verification token. Retry in a few hours; there's nothing we can do client-side." |
|| `NotTranslatable` | `ERROR: NOT_TRANSLATABLE` | 1 | "The selected transcript is auto-generated and can't be translated. Try fetching the source language instead." |
|| any other exception | `ERROR: UNKNOWN: <class name>` | 1 | "Transcript fetch failed with an unexpected error: `<class name>`. Try again, or open an issue if it persists." |

## Notes for the agent

- **Always show the stderr line to the user** when exit code is non-zero.
  The `ERROR: <CODE>:` prefix is a stable contract; downstream automation
  (alerting, logging) can match on it.
- **Do not retry automatically on `RATE_LIMITED`.** Retries make the
  block last longer. Surface the error and let the user decide.
- **Do not retry on `PO_TOKEN_REQUIRED`.** The verification challenge
  is YouTube-side; retrying just wastes the user's time.
- **Do retry on `NO_TRANSCRIPT_FOUND`** with a different language —
  that's the documented language-fallback path, not an error to
  surface.
- **`VIDEO_UNAVAILABLE` is final** for that video; do not retry.
- The `<CODE>` is always uppercase with underscores (machine-readable).
  The human message after it is a regular English sentence. They are
  separated by `: ` (colon + space) so a parser can split on the first
  colon if needed.

## Format

Every error line on stderr has the shape:

```
ERROR: <CODE>: <human-readable message>
```

Plus a blank line for readability, plus the original library
exception's message on a third line (when available). Exit code is
1 for all errors above; exit code 2 is reserved for usage errors
(unknown flag, missing positional argument, `--format` value not
in `{json, text, both}`).
