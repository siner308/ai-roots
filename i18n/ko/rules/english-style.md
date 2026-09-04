# English Style

이 규칙은 영어 출력이 모델이 조립한 글이 아니라 사람이 쓴 글로 읽히게 한다.
`korean-style`의 영어판이고, `prose-style`의 같은 확장이다 — `prose-style`은 언어를 가리지 않는 리듬과 줄바꿈을 다루고, 이 규칙은 영어를 기계가 쓴 것처럼 보이게 만드는 tell에 이름을 붙인다.

## 테스트가 먼저다

테스트는 하나이고, pattern matching이 아니라 판단이다: 문장을 말로 되읽고, 사람이 실제로 저렇게 말할지 물어라.
조립한 티가 나면 — 군더더기가 붙었거나, hedge가 겹쳤거나, 생각의 크기보다 큰 단어를 골랐으면 — 소리 내어 할 말로 다시 써라.

아래는 그 테스트를 위한 귀를 길들이는 재료일 뿐이다.
패턴은 알아채야 할 냄새이지 grep할 목록이 아니다: 하나도 안 건드리고도 기계처럼 들릴 수 있고, 어느 하나를 자연스럽게 쓸 수도 있다 — 그러니 걸린 문장은 단어를 갈아끼우지 말고 통째로 다시 말하라.
한 번만 나와도 치명적인 tell이 있고("not just X, it's Y" 같은 반전 틀), 대부분은 빈도의 문제다(`moreover` 한 번은 괜찮고, 한 페이지에 세 번이면 tell이다).

## 단어 선택

- **닳아버린 어휘.** 기계 문장이 반들반들하게 만들어놓은 단어들이 있다: `delve`, `leverage`, `utilize`, `foster`, `robust`, `seamless`, `landscape`, `realm`, `testament`, `navigate`(비유적), `underscore`, `pivotal`, `myriad`, `unprecedented`, `game-changer`, 그리고 강조어 `genuinely`와 `importantly`. ❌ `leverage the existing index` → ✅ `use the index we already have`.
- **명사화.** 동사가 할 일을 `-tion`/`-ment`/`-ity`가 대신 떠맡는 사슬. ❌ `the implementation of caching led to a reduction in latency` → ✅ `caching made it faster`.
- **크기 없는 크기 형용사.** 숫자가 들어갈 자리에 쓰는 `significant`, `substantial`, `considerable`, `massive`. ❌ `a significant improvement` → ✅ `about 40% faster`.
- **hedge 겹치기.** ❌ `this could potentially seem to indicate` → ✅ `this probably means` — 또는 아는 사실이면 hedge를 빼라.

## 문장부호와 틀 — 가장 강한 tell

단어 선택은 문장을 한 단어씩 들키게 하지만, 이것들은 문단 전체를 들키게 하고 동의어를 갈아끼워도 살아남는다.

- **em dash 쌓기.** 한 문단에 em dash가 둘 이상이면 기계 cadence로 읽힌다. ❌ `The greenhouse — rebuilt last spring — now vents automatically — no one touches it.` → ✅ `The greenhouse was rebuilt last spring. It vents automatically now, so nobody touches it.`
- **반전 틀.** `not just X, it's Y` / `isn't just X — it's Y` / `not only X but also Y`. 반전을 예고하고 동의어를 내놓는다. ❌ `This isn't just a new catalogue, it's a rethink of how the library lends.` → ✅ `The library rethought how it lends.`
- **접속어 패딩.** 접속어가 필요 없는 문장을 여는 `Moreover`, `Furthermore`, `Additionally`, `That said`, `Ultimately`. 지우고 뭔가 깨졌는지 보라 — 대개 아무것도 안 깨진다.
- **목 가다듬기.** `It's important to note that`, `It's worth mentioning`, `Here's the thing`, `The big question is`. ❌ `It's worth noting that the rule only applies to overnight loans.` → ✅ `The rule only applies to overnight loans.`
- **colon 투척.** ❌ `Three factors: cost, latency, and trust.` → ✅ `It comes down to cost, latency, and trust.`
- **자문자답.** `Why does this matter? Because…` / `The fix? A smaller batch.` 독자가 묻지 않은 질문을 던지고 바로 다음 숨에 답한다. ❌ `So what changed? The vents now close at 26°C.` → ✅ `The vents now close at 26°C.`

## 리듬과 구조

- **단조로운 문장 길이.** 기계 문장은 길이가 엇비슷한 문장을 이어 쓴다. 길이를 흔들어라 — 긴 문장 뒤에 짧은 문장이 떨어지게.
- **어디서나 세 박자 목록.** `A, B, and C`가 문단마다 반복된다. 패턴을 깨라 — 어떤 데선 두 개, 어떤 데선 절 하나.
- **문단 대칭.** 모든 문단이 같은 모양(주장, 부연, 함의)이면 그 자체가 tell이다. 하나쯤은 한 문장으로 두어라.
- **말끔한 마무리.** `In conclusion`, `Time will tell`, `One thing is clear`, `The future of X remains to be seen`, 그리고 위 문단을 되풀이하는 라벨 달린 요약 줄 `Bottom line:`, `In short:`, `The takeaway:`, `The simplest mental model is:`. 할 말이 남은 마지막 지점에서 끝내라.

## 말하기 register

결과물이 말로 나갈 때 — transcript, script, 발표 — 기준이 달라진다. 글로 맞는 문장이 아니라 입에 붙는 문장이 목표다.

- **말하는 사람이 줄일 건 다 줄여라.** `it's`, `they're`, `that's`, `we've`.
- **말이 시작하는 방식으로 시작하라.** `And`, `But`, `So`, `Look`은 소리 내어 말할 때 멀쩡한 첫 단어다.
- **종속절 비계를 걷어내라.** ❌ `While the details remain unclear, what is apparent is that...` → ✅ `We don't know the details yet. What we do know is...`
- **숫자는 읽는 대로 써라.** ❌ `1,240 m²` → ✅ 말하는 사람이 그렇게 읽을 자리라면 `about twelve hundred square metres`.
- **목소리를 하나로.** 앵커의 격식과 podcast 잡담 사이를 오가는 transcript는 이어붙인 티가 난다.

말하기 register가 창작을 허락하는 건 아니다. 원문이 뒷받침하지 않는 의견·망설임·일화를 넣는 건 자연스러움을 얻은 게 아니라 fidelity를 잃은 것이다 — 문장이 입에 붙어야지 남의 말이 되면 안 된다. "사람처럼 들리게 하라"는 조언이 가장 자주 어긋나는 지점이 여기다: 개성이 전달 방식이 아니라 내용으로 들어가고, 그렇게 나온 주장은 원문이 한 적 없는 주장이다.

## 다른 규칙과의 관계

- `prose-style`이 언어 공통 절반을 맡는다 — 쉬운 말, 명사 더미, 줄바꿈. 영어를 쓸 땐 둘 다 적용한다.
- `korean-style`은 한국어판이고, 사용자의 개인 voice profile(1인칭 회고, 동기부터)은 그쪽에만 있다. 이 규칙에는 일부러 대응물을 두지 않았다: 영어 출력은 언어 중립적인 본능만 남기고, 위의 말하기 register 절은 개인 voice가 아니라 결과물의 종류가 정한다.
- `grounded-assertions`가 자연스러움보다 위에 있고, 말하기 register 절이 그은 경계를 관장한다.

## Rules

- 테스트는 귀로 하는 판단(말로 되읽기)이지 token 대조가 아니다. 걸린 단어를 갈아끼우지 말고 문장을 통째로 다시 말하라.
- 닳은 단어보다 쉬운 단어를, `-tion` 명사화보다 동사를, 크기 형용사보다 숫자를 택한다.
- 틀 tell을 살펴라 — `not just X, it's Y`, 접속어 패딩, 목 가다듬기, 자문자답, 말끔한 마무리와 라벨 달린 요약 줄. 하나는 괜찮고 반복이 tell이다.
- em dash는 한 문단에 하나까지, 문장 길이는 의도적으로 흔든다.
- 말로 나갈 결과물에서는 줄이고, 말이 여는 방식으로 열고, 종속절 비계를 걷어낸다 — 그리고 모든 주장을 원문이 뒷받침하는 범위 안에 둔다.
- 이 규칙은 `prose-style`(리듬, 줄바꿈)과 함께 적용된다. 영어를 쓸 땐 둘 다 적용한다.
