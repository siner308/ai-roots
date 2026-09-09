# Prose Style

직접 쓰는 모든 산문에 적용된다. 채팅 답변, 문서, 주석, commit 본문.

## 규칙

- 기준은 귀로 하는 판단이다. 문장을 소리 내어 읽고 사람이 이렇게 말할지 자문한다. 아래 패턴은 훑어 거를 목록이 아니라 냄새이니, 걸린 문장은 단어만 바꾸지 말고 통째로 다시 말해서 고친다. 어떤 표시는 한 번으로 치명적이고 대부분은 빈도가 문제다.
- 키보드가 치는 문자를 치고, 보이지 않는 codepoint는 절대 쓰지 않는다. 대체 표를 본다.
- 막힌 문자를 남기는 건 그 문자가 내용일 때뿐이다: 그 문자를 다루는 글, 인용한 원문이나 상위 데이터, 식별자, 언어가 요구하는 부호, 수식과 단위와 통화 기호, `❌`/`✅` 비교 라벨.
- 명사화보다 동사를 쓰고, 동료에게 소리 내어 할 법한 문장을 쓴다.
- 그대로 말할 표현이 있으면 그대로 말한다. 직설적인 서술 자리에 넣은 비유는 글쓴이가 돋보이려고 독자를 더 애쓰게 만들고, 의도하지 않은 함축까지 끌고 온다([Anthropic prompt engineering 문서](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#writing-density)).
- 정확한 전문용어는 유지한다. 평이함이 겨냥하는 건 리듬이지 어휘 깊이가 아니다.
- 낱말 선택 규율은 산문이 나타나는 모든 곳에 적용된다. 표와 제목도 포함이다.
- 사용자의 언어와 어투에 맞춘다. 구어체 리듬은 대화체와 설명체 산문에서만 기본이고, 구조적 산출물은 자기 어조를 지킨다.
- priming과 도메인 키워드는 사고 단계에 머문다. 이름 자체가 독자에게 도움 될 때만 드러낸다.
- 시킨 내용을 글에 옮겨 적지 않는다. 명료하게 쓰고, 명료하다고 선언하지 않는다.
- *지금 쓰는 언어로* 독자가 찾아볼 수 있는 말로 이름 붙이고, 한 일 자체를 말한다.
- 줄 너비 한계가 아니라 의미 경계에서 끊는다. 모든 문장 경계가 끊을 자리는 아니다. 흐름이 멈추는 곳에서 끊고, 한 호흡으로 읽히는 문장은 같은 줄에 둔다.
- soft-wrap 되는 산문(Markdown, 채팅)은 소스 수준 하드 줄넘김을 쓰지 않는다. 그냥 흘려보낸다. rendered break(`\`, `<br>`, 빈 줄)는 흐름이 멈추는 곳에만 되고 문장 중간에는 안 된다.
- 파일에 원래 있던 hard-wrap 스타일도, 보는 사람의 화면 폭도 너비 제한이 아니다. 도구가 오류를 내는 줄 너비 관례나 고정폭 매체(코드 주석, commit 본문)만 소스 수준 하드 줄넘김을 정당화하고, 손대는 문단은 다시 흘려 쓴다.
- 출처는 문서 끝의 references 블록이 아니라 주장이 있는 자리에 붙인다. 부착 표를 본다.

## 문자

em dash는 ChatGPT의 지문으로 아예 지목되고([AI타임스](https://www.aitimes.com/news/articleView.html?idxno=169525)), 탐지 도구는 이것을 굽은 인용부호와 보이지 않는 codepoint 일곱 개(U+200B, U+200C, U+200D, U+2060, U+FEFF, U+00A0, U+2062)와 함께 걸러낸다([Originality.AI](https://originality.ai/blog/invisible-text-detector-remover)). 나머지는 인용 근거가 아니라 같은 습관 때문에 막는다.

| 문자 | 대신 쓸 것 |
|------|-----------|
| `—` em dash (U+2014) | 마침표, 쉼표, 콜론, 또는 괄호 |
| `–` en dash (U+2013) | 하이픈, 범위라면 `to` |
| `·` 가운뎃점 (U+00B7) | 쉼표, 또는 `and` / `와`/`과`. 가운뎃점은 대등한 명사를 잇는 정식 한국어 부호이지만 많이 쓰면 기계 출력으로 읽힌다. |
| `“ ” ‘ ’` 굽은 인용부호와 아포스트로피 | ASCII `"`와 `'`. 굽은 것은 독자가 복사하는 순간 code snippet과 Markdown, shell 명령까지 깨뜨린다. |
| `…` 줄임표 (U+2026) | 마침표 세 개 |
| `→ ⇒ ←` 화살표 | `->`, 또는 관계를 말로 |
| `• ◦ ‣ ▪` 장식용 글머리 기호 | `-` |
| 글머리 기호나 구분선을 대신하는 emoji | 낱말 |
| 보이지 않는 codepoint 전부: non-breaking과 고정폭 공백, zero-width 표시, word joiner, byte-order mark, soft hyphen, 방향 표시, 보이지 않는 연산자 | 평범한 ASCII 공백, 또는 아무것도 |

## 낱말

- **겉멋 든 문체**: 평범한 서술 자리에 비유나 수식을 세우는 것. "바꿔볼 만한 parameter" 대신 "돌려볼 만한 다이얼", "이 부분은 여전히 중요합니다" 대신 "이 대목은 제 몫을 합니다". 비유는 그대로 쓴 문장이 담지 못하는 것을 담을 때만 남긴다.
- **추상명사 사슬**: `-tion`/`-성`/`-화` 명사를 조사나 전치사로 엮은 사슬. "the minimization of operational burden through the acquisition of observability".
- **번역투 리듬**: 동사면 될 자리에 "~을 통한", "~에 대한", "~의 관점에서"를 쌓는 것.
- **지시 내용 옮겨 적기**: 시킨 내용의 틀을 산출물 안에 옮겨 적는 것. 대상("초보도 이해되게"), 지시("요청하신 대로"), 형식 요구.
- **즉석 합성어 라벨**: 세션 중에 만든 하이픈 명사구를 용어인 것처럼 쓰는 것(`exact-head checks`, `묵음 dedup`). 독자가 찾아볼 수 있는 합성어(`read-only`, `no-op`, `dry run`)는 용어이니 유지하지만, 한국어 문장 안의 영어 합성어는 찾아볼 수 없으니 영어 독자라면 알 만한 `catch-all`도 한국어로 풀어 쓴다.
- **안 할 일 서술**: 한 일을 말하기 전에 안 할 일이나 그대로 두는 것을 먼저 말하는 것. "일정은 안 건드릴게요", "세 묶음으로 나눌게요".
- **묻지 않은 대조**: 아무도 Y를 꺼내지 않았는데 쓰는 `X, not Y`. 금지하는 잘못을 정확히 이름 붙여야 하는 지시문은 다른 장르이니 대조를 유지한다.

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

PR 본문은 `github-pr-markdown` skill이 관장한다. 거기서는 구어체 리듬을 적용하지 말고 그 skill을 따른다.

## 줄넘김

결합도가 가장 낮은 자리에서 끊되 문장 경계를 먼저, 그다음 절 경계(접속사 뒤, 주제어 `~는/은` 뒤, 새 논리 단위 앞), 그다음 완성된 목록 항목 사이를 고른다.
주어와 술어 사이, 괄호나 묶인 목록 내부, token과 수식어 사이는 절대 끊지 않는다. 대명사로 이어지는 후속 문장, 주장과 그 단서, 진술과 그것을 풀어주는 예시는 한 줄에 둔다.

❌ 마침표마다 끊어서 한 생각이 반으로 갈리고, 줄 너비 한계가 묶음을 쪼갠다:

```
// The vents open at 30°C.
// They close again at 26 to avoid oscillation.
// Lorem ipsum dolor sit amet, consectetur (alpha, beta,
// gamma) adipiscing elit.
```

✅ 붙어 읽히는 두 문장이 같은 줄에 있고, 끊김은 주제가 바뀌는 자리에 떨어지고, 묶음은 통째로 유지된다:

```
// The vents open at 30°C. They close again at 26 to avoid oscillation.
// Lorem ipsum dolor sit amet, consectetur (alpha, beta, gamma) adipiscing elit.
```

## 출처

| 주장이 있는 자리 | 출처가 갈 자리 |
|------------------|----------------|
| 문장이나 목록 항목 | 그 끝에, 주장 하나당 링크 하나: `습도 85%를 넘으면 돔이 닫힌다([운영 매뉴얼](url)).` |
| 인용 | 인용문 앞 머리에 |
| 표 | 주장을 담은 셀, 또는 하나의 출처가 표 전체를 덮으면 캡션에. 표 아래 산문에만 적은 출처는 모든 행을 무출처로 남긴다. |
| 같은 문서 안의 증거 | `id`로 anchor 링크: `[capture](#fig-closures)`. 말로 가리키는 것("4절의 캡처 참고")은 위장한 references 블록이다. |
| deep link이 없는 출처 | 가장 가까운 안정적 페이지에 링크하고 경로를 말로 적는다: `[Registry](url), Search, 건물명 순서`. 홈페이지 링크를 인용처럼 내놓으면 오해를 만든다. |

건드리지 않는 두 가지: 본문에 표시가 있는 각주(`[^3]`가 주장 자리에 있고, 주석이 어디에 렌더링되는지는 형식의 선택이다), 그리고 특정 주장을 받치지 않는 마무리 읽을거리 목록. 다만 그것이 문서의 출처가 나타나는 유일한 자리여서는 안 된다.

## 다른 규칙과의 관계

- `korean-style`과 `english-style`은 언어별 확장이다. 각 언어에 특유한 표시를 짚는다. 어느 언어로 쓰든 이 규칙과 그 규칙 둘 다 적용한다.
- `thinking-expansion`은 사고를 위해 어휘를 활성화한다. 이 규칙은 그것이 출력에 새어 나오지 않게 하고, 출력 경계에서 이긴다.
- `grounded-assertions`는 주장에 근거가 있는지를 판단하고, 여기의 출처 표는 그 근거가 어디 앉는지를 정한다.
- `char-discipline` hook(수정과 채팅 답변, 전체 codepoint 표를 갖고 있다), `gh-markdown-style` hook(PR과 이슈 본문), `prose-discipline` hook이 문자, 줄넘김, 출처, 간결성 기준을 강제한다. 세부는 hook이 갖고, 이 규칙은 지시를 갖는다.
