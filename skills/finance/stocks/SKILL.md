---
name: stocks
description: Read-only stock market data via Yahoo Finance — quote, search, history, compare, and crypto prices with no API key required
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks for a current stock price or ticker quote
  - User wants to look up a ticker symbol by company name
  - User requests OHLCV history or performance over a date range
  - User wants to compare several tickers side by side
  - User asks for cryptocurrency prices (BTC, ETH, SOL, etc.)
related_skills:
  - dcf-model
  - 3-statement-model
---

# Stocks

## Description

Read-only market data via Yahoo Finance. Five commands: quote, search, history, compare, crypto. Python stdlib only — no API key, no pip installs. Yahoo's endpoint is unofficial and may rate-limit or change.

## Prerequisites

- Python 3.8+ (stdlib only, no pip dependencies)
- Internet access for Yahoo Finance endpoints
- Optional: `ALPHA_VANTAGE_KEY` environment variable to enrich `market_cap`, `pe_ratio`, and 52-week levels when Yahoo's crumb-protected fields return null. Free key at <https://www.alphavantage.co/support/#api-key>

## Steps

### 1. Install and run the stocks client

```bash
SCRIPT=~/.hermes/skills/finance/stocks/scripts/stocks_client.py
python3 $SCRIPT quote AAPL
```

All output is JSON on stdout — pipe through `jq` for slicing.

### 2. Quote — Get current price and summary

```bash
python3 $SCRIPT quote AAPL
python3 $SCRIPT quote AAPL MSFT GOOGL TSLA
```

Returns: current price, change, change%, volume, 52-week high/low.

### 3. Search — Find tickers by company name

```bash
python3 $SCRIPT search "Tesla"
```

Returns top 5: symbol, name, exchange, type.

### 4. History — Daily OHLCV plus stats

```bash
python3 $SCRIPT history NVDA --range 6mo
```

Ranges: `1mo`, `3mo`, `6mo`, `1y`, `5y`. Default: `1mo`. Returns min, max, avg, total return %.

### 5. Compare — Side-by-side ticker comparison

```bash
python3 $SCRIPT compare AAPL MSFT GOOGL
```

Returns: price, change%, 52-week performance for each symbol.

### 6. Crypto — Cryptocurrency prices

```bash
python3 $SCRIPT crypto BTC ETH SOL
```

Pass the base symbol (e.g., `BTC`); the script appends `-USD` automatically.

## Pitfalls

1. **Yahoo Finance API is unofficial** — Endpoints can change or rate-limit without notice. If requests start failing, that is why; consider falling back to Alpha Vantage when Yahoo is down.
2. **`market_cap` and `pe_ratio` may return null** — When Yahoo's crumb session is not established, these fields come back empty. Set `ALPHA_VANTAGE_KEY` environment variable to backfill them.
3. **Rate limiting on bulk requests** — Add a small delay (e.g., `sleep 1`) between sequential requests to avoid being blocked by Yahoo's rate limiter.
4. **This is read-only** — No order placement, no account integration, no trading functionality.
5. **Crypto symbol formatting** — Pass `BTC` not `BTC-USD`; the script handles the suffix automatically.

## Verification

1. **Quote returns valid JSON**: Run `python3 ~/.hermes/skills/finance/stocks/scripts/stocks_client.py quote AAPL` and confirm the output is valid JSON containing `symbol: "AAPL"` and a numeric `price` field.

## Cross-References

- **dcf-model** — DCF valuation for equity analysis using stock prices as inputs
- **3-statement-model** — Financial modeling that pairs with stock data