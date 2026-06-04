# Prose Style

글이 독자에게 닿는 방식은 두 가지 별개의 선택으로 갈린다: 문장 *안의 단어*, 그리고 *줄을 어디서 끊느냐*. 둘 다 명료한 사고를 기계 같은 출력으로 조용히 바꿔놓을 수 있고, 망가지는 방식이 서로 다르다 — 그래서 이 규칙은 둘 다 다룬다.

내부 사고 규칙(`concept-priming`, `capability-overhang`, `progressive-deepening`)은 retrieval을 넓히려고 일부러 도메인 용어와 교차 도메인 키워드를 끌어온다 — 하지만 그 단어들은 *사고*용이지 *출력*용이 아니다. 그것들은 문장에 쉽게 새어 나와, 사람의 말이 아니라 기계의 출력처럼 읽히는 빽빽한 명사 더미와 번역투 표현을 만든다. 이 규칙은 출력 쪽의 평형추다: 사고 단계에서 용어를 아무리 많이 활성화했어도, 사용자에게 닿는 문장은 평이하게 유지되고, 의미가 멈추는 곳에서 줄이 끊긴다.

## 평이한 언어

### 피해야 할 것

- **Abstract-noun stacks** — `-tion`/`-성`/`-화` 명사를 조사나 전치사로 엮은 사슬. EN: "the minimization of operational burden through the acquisition of observability". KO: "관찰 가능성 확보를 통한 운영 부담의 최소화". 둘 다 문장인 척하는 추상명사 네 개다.
- **Translated-English rhythm** — 동사면 될 자리에 "~을 통한", "~에 대한", "~의 관점에서"를 쌓는 것. 영어를 직역한 것처럼 읽히면, 네가 실제로 할 법한 말로 다시 써라.
- **Gratuitous concept citation** — 평이한 문장이 같은 요점을 전달하는데도 원칙 이름(Goodhart's Law, backpressure, idempotency)을 갖다 붙이는 것. 개념 이름은 그 이름 자체가 독자에게 값할 때만 인용하고, 장식으로 쓰지 마라.
- **Density theater** — 정보 있어 *보이려고* 전문용어를 욱여넣는 것. 단어 밀도가 높다고 정보 밀도가 높은 건 아니다.

### 대신 할 것

- 명사화보다 동사를 써라. EN: "Cache it so requests come back faster"가 "utilization of caching for latency reduction"를 이긴다. KO: "로그를 잘 남겨두면 나중에 덜 고생해요"가 "로깅을 통한 운영 효율성 증대"를 이긴다.
- 동료에게 소리 내어 할 법한 문장을 쓰고, 그대로 둬라.
- 그게 정확한 단어일 때는 전문용어를 유지하라 (`idempotent`, `deadlock`, `index`) — 평이함은 리듬과 명사 쌓기에 대한 것이지 어휘를 낮추는 게 아니다.
- 사용자의 언어와 톤에 맞춰라.

### 예시

이 표는 시간이 지나며 쌓인다 — 실제로 거슬렸던 표현이 나올 때마다 ❌/✅ 쌍을 추가하고, 어느 언어에서 나왔는지 태그를 달아라. 번역투는 언어마다 다르다: `묵음 dedup`은 한국어에서만 망가져 보이고(영어 용어를 그대로 직역한 것), 그래서 예시는 언어를 가로질러 번역하지 않고 그게 거슬리는 언어 아래에 정리한다.

| Lang | ❌ | ✅ |
|------|----|----|
| EN | utilization of caching for latency reduction | cache it so requests come back faster |
| KO | 관찰 가능성 확보를 통한 운영 부담의 최소화 | 로그를 잘 남겨두면 나중에 운영할 때 덜 고생해요 |
| KO | `Create`의 묵음 dedup | `Create`는 중복이 들어와도 에러 없이 조용히 무시해요 |

### 적용 범위 — 두 축을 따로 적용

평이한 언어 자체가 독립적인 두 축으로 나뉜다. 둘을 뭉뚱그리는 게 "어디서나 평이한 언어"를 과하게 느껴지게 만든다.

- **Word choice** (추상명사 더미 금지, 번역투 금지, 명사화보다 동사) — prose가 나타나는 **모든 곳**에 적용된다. 표 칸, 제목, 불릿 라벨 포함. 표 칸이라고 "관찰 가능성 확보를 통한 운영 부담의 최소화"를 써도 되는 건 아니다.
- **Spoken rhythm** (소리 내어 말할 법한 완결된 문장) — **대화체·설명체 prose에만** 적용된다. 구조화된 산출물은 자기 톤을 유지한다 — 억지로 구어체로 만들지 마라.

| Target | Word choice (no noun-stacks / translationese) | Spoken rhythm |
|--------|:---:|:---:|
| Conversational / explanatory prose | ✅ | ✅ |
| Table cells, headings, bullet labels | ✅ | ❌ — terse phrases/fragments are fine |
| Code, identifiers, commit messages, PR bodies, quoted errors/specs | own convention wins | ❌ |

PR 본문은 `github-pr-markdown` skill이 관장한다. 거기서는 spoken rhythm을 적용하지 말고 그 skill을 따라라.

## 줄넘김은 의미를 따른다

하드 줄넘김은 경계로 읽힌다. 독자는 한 줄의 끝을 작은 멈춤 — 한 생각이 끝나고 다음 생각이 시작되는 자리 — 로 받아들인다. 그래서 줄을 어디서 끊을지 네가 정할 때, 그 끊김은 의도하든 안 하든 의미를 담는다.

흔한 실수는 컬럼 한계가 닿는 아무 자리에서나 끊는 것이다. 그러면 구(句) 한가운데 경계가 떨어지고, 독자가 그걸 다시 이어 붙여야 한다 — 다음 줄에 떨어진 형제 항목을 리스트 항목과 다시 잇거나, 뒤따르는 술어를 주제어와 다시 잇는 식으로. 텍스트는 여전히 파싱되지만, 구 중간의 끊김 하나마다 이해의 박자를 한 번씩 깎아먹는다.

### 어디에 적용되나

끊는 자리가 네 몫이고 실제 너비 제한이 끊김을 강제하는 곳에서만 — 코드 주석, 커밋 메시지 본문, 고정폭 텍스트. soft-wrap 되는 prose(Markdown, 채팅)는 하드 줄넘김이 아예 필요 없다: 그냥 흘려보내라, 한 줄에 한 문장. 이미 스스로 흐르는 텍스트에 수동 줄넘김을 끼워 넣지 마라.

### 끊어야 할 곳

결합도가 가장 낮은 지점에서 끊되, 다음 순서로(높은 것부터):

- 문장 경계 — `.`, `—`, `;`
- 절 경계 — 접속사 뒤, 주제어(`~는/은`) 뒤, 새 논리 단위 앞
- 완성된 리스트 항목 사이 — 한 항목과 그 하위 요소는 같은 줄에 유지

### 끊으면 안 되는 곳

- 주어와 술어 사이 — 주제어(`~는/은`)가 그것이 끌어들이는 절과 떨어지는 것
- 괄호 안이나 그룹 리스트 내부 (`(alpha, beta,` / `gamma)`)
- 토큰과 그 수식어 사이

### 예시

❌ 컬럼 한계가 닿는 아무 자리에서나 끊김 — 괄호 그룹이 쪼개지고 절이 구 중간에서 끊긴다:

```
// Lorem ipsum dolor sit amet, consectetur (alpha, beta,
// gamma) adipiscing elit — sed do eiusmod tempor incididunt ut
// labore et dolore magna aliqua. Ut enim ad minim veniam quis.
```

✅ 문장 경계에서 끊기고, `(alpha, beta, gamma)` 그룹은 통째로 유지된다:

```
// Lorem ipsum dolor sit amet, consectetur (alpha, beta, gamma) adipiscing elit.
// Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
// Ut enim ad minim veniam quis nostrud exercitation.
```

이제 각 줄이 구 중간에서 다음 줄로 흘러내리지 않고, 하나의 완결된 문장이다.

## 다른 규칙과의 관계

- `terminology-discipline`는 *식별자와 도메인 용어*를 관장한다 (약어 풀어쓰기, 충돌 구분). 이 규칙은 *prose 리듬과 줄넘김*을 관장한다. 둘은 함께 작동한다: 한 문장이 올바르게 풀어쓴 용어를 쓰면서도 여전히 명사 더미일 수 있고, 어색한 컬럼에서 끊길 수도 있다.
- `concept-priming`과 `capability-overhang`은 사고용 어휘를 활성화한다. 이 규칙은 그 어휘가 독자에게 진짜로 도움 되지 않는 한 출력에 못 나오게 막는다. 둘이 반대 방향으로 당길 때, 출력 경계에서는 이 규칙이 이긴다.
- 이 repo 자체의 `CLAUDE.md`는 Markdown에서 문장 중간 하드 줄넘김을 금한다 (soft-wrap에 맡겨라). 여기 줄넘김 섹션은 그 반대편을 다룬다: 하드 줄넘김이 불가피할 때, 어디서 끊어야 하는가.

## 규칙

- word-choice 규율(명사 더미 금지, 번역투 금지, 명사화보다 동사)은 prose가 나타나는 모든 곳에 적용된다 — 표와 제목 포함.
- spoken rhythm은 대화체·설명체 prose에서만 기본이다. 구조화된 산출물은 자기 톤을 유지한다 (Scope 참고).
- priming과 도메인 키워드는 사고 단계에 머문다. 이름 자체가 독자에게 도움 되지 않는 한 문장에 드러내지 마라.
- 정확한 전문용어는 유지하라 — 평이함이 겨냥하는 건 리듬이지 어휘 깊이가 아니다.
- 줄을 어디서 끊을지 정할 때는 컬럼 한계가 아니라 의미 경계에서 끊어라. 그룹 리스트와 주어–술어 쌍은 한 줄에 유지하라.
- soft-wrap 되는 prose(Markdown, 채팅)는 하드 줄넘김을 넣지 마라 — 그냥 흘려보내라.
