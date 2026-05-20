---
name: osint-investigation
description: Public-records OSINT investigation framework — SEC EDGAR, USAspending, Senate lobbying, OFAC sanctions, ICIJ offshore leaks, NYC ACRIS property, OpenCorporates, CourtListener, Wayback Machine, GDELT news — entity resolution, cross-link analysis, timing correlation, evidence chains
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to "follow the money" or investigate government contracts, lobbying, or sanctions
  - User wants corporate due diligence — who controls a company, where it is incorporated, board members, filings
  - User asks about sanctions screening, offshore leaks, or pay-to-play patterns
  - User wants to find property records, court records, or web archives for an entity
  - User requests multi-source entity resolution with confidence scoring
  - User asks "what's been said about X" in news or Wikipedia
related_skills:
  - sherlock
  - searxng-search
---

# OSINT Investigation — Public Records Cross-Reference

## Description

Investigative framework for public-records OSINT: government contracts, corporate filings, lobbying, sanctions, offshore leaks, property records, court records, web archives, knowledge bases, and global news. Resolve entities across heterogeneous sources, build cross-links with explicit confidence, run statistical timing tests, and produce structured evidence chains.

**Python stdlib only.** Zero install. Most sources work with no API key (OpenCorporates has an optional free token that raises rate limits).

## Prerequisites

- Python 3.8+ (stdlib only: `urllib.request`, `json`, `csv`, `concurrent.futures`)
- Internet access for public records APIs
- Optional environment variables for higher rate limits:
  - `SEC_USER_AGENT` — SEC EDGAR polite user-agent string
  - `SENATE_LDA_TOKEN` — Senate lobbying API token
  - `OPENCORPORATES_API_TOKEN` — OpenCorporates free API token
  - `COURTLISTENER_TOKEN` — CourtListener API token

## Steps

### 1. Identify which sources apply

Read the data-source reference entries to plan the investigation:

```bash
ls SKILL_DIR/references/sources/

# Federal financial / regulatory
cat SKILL_DIR/references/sources/sec-edgar.md
cat SKILL_DIR/references/sources/usaspending.md
cat SKILL_DIR/references/sources/senate-ld.md
cat SKILL_DIR/references/sources/ofac-sdn.md
cat SKILL_DIR/references/sources/icij-offshore.md

# Identity / property / litigation / archives / news
cat SKILL_DIR/references/sources/nyc-acris.md
cat SKILL_DIR/references/sources/opencorporates.md
cat SKILL_DIR/references/sources/courtlistener.md
cat SKILL_DIR/references/sources/wayback.md
cat SKILL_DIR/references/sources/wikipedia.md
cat SKILL_DIR/references/sources/gdelt.md
```

### 2. Acquire data

Each source has a stdlib-only fetch script in `SKILL_DIR/scripts/`:

**Federal financial / regulatory:**

```bash
# SEC EDGAR filings (corporate disclosures)
python3 SKILL_DIR/scripts/fetch_sec_edgar.py --cik 0000320193 \
    --types 10-K,10-Q --out data/edgar_filings.csv

# USAspending federal contracts
python3 SKILL_DIR/scripts/fetch_usaspending.py --recipient "EXAMPLE CORP" \
    --fy 2024 --out data/contracts.csv

# Senate LD-1 / LD-2 lobbying disclosures
python3 SKILL_DIR/scripts/fetch_senate_ld.py --client "EXAMPLE CORP" \
    --year 2024 --out data/lobbying.csv

# OFAC SDN sanctions list (full snapshot)
python3 SKILL_DIR/scripts/fetch_ofac_sdn.py --out data/ofac_sdn.csv

# ICIJ Offshore Leaks (downloads ~70 MB bulk CSV on first use, cached 30 days)
python3 SKILL_DIR/scripts/fetch_icij_offshore.py --entity "EXAMPLE CORP" \
    --out data/icij.csv
```

**Identity / property / litigation / archives / news:**

```bash
# NYC property records (ACRIS via Socrata)
python3 SKILL_DIR/scripts/fetch_nyc_acris.py --name "SMITH, JOHN" \
    --out data/acris.csv
python3 SKILL_DIR/scripts/fetch_nyc_acris.py --address "571 HUDSON" \
    --out data/acris_addr.csv

# OpenCorporates — 130+ jurisdiction corporate registry
python3 SKILL_DIR/scripts/fetch_opencorporates.py --query "Example Corp" \
    --jurisdiction us_ny --out data/opencorporates.csv

# CourtListener — federal + state court opinions
python3 SKILL_DIR/scripts/fetch_courtlistener.py --query "Smith v. Example Corp" \
    --type opinions --out data/courts.csv

# Wayback Machine — historical web captures
python3 SKILL_DIR/scripts/fetch_wayback.py --url "example.com" \
    --match host --collapse digest --out data/wayback.csv

# Wikipedia + Wikidata — narrative bio + structured facts
python3 SKILL_DIR/scripts/fetch_wikipedia.py --query "Bill Gates" \
    --out data/wp.csv

# GDELT — global news in 100+ languages
python3 SKILL_DIR/scripts/fetch_gdelt.py --query '"Example Corp"' \
    --timespan 1y --out data/gdelt.csv
```

All outputs are normalized CSV with a header row. Scripts are idempotent — re-run safely.

### 3. Resolve entities across sources

Normalize names and find matches between two CSV files:

```bash
python3 SKILL_DIR/scripts/entity_resolution.py \
    --left  data/lobbying.csv   --left-name-col  client_name \
    --right data/contracts.csv  --right-name-col recipient_name \
    --out data/cross_links.csv
```

Three matching tiers with explicit confidence:
- **exact** — Normalized strings equal after suffix/punctuation strip → high confidence
- **fuzzy** — Sorted-token equality (word-bag match) → medium confidence
- **token_overlap** — ≥60% token overlap, ≥2 shared tokens, tokens ≥4 chars → low confidence

### 4. Statistical timing correlation (optional)

Test whether two time series cluster suspiciously close together using a permutation test:

```bash
python3 SKILL_DIR/scripts/timing_analysis.py \
    --donations data/lobbying.csv --donation-date-col filing_date \
        --donation-amount-col income --donation-donor-col client_name \
        --donation-recipient-col registrant_name \
    --contracts data/contracts.csv --contract-date-col award_date \
        --contract-vendor-col recipient_name \
    --cross-links data/cross_links.csv \
    --permutations 1000 \
    --out data/timing.json
```

### 5. Build the findings JSON (evidence chain)

```bash
python3 SKILL_DIR/scripts/build_findings.py \
    --cross-links data/cross_links.csv \
    --timing data/timing.json \
    --out data/findings.json
```

Every finding has `id, title, severity, confidence, summary, evidence[], sources[]`. Each evidence item points back to a specific row in a source CSV.

## Pitfalls

1. **Entity resolution produces candidates, NOT conclusions** — A `fuzzy` match between "ACME LLC" and "Acme Holdings Group" is a lead, not a fact. Always communicate confidence tiers to the user.
2. **Statistical significance ≠ wrongdoing** — A p-value < 0.05 means the timing pattern is unlikely under the null hypothesis. It does NOT establish corruption or causation.
3. **Rate limits are real** — Scripts surface 429 responses immediately. If hitting rate limits, set environment variables for API tokens or add delays between requests.
4. **Public records can be stale or inaccurate** — Some sources have delays (SEC filings lag weeks), redactions (GDPR), or errors (ICIJ data may be incomplete).
5. **WHOIS/port 43 may be blocked** — Some networks block outbound TCP 43. Consider a VPN or alternative network if WHOIS queries fail.

## Verification

1. **Fetch works**: Run `python3 SKILL_DIR/scripts/fetch_sec_edgar.py --cik 0000320193 --out /tmp/test_edgar.csv` and confirm it produces a non-empty CSV with Apple Inc. filing data.
2. **Entity resolution works**: Run `python3 SKILL_DIR/scripts/entity_resolution.py` with two small CSV files and confirm it produces a cross_links.csv with correct match_type, confidence, and normalized name columns.
3. **Evidence chain is traceable**: Verify that each row in findings.json references a specific source CSV row, and the chain can be manually followed back to the original public record.