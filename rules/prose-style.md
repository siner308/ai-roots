# Prose Style

How writing reaches the reader comes down to three separate choices: the *words* inside a sentence, *where the lines are cut*, and *where the source of a claim sits*. Each can quietly turn clear thinking into machine-looking output, and they fail in different ways — so this rule covers all three.

The internal thinking rule (`thinking-expansion`) deliberately pulls in domain terminology and cross-domain keywords to broaden retrieval — but those words are for *thinking*, not for *output*. They leak into sentences easily, producing dense noun-stacks and translated-English phrasing that read as machine output rather than human speech. This rule is the output-side counterweight: no matter how much terminology the thinking step activated, the prose that reaches the user stays plain, and it breaks where the meaning pauses.

## Plain language

### What to avoid

- **Abstract-noun stacks** — chains of `-tion`/`-성`/`-화` nouns joined by particles or prepositions. EN: "the minimization of operational burden through the acquisition of observability". KO: "관찰 가능성 확보를 통한 운영 부담의 최소화". Both are four abstract nouns pretending to be a sentence.
- **Translated-English rhythm** — "~을 통한", "~에 대한", "~의 관점에서" piled up where a verb would do. If it reads like a literal translation of English, rewrite it as something you'd actually say.
- **Narrating the brief** — restating the request's framing inside the deliverable: the audience ("so a beginner can follow"), the instruction ("as requested", "to keep it concise"), or the format ask. How and for whom you were told to write is context for the writing, not content to put in it — the artifact should *be* clear, not announce that it is. This is a strong AI tell: a human writing the same doc would never label it with its own brief.
- **Invented compound labels** — a hyphenated noun phrase minted in the session and then used as if it were a term: `exact-head checks`, `editorial-row layouts`, `묵음 dedup`. The reader has no definition to look up, so the label hides the relationship it pretends to name. Say that relationship with a plain verb and a preposition. A compound the reader can look up (`read-only`, `no-op`, `dry run`) is a term, not a label — keep it.
- **Negative-space narration** — saying what you won't do, what stays unchanged, or how you will sort the result before saying what you did: "I won't touch the schedule", "the vent logic stays as is", "I'll split this into three groups". The reader asked for the change, not the boundary drawn around it. State the action.
- **Unprompted contrast** — `X, not Y` / `X—not Y` / `X가 아니라 Y` where nobody raised Y. It manufactures an alternative so the sentence can knock it down; state X. A directive that has to name the exact wrong move it forbids is a different genre and keeps its contrast.

### What to do instead

- Use verbs over nominalizations. EN: "Cache it so requests come back faster" beats "utilization of caching for latency reduction". KO: "로그를 잘 남겨두면 나중에 덜 고생해요" beats "로깅을 통한 운영 효율성 증대".
- Write the sentence you'd say out loud to a colleague, then keep that.
- Keep technical terms when they are the precise word (`idempotent`, `deadlock`, `index`) — plainness is about rhythm and noun-stacking, not about dumbing down vocabulary.
- Match the user's language and register.

### Examples

| Lang | ❌ | ✅ |
|------|----|----|
| EN | utilization of caching for latency reduction | cache it so requests come back faster |
| KO | 관찰 가능성 확보를 통한 운영 부담의 최소화 | 로그를 잘 남겨두면 나중에 운영할 때 덜 고생해요 |
| KO | `Create`의 묵음 dedup | `Create`는 중복이 들어와도 에러 없이 조용히 무시해요 |
| KO | 파드는 컨테이너 묶음이에요 (쿠버네티스 잘 몰라도 이해되게) | 파드는 컨테이너 묶음이에요 |
| EN | Here's a concise summary, as you asked: … | … |
| EN | added a dedupe-aware ingest path | ingest now skips a record it has already seen |
| EN | I won't touch the schedule, and the vent logic stays as is. I'll only change the threshold. | The vents now open at 30°C instead of 28. |
| EN | This is a threshold problem, not a sensor problem. | The threshold is set too low. |

PR bodies are governed by the `github-pr-markdown` skill; defer to it there rather than applying spoken rhythm.

## Line breaks follow meaning

A hard line break reads as a boundary. The reader treats the end of a line as a small pause — a place where one thought finishes and the next begins. So when you control where a line breaks, the break carries meaning whether you intend it to or not.

The common failure is breaking wherever a column limit happens to land. That drops a boundary into the middle of a phrase, and the reader has to undo it — re-joining a list item with the sibling stranded on the next line, or a topic word with the predicate that follows it. The text still parses, but every mid-phrase break costs a beat.

### Where this applies

Only where the break is yours to place, and in two situations: a real width limit forces one (code comments, commit message bodies, fixed-width text), or the break itself renders — `\` or `<br>` in Markdown/MDX, anything the reader actually sees as a line break. Soft-wrapping prose (Markdown, chat) needs no *source-level* hard breaks at all: let it wrap, one sentence per line. Let text that already flows on its own do the wrapping.

A "real width limit" is a property of the *file* — a column width a formatter or linter actually errors on, or a genuinely fixed-width medium. The viewer's screen or terminal width is **not** one: it is the reader's window, not a constraint on the content, and it differs from reader to reader. Never break a line to fit how wide your current display happens to be — the file's content does not depend on your viewport. A file's incumbent hard-wrap style is not a width limit either: that a document was historically wrapped at 80 columns obliges nothing — matching it reproduces mid-phrase breaks with fresh text. Unless tooling errors on the width, keep each sentence on one line (several sentences may share a line) and re-flow the paragraphs you touch.

A rendered break is the width-independent case: the reader actually sees it, so it is a presentation choice, and it follows the same judgment as any cut you place — add one where the flow pauses (a topic shift, a breath), keep sentences read in one breath flowing together, and never put one inside a sentence. The no-hard-breaks default above targets source-level wraps the renderer collapses anyway; it does not forbid a deliberate rendered break that carries meaning.

### Where to break

Cut at the lowest-cohesion gap available, preferring (high to low):

- Sentence boundary — `.`, `—`, `;`
- Clause boundary — after a conjunction, after a topic marker (`~는/은`), before a new logical unit
- Between complete list items — keep one item and its sub-parts together on one line

Within the top tier, not every sentence boundary earns a break. A period marks a candidate cut, not an obligation: break where the flow actually pauses — the topic shifts, or a reader would take a breath before the next sentence — and let sentences that are read in one breath share a line. A pronoun-linked follow-on, a claim and its immediate qualifier, a statement and the example that unpacks it belong together; a break between them inserts a pause the reader shouldn't take.

❌ a break at every period cuts one thought in half:

```
// The vents open at 30°C.
// They close again at 26 to avoid oscillation.
// Watering runs on a separate schedule.
```

✅ the coupled pair shares a line; the break falls where the topic shifts:

```
// The vents open at 30°C. They close again at 26 to avoid oscillation.
// Watering runs on a separate schedule.
```

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

## Sources sit where the claim is

A reader looks for the source at the moment a claim raises doubt. Put the link there — in the sentence, list item, table cell, or quote head that makes the claim — and the doubt is answered where it arose. A references block at the end of the document answers it somewhere else: the reader leaves the claim, scans a list, guesses which entry backs which sentence, and comes back. One list for the whole document also hides gaps, because nobody can tell which claims are sourced and which are not.

### How to attach a source

- **A sentence or list item** ends with the link that backs it: `The dome closes when humidity passes 85% — [operations manual](url).` When one item makes several claims, each claim carries its own link.
- **A quotation** names its source at the head, before the quoted text, so the reader knows whose words follow.
- **A table** links in the cell that carries the claim — an identifier column linking to each row's record, or a source column — or in the caption when one source covers the whole table. A source named only in the prose under the table leaves every row unsourced.
- **Evidence elsewhere in the same document** (a screenshot, an appendix, a captured page) gets an `id` and is linked by anchor: `[capture](#fig-closures)`. A pointer in words (`see the capture in section 4`) is a references block in disguise — the reader still has to go looking.
- **A source with no deep link** (a record behind a search form, one URL for every query) gets the nearest stable page linked and the path stated in words: `[Registry](url) → Search → building name → record`. Say what the link does not reach; a home-page link presented as a citation misleads.

### What this leaves alone

- Footnotes with inline markers (`[^3]` at the claim, the note at the end). The marker sits at the point of use; where the note renders is the format's choice.
- A closing reading list of material that backs no specific claim. It is a reading list, not a citation, and it must not be the only place the document's sources appear.

### Example

❌ sources bunched at the end, and one pointer in words:

```
- The dome closes when humidity passes 85%.
- Three closures last month were logged as weather, not faults (see the capture in section 4).

## References
- https://example.org/ops-manual
- https://example.org/log/2026-08
```

✅ each source sits with its claim, and the capture is an anchor:

```
- The dome closes when humidity passes 85% — [operations manual](https://example.org/ops-manual).
- Three closures last month were logged as weather, not faults — [August log](https://example.org/log/2026-08), [capture](#fig-closures).
```

## Relationship to other rules

- `korean-style` is the Korean-specific extension of this rule: it names the AI-Korean tells (comma habits, transliterated loanwords, translationese, sentence rhythm) with concrete ❌/✅ examples. When writing Korean, apply both — this rule for cross-language rhythm, that one for the Korean-only tells.
- `english-style` is the same extension for English: it names the AI-English tells (stock lexicon, em-dash pileups, the `not just X, it's Y` frame, connective padding) with the same ❌/✅ treatment, and carries the spoken-register guidance for transcripts and scripts. When writing English, apply both.
- `thinking-expansion` activates vocabulary for thinking. This rule keeps that vocabulary out of the output unless it genuinely helps the reader. When the two pull in opposite directions, this rule wins at the output boundary.
- `grounded-assertions` decides whether a claim has evidence; the source-placement section here decides where that evidence sits in the artifact. A claim that passes the first and fails the second is sourced but unfindable.
- The repo's own `CLAUDE.md` forbids mid-sentence hard breaks in Markdown (let it soft-wrap). The line-break section here covers the other side: when a hard break is unavoidable, where it should fall.

## Rules

- Word-choice discipline (no noun-stacks, no translationese, verbs over nominalizations) applies everywhere prose appears — including tables and headings.
- Spoken rhythm is the default only for conversational and explanatory prose; structured artifacts keep their own register.
- Priming and domain keywords stay in the thinking step; surface them in sentences only when the name itself helps the reader.
- Keep precise technical terms — plainness targets rhythm, not vocabulary depth.
- Never narrate the brief: the request's audience, instruction, or format ask is context for writing, not content to state in the artifact. Make it clear; don't announce that it is.
- Name things with words the reader can look up, and state the action itself: no compound label minted in the session, no announcing what stays untouched or how results will be sorted, no `X, not Y` against an alternative the reader never raised. A directive that must name the exact anti-pattern it forbids keeps its contrast; prose to a reader drops it.
- When you choose where a line breaks, break at the meaning boundary, not the column limit; keep grouped lists and subject–predicate pairs on one line.
- Not every sentence boundary earns a break: cut where the flow pauses — a topic shift, a breath — and keep sentences that are read in one breath on the same line.
- Soft-wrapping prose (Markdown, chat) takes no source-level hard breaks — never split a sentence across lines, let it wrap. A rendered break (`\`, `<br>`, or a blank-line paragraph in Markdown) is a presentation choice, not a wrap: allowed where the flow pauses, never mid-sentence.
- A file's incumbent hard-wrap style is not a width limit. Unless a linter or formatter errors on the width, re-flow the paragraphs you edit so no sentence is split across lines, rather than imitating the wrap. Breaking after a sentence is allowed, never required.
- The viewer's screen/terminal width is not a width limit — never insert a hard break to fit your current display. Only a file-level column convention or a fixed-width medium justifies one.
- Attach each source where its claim is made — at the end of the sentence or list item, in the table cell or caption, at the head of a quote — instead of in a references block at the end of the document. Link evidence elsewhere in the document by anchor, never by a pointer in words, and give a source with no deep link the nearest stable page plus the path in words.
