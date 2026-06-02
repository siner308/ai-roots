# Web Research Protocol

**Default tool for web browsing is `agent-browser`, not WebSearch/WebFetch.** Use agent-browser proactively for any task that involves visiting websites, extracting data, or interacting with web pages. Don't wait for WebSearch to fail first.

**But the inverse is also a trap:** when a page is bot-blocked or fully dynamic, `agent-browser` cannot win by trying harder. The moment you see block signals, stop escalating the browser engine and switch to a search-based tool — see "Block-signal → search fallback" below. This is the single most common way web research stalls.

## Tool Priority

| Priority | Tool | When to use |
|----------|------|-------------|
| 1 (default) | `agent-browser --engine lightpanda` | All web browsing. 10x faster, 10x less memory than Chrome. Use for page content extraction, data scraping, reading articles, fetching structured data |
| 2 (fallback) | `agent-browser` (chrome engine) | When lightpanda fails on a page that is *renderable but heavy* — complex JS interactions, login flows, form submissions with dynamic validation, screenshots |
| 3 (block-bypass) | `WebSearch`, or Codex `--search` web-research mode | **When the page is bot-blocked or its data lives in dynamic JS that neither engine renders.** Search indexes return snippets without rendering the page, so they walk straight past Cloudflare / SPA walls. Promote this ABOVE chrome the moment block signals appear (see below). |
| 4 (last resort) | `WebFetch` | Only when agent-browser is unavailable and the page is static HTML |

## Block-signal → search fallback (the key rule)

`agent-browser` (either engine) renders the live page, so it inherits every anti-bot defense the site has. Searching does NOT render the page — it reads the search engine's already-indexed snippet. That difference is why search bypasses blocks that no browser engine can.

**Block signals — when ANY of these appear, stop escalating the browser and switch to search:**
- Empty / broken `body` text, or a "Just a moment…" / Cloudflare challenge string
- The number you want is absent from `body` text (it's behind a chart or lazy-loaded JS)
- HTTP 4xx/5xx, or 3 consecutive timeouts
- A search-engine page itself returns mangled/encoded garbage (engine couldn't run its result JS)

**Do NOT** respond to a block by: switching lightpanda→chrome and retrying the same blocked URL, guessing alternate URLs on the same blocked domain, or looping the same fetch 3+ times. Those repeat the failure. The block is on *live rendering*; only a non-rendering path (search) gets around it.

**Sites where this fires most:** market-research firms (SHD Group, Gartner-style), financial aggregators (Yahoo Finance, Bloomberg, MarketBeat, Morningstar), government filings (SEC EDGAR, DART), and the search engines' own result pages (Google/Bing/DuckDuckGo HTML often won't render snippets under lightpanda).

**Concrete escalation order for a hard-to-fetch number:**
1. `agent-browser --engine lightpanda` on the source page.
2. Block signal? → `WebSearch` with a keyword query that embeds the exact figure you need (e.g. `Arm Holdings 20-F China revenue percent 2026`). Read the snippet; it often contains the number outright.
3. Still missing, and the source is an **official primary doc** (SEC/DART/regulator/issuer IR)? → chrome engine on that *primary* URL is worth it (the data exists nowhere else). For aggregator/secondary data, prefer another search query or another aggregator over chrome.
4. If a cross-provider check is already warranted, Codex `--search -a never exec --sandbox read-only` runs the same web_search tool and is excellent at pulling figures out of primary filings — but it is heavier; reach for it for verification passes, not first-line lookups.

This protocol applies to every research lane — news, filings, analyst data, market-research forecasts. The lesson behind it: `lessons-web-fetch-block-then-search.md`.

## Lightpanda First

Always try lightpanda first. It handles most static and semi-dynamic pages perfectly:

```bash
# Default pattern — lightpanda for fast content extraction
agent-browser --engine lightpanda open <url> && agent-browser --engine lightpanda wait --load networkidle && agent-browser --engine lightpanda get text body

# Set env var to avoid repeating --engine flag
export AGENT_BROWSER_ENGINE=lightpanda
agent-browser open <url> && agent-browser wait --load networkidle && agent-browser get text body
```

**Switch to chrome engine when** the page is renderable-but-heavy (NOT when it's bot-blocked — that's the search fallback above):
- Page returns empty/broken content with lightpanda because of a heavy SPA you still need to *interact* with
- Need to interact with forms, dropdowns, or dynamic UI
- Need screenshots or visual verification
- Need to use --extension, --profile, --state, or --allow-file-access

## Common Patterns

### Data extraction (articles, reviews, documentation)
```bash
agent-browser --engine lightpanda open <url>
agent-browser --engine lightpanda wait --load networkidle
agent-browser --engine lightpanda get text body
```

### Interactive research (filtering, pagination, login)
```bash
agent-browser open <url> && agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser fill @ref "value"
agent-browser click @ref
agent-browser snapshot -i  # Re-snapshot after interaction
```

### Bulk data collection (multiple pages)
```bash
# Use lightpanda for speed when scraping multiple URLs
export AGENT_BROWSER_ENGINE=lightpanda
for url in url1 url2 url3; do
  agent-browser open "$url" && agent-browser wait --load networkidle && agent-browser get text body > "output_$i.txt"
done
```

### Hard-to-fetch numbers (blocked aggregators, filings)
```bash
# 1) try the page; 2) on a block signal, switch to search with the figure in the query
WebSearch: "<entity> <metric> <unit/year>"   # snippet often carries the number
# for primary filings (SEC/DART), chrome on the primary URL is the justified escalation
```

### Real estate research (네이버 부동산, 호갱노노, KB부동산)
These are JS-heavy SPAs you must interact with — use chrome engine:
1. `agent-browser open <url>` (chrome engine)
2. Apply filters via snapshot + fill/click
3. Snapshot to extract data
4. Scroll and re-snapshot for pagination

## Chrome DevTools MCP

Use as secondary option when agent-browser has issues with complex JS-heavy pages, or for advanced debugging (network inspection, performance profiling).
