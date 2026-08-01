
import sys
import os
from pathlib import Path

# Add the script directory to sys.path
sys.path.append(str(Path('skills/productivity/youtube-transcript/scripts').absolute()))

try:
    from get_transcript import extract_video_id, InvalidVideoId
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
