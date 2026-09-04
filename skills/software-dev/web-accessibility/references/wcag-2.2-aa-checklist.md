# WCAG 2.2 AA Engineering Checklist

This is a routing checklist, not a substitute for the normative [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) and its Understanding documents. Mark a row **pass**, **fail**, **not applicable**, or **unverified**, and attach the route/state plus evidence.

## Perceivable

- Text alternatives communicate the purpose of meaningful non-text content; decorative content is ignored.
- Captions, transcripts, audio description, and media controls satisfy the media in scope.
- Structure and relationships survive without visual styling: headings, landmarks, lists, labels, tables, reading order, and instructions.
- Content does not depend only on shape, position, sound, or color.
- Text and large text meet the applicable contrast ratios; controls, focus indicators, and meaningful graphics have sufficient non-text contrast.
- Text can resize to 200%; content reflows at the WCAG 2.2 AA dimensions without two-dimensional scrolling except for allowed content.
- Text spacing overrides, orientation changes, zoom, and responsive variants do not clip or lose content or function.

## Operable

- Every function works by keyboard without a trap; focus order follows meaning and operation.
- Bypass mechanisms, page title, headings, labels, and link purpose support navigation.
- Focus is visible and not entirely hidden by author-created content.
- Timing can be extended or disabled where required; moving or auto-updating content can be paused.
- Flashing content stays below seizure thresholds; motion triggered by interaction can be disabled when not essential.
- Pointer gestures have simple alternatives; dragging has a non-drag alternative; cancellation and label-in-name behavior are correct.
- Targets meet WCAG 2.2 minimum sizing or an allowed exception, with adequate spacing where used.

## Understandable

- Page and passage languages are programmatically identified.
- Navigation, identification, and help placement are consistent where the criteria apply.
- Controls do not cause unexpected context changes on focus or input without warning.
- Labels and instructions precede input; errors are identified, described, associated, and recoverable.
- Repeated information can be reused or selected rather than re-entered where WCAG 2.2 requires it.
- Authentication does not depend solely on memorization, transcription, or puzzle solving; paste, password managers, and accessible alternatives remain available.

## Robust

- Interactive elements expose correct accessible name, role, value, state, and relationships.
- Status messages are announced without moving focus when appropriate.
- Custom widgets implement the complete keyboard and state model from the relevant [ARIA APG pattern](https://www.w3.org/WAI/ARIA/apg/patterns/).
- Native HTML is used when it already provides the needed semantics and behavior.

## Evidence limits

Automated tools are useful for deterministic DOM rules such as missing names, invalid ARIA, some contrast failures, and duplicate IDs. They do not prove reading order, keyboard usability, meaningful text alternatives, error recovery, cognitive accessibility, screen-reader announcements, or full-page conformance. Preserve automated **incomplete** results for manual review instead of treating them as passes.
