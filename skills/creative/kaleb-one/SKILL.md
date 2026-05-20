---
name: kaleb-one
description: Material Design 3 design system from the kaleb.one ecosystem — 4 palettes (Obsidian, Midnight Ocean, Volcanic, Frost), full token system, pre-built M3 components, and Tailwind preset.
version: 1.0.0
author: triursa
license: MIT
trigger:
  - User asks to build or update UI/UX with Kaleb One theme
  - User mentions "kaleb", "kaleb.one", "theme-kaleb-one", "obsidian palette", or "M3 design tokens"
  - User wants Material Design 3 theming with CSS custom properties
  - User requests dark-mode-first design with pre-built component styles
  - User asks for a Tailwind CSS preset with M3 tokens
inputs:
  - name: palette
    description: "Which palette to use: obsidian (default), midnight-ocean, volcanic, or frost"
    required: false
  - name: framework
    description: "Target framework: vanilla-html, tailwind, or npm"
    required: false
outputs:
  - name: styled_page
    description: HTML/CSS output using kaleb-one design tokens and components
metadata:
  hermes:
    tags: [material-design-3, m3, design-tokens, dark-theme, tailwind, css-custom-properties, component-library]
    related_skills: [pages-viz]
---

# Kaleb One — Material Design 3 Theme System

> **Source:** [triursa/theme-kaleb-one](https://github.com/triursa/theme-kaleb-one) — MIT License

A shared Material Design 3 design system for the kaleb.one ecosystem. Provides 4 curated palettes, a complete token system (colors, typography, spacing, elevation, shape, motion), pre-built M3 component CSS, and a Tailwind CSS preset.

## Description

Kaleb One is a design token system and component library implementing Material Design 3 (M3). It ships 4 production-ready palettes with full color role derivation, 15 typography scale levels, a 4px-based spacing scale, M3 elevation with dark-mode overlays, shape radii, and motion tokens — all as CSS custom properties. A pre-built component CSS file provides ready-to-use M3 components (buttons, cards, chips, dialogs, nav rails, etc.). Use it when building any dark-mode-first app, dashboard, or static page that needs a polished M3 aesthetic.

## Prerequisites

- Modern browser (CSS custom properties + `color-mix()` support required for dark elevation overlays)
- For npm usage: Node.js 16+ and a bundler (Vite, webpack, etc.)
- For static HTML: no build tools needed — just CDN links

## Steps

### 1. Choose your palette

| # | Name | `data-theme` | Vibe | Use Case |
|---|------|-------------|------|----------|
| 1 | **Obsidian** | `obsidian` | Dark slate, electric accent — sharp, modern, minimal | Default for all apps |
| 2 | **Midnight Ocean** | `midnight-ocean` | Deep navy, teal accent — calm authority | Dashboards, data viz |
| 3 | **Volcanic** | `volcanic` | Dark warm gray, amber/orange accent — warm, grounded | Content sites, editorial |
| 4 | **Frost** | `frost` | Light theme — cool gray, blue accent — clean | Documentation, public sites |

**Default:** Always use **Obsidian** unless the project explicitly calls for a different palette. Never mix palettes on a single page.

### 2. Load the theme and fonts (CDN — recommended for static pages)

```html
<!-- Fonts (required) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<!-- All palettes (switchable at runtime via data-theme) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/triursa/theme-kaleb-one@main/dist/theme-all.css">

<!-- OR a single palette (smaller file, applies to :root) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/triursa/theme-kaleb-one@main/dist/theme-obsidian.css">

<!-- M3 component styles (optional but recommended) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/triursa/theme-kaleb-one@main/dist/components.css">
```

### 3. Activate the palette

```html
<html data-theme="obsidian">
```

For single-palette CSS files, colors apply to `:root` directly — no `data-theme` needed.

### 4. Use tokens in your CSS

```css
/* ✅ Correct — use design tokens */
background-color: var(--md-sys-color-surface);
color: var(--md-sys-color-on-surface);
padding: var(--md-sys-spacing-4);
border-radius: var(--md-sys-shape-corner-medium);
font-size: var(--md-sys-typescale-body-medium-size);
transition: all var(--md-sys-motion-duration-medium2) var(--md-sys-motion-easing-standard);

/* ❌ Wrong — never hardcode values */
background-color: #11151C;
padding: 16px;
border-radius: 12px;
```

### 5. Use pre-built components (if components.css loaded)

```html
<button class="md-button md-button--filled">Primary Action</button>
<div class="md-card md-card--elevated">
  <div class="md-card-title">Title</div>
  <div class="md-card-body">Content</div>
</div>
```

### 6. Use npm (for build-tool projects)

```bash
npm install @kaleb-one/theme
```

```js
// Import a specific palette CSS
import '@kaleb-one/theme/css/obsidian';

// Or import all palettes
import '@kaleb-one/theme/css/all';

// Import component styles
import '@kaleb-one/theme/css/components';
```

### 7. Use Tailwind preset (v3)

```js
// tailwind.config.js
module.exports = {
  presets: [require('@kaleb-one/theme/tailwind')],
};
```

For Tailwind v4, import tokens as CSS and use arbitrary values: `bg-[var(--md-sys-color-surface)]`

## Pitfalls

1. **Never hardcode color values** — always use `var(--md-sys-color-*)` tokens so palette switching works
2. **Never mix palettes on one page** — pick one palette per page/app
3. **Don't skip Google Fonts** — Inter and JetBrains Mono must be loaded for typography scale to render correctly
4. **Dark elevation requires BOTH shadow AND overlay** — use `box-shadow: var(--md-sys-elevation-N)` PLUS `.md-elevation-N` class for tinted background in dark themes
5. **Nav rail needs margin offset** — when using `.nav-rail`, add `margin-left: 80px` to `.app-bar` and `.main-content` (included in components.css)
6. **Frost is a LIGHT theme** — its `surface` and `on-surface` colors are inverted compared to the 3 dark palettes
7. **`color-mix()` CSS function** is required for dark elevation overlays — works in all modern browsers but not IE11
8. **Single-palette CSS files** apply to `:root` without `data-theme`; `theme-all.css` requires the `data-theme` attribute on `<html>`
9. **Surface hierarchy matters in dark themes** — never use `surface` for elevated cards. Use `surface-container-low` → `surface-container` → `surface-container-high` → `surface-container-highest` for increasing elevation levels

## Verification

1. Load `theme-all.css` + `components.css` + Google Fonts in a blank HTML page
2. Set `data-theme="obsidian"` on `<html>`
3. Verify: page background is `#11151C` and text is `#DCE1E9`
4. Switch palette to `midnight-ocean` — colors should change, layout stays stable
5. Add a card with `class="md-card md-card--elevated"` — it should render with shadow and surface-container-low background
6. Add a button with `class="md-button md-button--filled"` — it should use primary color (`#BACFE5` bg on Obsidian)
7. Check that all typography tokens produce correct sizes/weights at each scale level

## Cross-References

- **Theme source repo:** [triursa/theme-kaleb-one](https://github.com/triursa/theme-kaleb-one)
- **NPM package:** `@kaleb-one/theme`
- **CDN:** `jsdelivr.net/gh/triursa/theme-kaleb-one@main/dist/`
- **Showcase:** [theme.kaleb.one](https://theme.kaleb.one)