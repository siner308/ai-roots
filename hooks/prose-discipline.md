# Prose Discipline Hook

A `PostToolUse` hook on `Edit|Write|MultiEdit` that governs prose hygiene in non-code files (Markdown).
It enforces two things: hard breaks fall at meaning boundaries, and a substantial prose addition earns a conciseness re-check.

## Why it exists

The prose-style rule already covers both concerns, but a resident rule competes with the whole context and loses — the same reason `comment-discipline` became a hook.
Two failure modes recur.
When editing a file already hard-wrapped at some column, matching the incumbent style reads as good citizenship, and fresh text gets wrapped at the limit — stranding articles from nouns and splitting parentheticals.
And prose accretes: each added sentence feels justified in isolation, so docs drift toward rambling that no single edit owns.

## Scope: non-code prose, not code comments

This hook covers Markdown.
The same two concerns for **code comments** live in the [`comment-discipline`](comment-discipline) hook: that one fires on every comment an edit adds, and folds its own line-break check into that handoff.
Splitting the two media across two hooks means a code edit triggers only `comment-discipline` and a Markdown edit only this one — they never double-fire.
Line-break detection here stays static because a punctuation-based check is language-agnostic enough for Markdown (a Korean sentence still ends on `다.`/`요.`).

## What it does

On every Markdown edit it scans only the added text (Write content, Edit/MultiEdit new strings — pre-existing prose elsewhere never fires it), and can emit either or both of:

- **line breaks** — a line is flagged when it ends without sentence-terminal punctuation and the next line continues the same sentence. The block asks for the lines to be re-joined so every hard break falls at a sentence boundary. A line holding several sentences is fine; breaking after a sentence is allowed, never required. The one exemption is a project linter or formatter that errors on line width — name it and keep the wrap.
- **conciseness** — once the added prose passes a sentence-count gate (`CONCISE_SENTENCE_GATE`, default 6), the block asks the model to re-read it as a skeptical editor and cut sentences that restate a neighbor, state the obvious, or hedge. A doc is expected to hold prose, so the instruction is trim, not the delete-by-default that `comment-discipline` applies to comments. Conciseness cannot be judged statically, so the gate only decides *when* to ask; the model makes the call, which is why it works in any language.

## What it skips

- Non-Markdown files (code goes to `comment-discipline`; everything else is ignored).
- Fenced code blocks and YAML frontmatter.
- Structural lines: headings, table rows, fence markers, `---` rules — for both the break check and the sentence count.
- A line whose successor starts a new block (heading, list item, table, blockquote, fence) — that break is a real boundary, not a wrap.

## Known limitations (reviewed, accepted)

Heuristic, not a parser.
A sentence legitimately ending in an abbreviation without terminal punctuation, or a deliberate semantic-line-break style, will be flagged — the verdict-style block lets the model keep it with a stated reason.
The sentence count keys on terminal punctuation, so an abbreviation like `e.g.` nudges it up and a period-less style nudges it down; the gate is a rough volume signal, not an exact count.
Edit fragments are only checked internally, so a fragment whose last line joins mid-sentence with unchanged file text escapes; the dominant failure (wrapping or dumping whole fresh paragraphs) is covered.
