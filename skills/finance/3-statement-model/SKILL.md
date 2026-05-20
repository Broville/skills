---
name: 3-statement-model
description: Build fully-integrated 3-statement financial models (IS, BS, CF) in Excel with working capital schedules, D&A roll-forwards, and debt schedules using openpyxl
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to build a financial model with income statement, balance sheet, and cash flow
  - User wants an integrated 3-statement model in Excel
  - User provides historical financials and wants projections with proper linkages
  - User needs working capital schedules, depreciation roll-forwards, or debt schedules
related_skills:
  - excel-author
  - dcf-model
  - stocks
---

# 3-Statement Financial Model

## Description

Build fully-integrated 3-statement models (Income Statement, Balance Sheet, Cash Flow Statement) in Excel with working capital schedules, D&A roll-forwards, debt schedules, and the plugs that make cash and retained earnings tie. Produces `.xlsx` files using headless openpyxl. Pairs with the `excel-author` skill for formatting conventions.

## Prerequisites

- Python 3.8+ with `openpyxl` installed (`pip install openpyxl`)
- The `excel-author` skill's recalc script for delivery validation: `python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx`
- Source data: historical financials from SEC filings, company IR pages, or user-provided data

## Steps

### 1. Analyze the template structure

Before entering any data, thoroughly review the template:

1. Identify input vs. formula cells (blue font = inputs, black font = formulas, green font = cross-tab links)
2. Map the template's flow (e.g., Assumptions → IS → BS → CF)
3. Note any supporting schedules and their linkages to main statements
4. Document the template's specific line items and structure

### 2. Populate historical data (confirm with user first)

1. Enter historical actuals for each statement period
2. Verify formulas calculate correctly for historical periods
3. Show the user the historical block and confirm values/periods match source data

### 3. Build Income Statement projections

1. Project revenue using growth rates from Assumptions tab
2. Project operating expenses as percentages of revenue
3. Calculate subtotals (Gross Profit, EBIT, EBT, Net Income)
4. Run subtotal checks — show the user projected IS before moving on

### 4. Build Balance Sheet

1. Link working capital accounts to supporting schedules
2. Project non-current assets with D&A roll-forward
3. Link debt balances to debt schedule
4. **Critical check**: Verify Assets = Liabilities + Equity for every period before moving to CF

### 5. Build Cash Flow Statement

1. Start with Net Income from IS (must match)
2. Add back non-cash items (D&A, SBC)
3. Working capital changes with correct signs (increase in asset = use of cash = negative)
4. CapEx ties to PP&E schedule
5. Financing activities tie to changes in debt and equity
6. **Critical check**: CF ending cash must match BS cash

### 6. Cross-statement integrity checks

After all three statements are complete, confirm:

| Check | Formula | Expected Result |
|-------|---------|-----------------|
| Balance Sheet Balance | Assets - Liabilities - Equity | = 0 |
| Cash Tie-Out | CF Ending Cash - BS Cash | = 0 |
| Net Income Link | IS Net Income - CF Starting Net Income | = 0 |
| Retained Earnings | Prior RE + NI - Dividends - BS Ending RE | = 0 |

### 7. Add scenario analysis (if requested)

Use a scenario toggle (dropdown) in the Assumptions tab with CHOOSE or INDEX/MATCH formulas:

- **Base Case**: Management guidance or consensus estimates
- **Upside Case**: Above-guidance growth, margin expansion
- **Downside Case**: Below-trend growth, margin compression

### 8. Final validation

1. Recalculate the workbook: `python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx`
2. Fix all errors until status is `success`
3. Zero formula errors required (`#REF!`, `#DIV/0!`, `#VALUE!` not allowed)
4. Toggle through all scenarios and verify checks pass in each case

## Formatting Conventions

Use the professional blue/grey palette unless the template specifies otherwise:

- **Section headers**: Dark blue `#1F4E79`, white bold font
- **Column headers**: Light blue `#D9E1F2`, black bold font
- **Input cells**: Light grey `#F2F2F2` or white, blue `#0000FF` font
- **Formula cells**: White fill, black font
- **Cross-tab links**: White fill, green `#008000` font
- **Check rows / key totals**: Medium blue `#BDD7EE`, black bold font

## Golden Rules

1. **Formulas over hardcodes (non-negotiable)** — Every projection cell must be an Excel formula, never a pre-computed value. The ONLY hardcoded numbers allowed are: (1) historical actuals, (2) assumption drivers, (3) current market data.
2. **Verify step-by-step with the user** — Do NOT populate the entire model end-to-end and present it complete. Break at each statement, show the work, catch errors early.
3. **Sign conventions** — CFO: D&A/SBC positive (add-back), ΔAR increase negative (use of cash), ΔAP increase positive (source). CFI: CapEx negative. CFF: Debt issuance positive, repayments/dividends negative.

## Common Tab Names

| Tab Name | Contents |
|----------|----------|
| IS, P&L, Income Statement | Income Statement |
| BS, Balance Sheet | Balance Sheet |
| CF, CFS, Cash Flow | Cash Flow Statement |
| WC, Working Capital | Working Capital Schedule |
| DA, D&A, Depreciation, PP&E | Depreciation & Amortization Schedule |
| Debt, Debt Schedule | Debt Schedule |
| Assumptions, Inputs, Drivers | Driver assumptions and inputs |
| Checks, Audit, Validation | Error-checking dashboard |

## Pitfalls

1. **Hardcoding computed values in projection cells** — This breaks the model when assumptions change. Always use `=D14*(1+Assumptions!$B$5)` style formulas, never computed results like `12500`.
2. **Skipping step-by-step verification** — A wrong margin assumption discovered after the CF is built means rebuilding everything downstream. Show the user each stage.
3. **Incorrect working capital sign conventions** — Increase in an asset is a use of cash (negative in CFO); increase in a liability is a source of cash (positive). Getting these signs wrong breaks the cash tie-out silently.
4. **Forgetting to recalculate before delivery** — Always run `recalc.py` and fix all errors before delivering the model.
5. **Mixed absolute/relative references** — Use `$` correctly when copying formulas across periods. Wrong references cascade errors through the entire model.
6. **Deleting rows/columns without checking dependencies** — Always use Trace Precedents/Dependents before modifying template structure.

## Verification

1. **Balance sheet balances**: For every period, `Assets - Liabilities - Equity = 0` (add check rows and confirm they all read zero)
2. **Cash ties out**: `CF ending cash = BS cash` for every period
3. **Net income links**: `IS Net Income = CF starting Net Income` for every period
4. **Retained earnings roll forward**: `Prior RE + NI - Dividends = Ending RE` for every period
5. **Recalc passes**: Run `python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx` and confirm status is `success` with zero formula errors

## Cross-References

- **excel-author** — Formatting conventions, cell styling, named ranges, and sensitivity table patterns
- **dcf-model** — DCF valuation builds on the 3-statement model's outputs
- **stocks** — Source market data for current share prices and historicals