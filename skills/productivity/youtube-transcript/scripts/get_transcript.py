#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "youtube-transcript-api==1.2.4",
# ]
# ///

"""Fetch a YouTube transcript and print a JSON envelope or plain text.

This script is intentionally a self-contained CLI tool. Agents invoke it with:

    uv run --script scripts/get_transcript.py <url-or-video-id> [options]

It is model-agnostic and returns structured transcript data on stdout. All
library exceptions are mapped to one-line stderr messages of the form:

    ERROR: <CODE>: <human-readable message>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    AgeRestricted,
    InvalidVideoId,
    IpBlocked,
    NoTranscriptFound,
    NotTranslatable,
    PoTokenRequired,
    RequestBlocked,
    TranscriptsDisabled,
    VideoUnavailable,
)

# Regexes used as a fallback / sanity check for URL forms. The parser
# prefers urllib.parse for watch/mobile URLs and falls back to these for
# embed/shorts/legacy/short/raw forms. Keep in sync with
# references/url-formats.md.
URL_PATTERNS = [
    # youtube.com/watch?v=ID (with or without www, any params around it)
    r"(?:^|[^A-Za-z0-9_-])youtube\.com/watch\?.*?v=([A-Za-z0-9_-]{10,11})(?:[&#]|$)",
    # youtu.be/ID
    r"(?:^|[^A-Za-z0-9_-])youtu\.be/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # youtube.com/embed/ID
    r"youtube\.com/embed/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # youtube.com/v/ID (legacy)
    r"youtube\.com/v/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # youtube.com/shorts/ID
    r"youtube\.com/shorts/([A-Za-z0-9_-]{10,11})(?:[?&#]|$)",
    # bare video ID
    r"^([A-Za-z0-9_-]{10,11})$",
]

YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def extract_video_id(raw: str) -> str:
    """Return the 10-11 character video ID from a URL or raw ID string."""
    raw = raw.strip()
    if not raw:
        raise InvalidVideoId("Input is empty")

    # Plain video ID (no scheme, no slash)
    if re.match(r"^[A-Za-z0-9_-]{10,11}$", raw):
        return raw

    parsed = urlparse(raw)

    # www.youtube.com / m.youtube.com / youtube.com / youtu.be
    netloc = parsed.netloc.lower().lstrip("www.")
    if parsed.scheme not in {"http", "https", ""}:
        raise InvalidVideoId(f"Unsupported URL scheme: {parsed.scheme}")

    if netloc in {"youtube.com", "m.youtube.com"} or parsed.netloc == "youtu.be":
        if parsed.path.lower().startswith("/watch"):
            query = parse_qs(parsed.query)
            video_ids = query.get("v", [])
            if video_ids:
                candidate = video_ids[0]
                if re.match(r"^[A-Za-z0-9_-]{10,11}$", candidate):
                    return candidate
                raise InvalidVideoId(f"Invalid video ID in query parameter: {candidate}")
        elif parsed.path.lower().startswith("/shorts/"):
            candidate = parsed.path.split("/")[2].split("?")[0]
            if re.match(r"^[A-Za-z0-9_-]{10,11}$", candidate):
                return candidate
        elif parsed.path.lower().startswith("/embed/"):
            candidate = parsed.path.split("/")[2].split("?")[0]
            if re.match(r"^[A-Za-z0-9_-]{10,11}$", candidate):
                return candidate
        elif parsed.path.lower().startswith("/v/"):
            candidate = parsed.path.split("/")[2].split("?")[0]
            if re.match(r"^[A-Za-z0-9_-]{10,11}$", candidate):
                return candidate
        elif parsed.netloc == "youtu.be":
            candidate = parsed.path.lstrip("/").split("?")[0]
            if re.match(r"^[A-Za-z0-9_-]{10,11}$", candidate):
                return candidate

    # Fallback: try the combined regex list (covers pasted text that might
    # contain other surrounding characters).
    for pattern in URL_PATTERNS:
        match = re.search(pattern, raw)
        if match:
            return match.group(1)

    raise InvalidVideoId(f"Could not extract a valid YouTube video ID from: {raw}")


def build_canonical_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    mins, secs = divmod(total, 60)
    return f"{mins:02d}:{secs:02d}"


def list_transcripts(video_id: str) -> list[dict]:
    """Return available transcripts as a list of serializable dicts."""
    api = YouTubeTranscriptApi()
    transcripts = api.list(video_id)
    result = []
    for transcript in transcripts:
        result.append(
            {
                "language_code": transcript.language_code,
                "language": transcript.language,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable,
            }
        )
    return result


def fetch_transcript(video_id: str, languages: list[str]) -> tuple[list[dict], dict]:
    """Fetch transcript and return (segments, metadata dict)."""
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=languages)

    segments = [
        {
            "start": snippet.start,
            "duration": snippet.duration,
            "text": snippet.text,
        }
        for snippet in transcript
    ]

    metadata = {
        "language": transcript.language,
        "language_code": transcript.language_code,
        "is_generated": transcript.is_generated,
    }
    return segments, metadata


def build_envelope(
    video_id: str,
    segments: list[dict],
    metadata: dict,
    available_languages: list[str],
) -> dict:
    plain = " ".join(seg["text"] for seg in segments)
    return {
        "video_id": video_id,
        "url": build_canonical_url(video_id),
        "language": metadata.get("language", ""),
        "language_code": metadata.get("language_code", ""),
        "is_generated": metadata.get("is_generated", False),
        "available_languages": available_languages,
        "transcript": segments,
        "transcript_plain": plain,
    }


def print_error(code: str, message: str, exit_code: int = 1) -> None:
    sys.stderr.write(f"ERROR: {code}: {message}\n")
    sys.exit(exit_code)


def handle_exception(exc: Exception) -> None:
    if isinstance(exc, InvalidVideoId):
        print_error(
            "INVALID_VIDEO_ID",
            "That doesn't look like a valid YouTube video ID or URL. Double-check the link.",
        )
    if isinstance(exc, VideoUnavailable):
        print_error(
            "VIDEO_UNAVAILABLE",
            "This video is private, deleted, or region-locked. I can't fetch its transcript.",
        )
    if isinstance(exc, TranscriptsDisabled):
        print_error(
            "TRANSCRIPTS_DISABLED",
            "The creator has disabled captions on this video, so there's no transcript to fetch.",
        )
    if isinstance(exc, NoTranscriptFound):
        print_error(
            "NO_TRANSCRIPT_FOUND",
            "No captions available in the requested language(s). Try --list to see what's offered.",
        )
    if isinstance(exc, AgeRestricted):
        print_error(
            "AGE_RESTRICTED",
            "This video is age-restricted. The library can't authenticate to bypass that right now (YouTube cookie auth is broken upstream).",
        )
    if isinstance(exc, (IpBlocked, RequestBlocked)):
        print_error(
            "RATE_LIMITED",
            "YouTube is rate-limiting from this network. Wait a few minutes, or try from a different network.",
        )
    if isinstance(exc, PoTokenRequired):
        print_error(
            "PO_TOKEN_REQUIRED",
            "YouTube is asking for a verification token. Retry in a few hours; there's nothing we can do client-side.",
        )
    if isinstance(exc, NotTranslatable):
        print_error(
            "NOT_TRANSLATABLE",
            "The selected transcript is auto-generated and can't be translated. Try fetching the source language instead.",
        )

    print_error(
        f"UNKNOWN: {exc.__class__.__name__}",
        f"Transcript fetch failed with an unexpected error: {exc.__class__.__name__}. Try again, or open an issue if it persists.",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript as JSON or plain text.",
    )
    parser.add_argument(
        "url_or_video_id",
        help="YouTube URL (watch, youtu.be, embed, Shorts, mobile) or raw 10-11 char video ID",
    )
    parser.add_argument(
        "--languages",
        default="en",
        help="Comma-separated, priority-ordered ISO 639-1 language codes (default: en)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text", "both"],
        default="both",
        help="Output format: json, text, or both (default: both)",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="In text mode, prefix each line with [MM:SS]",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available transcripts and exit (no content returned)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    languages = [lang.strip() for lang in args.languages.split(",") if lang.strip()]

    try:
        video_id = extract_video_id(args.url_or_video_id)
    except InvalidVideoId as exc:
        print_error(
            "INVALID_VIDEO_ID",
            "That doesn't look like a valid YouTube video ID or URL. Double-check the link.",
        )
        return 1

    try:
        if args.list:
            available = list_transcripts(video_id)
            print(json.dumps(available, indent=2))
            return 0

        segments, metadata = fetch_transcript(video_id, languages)
        available = [t["language_code"] for t in list_transcripts(video_id)]

        if args.format == "json":
            envelope = build_envelope(video_id, segments, metadata, available)
            print(json.dumps(envelope, indent=2))
        elif args.format == "both":
            envelope = build_envelope(video_id, segments, metadata, available)
            print(json.dumps(envelope, indent=2))
        elif args.format == "text":
            if args.timestamps:
                for seg in segments:
                    print(f"[{format_timestamp(seg['start'])}] {seg['text']}")
            else:
                print(" ".join(seg["text"] for seg in segments))

        return 0
    except Exception as exc:
        handle_exception(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
