# Playwright CLI Reference

This reference documents the Playwright CLI commands available for browser automation.

## Core Commands

### Navigation

```bash
"$PWCLI" open <url> [--headed]     # Open a page (use --headed for visible browser)
"$PWCLI" close                      # Close current page
```

### Snapshot and Inspection

```bash
"$PWCLI" snapshot                   # Get accessibility tree with element refs (e5, e12, etc.)
```

### Interaction

```bash
"$PWCLI" click <ref>                # Click element by ref
"$PWCLI" type <text>               # Type text at current focus
"$PWCLI" fill <ref> <text>          # Fill a form field by ref
"$PWCLI" press <key>                # Press a key (Enter, Tab, Escape, etc.)
```

### Tabs

```bash
"$PWCLI" tab-new <url>              # Open a new tab
"$PWCLI" tab-list                    # List open tabs
"$PWCLI" tab-select <index>         # Switch to tab by index
```

### Artifacts

```bash
"$PWCLI" screenshot                  # Capture a screenshot
"$PWCLI" tracing-start               # Start trace recording
"$PWCLI" tracing-stop                # Stop trace recording and save
```

## Element Reference System

The `snapshot` command returns an accessibility tree with element references like `e3`, `e12`, `e45`. These references are stable only until the next DOM change. Always re-snapshot after navigation, clicks that change the UI, or modal/panel transitions.

## Common Patterns

### Form Fill

```bash
"$PWCLI" open https://example.com/form
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e3
"$PWCLI" snapshot
```

### Multi-Tab

```bash
"$PWCLI" open https://example.com
"$PWCLI" snapshot
"$PWCLI" tab-new https://example.com/settings
"$PWCLI" snapshot
"$PWCLI" tab-select 0
"$PWCLI" snapshot
```

### Debug with Traces

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" tracing-start
# ...interactions...
"$PWCLI" tracing-stop
```