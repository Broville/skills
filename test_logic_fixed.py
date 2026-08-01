
import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

# Setup imports
sys.path.append(str(Path('skills/productivity/youtube-transcript/scripts').absolute()))

# Mock the library entirely
import types
mock_lib = types.ModuleType('youtube_transcript_api')
sys.modules['youtube_transcript_api'] = mock_lib

# Mock the main class
mock_api = MagicMock()
mock_lib.YouTubeTranscriptApi = mock_api

# Mock the errors module
mock_errors = types.ModuleType('youtube_transcript_api._errors')
sys.modules['youtube_transcript_api._errors'] = mock_errors

class InvalidVideoId(Exception): pass
class VideoUnavailable(Exception): pass
class TranscriptsDisabled(Exception): pass
class NoTranscriptFound(Exception): pass
class AgeRestricted(Exception): pass
class IpBlocked(Exception): pass
class RequestBlocked(Exception): pass
class PoTokenRequired(Exception): pass
class NotTranslatable(Exception): pass

error_map = [
    ('InvalidVideoId', InvalidVideoId), ('VideoUnavailable', VideoUnavailable),
    ('TranscriptsDisabled', TranscriptsDisabled), ('NoTranscriptFound', NoTranscriptFound),
    ('AgeRestricted', AgeRestricted), ('IpBlocked', IpBlocked),
    ('RequestBlocked', RequestBlocked), ('PoTokenRequired', PoTokenRequired),
    ('NotTranslatable', NotTranslatable),
]

for name, cls in error_map:
    setattr(mock_errors, name, cls)

# Now we can import from the script
try:
    from get_transcript import (
        build_envelope, 
        format_timestamp, 
        handle_exception, 
        extract_video_id
    )
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)

# Mock Data
mock_segments = [
    {"start": 1.36, "duration": 1.68, "text": "[♪♪♪]"},
    {"start": 18.64, "duration": 3.24, "text": "♪ We're no strangers to love ♪"},
    {"start": 22.0, "duration": 3.5, "text": "♪ You know the rules and so do I ♪"},
]
mock_metadata = {
    "language": "English",
    "language_code": "en",
    "is_generated": False,
}
mock_available = ["en", "de-DE"]

def test_output_formats():
    print("Testing output formats...")
    # Test JSON envelope
    envelope = build_envelope("dQw4w9WgXcQ", mock_segments, mock_metadata, mock_available)
    assert envelope['video_id'] == "dQw4w9WgXcQ"
    assert "We're no strangers to love" in envelope['transcript_plain']
    assert len(envelope['transcript']) == 3
    print("  JSON envelope: PASS")

    # Test timestamp formatting
    assert format_timestamp(1.36) == "00:01"
    assert format_timestamp(18.64) == "00:18"
    assert format_timestamp(61.0) == "01:01"
    print("  Timestamp formatting: PASS")

def test_error_mapping():
    print("Testing error mapping...")
    from io import StringIO
    
    cases = [
        (InvalidVideoId, "ERROR: INVALID_VIDEO_ID"),
        (VideoUnavailable, "ERROR: VIDEO_UNAVAILABLE"),
        (TranscriptsDisabled, "ERROR: TRANSCRIPTS_DISABLED"),
        (NoTranscriptFound, "ERROR: NO_TRANSCRIPT_FOUND"),
        (AgeRestricted, "ERROR: AGE_RESTRICTED"),
        (IpBlocked, "ERROR: RATE_LIMITED"),
        (RequestBlocked, "ERROR: RATE_LIMITED"),
        (PoTokenRequired, "ERROR: PO_TOKEN_REQUIRED"),
        (NotTranslatable, "ERROR: NOT_TRANSLATABLE"),
    ]

    for exc_cls, expected_prefix in cases:
        with patch('sys.stderr', new=StringIO()) as fake_out:
            try:
                handle_exception(exc_cls())
            except SystemExit:
                pass
            output = fake_out.getvalue()
            assert expected_prefix in output
            print(f"  {exc_cls.__name__} -> {expected_prefix}: PASS")

test_output_formats()
test_error_mapping()
print("ALL TESTS PASSED")
