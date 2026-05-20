---
name: memento-flashcards
description: Spaced-repetition flashcard system — create cards from facts, review with adaptive scheduling, generate quizzes from YouTube transcripts, export/import as CSV. All data stored locally, no API keys required.
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - Mention "flashcard", "memorize", "remember this", or "save this card"
  - Want to review due flashcards or study with spaced repetition
  - Send a YouTube URL and want a quiz generated from it
  - Ask to export, import, or manage flashcard decks
related_skills:
  - concise-planning
  - verification-before-completion
---

# Memento Flashcards

## Description

A local, file-based flashcard system with spaced-repetition scheduling. Create Q/A cards from statements, review due cards with adaptive intervals, generate quizzes from YouTube transcripts, and manage decks with JSON storage and CSV import/export. No external API keys required — the agent generates flashcard content and quiz questions directly, using a Python script for card management and scheduling.

All card data lives in a single JSON file at `~/.hermes/skills/productivity/memento-flashcards/data/cards.json`. The Python helper script handles atomic writes to prevent corruption.

## Prerequisites

- Python 3.x available on the system
- Helper scripts installed at `~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py`
- For YouTube quiz generation: `youtube-transcript-api` package (`pip install youtube-transcript-api`)

```bash
# Verify helper script is available
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py stats

# Install YouTube transcript dependency (optional, for quiz generation)
pip install youtube-transcript-api
```

## Steps

### Step 1: Creating Cards from Facts

When the user mentions a fact or wants to remember something:

**Activation tiers:**
- **Explicit** — user mentions "flashcard", "remember this", "save this card" → create directly
- **Implicit** — user sends a factual statement without mentioning flashcards → ask: "Want me to save this as a flashcard?"
- **No intent** — coding tasks, questions, normal conversation → do NOT activate

To create a card:

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add \
  --question "What year did World War 2 end?" \
  --answer "1945" \
  --collection "History"
```

Default collection is `"General"` if none is specified.

### Step 2: Reviewing Due Cards

Fetch all due cards:

```bash
# All due cards
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due

# Filter by collection
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due --collection "History"
```

Review flow (free-text grading):
1. Show only the question. Wait for the user to answer.
2. Compare their answer to the expected answer and grade: **correct**, **partial**, or **incorrect**
3. Tell the user the correct answer and how they did (keep it brief and plain-text):
   - Correct: `"Correct. Answer: {answer}. Next review in 7 days."`
   - Partial: `"Close. Answer: {answer}. {what they missed}. Next review in 3 days."`
   - Incorrect: `"Not quite. Answer: {answer}. Next review tomorrow."`
4. Rate the card:

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py rate \
  --id CARD_ID --rating easy --user-answer "what the user said"
```

Rating intervals:
- **hard** → +1 day, reset ease streak, stays learning
- **good** → +3 days, reset ease streak, stays learning
- **easy** → +7 days, +1 ease streak, if streak ≥ 3 → retired
- **retire** → permanent, removed from reviews

If no cards are due: `"No cards due for review right now. Check back later!"`

### Step 3: Generating a YouTube Quiz

When the user sends a YouTube URL and wants a quiz:

1. Extract the video ID from the URL (e.g., `dQw4w9WgXcQ` from `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Fetch the transcript:

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/youtube_quiz.py fetch VIDEO_ID
```

3. Generate 5 quiz questions from the first 15,000 characters of the transcript (the agent generates these — not an API call)
4. Validate the output is valid JSON with exactly 5 items, each having `question` and `answer`
5. Store quiz cards:

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add-quiz \
  --video-id "VIDEO_ID" \
  --questions '[{"question":"...","answer":"..."},...]' \
  --collection "Quiz - Episode Title"
```

The script deduplicates by `video_id` — if cards for that video exist, it skips creation.
6. Present questions one-by-one using the same free-text grading flow from Step 2

### Step 4: Exporting and Importing CSV

**Export:**

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py export \
  --output ~/flashcards.csv
```

Produces a 3-column CSV: `question,answer,collection` (no header row).

**Import:**

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py import \
  --file ~/flashcards.csv \
  --collection "Imported"
```

Reads a CSV with columns: question, answer, and optionally collection (column 3). If the collection column is missing, uses the `--collection` argument.

### Step 5: Checking Statistics

```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py stats
```

Returns JSON with: `total`, `learning`, `retired`, `due_now`, and `collections` breakdown.

### Step 6: Deleting Cards

```bash
# Delete a specific card
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py delete --id CARD_ID

# Delete an entire collection
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py delete-collection --collection "History"
```

## Pitfalls

1. **Never edit `cards.json` directly** — Always use the `memento_cards.py` subcommands. The script handles atomic writes (write to temp file, then rename) to prevent corruption.
2. **Skipping feedback during review** — The user MUST see the correct answer and a brief assessment before you move to the next card. Every answer gets visible feedback.
3. **Transcript failures on YouTube** — Some videos have no English transcript or have transcripts disabled. Inform the user and suggest another video rather than failing silently.
4. **Missing `youtube-transcript-api` dependency** — The quiz feature requires `pip install youtube-transcript-api`. If the script reports `missing_dependency`, tell the user to install it.
5. **Video ID extraction** — Support both `youtube.com/watch?v=ID` and `youtu.be/ID` URL formats, otherwise quiz generation will fail on valid URLs.
6. **Creating cards without confirmation** — Only create a card directly when the user explicitly mentions flashcards. For implicit factual statements, always ask first.

## Verification

1. **Helper script works:**
   ```bash
   python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py stats
   ```
2. **Card creation works:**
   ```bash
   python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add --question "Capital of France?" --answer "Paris" --collection "General"
   ```
3. **Due cards can be fetched:**
   ```bash
   python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due
   ```
4. **Review feedback includes correct answer** — After each card, the user sees the right answer and a brief assessment before the next question