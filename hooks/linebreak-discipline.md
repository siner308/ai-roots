# Linebreak Discipline Hook

A `PostToolUse` hook on `Edit|Write|MultiEdit` that flags newly added Markdown lines that hard-break mid-sentence.
The rule it enforces: a hard break may fall only where a sentence ends, unless a linter or formatter errors on the width.
Breaking after every sentence is not required — a line holding several sentences is fine.

## Why it exists

The prose-style rule already forbids mid-sentence hard breaks, but it lost in practice to a stronger pull: when editing a file that is already hard-wrapped at some column, matching the incumbent style reads as good citizenship, and fresh text gets wrapped at the column limit — stranding articles from nouns and splitting parentheticals.
A resident rule competes with the whole context and loses exactly when the surrounding file models the wrong behavior.
The same failure mode made `comment-discipline` a hook.

## What it does

On every Markdown edit it scans only the added text (Write content, Edit/MultiEdit new strings — pre-existing wrapping elsewhere in the file never fires it).
A line is flagged when it ends without sentence-terminal punctuation and the next line continues the same sentence.
Findings come back as `decision: "block"` demanding the lines be re-joined so every hard break falls at a sentence boundary.

The stated exemption: a linter or formatter in the project that errors on line width — name the tool and keep the wrap.
A file's existing wrap style or the current display width does not qualify.

## What it skips

- Non-Markdown files, fenced code blocks, YAML frontmatter.
- Structural lines: headings, table rows, fence markers, `---` rules.
- A line whose successor starts a new block (heading, list item, table, blockquote, fence) — that break is a real boundary, not a wrap.

## Known limitations (reviewed, accepted)

Heuristic, not a parser: a sentence legitimately ending in an abbreviation without terminal punctuation, or deliberately split semantic-line-break styles that cut at clause boundaries, will be flagged — the verdict-style block lets the model keep them with a stated reason.
Edit fragments are only checked internally, so a fragment whose last line joins mid-sentence with unchanged file text escapes; the dominant failure (wrapping whole fresh paragraphs) is covered.
