---
name: dcf-model
description: Build institutional-quality DCF valuation models in Excel with revenue projections, FCF build, WACC, terminal value, scenario analysis, and sensitivity tables using openpyxl
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to value a company using DCF (discounted cash flow) analysis
  - User wants intrinsic-value equity analysis with sensitivity tables
  - User needs WACC calculation, terminal value, or equity value bridge
  - User requests scenario analysis (Bear/Base/Bull) for a company valuation
related_skills:
  - excel-author
  - 3-statement-model
  - stocks
---

# DCF Model Builder

## Description

Creates institutional-quality DCF valuation models for equity analysis following investment banking standards. Each analysis produces a detailed Excel model with revenue projections, FCF build, WACC calculation, terminal value, Bear/Base/Bull scenarios, and 5×5 sensitivity tables. Uses headless openpyxl.

## Prerequisites

- Python 3.8+ with `openpyxl` installed (`pip install openpyxl`)
- The `excel-author` skill's recalc script for delivery validation
- Source data: company financials from SEC filings, company IR pages, or user-provided data
- Market data: current share price, diluted shares outstanding, beta, risk-free rate

## Steps

### 1. Data retrieval and validation

Fetch data from available sources (user-provided, web search, SEC EDGAR):

1. Collect: revenue, margins, shares outstanding, net debt, current stock price
2. Verify: net debt vs. net cash (critical for equity bridge)
3. Confirm: diluted shares outstanding (check for buybacks/issuances)
4. Validate: historical margin consistency with business model
5. Show the user the raw inputs block and confirm before projecting

### 2. Historical analysis (3-5 years)

Build summary tables showing:

- Revenue growth trends (CAGR, drivers)
- Margin progression (gross margin, EBIT margin, FCF margin)
- Capital intensity (D&A and CapEx as % of revenue)
- Working capital efficiency (NWC changes as % of revenue growth)
- Return metrics (ROIC, ROE trends)

### 3. Build revenue projections

1. Apply growth rates for each projection year (typically 5 years)
2. Show both dollar amounts AND calculated growth %
3. Use a consolidation column with INDEX formulas referencing scenario blocks
4. Show projected top line and growth rates — confirm with user before building margin build

**Three-scenario approach:**

- Bear: Conservative growth
- Base: Most likely scenario
- Bull: Optimistic growth

### 4. Operating expense modeling

1. Model S&M, R&D, and G&A as % of revenue (not gross profit)
2. Show operating leverage — % should decline as revenue scales
3. Calculate EBIT = Gross Profit - Total OpEx
4. Confirm FCF schedule logic with user before computing WACC

### 5. Free cash flow calculation

Build FCF in proper sequence:

```
EBIT
(-) Taxes (EBIT × Tax Rate)
= NOPAT
(+) D&A (non-cash expense, % of revenue)
(-) CapEx (% of revenue, typically 4-8%)
(-) Δ NWC (change in working capital)
= Unlevered Free Cash Flow
```

### 6. Cost of capital (WACC)

Calculate using CAPM:

- **Cost of Equity** = Risk-Free Rate + Beta × Equity Risk Premium (5.0-6.0% standard)
- **After-Tax Cost of Debt** = Pre-Tax Cost of Debt × (1 - Tax Rate)
- **WACC** = (Cost of Equity × Equity Weight) + (After-Tax Cost of Debt × Debt Weight)

Typical ranges: Large Cap/Stable 7-9%, Growth 9-12%, High Risk 12-15%.

Show calculation and inputs — confirm with user before discounting.

### 7. Discount rate application

Use mid-year convention:

- Discount periods: 0.5, 1.5, 2.5, 3.5, 4.5
- Discount Factor = 1 / (1 + WACC)^Period
- PV of FCF = Unlevered FCF × Discount Factor

### 8. Terminal value calculation

**Perpetuity Growth Method (preferred):**

```
Terminal FCF = Final Year FCF × (1 + Terminal Growth Rate)
Terminal Value = Terminal FCF / (WACC - Terminal Growth Rate)
```

Constraint: Terminal Growth < WACC (otherwise infinite value).

Terminal growth rates: Conservative 2.0-2.5% (GDP), Moderate 2.5-3.5%, Aggressive 3.5-5.0% (market leaders only).

**Exit Multiple Method (alternative):**

```
Terminal Value = Final Year EBITDA × Exit Multiple (typically 8-15x)
```

Terminal value should represent 50-70% of Enterprise Value. If >75%, model is over-reliant on terminal assumptions.

### 9. Enterprise to equity value bridge

```
(+) Sum of PV of Projected FCFs
(+) PV of Terminal Value
= Enterprise Value
(-) Net Debt [or + Net Cash if negative]
= Equity Value
÷ Diluted Shares Outstanding
= Implied Price per Share
```

### 10. Sensitivity analysis

Build three 5×5 sensitivity tables:

1. **WACC vs Terminal Growth** — Shows enterprise value sensitivity
2. **Revenue Growth vs EBIT Margin** — Impact of top-line growth and operating leverage
3. **Beta vs Risk-Free Rate** — Sensitivity to cost of equity components

Each table uses ODD dimensions (5×5) so the center cell is the base case. Center cell = model's actual implied share price (sanity check). Highlight center cell with medium blue fill `#BDD7EE` + bold font.

**Every cell must contain a full DCF recalculation formula** — no placeholder text, no linear approximations, no manual steps required. Use openpyxl loops to write formulas programmatically.

### 11. Final validation

1. Run `python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx 30`
2. Fix ALL errors until status is `success`
3. Zero formula errors required

## Model Structure

### Scenario block format (MANDATORY)

Each scenario block must have three structural elements:

1. **Section header row** (merged cells): e.g., "BEAR CASE ASSUMPTIONS"
2. **Column header row** showing projection years (e.g., FY2025E, FY2026E)
3. **Data rows** with assumption values across projection years

### Cell comments (MANDATORY)

Add cell comments AS each hardcoded value is created:

```
Source: [System/Document], [Date], [Reference], [URL if applicable]
```

Every blue input must have a comment before moving to the next section.

### Layout planning

1. Write ALL headers and labels FIRST
2. Write ALL section dividers and blank rows SECOND
3. THEN write formulas using the locked row positions
4. Test formulas immediately after creation

## Pitfalls

1. **Hardcoding computed values** — Every projection, margin, discount factor, PV, and sensitivity cell MUST be a live Excel formula. Writing `ws["D20"] = calculated_revenue` in Python is WRONG; use `ws["D20"] = "=D19*(1+$B$8)"`.
2. **Skipping step-by-step verification** — A wrong margin assumption discovered after sensitivity tables means rebuilding everything downstream. Show the user each stage.
3. **Sensitivity tables with placeholder text** — Every cell (75 total across 3 tables) must contain a full DCF recalculation formula. No empty cells, no "TODO" notes, no linear approximations.
4. **Missing cell comments on hardcoded values** — Every hardcoded input (historical actuals, assumption drivers, market data) must have a source comment. No deferred "TODO: add source".
5. **Wrong row references** — If formulas are written before headers are inserted, row references shift and point to wrong cells. Lock row layout FIRST, then write formulas.
6. **Terminal value >75% of EV** — If terminal value represents more than 75% of enterprise value, the model may be over-reliant on terminal assumptions. Check and flag.
7. **Missing scenario column headers** — Without projection year labels (FY2025E, etc.), users cannot tell which assumption corresponds to which year. This row is MANDATORY.

## Verification

1. **Center cell of sensitivity tables equals model's implied share price** — The base case cell in each table must match the valuation summary's share price exactly
2. **Balance sheet balances** — Assets = Liabilities + Equity for every period
3. **Cash ties out** — CF ending cash = BS cash for every period
4. **Recalc passes** — Run `python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx 30` with zero errors
5. **Scenario hierarchy holds** — Upside > Base > Downside for NI, EBITDA, FCF, and margins

## Cross-References

- **excel-author** — Cell coloring, named ranges, sensitivity table conventions, and recalc script
- **3-statement-model** — Financial modeling foundation that DCF builds on
- **stocks** — Source market data for share prices, beta, and shares outstanding