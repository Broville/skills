# Kaleb One — Component Patterns

Complete HTML patterns for all pre-built M3 component classes in `components.css`.

## Standard HTML Boilerplate

```html
<!DOCTYPE html>
<html lang="en" data-theme="obsidian">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>App Name</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/triursa/theme-kaleb-one@main/dist/theme-all.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/triursa/theme-kaleb-one@main/dist/components.css">
</head>
<body>
  <nav class="nav-rail">
    <a href="#" class="nav-rail-item nav-rail-item--active">
      <div class="nav-rail-icon">🏠</div>
      <span>Home</span>
    </a>
    <a href="#" class="nav-rail-item">
      <div class="nav-rail-icon">📊</div>
      <span>Dashboard</span>
    </a>
    <a href="#" class="nav-rail-item">
      <div class="nav-rail-icon">⚙️</div>
      <span>Settings</span>
    </a>
  </nav>

  <header class="app-bar">
    <h1>App Name</h1>
    <div class="palette-switcher">
      <button class="palette-btn palette-btn--active" onclick="document.documentElement.setAttribute('data-theme','obsidian')">
        <span class="palette-swatch" style="background:#7B8FA8"></span> Obsidian
      </button>
      <button class="palette-btn" onclick="document.documentElement.setAttribute('data-theme','midnight-ocean')">
        <span class="palette-swatch" style="background:#4A90D9"></span> Ocean
      </button>
      <button class="palette-btn" onclick="document.documentElement.setAttribute('data-theme','volcanic')">
        <span class="palette-swatch" style="background:#D4853A"></span> Volcanic
      </button>
      <button class="palette-btn" onclick="document.documentElement.setAttribute('data-theme','frost')">
        <span class="palette-swatch" style="background:#3B82F6"></span> Frost
      </button>
    </div>
  </header>

  <main class="main-content">
    <!-- Your content here -->
  </main>

  <button class="md-fab">＋</button>
</body>
</html>
```

## Navigation Rail

```html
<nav class="nav-rail">
  <a href="#" class="nav-rail-item nav-rail-item--active">
    <div class="nav-rail-icon">🏠</div>
    <span>Home</span>
  </a>
  <a href="#" class="nav-rail-item">
    <div class="nav-rail-icon">📊</div>
    <span>Stats</span>
  </a>
</nav>
```

**Important:** When using `.nav-rail`, apply `margin-left: 80px` to `.app-bar` and `.main-content`.

## App Bar

```html
<header class="app-bar">
  <h1>Page Title</h1>
</header>
```

## Buttons

```html
<button class="md-button md-button--filled">Filled (Primary)</button>
<button class="md-button md-button--filled-secondary">Filled (Secondary)</button>
<button class="md-button md-button--filled-tertiary">Filled (Tertiary)</button>
<button class="md-button md-button--outlined">Outlined</button>
<button class="md-button md-button--tonal">Tonal</button>
<button class="md-button md-button--text">Text Button</button>
<button class="md-button md-button--icon">🔍</button>
<button class="md-button md-button--fab">＋</button>
```

## Cards

```html
<div class="md-card md-card--elevated">
  <div class="md-card-title">Card Title</div>
  <div class="md-card-subtitle">Subtitle text</div>
  <div class="md-card-body">Body text content here.</div>
</div>

<div class="md-card md-card--filled">Filled card</div>
<div class="md-card md-card--outlined">Outlined card</div>
```

## Card Grid

```html
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: var(--md-sys-spacing-4);">
  <div class="md-card md-card--elevated">
    <div class="md-card-title">Title</div>
    <div class="md-card-body">Content</div>
  </div>
</div>
```

## Chips

```html
<span class="md-chip md-chip--assist">Assist Chip</span>
<span class="md-chip md-chip--filter">Filter Chip</span>
<span class="md-chip md-chip--suggestion">Suggestion Chip</span>
```

## Text Fields

```html
<div class="md-textfield">
  <input type="text" id="name" placeholder=" ">
  <label for="name">Name</label>
</div>
```

## Dialog

```html
<div class="md-dialog-overlay">
  <div class="md-dialog">
    <div class="md-dialog-title">Confirm Action?</div>
    <div class="md-dialog-body">Are you sure you want to proceed?</div>
    <div class="md-dialog-actions">
      <button class="md-button md-button--text">Cancel</button>
      <button class="md-button md-button--filled">Confirm</button>
    </div>
  </div>
</div>
```

## Snackbar

```html
<div class="md-snackbar">
  Item archived
  <button class="md-button md-button--text">Undo</button>
</div>
```

## Divider

```html
<hr class="md-divider">
```

## List Items

```html
<div class="md-list">
  <div class="md-list-item">
    <div class="md-list-item-icon">📥</div>
    <div class="md-list-item-text">
      <div class="md-list-item-headline">Inbox</div>
      <div class="md-list-item-supporting">12 new messages</div>
    </div>
  </div>
</div>
```

## Progress Bar

```html
<div class="md-progress-linear">
  <div class="md-progress-linear__bar" style="width: 75%;"></div>
</div>
```

## Tabs

```html
<div class="md-tabs">
  <button class="md-tab md-tab--active">Tab 1</button>
  <button class="md-tab">Tab 2</button>
  <button class="md-tab">Tab 3</button>
</div>
```

## Toggle Group

```html
<div class="toggle-group">
  <button class="toggle-option toggle-option--active">Option A</button>
  <button class="toggle-option">Option B</button>
  <button class="toggle-option">Option C</button>
</div>
```

## Status Badge / Pill

```html
<span style="
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  padding: var(--md-sys-spacing-1) var(--md-sys-spacing-3);
  border-radius: var(--md-sys-shape-corner-full);
  font-size: var(--md-sys-typescale-label-small-size);
">Active</span>
```

## Data Table Row

```html
<div style="
  background-color: var(--md-sys-color-surface-container-low);
  border-radius: var(--md-sys-shape-corner-small);
  padding: var(--md-sys-spacing-3) var(--md-sys-spacing-4);
  margin-bottom: var(--md-sys-spacing-2);
">
  <span style="
    color: var(--md-sys-color-on-surface);
    font-size: var(--md-sys-typescale-body-medium-size);
  ">Row content</span>
</div>
```

## Palette Switching at Runtime

```html
<script>
  function setTheme(name) {
    document.documentElement.setAttribute('data-theme', name);
    document.querySelectorAll('.palette-btn').forEach(btn => {
      btn.classList.toggle('palette-btn--active',
        btn.textContent.trim().toLowerCase().includes(name.replace('-', ' ')));
    });
  }
</script>
```

Valid theme names: `obsidian`, `midnight-ocean`, `volcanic`, `frost`.

## Responsive Behavior

On screens < 768px, the nav rail is hidden (`display: none`). The component CSS includes this media query automatically. Ensure your app works without the nav rail on mobile viewports.