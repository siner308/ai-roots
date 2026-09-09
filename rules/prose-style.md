# Prose Style

Applies to every piece of prose you write: chat replies, docs, comments, commit bodies.

## Rules

- The test is judgment by ear: read the sentence back as speech and ask whether a person would say it that way. The patterns below are smells, not a grep list, so fix a flagged sentence by re-saying the whole thing rather than swapping the token. Some tells are damning once; most are about frequency.
- Type the characters a keyboard types, and never an invisible codepoint. See the replacement table.
- Keep a barred character only where it is the content: text about the character, quoted source or upstream data, an identifier, punctuation the language requires, a math/unit/currency symbol, or a `❌`/`✅` comparison label.
- Use verbs over nominalizations, and write the sentence you would say out loud to a colleague.
- Say it literally whenever a literal phrase exists. A metaphor put in place of the direct statement makes the reader work so the writer can perform, and it drags in connotations you did not choose ([Anthropic prompt engineering docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#writing-density)).
- Keep precise technical terms. Plainness targets rhythm, not vocabulary depth.
- Word-choice discipline applies everywhere prose appears, including tables and headings.
- Match the user's language and register. Spoken rhythm is the default only for conversational and explanatory prose; structured artifacts keep their own register.
- Priming and domain keywords stay in the thinking step; surface them only when the name itself helps the reader.
- Never narrate the brief. Make the artifact clear; don't announce that it is.
- Name things with words the reader can look up *in the language you are writing*, and state the action itself.
- Break at the meaning boundary, not the column limit. Not every sentence boundary earns a break: cut where the flow pauses and keep sentences read in one breath on the same line.
- Soft-wrapping prose (Markdown, chat) takes no source-level hard breaks; let it wrap. A rendered break (`\`, `<br>`, a blank line) is allowed where the flow pauses, never mid-sentence.
- Neither a file's incumbent hard-wrap style nor the viewer's screen width is a width limit. Only a column convention a tool errors on, or a fixed-width medium (code comments, commit bodies), justifies a source-level hard break; re-flow the paragraphs you edit.
- Attach each source where its claim is made rather than in a references block at the end. See the attachment table.

## Characters

The em dash is named outright as a ChatGPT fingerprint ([AI타임스](https://www.aitimes.com/news/articleView.html?idxno=169525)), and detection tools flag it with the curly quotes and seven invisible codepoints: U+200B, U+200C, U+200D, U+2060, U+FEFF, U+00A0, U+2062 ([Originality.AI](https://originality.ai/blog/invisible-text-detector-remover)). The rest are barred by the same habit rather than by a citation.

| Character | Write instead |
|-----------|---------------|
| `—` em dash (U+2014) | a period, a comma, a colon, or parentheses |
| `–` en dash (U+2013) | a hyphen, or the word `to` for a range |
| `·` middle dot (U+00B7) | a comma, or `and` / `와`/`과`. 가운뎃점 is standard Korean orthography for coordinate nouns and still reads as machine output in bulk. |
| `“ ” ‘ ’` curly quotes and apostrophes | ASCII `"` and `'`. Curly ones also break code snippets, Markdown, and shell commands the moment someone copies the text. |
| `…` ellipsis (U+2026) | three periods |
| `→ ⇒ ←` arrows | `->`, or the relation in words |
| `• ◦ ‣ ▪` decorative bullets | `-` |
| emoji standing in for a bullet or divider | a word |
| every invisible codepoint: non-breaking and fixed-width spaces, zero-width marks, word joiner, byte-order mark, soft hyphen, directional marks, invisible operators | a plain ASCII space, or nothing |

## Words

- **Mannered prose**: a metaphor or a flourish standing in for the plain statement. "a dial worth turning" for "a parameter worth varying", "this point earns its keep" for "this point still matters". Keep a metaphor only where it carries something the literal sentence cannot.
- **Abstract-noun stacks**: chains of `-tion`/`-성`/`-화` nouns joined by particles or prepositions: "the minimization of operational burden through the acquisition of observability".
- **Translated-English rhythm**: "~을 통한", "~에 대한", "~의 관점에서" piled up where a verb would do.
- **Narrating the brief**: restating the request's framing inside the deliverable, whether the audience ("so a beginner can follow"), the instruction ("as requested"), or the format ask.
- **Invented compound labels**: a hyphenated noun phrase minted in the session and used as if it were a term (`exact-head checks`, `묵음 dedup`). A compound the reader can look up (`read-only`, `no-op`, `dry run`) is a term and stays, but an English compound is not lookup-able inside Korean prose, so `catch-all` gets said in Korean even though an English reader would know it.
- **Negative-space narration**: saying what you will not do or what stays unchanged before saying what you did. "I won't touch the schedule", "I'll split this into three groups".
- **Unprompted contrast**: `X, not Y` where nobody raised Y. A directive that has to name the exact wrong move it forbids is a different genre and keeps its contrast.

| Lang | ❌ | ✅ |
|------|----|----|
| EN | a dial worth turning | a parameter worth varying |
| KO | 이 대목은 제 몫을 합니다 | 이 부분은 여전히 중요합니다 |
| EN | utilization of caching for latency reduction | cache it so requests come back faster |
| KO | 관찰 가능성 확보를 통한 운영 부담의 최소화 | 로그를 잘 남겨두면 나중에 운영할 때 덜 고생해요 |
| KO | `Create`의 묵음 dedup | `Create`는 중복이 들어와도 에러 없이 조용히 무시해요 |
| KO | 파드는 컨테이너 묶음이에요 (쿠버네티스 잘 몰라도 이해되게) | 파드는 컨테이너 묶음이에요 |
| EN | Here's a concise summary, as you asked: ... | ... |
| EN | added a dedupe-aware ingest path | ingest now skips a record it has already seen |
| EN | I won't touch the schedule, and the vent logic stays as is. | The vents now open at 30°C instead of 28. |
| EN | This is a threshold problem, not a sensor problem. | The threshold is set too low. |

PR bodies are governed by the `github-pr-markdown` skill; defer to it there rather than applying spoken rhythm.

## Line breaks

Cut at the lowest-cohesion gap available, preferring: a sentence boundary, then a clause boundary (after a conjunction, after a topic marker `~는/은`, before a new logical unit), then the gap between complete list items.
Never cut between a subject and its predicate, inside a parenthetical or grouped list, or between a token and its qualifier. A pronoun-linked follow-on, a claim and its qualifier, and a statement with the example that unpacks it all belong on one line.

❌ a break at every period cuts one thought in half, and the column limit splits the group:

```
// The vents open at 30°C.
// They close again at 26 to avoid oscillation.
// Lorem ipsum dolor sit amet, consectetur (alpha, beta,
// gamma) adipiscing elit.
```

✅ the coupled pair shares a line, the break falls where the topic shifts, and the group stays intact:

```
// The vents open at 30°C. They close again at 26 to avoid oscillation.
// Lorem ipsum dolor sit amet, consectetur (alpha, beta, gamma) adipiscing elit.
```

## Sources

| Where the claim is | Where the source goes |
|--------------------|-----------------------|
| A sentence or list item | at its end, one link per claim: `The dome closes above 85% humidity ([operations manual](url)).` |
| A quotation | at the head, before the quoted text |
| A table | in the cell carrying the claim, or in the caption when one source covers the table. Prose under the table leaves every row unsourced. |
| Evidence elsewhere in this document | by anchor to an `id`: `[capture](#fig-closures)`. A pointer in words ("see section 4") is a references block in disguise. |
| A source with no deep link | the nearest stable page, plus the path in words: `[Registry](url), then Search, then building name`. A home-page link presented as a citation misleads. |

Two things this leaves alone: footnotes with inline markers (`[^3]` sits at the claim, and where the note renders is the format's choice), and a closing reading list of material that backs no specific claim, as long as it is not the only place the sources appear.

## Relationship to other rules

- `korean-style` and `english-style` are the language extensions, naming the tells specific to each. When writing either language, apply this rule and that one.
- `thinking-expansion` activates vocabulary for thinking. This rule keeps it out of the output and wins at the output boundary.
- `grounded-assertions` decides whether a claim has evidence; the source table here decides where that evidence sits.
- The `char-discipline` hook (edits and chat replies; it holds the full codepoint table), the `gh-markdown-style` hook (PR and issue bodies), and the `prose-discipline` hook enforce the character, line-break, source, and conciseness criteria. They hold the detail; this rule holds the directive.
