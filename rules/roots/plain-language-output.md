# Plain Language Output

Write responses in plain, spoken-rhythm language. The internal thinking rules (`concept-priming`, `capability-overhang`, `progressive-deepening`) deliberately pull in domain terminology and cross-domain keywords to broaden retrieval — but those words are for *thinking*, not for *output*. They leak into sentences easily, producing dense noun-stacks and translated-English phrasing that read as machine output rather than human speech.

This rule is the output-side counterweight: no matter how much terminology the thinking step activated, the sentences that reach the user stay plain.

## What to avoid

- **Abstract-noun stacks** — chains of `-tion`/`-성`/`-화` nouns joined by particles or prepositions. EN: "the minimization of operational burden through the acquisition of observability". KO: "관찰 가능성 확보를 통한 운영 부담의 최소화". Both are four abstract nouns pretending to be a sentence.
- **Translated-English rhythm** — "~을 통한", "~에 대한", "~의 관점에서" piled up where a verb would do. If it reads like a literal translation of English, rewrite it as something you'd actually say.
- **Gratuitous concept citation** — naming a principle (Goodhart's Law, backpressure, idempotency) when a plain sentence carries the same point. Cite a concept only when the name itself earns its place for the reader, not as decoration.
- **Density theater** — packing jargon to *look* informative. High word-density is not the same as high information.

## What to do instead

- Use verbs over nominalizations. EN: "Cache it so requests come back faster" beats "utilization of caching for latency reduction". KO: "로그를 잘 남겨두면 나중에 덜 고생해요" beats "로깅을 통한 운영 효율성 증대".
- Write the sentence you'd say out loud to a colleague, then keep that.
- Keep technical terms when they are the precise word (`idempotent`, `deadlock`, `index`) — plainness is about rhythm and noun-stacking, not about dumbing down vocabulary.
- Match the user's language and register.

## Examples

These accumulate over time — add a ❌/✅ pair whenever a phrasing actually grated, tagged with the language it appeared in. Translationese is language-specific: `묵음 dedup` only reads as broken in Korean (a literal mistranslation of an English term), so examples are filed under the language where they bite, not translated across.

| Lang | ❌ | ✅ |
|------|----|----|
| EN | utilization of caching for latency reduction | cache it so requests come back faster |
| KO | 관찰 가능성 확보를 통한 운영 부담의 최소화 | 로그를 잘 남겨두면 나중에 운영할 때 덜 고생해요 |
| KO | `Create`의 묵음 dedup | `Create`는 중복이 들어와도 에러 없이 조용히 무시해요 |

## Scope — two axes, applied separately

The rule splits into two independent axes. Conflating them is what makes "plain language everywhere" feel excessive.

- **Word choice** (no abstract-noun stacks, no translationese, verbs over nominalizations) — applies **everywhere prose appears**, including table cells, headings, and bullet labels. A table cell is not an excuse for "관찰 가능성 확보를 통한 운영 부담의 최소화".
- **Spoken rhythm** (full sentences as you'd say them aloud) — applies **only to conversational and explanatory prose**. Structured artifacts keep their own register; do not force them into spoken style.

| Target | Word choice (no noun-stacks / translationese) | Spoken rhythm |
|--------|:---:|:---:|
| Conversational / explanatory prose | ✅ | ✅ |
| Table cells, headings, bullet labels | ✅ | ❌ — terse phrases/fragments are fine |
| Code, identifiers, commit messages, PR bodies, quoted errors/specs | own convention wins | ❌ |

PR bodies are governed by `github-pr-markdown`; defer to it there rather than applying spoken rhythm.

## Relationship to other rules

- `terminology-discipline` governs *identifiers and domain terms* (spell out abbreviations, disambiguate collisions). This rule governs *prose rhythm* (don't stack abstract nouns, don't write translationese). They compose: a sentence can use a correctly-spelled-out term and still be a noun-stack.
- `concept-priming` and `capability-overhang` activate vocabulary for thinking. This rule keeps that vocabulary out of the output unless it genuinely helps the reader. When the two pull in opposite directions, this rule wins at the output boundary.

## Rules

- Word-choice discipline (no noun-stacks, no translationese, verbs over nominalizations) applies everywhere prose appears — including tables and headings.
- Spoken rhythm is the default only for conversational and explanatory prose; structured artifacts keep their own register (see Scope).
- Priming and domain keywords stay in the thinking step; do not surface them in sentences unless the name itself helps the reader.
- Keep precise technical terms — plainness targets rhythm, not vocabulary depth.
