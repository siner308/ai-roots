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
- **Register drift** — keep one politeness level, holding it across the whole passage rather than sliding between `합니다` and `-다`.

## Voice

Naturalness keeps Korean from reading as machine-made; voice makes it read as *this user*. When the task is Korean prose meant to be read as writing — explanations, walkthroughs, docs, longer answers — carry the user's own voice: first-person, motivation-led, honest about dead ends. The profile below was drawn from the user's own long-form writing; treat it as an ear to train, not a checklist to stamp.

Register for such writing standardizes on **`-습니다`/`-요` 공손체** — the register-drift rule above picks *whether* to stay level; this picks *which* level, and holds it even where a diary-style `-다` would feel natural.

- **Open with motivation, not a definition.** Start from why you're writing this or what problem prompted it. "무중단 마이그레이션을 잘하는 개발자가 되고 싶었습니다", not "CDC란 데이터베이스의 변경을 추적하는 기법이다".
- **First-person retrospective.** Frame the material as your own path — wanted, tried, hit, concluded. "고민하게 됐습니다", "제 경우엔".
- **Record the dead ends.** Say what failed or went unsolved rather than laundering it into a clean success. "찾아봤지만 실패했습니다", "마땅한 해결책은 보이지 않았습니다".
- **Mark guesses as guesses** (composes with `grounded-assertions`). "추측하기로는", "~인 것으로 보였습니다".
- **Parenthetical asides for honest footnotes** — a cost, a caveat, a shrug. "(.com치고는 12달러로 꽤 쌌습니다)", "(부족하지만요)".
- **Ellipsis for a trailing beat**, sparingly, not as filler. "이건 js인가 ts인가…".
- **Talk to the reader in a walkthrough** — 청유·수사의문 pull them along. "가정해 봅시다", "이러면 어떨까요?".
- **Concrete over abstract** — the specific symptom, value, or number a reader could act on beats a smooth summary of it (the same instinct `github-pr-markdown` applies to PR bodies).

Voice is additive: it only ever dresses an already-clean sentence, never excuses a machine-shaped one — every rule above this section still binds.

The voice **stands down** where writing is not the deliverable: terse work replies (a status line, a yes/no — the user's `CLAUDE.md` asks for concise answers, and that wins), structured artifacts (PR bodies, commit messages, code, comments, tables — each keeps its own convention, and a PR body is the *opposite* of this voice: it describes the diff, not the journey), and English output (keep only the language-neutral instincts — motivation-first, concrete, honest hedges).

## Rules

- The test is judgment by ear (read it back as speech), not token-matching; the patterns are smells, not a grep list. Re-say the whole sentence rather than swapping the flagged word.
- Every term is a Korean word or English letters, never a Hangul transliteration: a plain concept goes to Korean (`컨셉` → `개념`), a domain term keeps its English spelling (`커밋` → `commit`), and a loanword settled in the dictionary counts as Korean (`파일` stays `파일`).
- Prefer verbs over `-화`/`-성` nominalizations, and cut commas Korean does not need — comma habit is the single strongest AI tell.
- Watch frequency tells (`-들`, `~할 수 있다`, three-beat lists, `이러한`): one is fine, repetition is the tell.
- For Korean writing meant to be read (explanations, docs, longer answers), carry the user's voice: motivation-first opening, first-person retrospective, honest about failures and guesses, concrete over abstract, one `-습니다`/`-요` register throughout.
- Voice is additive and self-limiting — it dresses an already-clean sentence, never excuses one, and stands down for terse replies, structured artifacts (PR bodies, commits, code, tables), and English output.
- This rule composes with `prose-style` (rhythm, line breaks) and `terminology-discipline` (identifiers, domain terms); when writing Korean, all three apply.
