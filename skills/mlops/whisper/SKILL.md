---
name: whisper
description: Local speech-to-text transcription using Whisper models — supports 99 languages, translation to English, CLI and Python API, GPU acceleration, and faster-whisper alternative
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to transcribe audio, recordings, podcasts, or meetings to text
  - User wants speech-to-text conversion for any language
  - User asks to translate audio content to English
  - User needs subtitles or captions generated from video/audio
  - User asks about local ASR or voice recognition tools
related_skills:
  - chroma
  - searxng-search
---

# Whisper — Robust Speech Recognition (Local Inference)

## Description

Whisper is an open-source speech recognition model that runs entirely locally. It supports 99 languages for transcription and translation to English, with six model sizes from tiny (39M params) to large (1550M params). This skill covers both the original `openai-whisper` package and the faster `faster-whisper` alternative that provides 4× speed improvement using CTranslate2.

All inference runs on your hardware — no cloud API, no data leaves your machine.

## Prerequisites

- Python 3.8-3.11
- `ffmpeg` installed (`sudo apt install ffmpeg` on Ubuntu)
- GPU recommended but not required (10-20× faster on CUDA)
- Install one of:
  - Standard: `pip install -U openai-whisper`
  - Faster alternative: `pip install faster-whisper` (recommended for speed)

## Steps

### 1. Basic transcription (openai-whisper)

```bash
# Install
pip install -U openai-whisper

# CLI — simplest usage
whisper audio.mp3

# Specify model and output format
whisper audio.mp3 --model turbo --output_format srt
```

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
print(result["text"])

# Access segments with timestamps
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

### 2. Select model size

| Model | Parameters | Multilingual | Speed (relative) | VRAM | Best For |
|-------|-----------|--------------|-------------------|------|----------|
| tiny | 39M | ✓ | ~32× | ~1 GB | Quick prototyping |
| base | 74M | ✓ | ~16× | ~1 GB | Good balance for speed |
| small | 244M | ✓ | ~6× | ~2 GB | Enhanced accuracy |
| medium | 769M | ✓ | ~2× | ~5 GB | High accuracy needs |
| large | 1550M | ✓ | 1× | ~10 GB | Best accuracy |
| turbo | 809M | ✓ | ~8× | ~6 GB | Best speed/quality |

```python
model = whisper.load_model("turbo")  # Recommended for most use cases
```

### 3. Transcription options

```python
# Auto-detect language
result = model.transcribe("audio.mp3")

# Specify language (faster)
result = model.transcribe("audio.mp3", language="en")

# Translate to English
result = model.transcribe("spanish.mp3", task="translate")

# Improve accuracy with context prompt
result = model.transcribe(
    "audio.mp3",
    initial_prompt="This is a technical podcast about machine learning."
)

# Word-level timestamps
result = model.transcribe("audio.mp3", word_timestamps=True)
```

### 4. Batch processing

```python
import os

audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]
for audio_file in audio_files:
    result = model.transcribe(audio_file)
    output_file = audio_file.replace(".mp3", ".txt")
    with open(output_file, "w") as f:
        f.write(result["text"])
```

### 5. Faster transcription with faster-whisper (recommended alternative)

```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

# CPU mode
model = WhisperModel("base", device="cpu", compute_type="int8")

# GPU mode (4× faster than openai-whisper)
model = WhisperModel("base", device="cuda", compute_type="float16")

# Transcribe with streaming
segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

**When to use faster-whisper**: Always, unless you need the exact original API. It's 4× faster with comparable quality, uses less memory, and supports streaming output.

### 6. GPU acceleration

```python
# Auto-detect (uses GPU if available)
model = whisper.load_model("turbo")

# Force CPU
model = whisper.load_model("turbo", device="cpu")

# Force CUDA GPU
model = whisper.load_model("turbo", device="cuda")
```

### 7. Extract audio from video

```bash
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav
whisper audio.wav
```

### 8. CLI output formats

```bash
whisper audio.mp3 --output_format txt     # Plain text
whisper audio.mp3 --output_format srt     # SubRip subtitles
whisper audio.mp3 --output_format vtt     # WebVTT
whisper audio.mp3 --output_format json    # JSON with timestamps
```

## Pitfalls

1. **Python version constraint** — `openai-whisper` requires Python 3.8-3.11. Python 3.12+ is not supported. Check with `python3 --version` before installing.
2. **Hallucinations on silence** — Whisper may invent text when given long silence. Split audio into <30-minute chunks and filter out segments with very low confidence.
3. **Long-form audio degradation** — Accuracy degrades on audio longer than 30 minutes. Split long files into segments using `ffmpeg` before transcribing.
4. **No speaker diarization** — Whisper identifies WHAT was said, not WHO said it. For speaker identification, pair with a diarization tool like `pyannote.audio`.
5. **faster-whisper compute_type differs** — Use `int8` for CPU, `float16` for GPU. Using the wrong type causes cryptic errors or poor quality.

## Verification

1. **CLI works**: Run `whisper --help` and confirm it prints usage information. Then transcribe a short audio file and confirm it produces readable text output.
2. **Python module works**: Run `python3 -c "import whisper; model = whisper.load_model('tiny'); print(model)"` and confirm it loads without error.
3. **faster-whisper works**: Run `python3 -c "from faster_whisper import WhisperModel; model = WhisperModel('tiny', device='cpu', compute_type='int8'); print('OK')"` and confirm it prints `OK`.