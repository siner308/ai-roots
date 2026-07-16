# Korean Style

This rule makes Korean output read as if a Korean person wrote it, not as if it were translated from English.
It is the Korean-specific extension of `prose-style`: that rule governs prose rhythm and line breaks in any language, this one names the tells that mark Korean as machine-made.

## The test comes first

There is one test, and it is judgment, not pattern-matching: read the sentence back as speech, and ask whether a Korean colleague would actually say or write it.
If it sounds translated — stiff, noun-heavy, strewn with commas — rewrite it as something you'd say out loud.

Everything below just trains your ear for that test.
The patterns are smells to recognize, never a token list to grep: you can trip none of them and still sound translated, and you can use any one of them naturally — so fix a flagged sentence by re-saying the whole thing, not by swapping the token.
Some tells are damning on a single appearance (an English-shaped passive); most are about frequency (one comma is fine, a sentence strung with them is the tell).

## Word choice

- **Transliterated loanwords** — a Hangul-spelled English word is never the answer. Ask the dictionary first: if a plain Korean word exists, use it, whether the loanword arrived in English or in Hangul (`concept`·`컨셉` → `개념`; `브리프` → `지시`·`요청`). If there is no Korean word, it is a domain term — write it in English letters, never a Hangul transliteration (`commit` not `커밋`, `index` not `인덱스`, `kubernetes` not `쿠버네티스`). A loanword long since naturalized into the dictionary (`파일`, `컴퓨터`) already counts as a Korean word — keep it. The rule targets un-naturalized jargon, not settled borrowings.
- **Unnecessary 한자어** — when an everyday Korean word carries the same meaning, prefer it. ❌ `조사를 실시한다` → ✅ `조사한다`.
- **AI buzzwords** — `혁신적`, `지속가능한`, `핵심적`, `상당한` piled together. ❌ `혁신적 솔루션으로 지속가능한 미래를` → ✅ `새로운 방법으로 오래 갈 미래를`.
- **Nominalization over verbs** — `-화`/`-성`/`-도` abstractions where a verb would do the work. ❌ `효율의 증대와 비용의 절감` → ✅ `효율을 높이고 비용을 줄인다`.

## Punctuation — the strongest tell

Comma habits separate AI Korean from human Korean more reliably than anything else, because Korean needs far fewer commas than English and AI carries the English rate over.

- **Comma overuse** — ❌ `중요한, 효과적인, 혁신적인 방법` → ✅ `중요하고 혁신적인 방법`.
- **English-style serial comma** before `그리고` — ❌ `AI, 기계학습, 그리고 자동화` → ✅ `AI, 기계학습, 자동화`.
- **Comma after a connective ending** (`-고,` / `-며,` / `-면서,`) — ❌ `발전했고, 혁신을 이뤘다` → ✅ `발전했고 혁신을 이뤘다`.
- **English colon/dash dumps** — ❌ `핵심 요소: 효율, 비용` → ✅ `핵심 요소는 효율과 비용이다`.

## Translationese

- **`~에 대해`** (about) — ❌ `효율에 대해 논의한다` → ✅ `효율을 논의한다`.
- **`~를 통해`** (through) — ❌ `조사를 통해 확인했다` → ✅ `조사로 확인했다`.
- **`가지고 있다`** (have) — ❌ `장점을 가지고 있다` → ✅ `장점이 많다`.
- **`~에 의해` / `되어진다`** (passive "by", double passive) — ❌ `AI에 의해 분석된다` → ✅ `AI가 분석한다`.

## Overused fillers

- **Plural `-들`** where Korean leaves number implicit — ❌ `데이터들을 분석한 결과들` → ✅ `데이터를 분석한 결과`.
- **Pronoun / demonstrative repetition** (`이것`·`그것`, `이러한`·`그러한`) — ❌ `이러한 방법으로 이를 진행한다` → ✅ `이 방법으로 진행한다`.
- **`~할 수 있다` overuse** — ❌ `효과를 낼 수 있고 비용을 줄일 수 있다` → ✅ `효과를 내고 비용을 줄인다`.
- **Assertive `~것이다` and AI closers** (`결론적으로`, `앞으로도 계속될 것이다`) — a hedge or a plain statement usually reads more human than a confident forecast.

## Rhythm and structure

- **Monotone sentence length** — AI writes sentences of near-identical length; vary them, let a short one land after a long one.
- **Three-beat lists** — `A, B, C` triplets repeated across paragraphs. Break the pattern; sometimes two items, sometimes a clause.
- **Connective overuse** — `그리고`, `또한`, `뿐만 아니라` stacked. Join clauses with endings (`-고`, `-며`) instead of starting sentences with a conjunction.
- **Register drift** — keep one politeness level; don't slide between `합니다` and `-다` in the same passage.

## Rules

- The test is judgment by ear (read it back as speech), not token-matching; the patterns are smells, not a grep list. Re-say the whole sentence, don't swap the flagged word.
- Every term is a Korean word or English letters, never a Hangul transliteration: a plain concept goes to Korean (`컨셉` → `개념`), a domain term keeps its English spelling (`커밋` → `commit`), and a loanword settled in the dictionary counts as Korean (`파일` stays `파일`).
- Prefer verbs over `-화`/`-성` nominalizations, and cut commas Korean does not need — comma habit is the single strongest AI tell.
- Watch frequency tells (`-들`, `~할 수 있다`, three-beat lists, `이러한`): one is fine, repetition is the tell.
- This rule composes with `prose-style` (rhythm, line breaks) and `terminology-discipline` (identifiers, domain terms); when writing Korean, all three apply.
