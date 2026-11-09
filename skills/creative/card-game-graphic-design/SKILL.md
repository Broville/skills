---
name: card-game-graphic-design
description: Design accessible, print-safe card-game visuals and prototypes in SVG, HTML, and optional raster/image-generation workflows. Use when ideating a deck, card face, symbol system, visual hierarchy, or printable mockup.
license: MIT
compatibility: Open Agent Skills format. Works with standards-compatible hosts; SVG and HTML require no external runtime. Optional PDF/raster/image generation depends on host capabilities and must be detected before use.
metadata:
  author: Broville
  version: "1.0.0"
  platforms: '["linux","macos","windows"]'
  triggers: '["User asks for card-game graphic design or visual ideation","User wants a card face, deck layout, icon or symbol system","User requests a printable card prototype or mockup","User asks for image prompts or optional generated art for a card game"]'
  inputs: '[{"name":"game-brief","description":"Theme, audience, mechanics, card types, and intended output","required":true},{"name":"card-spec","description":"Card size, bleed, safe area, orientation, and production target","required":false},{"name":"asset-policy","description":"Allowed image sources, licenses, and whether generated imagery is permitted","required":false}]'
  outputs: '[{"name":"design-spec","description":"Tokenized visual system and card-layout decisions"},{"name":"prototype","description":"Self-contained SVG or HTML prototype, with optional PDF/raster export when verified"},{"name":"asset-record","description":"Prompts, provenance, licenses, and unresolved production risks"}]'
  tags: '["card-games","graphic-design","print","svg","html","accessibility","prototyping","image-production"]'
  related-skills: '["arts-crafts","design-system-engineering","stable-diffusion-image-generation","web-accessibility","pdf","screenshot"]'
---

# Card-Game Graphic Design

## Description

Use this skill to turn a card-game brief into a coherent, playable visual system and a testable prototype. Prioritize information hierarchy and playability over decorative art. Keep source assets editable and portable: prefer inline SVG, self-contained HTML, and structured card data. Treat image generation as optional; never imply that a host can generate images until its capability is detected and a real test succeeds.

## Prerequisites

- A game brief containing audience, theme, mechanics, card types, and player actions.
- A chosen physical card specification or an explicit digital-only target.
- A host with file writing for prototypes; PDF, raster, browser, or image-generation capabilities are optional.
- Asset licensing/provenance rules. Do not use copyrighted or private assets without permission.

## Steps

1. **Extract the play information.** List what must be recognized at a glance, during hand management, and during rules lookup: card type, cost, strength, suit/faction, timing, targets, state changes, and flavor text. Rank these items by decision importance.
2. **Choose a production spec.** Default to poker size 2.5 × 3.5 inches only when the user has not specified another size. For print prototypes, use 0.125 inch / 3 mm bleed and keep critical content inside a 0.125 inch / 3 mm safe margin; use a larger safe margin for small text or manufacturing with uncertain trim tolerance. Record units, orientation, corner radius, resolution target, and color mode in the design spec.
3. **Build a tokenized visual system.** Define a small palette with semantic roles, typography by role, spacing, border/radius rules, icon stroke/fill rules, and a contrast check. Do not make color the only carrier of meaning: pair color with labels, shape, pattern, or position.
4. **Draft the card anatomy.** Make the title and primary value easy to find from a fanned hand. Put repeated indexes in consistent corners. Reserve a stable rules-text region, use short lines, and avoid placing essential text over busy art. Design the card back separately and test whether orientation or asymmetry leaks information.
5. **Create symbols and icons.** Use simple silhouettes that remain distinct at the smallest intended size. Provide a text label or legend for novel symbols. Test in grayscale, at low resolution, and with common color-vision deficiencies; use shape and line treatment in addition to hue.
6. **Produce a prototype.** Start with the bundled `templates/card-face.svg` for a single card or create a self-contained HTML board for variants. Keep source card data separate from presentation when making more than a few cards. Use inline SVG/CSS and no remote fonts, CDN scripts, tracking, or remote image URLs in offline prototypes.
7. **Handle image production safely.** If the host exposes image generation, inspect its documented capability and run a small, non-sensitive test before promising generated art. Use prompts that specify composition, palette, aspect ratio, negative constraints, and empty space for rules text. Preserve prompt, model/provider, seed if available, date, and license/usage terms. Treat generated art as an illustration layer, not a source of authoritative rules text or tiny symbols; add those in vector/text layers.
8. **Export only through detected capabilities.** SVG is the source of truth. If a PDF or PNG renderer exists, export from the SVG/HTML and verify dimensions, page count, and readability. If a renderer is unavailable, report that limitation and leave the verified SVG/HTML source rather than fabricating an export result.
9. **Run the playability review.** Check at least: 3-second recognition, fanned-hand scan, two-player distance, low-light readability, grayscale, color-vision differences, icon ambiguity, text size, bleed/safe area, card-back information leakage, and whether art competes with the action cue.
10. **Record the asset manifest.** For every external or generated asset, record source URL or prompt, author/provider, license/permission, local filename, transformation, and unresolved risk. Never embed credentials, private paths, or opaque downloaded binaries in the skill or prototype.

## Pitfalls

- **Art-first layouts hide mechanics.** Put the decision cue, cost, and identity before decorative illustration.
- **Color-only encoding fails.** Add labels, symbols, patterns, or redundant placement.
- **Uniform hairline borders expose trim variance.** Use generous margins or borderless backgrounds when a printed border would make small cutting differences obvious.
- **Generated art is not reliable typography.** Keep names, numbers, rules, and icons as editable vector/text elements.
- **Unverified image tooling is not availability.** A configured tool, package, or model name is not evidence of successful generation.
- **Remote assets make prototypes fragile and may create supply-chain or licensing risk.** Keep prototypes self-contained and obtain permission before redistribution.
- **Tiny text and dense effects are hard to print.** Test at intended physical size, not only on a large monitor.
- **Symmetric backs can still leak through edge wear or orientation.** Check repeated marks, directional motifs, and crop tolerance.

## Verification

1. Confirm `SKILL.md` and supporting files contain no secrets, private absolute paths, executable downloads, prompt-injection instructions, or destructive commands.
2. Open the SVG/HTML prototype in a standards-compatible viewer or parse it with an available validator; confirm the card dimensions, bleed, safe zone, text labels, and symbols are present.
3. If an export was requested and the host supports it, verify the output exists and inspect its dimensions/page count with the relevant local tool. Report static review separately from runtime export testing.
4. Run the grayscale and contrast review. Body text should meet WCAG 2.2 AA contrast guidance where applicable; large text has the lower large-text threshold. Do not treat contrast compliance as a substitute for physical-size testing.
5. Perform a manual playability review with at least one printed-size or reduced-scale check, and document any unresolved ambiguity or production risk.

## Cross-References

- `references/production-spec.md` contains the print and accessibility checklist used by this workflow.
- `templates/card-face.svg` is a portable poker-size starting point with visible bleed and safe-area guides.
- W3C WCAG 2.2 contrast guidance: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
- PrintNinja card setup guidance: https://printninja.com/card-deck-setup-guides/
- The Game Crafter poker card dimensions and templates: https://www.thegamecrafter.com/make/custom-playing-cards
- Inkscape export documentation: https://inkscape.org/doc/inkscape-man100.html
