# Prose Style

How writing reaches the reader comes down to two separate choices: the *words* inside a sentence, and *where the lines are cut*. Both can quietly turn clear thinking into machine-looking output, and they fail in different ways — so this rule covers both.

The internal thinking rule (`thinking-expansion`) deliberately pulls in domain terminology and cross-domain keywords to broaden retrieval — but those words are for *thinking*, not for *output*. They leak into sentences easily, producing dense noun-stacks and translated-English phrasing that read as machine output rather than human speech. This rule is the output-side counterweight: no matter how much terminology the thinking step activated, the prose that reaches the user stays plain, and it breaks where the meaning pauses.

## Plain language

### What to avoid

- **Abstract-noun stacks** — chains of `-tion`/`-성`/`-화` nouns joined by particles or prepositions. EN: "the minimization of operational burden through the acquisition of observability". KO: "관찰 가능성 확보를 통한 운영 부담의 최소화". Both are four abstract nouns pretending to be a sentence.
- **Translated-English rhythm** — "~을 통한", "~에 대한", "~의 관점에서" piled up where a verb would do. If it reads like a literal translation of English, rewrite it as something you'd actually say.
- **Gratuitous concept citation** — naming a principle (Goodhart's Law, backpressure, idempotency) when a plain sentence carries the same point. Cite a concept only when the name itself earns its place for the reader, not as decoration.
- **Density theater** — packing jargon to *look* informative. High word-density is not the same as high information.

### What to do instead

- Use verbs over nominalizations. EN: "Cache it so requests come back faster" beats "utilization of caching for latency reduction". KO: "로그를 잘 남겨두면 나중에 덜 고생해요" beats "로깅을 통한 운영 효율성 증대".
- Write the sentence you'd say out loud to a colleague, then keep that.
- Keep technical terms when they are the precise word (`idempotent`, `deadlock`, `index`) — plainness is about rhythm and noun-stacking, not about dumbing down vocabulary.
- Match the user's language and register.

### Examples

These accumulate over time — add a ❌/✅ pair whenever a phrasing actually grated, tagged with the language it appeared in. Translationese is language-specific: `묵음 dedup` only reads as broken in Korean (a literal mistranslation of an English term), so examples are filed under the language where they bite, not translated across.

| Lang | ❌ | ✅ |
|------|----|----|
| EN | utilization of caching for latency reduction | cache it so requests come back faster |
| KO | 관찰 가능성 확보를 통한 운영 부담의 최소화 | 로그를 잘 남겨두면 나중에 운영할 때 덜 고생해요 |
| KO | `Create`의 묵음 dedup | `Create`는 중복이 들어와도 에러 없이 조용히 무시해요 |

### Scope — two axes, applied separately

Plain language itself splits into two independent axes. Conflating them is what makes "plain language everywhere" feel excessive.

- **Word choice** (no abstract-noun stacks, no translationese, verbs over nominalizations) — applies **everywhere prose appears**, including table cells, headings, and bullet labels. A table cell is not an excuse for "관찰 가능성 확보를 통한 운영 부담의 최소화".
- **Spoken rhythm** (full sentences as you'd say them aloud) — applies **only to conversational and explanatory prose**. Structured artifacts keep their own register; do not force them into spoken style.

| Target | Word choice (no noun-stacks / translationese) | Spoken rhythm |
|--------|:---:|:---:|
| Conversational / explanatory prose | ✅ | ✅ |
| Table cells, headings, bullet labels | ✅ | ❌ — terse phrases/fragments are fine |
| Code, identifiers, commit messages, PR bodies, quoted errors/specs | own convention wins | ❌ |

PR bodies are governed by the `github-pr-markdown` skill; defer to it there rather than applying spoken rhythm.

## Line breaks follow meaning

A hard line break reads as a boundary. The reader treats the end of a line as a small pause — a place where one thought finishes and the next begins. So when you control where a line breaks, the break carries meaning whether you intend it to or not.

The common failure is breaking wherever a column limit happens to land. That drops a boundary into the middle of a phrase, and the reader has to undo it — re-joining a list item with the sibling stranded on the next line, or a topic word with the predicate that follows it. The text still parses, but every mid-phrase break costs a beat.

### Where this applies

Only where the break is yours to place and a real width limit forces one — code comments, commit message bodies, fixed-width text. Soft-wrapping prose (Markdown, chat) needs no hard breaks at all: let it wrap, one sentence per line. Don't insert manual breaks into text that already flows on its own.

A "real width limit" is a property of the *file* — a column width a formatter or linter actually errors on, or a genuinely fixed-width medium. The viewer's screen or terminal width is **not** one: it is the reader's window, not a constraint on the content, and it differs from reader to reader. Never break a line to fit how wide your current display happens to be — the file's content does not depend on your viewport. A file's incumbent hard-wrap style is not a width limit either: that a document was historically wrapped at 80 columns obliges nothing — matching it reproduces mid-phrase breaks with fresh text. Unless tooling errors on the width, keep each sentence on one line (several sentences may share a line) and re-flow the paragraphs you touch.

### Where to break

Cut at the lowest-cohesion gap available, preferring (high to low):

- Sentence boundary — `.`, `—`, `;`
- Clause boundary — after a conjunction, after a topic marker (`~는/은`), before a new logical unit
- Between complete list items — keep one item and its sub-parts together on one line

### Where not to break

- Between a subject and its predicate — a topic word (`~는/은`) stranded from the clause it introduces
- Inside a parenthetical or a grouped list (`(alpha, beta,` / `gamma)`)
- Between a token and its qualifier

### Example

❌ breaks fall wherever the column limit lands — the parenthetical group splits and a clause trails off mid-phrase:

```
// Lorem ipsum dolor sit amet, consectetur (alpha, beta,
// gamma) adipiscing elit — sed do eiusmod tempor incididunt ut
// labore et dolore magna aliqua. Ut enim ad minim veniam quis.
```

✅ breaks fall at sentence boundaries, and the `(alpha, beta, gamma)` group stays intact:

```
// Lorem ipsum dolor sit amet, consectetur (alpha, beta, gamma) adipiscing elit.
// Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
// Ut enim ad minim veniam quis nostrud exercitation.
```

Each line is now one complete sentence instead of trailing off mid-phrase into the next.

## Relationship to other rules

- `terminology-discipline` governs *identifiers and domain terms* (spell out abbreviations, disambiguate collisions). This rule governs *prose rhythm and line breaks*. They compose: a sentence can use a correctly-spelled-out term and still be a noun-stack, or be cut at an awkward column.
- `thinking-expansion` activates vocabulary for thinking. This rule keeps that vocabulary out of the output unless it genuinely helps the reader. When the two pull in opposite directions, this rule wins at the output boundary.
- The repo's own `CLAUDE.md` forbids mid-sentence hard breaks in Markdown (let it soft-wrap). The line-break section here covers the other side: when a hard break is unavoidable, where it should fall.

## Rules

- Word-choice discipline (no noun-stacks, no translationese, verbs over nominalizations) applies everywhere prose appears — including tables and headings.
- Spoken rhythm is the default only for conversational and explanatory prose; structured artifacts keep their own register (see Scope).
- Priming and domain keywords stay in the thinking step; do not surface them in sentences unless the name itself helps the reader.
- Keep precise technical terms — plainness targets rhythm, not vocabulary depth.
- When you choose where a line breaks, break at the meaning boundary, not the column limit; keep grouped lists and subject–predicate pairs on one line.
- Soft-wrapping prose (Markdown, chat) takes no hard breaks — never split a sentence across lines, let it wrap.
- A file's incumbent hard-wrap style is not a width limit. Unless a linter or formatter errors on the width, don't imitate the wrap — re-flow the paragraphs you edit so no sentence is split across lines. Breaking after a sentence is allowed, never required.
- The viewer's screen/terminal width is not a width limit — never insert a hard break to fit your current display. Only a file-level column convention or a fixed-width medium justifies one.
