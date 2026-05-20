---
name: playwright
description: Automate browser interactions using native browser tools (primary) or Playwright CLI (fallback). Navigate pages, click elements, fill forms, capture screenshots, and debug UI flows programmatically.
version: 1.0.0
author: Broville
license: MIT
platforms:
  - linux
trigger:
  - User asks to automate browser interactions or web flows
  - User asks to test a web application flow end-to-end
  - User asks to fill forms programmatically or extract data from web pages
  - User asks to capture screenshots of web pages
  - User mentions browser automation, browser testing, or UI flow debugging
inputs:
  - name: url
    description: Starting URL for browser navigation
    required: true
  - name: action
    description: Browser action to perform (navigate, click, type, fill, screenshot, snapshot)
    required: true
outputs:
  - name: page_state
    description: Current page state (DOM snapshot, accessibility tree, or screenshot)
  - name: extracted_data
    description: Data extracted from the page
metadata:
  hermes:
    tags:
      - browser
      - automation
      - testing
      - playwright
      - web
    related_skills:
      - screenshot
---

# Playwright

## Description

Automate browser interactions for testing web flows, filling forms, extracting data, and capturing page state. This skill supports two approaches:

1. **Native Browser Tools (Primary)** — Use `browser_navigate`, `browser_click`, `browser_snapshot`, `browser_vision`, and similar tools when available in the agent's environment. These provide direct browser control without external dependencies.

2. **Playwright CLI (Fallback)** — Use the `playwright-cli` command-line tool when native browser tools are not available. This requires Node.js and npm.

Always prefer native browser tools when they are available. Fall back to the Playwright CLI only when needed.

## Prerequisites

### Path 1: Native Browser Tools (Primary)

Check if native browser tools are available in your environment:

- `browser_navigate` — Navigate to a URL
- `browser_click` — Click an element
- `browser_snapshot` — Capture accessibility tree or DOM snapshot
- `browser_vision` — Capture a visual screenshot
- Additional tools: `browser_type`, `browser_fill`, `browser_scroll`, etc.

If these tools are available, no additional setup is required. Proceed to the native flow.

### Path 2: Playwright CLI (Fallback)

Verify Node.js/npm availability:

```bash
command -v npx >/dev/null 2>&1 && echo "npx available" || echo "npx not found"

# If missing, install Node.js first:
node --version
npm --version

# Then install Playwright CLI:
npm install -g @playwright/cli@latest
playwright-cli --help
```

Alternatively, use the bundled wrapper script from the skill's `scripts/` directory to run without a global install.

## Steps

### Path 1: Native Browser Tools

#### 1. Navigate to the starting page

Use the `browser_navigate` tool with the target URL.

#### 2. Capture page state

Use `browser_snapshot` to get the accessibility tree or DOM structure. This provides stable element identifiers for interaction.

#### 3. Interact with elements

Use `browser_click` to click buttons, links, or other interactive elements. Use `browser_type` or `browser_fill` to enter text into form fields.

#### 4. Re-snapshot after navigation

After any action that changes the page significantly (navigation, form submission, modal open/close, tab switch), capture a new snapshot. Element identifiers can become stale after DOM changes.

#### 5. Verify results

Use `browser_snapshot` or `browser_vision` to confirm the expected state of the page after interactions.

### Path 2: Playwright CLI

#### 1. Set up the CLI

```bash
# Using the skill's wrapper script (preferred)
export SKILL_HOME="${SKILL_HOME:-$HOME/.local/share/skills}"
export PWCLI="$SKILL_HOME/playwright/scripts/playwright_cli.sh"

# Or using global install:
npm install -g @playwright/cli@latest
```

#### 2. Open the page

```bash
"$PWCLI" open https://example.com
```

#### 3. Snapshot to get element references

```bash
"$PWCLI" snapshot
```

#### 4. Interact using element refs from the snapshot

```bash
"$PWCLI" click e3
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e5
```

#### 5. Re-snapshot after significant changes

```bash
"$PWCLI" snapshot
```

Refs become stale after navigation or DOM changes. Always re-snapshot after such events.

#### 6. Capture artifacts (optional)

```bash
"$PWCLI" screenshot
"$PWCLI" tracing-start
# ...interactions...
"$PWCLI" tracing-stop
```

### Common Patterns

#### Form fill and submit

**Native:**
1. Navigate to form URL
2. Snapshot the page
3. Fill each form field using `browser_fill`
4. Click the submit button using `browser_click`
5. Snapshot the result page

**CLI:**
```bash
"$PWCLI" open https://example.com/form
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e3
"$PWCLI" snapshot
```

#### Multi-page workflow

1. Navigate to the starting page
2. Snapshot and interact
3. After navigation or page transition, re-snapshot
4. Continue interactions on the new page
5. Repeat for each step in the flow

#### Debugging with screenshots

Use `browser_vision` (native) or `$PWCLI screenshot` (CLI) to capture visual state when text-based snapshots are insufficient for understanding page layout.

## Pitfalls

- **Stale element references**: Element IDs (like `e3` in CLI mode) become invalid after any DOM change. Always re-snapshot after navigation, clicks that change the UI, modal open/close, or tab switches. When a ref fails, snapshot again immediately.
- **Headless mode limitations**: Some pages render differently in headless mode. Use `--headed` flag with CLI or visual mode with native tools when visual verification is needed. Screenshots may reveal rendering issues that snapshots don't show.
- **Dynamic content timing**: Pages with dynamic content may need a moment to render after navigation. If a snapshot shows incomplete content, wait briefly and re-snapshot.
- **Authentication state**: Browser sessions may not persist authentication between separate invocations of CLI commands. Plan flows to include login steps when needed, or use the same browser session throughout.

## Verification

1. **Tool availability check**:
   ```bash
   # For CLI path: verify playwright-cli is accessible
   npx --package @playwright/cli playwright-cli --help
   # Expected: usage information displayed
   ```

2. **Basic navigation works**:
   ```bash
   # CLI path
   "$PWCLI" open https://example.com
   "$PWCLI" snapshot
   # Expected: page content displayed with element references
   ```

3. **Interaction produces expected result**:
   For any form fill or click action, snapshot the page afterward and confirm the expected state change occurred.

4. **Screenshot capture works**:
   ```bash
   "$PWCLI" screenshot
   # Expected: screenshot file created or displayed
   ```

## Cross-References

- **screenshot** (`monitoring/screenshot`) — For desktop-level screenshot capture (not browser-specific)
- CLI command reference: `references/cli.md`
- Workflow patterns and troubleshooting: `references/workflows.md`