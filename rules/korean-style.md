# Korean Style

The Korean extension of `prose-style`: the tells that mark Korean as machine-made, and the user's voice for Korean writing meant to be read. `prose-style` carries the read-it-back-as-speech test, the character table, and the cross-language word-choice tells; apply both when writing Korean.

## Rules

- Every term is a Korean word or English letters, never a Hangul transliteration. A plain concept goes to Korean whenever the dictionary has a word for it, whether it arrived in English or in Hangul (`concept`, `컨셉` to `개념`); a domain term keeps its English spelling (`커밋` to `commit`); a loanword settled in the dictionary counts as Korean (`파일` stays).
- The English-letters allowance covers one word (`commit`, `route`). A compound of two or more gets said in Korean however standard it looks in English.
- Prefer verbs over `-화`/`-성` nominalizations, and cut commas Korean does not need. Comma habit is the single strongest AI tell.
- Watch the frequency tells (`-들`, `~할 수 있다`, three-beat lists, `이러한`): one is fine, repetition is the tell. Break a repeated `A, B, C` triplet with two items or a clause.
- Vary sentence length, and let a short sentence land after a long one.
- Hold one politeness level across the whole passage.
- For Korean writing meant to be read (explanations, docs, longer answers), carry the user's voice: motivation-first opening, first-person retrospective, honest about failures and guesses, concrete over abstract, and `-습니다`/`-요` 공손체 throughout, even where a diary-style `-다` would feel natural.
- Voice is additive and self-limiting. It dresses an already-clean sentence, never excuses one, and stands down for terse replies, structured artifacts (PR bodies, commits, code, tables), and English output. Where it stands down the register does not: a Korean PR body still ends in `-습니다`, per `github-pr-markdown`. English output keeps only the language-neutral instincts (motivation-first, concrete, honest hedges) and follows `english-style`.

## Word choice

- **Transliterated loanwords**: `브리프` to `지시`; `인덱스` to `index`; `쿠버네티스` to `kubernetes`.
- **English compounds**: ❌ `catch-all은 match가 없는 route입니다` ✅ `조건을 안 적은 route는 앞에서 안 걸린 요청을 전부 받습니다`.
- **Unnecessary 한자어**: ❌ `조사를 실시한다` ✅ `조사한다`.
- **AI buzzwords**: ❌ `혁신적 솔루션으로 지속가능한 미래를` ✅ `새로운 방법으로 오래 갈 미래를`.
- **Nominalization over verbs**: ❌ `효율의 증대와 비용의 절감` ✅ `효율을 높이고 비용을 줄인다`.

## Punctuation

- **Comma overuse**: ❌ `중요한, 효과적인, 혁신적인 방법` ✅ `중요하고 혁신적인 방법`.
- **Serial comma before `그리고`**: ❌ `AI, 기계학습, 그리고 자동화` ✅ `AI, 기계학습, 자동화`.
- **Comma after a connective ending**: ❌ `발전했고, 혁신을 이뤘다` ✅ `발전했고 혁신을 이뤘다`.
- **English colon and dash dumps**: ❌ `핵심 요소: 효율, 비용` ✅ `핵심 요소는 효율과 비용이다`.
- **가운뎃점과 줄표**: correct orthography, still a machine tell; the character table in `prose-style` carries the replacement.

## Translationese

- **`~에 대해`**: ❌ `효율에 대해 논의한다` ✅ `효율을 논의한다`.
- **`~를 통해`**: ❌ `조사를 통해 확인했다` ✅ `조사로 확인했다`.
- **`가지고 있다`**: ❌ `장점을 가지고 있다` ✅ `장점이 많다`.
- **`~에 의해` / `되어진다`**: ❌ `AI에 의해 분석된다` ✅ `AI가 분석한다`.

## Fillers and rhythm

- **Plural `-들`**: ❌ `데이터들을 분석한 결과들` ✅ `데이터를 분석한 결과`.
- **Demonstrative repetition**: ❌ `이러한 방법으로 이를 진행한다` ✅ `이 방법으로 진행한다`.
- **`~할 수 있다` overuse**: ❌ `효과를 낼 수 있고 비용을 줄일 수 있다` ✅ `효과를 내고 비용을 줄인다`.
- **Assertive `~것이다` and AI closers** (`결론적으로`, `앞으로도 계속될 것이다`): state it plainly or hedge it.
- **Connective overuse**: join clauses with endings (`-고`, `-며`) instead of opening sentences with `그리고`, `또한`, `뿐만 아니라`.

## Voice

An ear to train, not a checklist to stamp; the profile comes from the user's own long-form writing.

- **Open with motivation, not a definition**: "무중단 마이그레이션을 잘하는 개발자가 되고 싶었습니다", not "CDC란 데이터베이스의 변경을 추적하는 기법이다".
- **First-person retrospective**: wanted, tried, hit, concluded. "고민하게 됐습니다", "제 경우엔".
- **Record the dead ends**: "찾아봤지만 실패했습니다", "마땅한 해결책은 보이지 않았습니다".
- **Mark guesses as guesses** (composes with `grounded-assertions`): "추측하기로는", "~인 것으로 보였습니다".
- **Parenthetical asides for honest footnotes**: "(.com치고는 12달러로 꽤 쌌습니다)", "(부족하지만요)".
- **Ellipsis for a trailing beat**, sparingly: "이건 js인가 ts인가...".
- **Talk to the reader in a walkthrough**: "가정해 봅시다", "이러면 어떨까요?".
- **Concrete over abstract**: the specific symptom, value, or number a reader could act on.
