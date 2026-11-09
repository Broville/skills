# Card-game prototype production checklist

## Default physical spec

- Poker card trim: 2.5 × 3.5 in (63.5 × 88.9 mm).
- Bleed: 0.125 in / 3 mm on every side unless the selected printer specifies otherwise.
- Safe area: keep critical text, indexes, and symbols at least 0.125 in / 3 mm inside trim; use 5 mm when small type or trim variance makes that safer.
- Corner radius: approximately 1/8 in / 3–3.5 mm is a common starting point, but follow the selected printer's die/template.
- Raster art: target 300 DPI at final size when raster output is required.
- Color: document whether the workflow is RGB for screen prototypes or CMYK for a printer's final prepress workflow; do not silently convert.

## Accessible visual checks

- Text and important symbols have strong light/dark contrast. Use WCAG 2.2 AA as a screen-design floor: 4.5:1 for ordinary text and 3:1 for large text.
- Never encode a faction, status, or card type with hue alone.
- Test grayscale and reduced-size views.
- Give every novel icon a label, legend, or redundant text cue.
- Keep line weights and counters open at the intended physical size.
- Check that the card remains scannable when held in a fan and at the table's expected distance.

## Prototype data record

For each card, retain stable fields such as `id`, `type`, `title`, `cost`, `tags`, `rules_text`, `icon_key`, `art_asset`, and `artist_or_source`. Keep this data separate from layout code when making a deck or variants.

## Asset manifest fields

`asset_id`, `filename`, `source_or_prompt`, `creator_or_provider`, `license_or_permission`, `model_and_seed_if_generated`, `transformations`, `date_obtained`, and `notes_or_risks`.

## Export evidence

Record the exact renderer and command or UI path used, output dimensions, page count, and whether the result was visually inspected. A valid SVG source is not evidence that a PDF, PNG, or AI-generated image was successfully produced.
