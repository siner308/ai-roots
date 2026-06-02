# When agent-browser Is Blocked, Search Instead of Escalating the Engine

A live browser fetch (`agent-browser`, either lightpanda or chrome) renders the actual page, so it inherits every anti-bot defense the site runs — Cloudflare challenges, lazy-loaded charts, SPA shells that never put the number into `body` text. A search tool (`WebSearch`, or Codex's `--search` web_search) does NOT render the page. It reads the search engine's already-indexed snippet. That is why search walks straight past blocks that no browser engine can defeat: the two tools fail for completely different reasons, so they are not a "try harder" ladder — they are different mechanisms.

The mistake is treating them as a ladder: lightpanda → chrome → another URL on the same domain → give up. Every rung there is still *live rendering*, so every rung hits the same wall.

## What actually happened

Fact-checking an ARM/RISC-V analysis, two numbers had to be confirmed: ARM's China revenue share and the RISC-V 2030 chip-shipment forecast.

- **The failing approach (live rendering, repeated):** `agent-browser --engine lightpanda` on SHD Group and `riscv.org/exchange` returned empty bodies. Switched to chrome — still empty. Tried Google, Bing, and DuckDuckGo HTML search pages *through agent-browser* — they returned mangled/encoded garbage because the engine couldn't run the result JS. Guessed alternate article URLs — 404s. Four-plus attempts, both numbers logged as "research failed."
- **The working approach (non-rendering search):** the same task handed to Codex `--search -a never exec --sandbox read-only` used its built-in `web_search` tool. Its log showed queries like `Arm Holdings annual report 2025 gross margin revenue ... 20-F` and `RISC-V chips forecasted by 2030`. The snippets carried the figures directly: **ARM China ≈16% of revenue (FY2026 20-F)** and **>16 billion RISC-V chips forecast by 2030 (RISC-V International / SHD Group)** — even surfacing the primary SEC filing URL.

Codex had no secret crawling technique. It used a search tool instead of a browser. The same bypass was available to the main session via `WebSearch` the whole time; the existing protocol just buried `WebSearch` at priority 3 and told the agent not to "wait for WebSearch to fail first" — which got mis-read as "keep using the browser."

## The rule

When `agent-browser` shows a block signal — empty/broken body, Cloudflare "Just a moment", the wanted figure absent from `body` text, HTTP 4xx/5xx, 3 consecutive timeouts, or a search-engine result page that renders as garbage — **stop escalating the browser engine and switch to a search-based tool.** Put the exact figure you need into the search query; the snippet often answers without any page load.

Reserve the chrome engine for pages that are *renderable but heavy and need interaction* (filters, login, forms), and for **official primary docs** (SEC EDGAR, DART, regulator/issuer IR) where the data exists nowhere else so a harder fetch is justified. For secondary/aggregator data, another search query or another aggregator beats chrome.

## Signals this lesson applies

- A market-research, financial-aggregator, government-filing, or search-engine page returns empty/blocked content under agent-browser.
- You are about to retry the same blocked URL with a different browser engine, or guess sibling URLs on the same domain.
- A needed number is "behind a chart" — present visually but absent from extracted `body` text.

In all three: switch to search. See the protocol in `web-research.md` §"Block-signal → search fallback".
