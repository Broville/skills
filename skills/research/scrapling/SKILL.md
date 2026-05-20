---
name: scrapling
description: Web scraping with anti-bot bypass via Scrapling — HTTP fetching, stealth browser automation, Cloudflare bypass, and spider crawling via CLI and Python
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to scrape a website or extract data from web pages
  - Built-in web_extract tool returns insufficient or blocked data
  - User needs to bypass Cloudflare or bot detection on a target site
  - User wants to crawl multiple pages with link following (spider mode)
  - User asks to scrape JS-rendered or dynamic content that static fetchers miss
related_skills:
  - searxng-search
  - domain-intel
---

# Scrapling — Web Scraping with Anti-Bot Bypass

## Description

Scrapling is a web scraping framework with three fetching strategies: static HTTP, dynamic JS-rendered, and stealth/Cloudflare bypass. It provides a CLI for quick extraction and a Python API for complex scraping workflows, including a spider framework for multi-page crawling.

**This skill is for educational and research purposes only.** Users must comply with local and international data scraping laws and respect website Terms of Service. Always check `robots.txt` and the site's ToS before scraping.

## Prerequisites

- Python 3.10+
- `pip install "scrapling[all]"` then `scrapling install` (installs browser binaries)
- For minimal (HTTP-only): `pip install scrapling` (no browser needed)
- For browser automation only: `pip install "scrapling[fetchers]"` then `scrapling install`

## Steps

### 1. Extract a static page (CLI)

```bash
# Basic markdown extraction
scrapling extract get 'https://example.com' output.md

# With CSS selector and browser impersonation
scrapling extract get 'https://example.com' output.md \
  --css-selector '.content' \
  --impersonate 'chrome'
```

### 2. Extract a JS-rendered page (CLI)

```bash
scrapling extract fetch 'https://example.com' output.md \
  --css-selector '.dynamic-content' \
  --disable-resources \
  --network-idle
```

### 3. Extract a Cloudflare-protected page (CLI)

```bash
scrapling extract stealthy-fetch 'https://protected-site.com' output.html \
  --solve-cloudflare \
  --block-webrtc \
  --hide-canvas
```

### 4. POST request (CLI)

```bash
scrapling extract post 'https://example.com/api' output.json \
  --json '{"query": "search term"}'
```

### 5. HTTP scraping (Python)

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
for q in quotes:
    print(q)
```

### 6. Session with persistent cookies (Python)

```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    page = session.get('https://example.com/', stealthy_headers=True)
    links = page.css('a::attr(href)').getall()
    for link in links[:5]:
        sub = session.get(link)
        print(sub.css('h1::text').get())
```

### 7. Dynamic page scraping with JS rendering (Python)

```python
from scrapling.fetchers import DynamicFetcher

page = DynamicFetcher.fetch('https://example.com', headless=True)
data = page.css('.js-loaded-content::text').getall()
```

### 8. Stealth mode for anti-bot bypass (Python)

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://protected-site.com',
    headless=True,
    solve_cloudflare=True,
    block_webrtc=True,
    hide_canvas=True,
)
content = page.css('.protected-content::text').getall()
```

### 9. Spider crawling (Python)

```python
from scrapling.spiders import Spider, Request, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10
    download_delay = 1

    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
                "tags": quote.css('.tag::text').getall(),
            }
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

result = QuotesSpider().start()
print(f"Scraped {len(result.items)} quotes")
```

## Pitfalls

1. **Browser install required** — Run `scrapling install` after pip install. Without it, `DynamicFetcher` and `StealthyFetcher` will fail with a missing browser error.
2. **Timeout units differ** — `DynamicFetcher` and `StealthyFetcher` timeouts are in **milliseconds** (default 30000), while `Fetcher` timeouts are in **seconds**. Mixing these up causes silent timeouts or hangs.
3. **Cloudflare bypass adds latency** — `solve_cloudflare=True` adds 5-15 seconds per fetch. Only enable when actually needed.
4. **Resource usage** — `StealthyFetcher` runs a real browser. Limit concurrent usage to avoid memory exhaustion on constrained systems.
5. **Legal and ethical considerations** — Always check `robots.txt` and website ToS before scraping. Respect rate limits. This tool is for educational and research purposes. Scraping personal data, copyrighted content behind paywalls, or circumventing authentication may violate laws.

## Verification

1. **CLI works**: Run `scrapling extract get 'https://quotes.toscrape.com/' /tmp/quotes_test.md` and confirm it creates a non-empty markdown file at `/tmp/quotes_test.md`.
2. **Python works**: Run the Fetcher example from Step 5 and confirm it prints quote texts from quotes.toscrape.com.
3. **Browser installed**: Run `scrapling install` and confirm no error — then test a DynamicFetcher fetch on a simple JS-rendered page.