
import sys
from pathlib import Path

# Mock the library before importing get_transcript
import types
mock_lib = types.ModuleType('youtube_transcript_api')
sys.modules['youtube_transcript_api'] = mock_lib
mock_lib.YouTubeTranscriptApi = lambda: None
mock_lib._errors = types.ModuleType('youtube_transcript_api._errors')
sys.modules['youtube_transcript_api._errors'] = mock_lib._errors

# Add mock error classes
class InvalidVideoId(Exception): pass
class VideoUnavailable(Exception): pass
class TranscriptsDisabled(Exception): pass
class NoTranscriptFound(Exception): pass
class AgeRestricted(Exception): pass
class IpBlocked(Exception): pass
class RequestBlocked(Exception): pass
class PoTokenRequired(Exception): pass
class NotTranslatable(Exception): pass

for name, cls in [
    ('InvalidVideoId', InvalidVideoId), ('VideoUnavailable', VideoUnavailable),
    ('TranscriptsDisabled', TranscriptsDisabled), ('NoTranscriptFound', NoTranscriptFound),
    ('AgeRestricted', AgeRestricted), ('IpBlocked', IpBlocked),
    ('RequestBlocked', RequestBlocked), ('PoTokenRequired', PoTokenRequired),
    ('NotTranslatable', NotTranslatable),
]:
    setattr(mock_lib._errors, name, cls)

# Now import the function
sys.path.append(str(Path('skills/productivity/youtube-transcript/scripts').absolute()))
try:
    from get_transcript import extract_video_id
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)

test_cases = [('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'), ('https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s', 'dQw4w9WgXcQ'), ('https://youtu.be/dQw4w9WgXcQ', 'dQw4w9WgXcQ'), ('https://youtu.be/dQw4w9WgXcQ?t=42', 'dQw4w9WgXcQ'), ('https://www.youtube.com/embed/dQw4w9WgXcQ', 'dQw4w9WgXcQ'), ('https://www.youtube.com/shorts/dQw4w9WgXcQ', 'dQw4w9WgXcQ'), ('https://m.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'), ('dQw4w9WgXcQ', 'dQw4w9WgXcQ')]

for url, expected in test_cases:
    try:
        actual = extract_video_id(url)
        status = "PASS" if actual == expected else f"FAIL (got {actual})"
        print(f"{url} -> {status}")
    except Exception as e:
        print(f"{url} -> FAIL (Exception: {e})")
