---
name: web-research
description: "Apply when browsing the web, extracting page content, scraping data, or fetching figures from sites — choosing between agent-browser (lightpanda default, chrome for heavy/interactive pages), WebSearch for discovery, and the insane-search skill for retrieving blocked content. Also apply the moment agent-browser returns blocked/empty/dynamic content and you are tempted to retry with another engine or guess sibling URLs — stop escalating the browser and switch to a search-based tool. Codex --search is the GPT-dependent last resort for cross-provider verification only."
---

# Web Research Protocol

**Default tool for web browsing is `agent-browser`, not WebSearch/WebFetch.** Use agent-browser proactively for any task that involves visiting websites, extracting data, or interacting with web pages. Reach for it from the start, ahead of WebSearch.

**But the inverse is also a trap:** when a page is bot-blocked or fully dynamic, `agent-browser` cannot win by trying harder. The moment you see block signals, stop escalating the browser engine and switch to a search-based tool — see "Block-signal → search fallback" below. This is the single most common way web research stalls.

## Tool Priority

| Priority | Tool | When to use |
|----------|------|-------------|
| 1 (default render) | `agent-browser --engine lightpanda` | All web browsing. 10x faster, 10x less memory than Chrome. Use for page content extraction, data scraping, reading articles, fetching structured data |
| 2 (heavy render) | `agent-browser` (chrome engine) | When lightpanda fails on a page that is *renderable but heavy, not blocked* — complex JS interactions, login flows, form submissions with dynamic validation, screenshots |
| 3 (discovery) | `WebSearch` | **Keyword → URL or fact.** Reads the index without rendering, so it also walks past Cloudflare / SPA walls. Often step 1 — and it's what feeds a URL to the retrieval lane below. Not demotable. |
| 4 (blocked-content retrieval) | **insane-search** skill (`python3 -m engine <url>`) | **When you need the actual content of a blocked, known URL — not a snippet.** Auto Phase 0→3 (official API → curl_cffi TLS impersonation → internal JSON API → real browser), no external LLM. Promote ABOVE chrome the moment block signals appear (see below). |
| 5 (last resort — verify) | Codex `--search` | Cross-provider figure extraction / verification over hard primary docs. The only GPT-dependent lane; reach for it last, for verification passes, not first-line lookups. |
| 6 (last resort — static) | `WebFetch` | Only when agent-browser is unavailable and the page is static HTML |

## Block-signal → search fallback (the key rule)

`agent-browser` (either engine) renders the live page, so it inherits every anti-bot defense the site has. Searching does NOT render the page — it reads the search engine's already-indexed snippet. The two tools fail for completely different reasons, so they are **not a "try harder" ladder — they are different mechanisms**. That difference is why search bypasses blocks that no browser engine can defeat.

**Block signals — when ANY of these appear, stop escalating the browser and switch to search:**
- Empty / broken `body` text, or a "Just a moment…" / Cloudflare challenge string
- The number you want is absent from `body` text (it's behind a chart or lazy-loaded JS)
- HTTP 4xx/5xx, or 3 consecutive timeouts
- A search-engine page itself returns mangled/encoded garbage (engine couldn't run its result JS)

**Do NOT** respond to a block by: switching lightpanda→chrome and retrying the same blocked URL, guessing alternate URLs on the same blocked domain, or looping the same fetch 3+ times. Those repeat the failure. The block is on *live rendering*; only a non-rendering path (search) gets around it.

**Sites where this fires most:** market-research firms, financial aggregators (Yahoo Finance, Bloomberg, MarketBeat, Morningstar), government filings (SEC EDGAR, DART), and the search engines' own result pages (Google/Bing/DuckDuckGo HTML often won't render snippets under lightpanda).

**Concrete escalation order for a hard-to-fetch number:**
1. `agent-browser --engine lightpanda` on the source page.
2. Block signal + you just need a value → `WebSearch` with a keyword query that embeds the exact figure you need (e.g. `<company> annual report <segment> revenue percent <year>`). Read the snippet; it often contains the number outright.
3. Block signal + you need the page's full content → the **insane-search** skill (it auto-triggers on block signals; `python3 -m engine "<url>"`). It tries the official API, TLS impersonation, and the site's internal JSON API before any browser — the no-render path that gets the real content, not a snippet.
4. Still missing, and the source is an **official primary doc** (SEC/DART/regulator/issuer IR)? → chrome engine on that *primary* URL is worth it (the data exists nowhere else). For aggregator/secondary data, prefer another search query or another aggregator over chrome.
5. Last resort, only when a cross-provider check is warranted: Codex `--search -a never exec --sandbox read-only` runs the same web_search tool and is good at pulling figures out of primary filings — but it is heavier and the only GPT-dependent lane; reach for it for verification, not first-line lookups.

This protocol applies to every research lane — news, filings, analyst data, market-research forecasts.

### The lesson behind the rule

This fallback was learned the hard way. Fact-checking an analysis, two hard figures (a company's regional revenue share from its annual filing, and an industry-body shipment forecast) had to be confirmed:

- **The failing approach (live rendering, repeated):** lightpanda on the source pages returned empty bodies. Switching to chrome — still empty. Google/Bing/DuckDuckGo result pages fetched *through agent-browser* returned mangled garbage (the engine couldn't run the result JS). Guessing alternate article URLs — 404s. Four-plus attempts, both numbers logged as "research failed." Every rung was still *live rendering*, so every rung hit the same wall.
- **The working approach (non-rendering search):** the same task run through a search tool put the exact figures in the query and read them straight out of the indexed snippets — which even surfaced the primary filing URL.

There was no secret crawling technique. A search tool was used instead of a browser. The same bypass had been available the whole time; the protocol had just buried `WebSearch` low and over-emphasized "agent-browser is default," which got mis-read as "keep using the browser."

## Blocked but you need the full content — delegate to insane-search

Search bypasses a block but only returns the *indexed snippet*. When you need the **actual page content** of a blocked site — a full Reddit thread, an X timeline, a product page — don't render it live (the browser inherits the block), and don't reach for Codex `--search` (that's the GPT lane, and it still returns snippets). Hand the URL to the **insane-search** skill, installed separately as a marketplace plugin. It retrieves blocked content with no external LLM and auto-triggers on block signals (403/402/WAF, X/Reddit/YouTube/Naver/Coupang/LinkedIn, etc.); if it hasn't fired, invoke it.

Its entrypoint is `python3 -m engine "<url>"`, which runs a Phase 0→3 escalation: official no-auth API first (Reddit `.rss`, X syndication, HN, `yt-dlp`, arXiv, …), then a WAF-product-driven TLS-impersonation grid (`curl_cffi`), then internal-JSON-API discovery, then a real browser — validating against challenge markers rather than trusting HTTP 200. Its own SKILL.md (rules R1–R7) drives the agent side; let it. Access public content only — it stops at auth walls and paywalls.

**If insane-search is not installed**, the same ideas by hand, in order:
- **Official public API** (no-auth, never WAF-challenged): Reddit `https://www.reddit.com/r/<sub>/.rss` (the `.json` path is blocked), X `cdn.syndication.twimg.com/tweet-result?id=<id>&token=a`, HN `hacker-news.firebaseio.com/v0/...`, media via `yt-dlp --dump-json <url>`, plus arXiv / Wikipedia REST / GitHub `gh` / Bluesky / Mastodon / Stack Overflow public APIs.
- **TLS impersonation**: `python3 -c "import curl_cffi" 2>/dev/null || pip install -q "curl_cffi>=0.15.0"`, then `r.get('<url>', impersonate='safari')`. If challenged, rotate `chrome`/`safari_ios`/`firefox` and try the `m.` mobile subdomain — a different identity, not the same one harder.
- **Internal API**: open once in `agent-browser` (chrome), find `/api`·`/graphql`·`.json` calls, fetch that endpoint directly.
- **200 ≠ success**: reject a body under ~3KB or carrying `Just a moment…`, `Access Denied`, `DataDome`, `Attention Required` — a 200 is where you *start* validating, not where you stop.

> insane-search is MIT-licensed ([`fivetaku/insane-search`](https://github.com/fivetaku/insane-search)). The manual fallback above is the same approach distilled, for when the plugin isn't present.

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
